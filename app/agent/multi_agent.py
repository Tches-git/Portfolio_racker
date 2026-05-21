"""AutoGen 多角色金融研究 Agent 工作流。"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from app.agent.autogen_adapter import AutoGenRuntime, create_autogen_runtime
from app.agent.role_specs import MULTI_AGENT_ROLES, PRE_WRITE_ROLE_IDS, RoleSpec, get_role_spec
from app.agent.tools import _make_tools, execute_tool
from app.evals.rag_eval import evaluate_rag_citations
from app.models import AnalysisState, PlanItem

RoleCallback = Callable[[str, str, dict[str, Any]], None]


@dataclass
class MultiAgentRoleTrace:
    role_id: str
    role_name: str
    status: str = "pending"
    summary: str = ""
    tool_call_count: int = 0
    duration_s: float = 0.0
    fallback_used: bool = False
    error: str = ""
    phase: str = "pre_write"
    objective: str = ""
    allowed_tools: list[str] = field(default_factory=list)
    input_summary: str = ""
    quality_checks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
            "status": self.status,
            "summary": self.summary,
            "tool_call_count": self.tool_call_count,
            "duration_s": self.duration_s,
            "fallback_used": self.fallback_used,
            "error": self.error,
            "phase": self.phase,
            "objective": self.objective,
            "allowed_tools": self.allowed_tools,
            "input_summary": self.input_summary,
            "quality_checks": self.quality_checks,
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "MultiAgentRoleTrace":
        spec = get_role_spec(str(payload.get("role_id") or "")) if payload else None
        return cls(
            role_id=str(payload.get("role_id") or ""),
            role_name=str(payload.get("role_name") or (spec.role_name if spec else "")),
            status=str(payload.get("status") or "pending"),
            summary=str(payload.get("summary") or ""),
            tool_call_count=int(payload.get("tool_call_count") or 0),
            duration_s=float(payload.get("duration_s") or 0.0),
            fallback_used=bool(payload.get("fallback_used") or False),
            error=str(payload.get("error") or ""),
            phase=str(payload.get("phase") or (spec.phase if spec else "pre_write")),
            objective=str(payload.get("objective") or (spec.objective if spec else "")),
            allowed_tools=list(payload.get("allowed_tools") or (list(spec.allowed_tools) if spec else [])),
            input_summary=str(payload.get("input_summary") or ""),
            quality_checks=list(payload.get("quality_checks") or (list(spec.quality_checks) if spec else [])),
        )


@dataclass
class MultiAgentTrace:
    mode: str = "autogen_graphflow"
    role_count: int = 0
    completed_role_count: int = 0
    failed_role_count: int = 0
    roles: list[MultiAgentRoleTrace] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "role_count": self.role_count,
            "completed_role_count": self.completed_role_count,
            "failed_role_count": self.failed_role_count,
            "roles": [role.to_dict() for role in self.roles],
        }


@dataclass
class MultiAgentResearchResult:
    answer: str
    trace: MultiAgentTrace = field(default_factory=MultiAgentTrace)
    total_steps: int = 0
    plan: list[PlanItem] = field(default_factory=list)
    reflection: str = ""


# 兼容少量旧测试/调用方命名；主流程不再使用旧 ReActAgent。
AgentResult = MultiAgentResearchResult


class AutoGenMultiAgentWorkflow:
    """面向研报生成的 AutoGen 多角色工作流。

    使用显式 directed workflow 固定七个角色顺序，避免自由对话式多智能体
    在研报任务里产生不可控分支。前六个角色在 RAG 正式写作前执行，
    CitationAuditAgent 在报告生成后执行。AutoGen runtime 可用时记录为
    ``autogen_graphflow``；不可用时使用同一流程的本地降级模式，保证测试和离线
    任务仍可复现。
    """

    def __init__(
        self,
        *,
        runtime: AutoGenRuntime | None = None,
        on_role_step: RoleCallback | None = None,
    ) -> None:
        self.runtime = runtime or create_autogen_runtime()
        self.on_role_step = on_role_step or (lambda *_: None)

    def run(self, stock_code: str, state: AnalysisState) -> MultiAgentResearchResult:
        context: dict[str, Any] = {"stock_code": stock_code}
        traces: list[MultiAgentRoleTrace] = []
        outputs: dict[str, str] = {}
        plan: list[PlanItem] = []

        for spec in self._pre_write_specs():
            role_trace = self._run_role(spec, state, context)
            traces.append(role_trace)
            outputs[spec.role_id] = role_trace.summary
            context[f"{spec.role_id}_summary"] = role_trace.summary
            if spec.role_id == "planner":
                plan = self._build_plan_from_state(state)
            if role_trace.status == "failed" and spec.critical:
                trace = self._build_trace(traces)
                self._apply_trace(state, trace, outputs)
                raise RuntimeError(f"{spec.role_name} 执行失败: {role_trace.error}")

        trace = self._build_trace(traces)
        answer = self._compose_research_conclusion(state, outputs)
        reflection = self._compose_reflection(outputs)
        self._apply_research_payload(state, answer=answer, plan=plan, reflection=reflection, outputs=outputs)
        self._apply_trace(state, trace, outputs)
        return MultiAgentResearchResult(answer=answer, trace=trace, total_steps=len(trace.roles), plan=plan, reflection=reflection)

    def run_post_write_audit(self, state: AnalysisState) -> MultiAgentTrace:
        """在正式报告生成后追加引用审计角色 Trace。"""

        spec = self._role_by_id("citation_audit")
        if spec is None:
            return self._current_trace_from_state(state)
        existing_trace = self._current_trace_from_state(state)
        traces = [role for role in existing_trace.roles if role.role_id != spec.role_id]
        outputs = dict(state.analysis_payload.get("multi_agent_role_outputs") or {})
        context = {f"{key}_summary": value for key, value in outputs.items()}
        role_trace = self._run_role(spec, state, context)
        traces.append(role_trace)
        outputs[spec.role_id] = role_trace.summary
        trace = self._build_trace(traces)
        self._refresh_research_summary_after_audit(state, outputs)
        self._apply_trace(state, trace, outputs)
        return trace

    def _run_role(self, spec: RoleSpec, state: AnalysisState, context: dict[str, Any]) -> MultiAgentRoleTrace:
        started = time.perf_counter()
        before_tools = len(state.tool_memory)
        self.on_role_step("role_start", f"{spec.role_name} 开始: {spec.objective}", {"role_id": spec.role_id})
        try:
            summary, fallback_used = self._dispatch_role(spec, state, context)
            status = "completed" if not fallback_used else "degraded"
            error = ""
        except Exception as exc:
            if spec.critical:
                summary = ""
                status = "failed"
                fallback_used = False
                error = str(exc)
            else:
                summary = f"{spec.role_name} 执行异常，已降级为已有数据复核: {exc}"
                status = "degraded"
                fallback_used = True
                error = str(exc)
        duration_s = round(time.perf_counter() - started, 3)
        tool_call_count = max(0, len(state.tool_memory) - before_tools)
        self.on_role_step(
            "role_done" if status != "failed" else "role_failed",
            f"{spec.role_name} {status}: {summary[:140]}",
            {"role_id": spec.role_id, "status": status, "tool_call_count": tool_call_count},
        )
        return MultiAgentRoleTrace(
            role_id=spec.role_id,
            role_name=spec.role_name,
            status=status,
            summary=summary,
            tool_call_count=tool_call_count,
            duration_s=duration_s,
            fallback_used=fallback_used,
            error=error,
            phase=spec.phase,
            objective=spec.objective,
            allowed_tools=list(spec.allowed_tools),
            input_summary=self._build_input_summary(spec, state, context),
            quality_checks=list(spec.quality_checks),
        )

    def _dispatch_role(self, spec: RoleSpec, state: AnalysisState, context: dict[str, Any]) -> tuple[str, bool]:
        if spec.role_id == "planner":
            return self._run_planner(state), not self.runtime.available
        if spec.role_id == "market_data":
            return self._run_market_data(spec, state), False
        if spec.role_id == "fundamental_valuation":
            return self._run_fundamental_valuation(spec, state), False
        if spec.role_id == "event_analysis":
            return self._run_event_analysis(state), False
        if spec.role_id == "risk_review":
            return self._run_risk_review(spec, state), False
        if spec.role_id == "report_writer":
            return self._run_report_writer(state, context), not self.runtime.available
        if spec.role_id == "citation_audit":
            return self._run_citation_audit(state)
        return f"{spec.role_name} 暂无执行逻辑", True

    def _run_planner(self, state: AnalysisState) -> str:
        state.plan = self._build_plan_from_state(state)
        agent_count = len(self.runtime.agents or [])
        runtime_note = f"AutoGen AgentChat runtime 可用，已创建 {agent_count} 个角色 Agent" if self.runtime.available else f"AutoGen runtime 降级: {self.runtime.error}"
        return (
            f"围绕 {state.stock_name or state.stock_code} 建立多角色研报流程：先确认研究范围，"
            "再完成行情分析、基本面估值、事件分析、风险复核、报告写作和报告后引用审计。"
            f"{runtime_note}。"
        )

    def _run_market_data(self, spec: RoleSpec, state: AnalysisState) -> str:
        tools = _make_tools(state)
        called: list[str] = []
        for tool_name in spec.allowed_tools:
            if self._should_run_tool(tool_name, state):
                self._execute_allowed_tool(spec, tools, tool_name, state)
                called.append(tool_name)
        if not called:
            data_level = "已有行情或结构化数据可供写作" if state.metrics or state.profile else "行情与趋势数据不足，报告需披露数据缺口"
            return f"行情分析阶段未触发新增计算；{data_level}。"
        return f"完成行情与趋势工具调用：{', '.join(called)}。"

    def _run_fundamental_valuation(self, spec: RoleSpec, state: AnalysisState) -> str:
        tools = _make_tools(state)
        called: list[str] = []
        for tool_name in spec.allowed_tools:
            if self._should_run_tool(tool_name, state):
                self._execute_allowed_tool(spec, tools, tool_name, state)
                called.append(tool_name)
        if not called:
            data_level = "已有财务画像可供定性复核" if state.metrics or state.profile else "财务与估值数据不足，报告需披露数据缺口"
            return f"基本面估值阶段未触发新增计算；{data_level}。"
        return f"完成基本面与估值工具调用：{', '.join(called)}。"

    def _run_event_analysis(self, state: AnalysisState) -> str:
        context = state.event_context or {}
        news_count = len(state.news or [])
        announcement_count = len(state.announcements or [])
        if context:
            title = context.get("title") or context.get("event_id") or "事件触发任务"
            state.analysis_payload["event_agent_summary"] = f"事件触发研报：{title}"
            return f"围绕触发事件「{title}」复核影响等级、情绪方向和来源链路；新闻 {news_count} 条，公告 {announcement_count} 条。"
        return f"未检测到单条触发事件，按常规新闻/公告进行事件分析；新闻 {news_count} 条，公告 {announcement_count} 条。"

    def _run_risk_review(self, spec: RoleSpec, state: AnalysisState) -> str:
        tools = _make_tools(state)
        called = False
        if state.metrics or state.news:
            self._execute_allowed_tool(spec, tools, "risk_assessment", state)
            called = True
        data_gaps = self._data_gap_summary(state)
        risk_count = len(state.risks or [])
        prefix = "已调用风险评估工具" if called else "基于已有上下文做风险复核"
        return f"{prefix}，识别风险 {risk_count} 项；{data_gaps}。"

    def _run_report_writer(self, state: AnalysisState, context: dict[str, Any]) -> str:
        brief_parts = [
            context.get("planner_summary", ""),
            context.get("market_data_summary", ""),
            context.get("fundamental_valuation_summary", ""),
            context.get("event_analysis_summary", ""),
            context.get("risk_review_summary", ""),
        ]
        brief = "\n".join(part for part in brief_parts if part).strip()
        state.analysis_payload["report_writer_brief"] = brief
        state.sections["multi_agent_writer_brief"] = brief
        return "已整合规划、数据、事件和风险复核结果，形成报告写作 brief，交由 RAG 写作链路生成正文。"

    def _run_citation_audit(self, state: AnalysisState) -> tuple[str, bool]:
        final_report = (state.final_report or "").strip()
        fallback_used = False
        if not final_report:
            fallback_used = True
            audit = {
                "citation_coverage_rate": 0.0,
                "unsupported_claim_count": 0,
                "source_reference_count": len(state.source_refs or []),
                "retrieval_topk_hit_rate": 0.0,
                "rerank_selected_count": 0,
            }
            state.analysis_payload["citation_audit"] = audit
            state.sections["citation_audit_summary"] = "正式报告为空，引用审计已降级为不可用说明。"
            return state.sections["citation_audit_summary"], fallback_used
        audit = evaluate_rag_citations(final_report, list(state.source_refs or []), stock_code=state.stock_code)
        state.analysis_payload["citation_audit"] = audit
        state.sections["citation_audit_summary"] = (
            f"来源 {audit.get('source_reference_count', 0)} 条；"
            f"引用覆盖率 {float(audit.get('citation_coverage_rate', 0) or 0):.1%}；"
            f"无来源观点 {audit.get('unsupported_claim_count', 0)} 条"
        )
        if not state.source_refs:
            fallback_used = True
            state.sections["citation_audit_summary"] += "；来源列表为空，审计结论仅作降级提示"
        return state.sections["citation_audit_summary"], fallback_used

    def _should_run_tool(self, tool_name: str, state: AnalysisState) -> bool:
        if tool_name in {"dupont_analysis", "trend_analysis"}:
            return bool(state.metrics)
        if tool_name == "dcf_valuation":
            return bool(state.metrics and state.profile)
        if tool_name == "comparable_valuation":
            return bool(state.profile and state.peers)
        if tool_name == "quantitative_scoring":
            return bool(state.metrics and state.dcf)
        return False

    def _execute_allowed_tool(self, spec: RoleSpec, tools: list[Any], tool_name: str, state: AnalysisState) -> Any:
        if tool_name not in spec.allowed_tools:
            raise PermissionError(f"{spec.role_name} 无权调用工具 {tool_name}")
        return execute_tool(tools, tool_name, {}, state=state)

    def _pre_write_specs(self) -> list[RoleSpec]:
        return [spec for spec in MULTI_AGENT_ROLES if spec.role_id in PRE_WRITE_ROLE_IDS]

    def _role_by_id(self, role_id: str) -> RoleSpec | None:
        return get_role_spec(role_id)

    def _current_trace_from_state(self, state: AnalysisState) -> MultiAgentTrace:
        payload = dict(state.run_payload.get("multi_agent_trace") or {})
        roles_payload = payload.get("roles") or []
        roles = [MultiAgentRoleTrace.from_payload(dict(item)) for item in roles_payload if isinstance(item, dict)]
        return MultiAgentTrace(
            mode=str(payload.get("mode") or (self.runtime.mode if self.runtime.available else "autogen_graphflow_fallback")),
            role_count=int(payload.get("role_count") or len(MULTI_AGENT_ROLES)),
            completed_role_count=int(payload.get("completed_role_count") or 0),
            failed_role_count=int(payload.get("failed_role_count") or 0),
            roles=roles,
        )

    def _build_input_summary(self, spec: RoleSpec, state: AnalysisState, context: dict[str, Any]) -> str:
        stock_label = f"{state.stock_name or state.stock_code}（{state.stock_code}）" if state.stock_name else state.stock_code
        if spec.role_id == "planner":
            return f"{stock_label}；事件上下文={'有' if state.event_context else '无'}；预取数据 {len(state.tool_memory)} 项。"
        if spec.role_id == "market_data":
            return f"行情/趋势上下文；财务期数 {len(state.metrics or [])}；工具缓存 {len(state.tool_memory)} 项。"
        if spec.role_id == "fundamental_valuation":
            return f"公司画像={'有' if state.profile else '无'}；财务期数 {len(state.metrics or [])}；同行 {len(state.peers or [])} 家。"
        if spec.role_id == "event_analysis":
            return f"新闻 {len(state.news or [])} 条；公告 {len(state.announcements or [])} 条；触发事件={'有' if state.event_context else '无'}。"
        if spec.role_id == "risk_review":
            previous = ", ".join(key for key in ("market_data_summary", "fundamental_valuation_summary", "event_analysis_summary") if context.get(key))
            return f"前序摘要：{previous or '暂无'}；已有风险 {len(state.risks or [])} 项。"
        if spec.role_id == "report_writer":
            previous_count = sum(1 for key in context if key.endswith("_summary") and context.get(key))
            return f"已收到 {previous_count} 个前置角色摘要；RAG 来源 {len(state.source_refs or [])} 条。"
        if spec.role_id == "citation_audit":
            return f"正式报告长度 {len(state.final_report or '')} 字；来源 {len(state.source_refs or [])} 条。"
        return "当前任务上下文。"

    def _build_plan_from_state(self, state: AnalysisState) -> list[PlanItem]:
        return [
            PlanItem("P1", f"确认 {state.stock_name or state.stock_code} 的研究范围与关键问题", "PlannerAgent"),
            PlanItem("P2", "完成行情、交易活跃度和技术走势分析", "MarketDataAgent"),
            PlanItem("P3", "完成财务质量、估值区间和量化评分复核", "FundamentalValuationAgent"),
            PlanItem("P4", "复核新闻、公告、触发事件和事件影响路径", "EventAnalysisAgent"),
            PlanItem("P5", "检查风险、数据缺口、降级状态和逻辑漏洞", "RiskReviewAgent"),
            PlanItem("P6", "整合多角色结论生成研报写作 brief", "ReportWriterAgent"),
            PlanItem("P7", "报告生成后审计来源引用与无来源观点风险", "CitationAuditAgent"),
        ]

    def _compose_research_conclusion(self, state: AnalysisState, outputs: dict[str, str]) -> str:
        stock_label = f"{state.stock_name or '目标公司'}（{state.stock_code}）"
        lines = [
            f"{stock_label} 多智能体研究结论：",
            f"1. 行情分析：{outputs.get('market_data', '暂无')}",
            f"2. 基本面估值：{outputs.get('fundamental_valuation', '暂无')}",
            f"3. 事件分析：{outputs.get('event_analysis', '暂无')}",
            f"4. 风险复核：{outputs.get('risk_review', '暂无')}",
            f"5. 写作准备：{outputs.get('report_writer', '暂无')}",
            f"6. 引用审计：{outputs.get('citation_audit', '报告生成后执行')}",
        ]
        return "\n".join(lines)

    def _compose_reflection(self, outputs: dict[str, str]) -> str:
        risk = outputs.get("risk_review", "未完成风险复核")
        citation = outputs.get("citation_audit", "未完成引用审计")
        return f"多 Agent 复核摘要：{risk}；{citation}。"

    def _refresh_research_summary_after_audit(self, state: AnalysisState, outputs: dict[str, str]) -> None:
        answer = self._compose_research_conclusion(state, outputs)
        reflection = self._compose_reflection(outputs)
        state.analysis_payload["research_conclusion"] = answer
        state.analysis_payload["research_reflection"] = reflection
        state.analysis_payload["multi_agent_role_outputs"] = outputs
        state.sections["research_conclusion"] = answer
        state.sections["research_reflection"] = reflection
        state.sections["multi_agent_role_outputs"] = "\n".join(f"- {key}: {value}" for key, value in outputs.items())

    def _apply_research_payload(
        self,
        state: AnalysisState,
        *,
        answer: str,
        plan: list[PlanItem],
        reflection: str,
        outputs: dict[str, str],
    ) -> None:
        plan_text = "\n".join(f"[{item.step_id}] {item.objective} → {item.preferred_tool}" for item in plan)
        state.analysis_payload.update({
            "research_conclusion": answer,
            "research_plan": plan_text,
            "research_reflection": reflection,
            "multi_agent_role_outputs": outputs,
        })
        state.sections["research_conclusion"] = answer
        state.sections["research_plan"] = plan_text
        state.sections["research_reflection"] = reflection
        state.sections["multi_agent_role_outputs"] = "\n".join(f"- {key}: {value}" for key, value in outputs.items())

    def _build_trace(self, roles: list[MultiAgentRoleTrace]) -> MultiAgentTrace:
        completed = sum(1 for role in roles if role.status in {"completed", "degraded"})
        failed = sum(1 for role in roles if role.status == "failed")
        mode = self.runtime.mode if self.runtime.available else "autogen_graphflow_fallback"
        return MultiAgentTrace(
            mode=mode,
            role_count=len(MULTI_AGENT_ROLES),
            completed_role_count=completed,
            failed_role_count=failed,
            roles=roles,
        )

    def _apply_trace(self, state: AnalysisState, trace: MultiAgentTrace, outputs: dict[str, str]) -> None:
        trace_payload = trace.to_dict()
        state.run_payload["multi_agent_trace"] = trace_payload
        state.analysis_payload["multi_agent_trace"] = trace_payload
        state.sections["multi_agent_trace"] = str(trace_payload)
        state.sections["multi_agent_role_count"] = str(trace.role_count)
        state.sections["multi_agent_completed_count"] = str(trace.completed_role_count)
        state.sections["multi_agent_failed_count"] = str(trace.failed_role_count)
        citation_audit = state.analysis_payload.get("citation_audit") or {}
        state.run_payload["multi_agent"] = {
            "mode": trace.mode,
            "role_outputs": outputs,
            "role_count": trace.role_count,
            "completed_role_count": trace.completed_role_count,
            "failed_role_count": trace.failed_role_count,
            "citation_audit_coverage_rate": float(citation_audit.get("citation_coverage_rate", 0.0) or 0.0)
            if isinstance(citation_audit, dict)
            else 0.0,
        }

    def _data_gap_summary(self, state: AnalysisState) -> str:
        gaps = []
        if not state.profile:
            gaps.append("公司画像缺失")
        if not state.metrics:
            gaps.append("财务数据缺失")
        if not state.source_refs:
            gaps.append("来源引用不足")
        if not gaps:
            return "核心数据较完整"
        return "数据缺口：" + "、".join(gaps)
