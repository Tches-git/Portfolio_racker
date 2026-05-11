"""研报评测框架 — 规则型 + LLM-as-Judge 评估"""
from __future__ import annotations
import logging
from dataclasses import asdict, dataclass, field

from app.evals.report_eval_helpers import (
    build_judge_prompt,
    check_report_consistency,
    collect_rule_metrics,
    collect_section_graph_feedback,
    format_eval_markdown,
)

logger = logging.getLogger("fin.evals")


def _pick_payload_value(primary, fallback, default=0):
    if primary not in (None, ""):
        return primary
    if fallback not in (None, ""):
        return fallback
    return default


@dataclass
class EvalResult:
    """评测结果"""
    stock_code: str = ""
    # 规则型指标
    section_coverage: float = 0.0      # 章节覆盖率 (0-1)
    has_tables: bool = False            # 是否包含表格
    has_numbers: bool = False           # 是否引用数据
    missing_sections: list[str] = field(default_factory=list)
    # 一致性指标
    rating_consistent: bool = False     # 评级与估值方向一致
    consistency_passed: bool = True
    consistency_issue_count: int = 0
    consistency_issues: list[str] = field(default_factory=list)
    # LLM 评分
    completeness: int = 0              # 完整性 (1-5)
    data_support: int = 0              # 数据支撑 (1-5)
    reasoning_quality: int = 0         # 推理质量 (1-5)
    readability: int = 0               # 可读性 (1-5)
    overall_score: float = 0.0         # 综合评分 (0-100)
    report_length: int = 0
    numeric_references: int = 0
    covered_sections: int = 0
    llm_judge_enabled: bool = True
    risk_evidence_count: int = 0
    risk_transmission_count: int = 0
    investment_anchor_present: bool = False
    postprocess_fix_count: int = 0
    data_gap_disclosure_count: int = 0
    source_reference_count: int = 0
    source_provenance_coverage: float = 0.0
    document_parse_success_rate: float = 0.0
    table_extraction_success_rate: float = 0.0
    live_tool_success_rate: float = 0.0
    memory_hit_count: int = 0
    memory_usefulness_score: float = 0.0
    historical_delta_coverage: float = 0.0
    duplicate_memory_injection_rate: float = 0.0
    memory_reference_present: bool = False
    memory_reference_coverage: float = 0.0
    repeated_risk_pattern_count: int = 0
    repeated_catalyst_pattern_count: int = 0
    thesis_stability_score: float = 0.0
    rating_drift_count: int = 0
    graph_hit_count: int = 0
    hybrid_retrieval_hit_rate: float = 0.0
    relationship_coverage: float = 0.0
    risk_path_completeness: float = 0.0
    graph_query_focus: str = "通用关系"
    graph_focus_coverage: float = 0.0
    graph_focus_summary: str = ""
    section_graph_hit_count: int = 0
    section_graph_focus_coverage: float = 0.0
    section_graph_summary: str = ""
    section_graph_prompt_injection_present: bool = False
    section_graph_absorption_count: int = 0
    section_graph_absorption_rate: float = 0.0
    section_graph_query_summary: str = ""
    section_graph_feedback_summary: str = ""
    section_graph_query_refinement_summary: str = ""
    section_graph_query_refined_count: int = 0
    section_graph_low_absorption_count: int = 0
    section_graph_low_absorption_sections: str = ""
    section_graph_refinement_triggered: bool = False
    section_graph_refinement_coverage: float = 0.0
    section_graph_refinement_comparison_summary: str = ""
    section_graph_refinement_improved_count: int = 0
    section_graph_refinement_improvement_rate: float = 0.0
    section_graph_low_improvement_summary: str = ""
    section_graph_no_hit_count: int = 0
    section_graph_no_gain_count: int = 0
    section_graph_low_absorption_only_count: int = 0
    section_graph_refinement_strategy_summary: str = ""

    def summary(self) -> str:
        return (
            f"章节覆盖: {self.section_coverage:.0%} | "
            f"表格: {'✅' if self.has_tables else '❌'} | "
            f"数据引用: {'✅' if self.has_numbers else '❌'} | "
            f"评级一致: {'✅' if self.rating_consistent else '❌'} | "
            f"LLM评分: 完整{self.completeness} 数据{self.data_support} "
            f"推理{self.reasoning_quality} 可读{self.readability} | "
            f"综合: {self.overall_score:.1f}/100"
        )


def evaluate_report(report: str, state=None, stock_code: str = "", *, use_llm_judge: bool = True) -> EvalResult:
    """评测研报质量"""
    result = EvalResult(stock_code=stock_code, llm_judge_enabled=use_llm_judge)
    result.report_length = len(report)

    # 1. 规则型指标
    rule_metrics = collect_rule_metrics(report)
    result.covered_sections = rule_metrics["covered_sections"]
    result.section_coverage = rule_metrics["section_coverage"]
    result.missing_sections = rule_metrics["missing_sections"]
    result.has_tables = rule_metrics["has_tables"]
    result.numeric_references = rule_metrics["numeric_references"]
    result.has_numbers = rule_metrics["has_numbers"]
    result.risk_evidence_count = rule_metrics["risk_evidence_count"]
    result.risk_transmission_count = rule_metrics["risk_transmission_count"]
    result.investment_anchor_present = rule_metrics["investment_anchor_present"]
    result.data_gap_disclosure_count = rule_metrics["data_gap_disclosure_count"]
    result.section_graph_absorption_count = rule_metrics.get("section_graph_absorption_count", 0)

    # 4. 评级一致性
    if state:
        runtime_payload = getattr(state, "runtime_input_payload", {}) or {}
        memory_payload = getattr(state, "memory_payload", {}) or {}
        graph_payload = getattr(state, "graph_payload", {}) or {}
        run_payload = getattr(state, "run_payload", {}) or {}
        postprocess_payload = run_payload.get("postprocess", {}) if isinstance(run_payload.get("postprocess", {}), dict) else {}
        result.postprocess_fix_count = int(_pick_payload_value(postprocess_payload.get("fix_count"), state.sections.get("postprocess_fix_count", "0"), 0) or 0)
        result.source_reference_count = len(getattr(state, "source_refs", []) or [])
        result.source_provenance_coverage = 0.0
        if result.source_reference_count:
            refs = getattr(state, "source_refs", []) or []
            with_source = sum(1 for ref in refs if ref.get("source") and ref.get("title"))
            result.source_provenance_coverage = round(with_source / result.source_reference_count, 4)
        documents_payload = runtime_payload.get("documents", {}) if isinstance(runtime_payload.get("documents", {}), dict) else {}
        live_tools_payload = runtime_payload.get("live_tools", {}) if isinstance(runtime_payload.get("live_tools", {}), dict) else {}
        result.document_parse_success_rate = float(_pick_payload_value(documents_payload.get("parse_success_rate"), state.sections.get("document_parse_success_rate", "0"), 0) or 0)
        result.table_extraction_success_rate = float(_pick_payload_value(documents_payload.get("table_extraction_success_rate"), state.sections.get("table_extraction_success_rate", "0"), 0) or 0)
        result.live_tool_success_rate = float(_pick_payload_value(live_tools_payload.get("success_rate"), state.sections.get("live_tool_success_rate", "0"), 0) or 0)
        result.memory_hit_count = int(float(_pick_payload_value(memory_payload.get("memory_hit_count"), state.sections.get("memory_hit_count", "0"), 0) or 0))
        result.historical_delta_coverage = float(_pick_payload_value(memory_payload.get("historical_delta_coverage"), state.sections.get("historical_delta_coverage", "0"), 0) or 0)
        result.duplicate_memory_injection_rate = float(_pick_payload_value(memory_payload.get("duplicate_memory_injection_rate"), state.sections.get("duplicate_memory_injection_rate", "0"), 0) or 0)
        result.repeated_risk_pattern_count = int(float(_pick_payload_value(memory_payload.get("repeated_risk_pattern_count"), state.sections.get("repeated_risk_pattern_count", "0"), 0) or 0))
        result.repeated_catalyst_pattern_count = int(float(_pick_payload_value(memory_payload.get("repeated_catalyst_pattern_count"), state.sections.get("repeated_catalyst_pattern_count", "0"), 0) or 0))
        result.thesis_stability_score = float(_pick_payload_value(memory_payload.get("thesis_stability_score"), state.sections.get("thesis_stability_score", "0"), 0) or 0)
        result.rating_drift_count = int(float(_pick_payload_value(memory_payload.get("rating_drift_count"), state.sections.get("rating_drift_count", "0"), 0) or 0))
        result.graph_hit_count = int(float(_pick_payload_value(graph_payload.get("graph_hit_count"), state.sections.get("graph_hit_count", "0"), 0) or 0))
        result.hybrid_retrieval_hit_rate = float(_pick_payload_value(graph_payload.get("hybrid_retrieval_hit_rate"), state.sections.get("hybrid_retrieval_hit_rate", "0"), 0) or 0)
        result.relationship_coverage = float(_pick_payload_value(graph_payload.get("relationship_coverage"), state.sections.get("relationship_coverage", "0"), 0) or 0)
        result.risk_path_completeness = float(_pick_payload_value(graph_payload.get("risk_path_completeness"), state.sections.get("risk_path_completeness", "0"), 0) or 0)
        result.graph_query_focus = str(_pick_payload_value(graph_payload.get("graph_query_focus"), state.sections.get("graph_query_focus", "通用关系"), "通用关系") or "通用关系")
        result.graph_focus_coverage = float(_pick_payload_value(graph_payload.get("graph_focus_coverage"), state.sections.get("graph_focus_coverage", "0"), 0) or 0)
        result.graph_focus_summary = str(_pick_payload_value(graph_payload.get("graph_focus_summary"), state.sections.get("graph_focus_summary", ""), "") or "")
        result.section_graph_hit_count = int(float(_pick_payload_value(graph_payload.get("section_graph_hit_count"), state.sections.get("section_graph_hit_count", "0"), 0) or 0))
        result.section_graph_focus_coverage = float(_pick_payload_value(graph_payload.get("section_graph_focus_coverage"), state.sections.get("section_graph_focus_coverage", "0"), 0) or 0)
        result.section_graph_summary = str(_pick_payload_value(graph_payload.get("section_graph_summary"), state.sections.get("section_graph_summary", ""), "") or "")
        result.section_graph_query_summary = str(_pick_payload_value(graph_payload.get("section_graph_query_summary"), state.sections.get("section_graph_query_summary", ""), "") or "")
        result.section_graph_query_refinement_summary = str(_pick_payload_value(graph_payload.get("section_graph_query_refinement_summary"), state.sections.get("section_graph_query_refinement_summary", ""), "") or "")
        result.section_graph_query_refined_count = int(float(_pick_payload_value(graph_payload.get("section_graph_query_refined_count"), state.sections.get("section_graph_query_refined_count", "0"), 0) or 0))
        result.section_graph_refinement_strategy_summary = str(_pick_payload_value(graph_payload.get("section_graph_refinement_strategy_summary"), state.sections.get("section_graph_refinement_strategy_summary", ""), "") or "")
        result.section_graph_refinement_comparison_summary = str(_pick_payload_value(graph_payload.get("section_graph_refinement_comparison_summary"), state.sections.get("section_graph_refinement_comparison_summary", ""), "") or "")
        result.section_graph_refinement_improved_count = int(float(_pick_payload_value(graph_payload.get("section_graph_refinement_improved_count"), state.sections.get("section_graph_refinement_improved_count", "0"), 0) or 0))
        section_graph_context_map = graph_payload.get("section_graph_context_map", {}) if isinstance(graph_payload.get("section_graph_context_map", {}), dict) else {}
        result.section_graph_prompt_injection_present = any(
            bool(_pick_payload_value(section_graph_context_map.get(section_id), state.sections.get(key, ""), ""))
            for section_id, key in (("risk", "section_graph_context_risk"), ("industry", "section_graph_context_industry"), ("valuation", "section_graph_context_valuation"))
        )
        section_graph_feedback = collect_section_graph_feedback(report, state)
        feedback_parts: list[str] = []
        injected_count = 0
        absorbed_count = 0
        low_absorption_labels: list[str] = []
        low_improvement_parts: list[str] = []
        for section_id, section_feedback in section_graph_feedback.items():
            label = str(section_feedback.get("label", section_id))
            injected = bool(section_feedback.get("injected"))
            absorbed = bool(section_feedback.get("absorbed"))
            if injected:
                injected_count += 1
            if injected and absorbed:
                absorbed_count += 1
            if injected and not absorbed:
                low_absorption_labels.append(label)
            feedback_parts.append(f"{label}=注入{'是' if injected else '否'}/吸收{'是' if absorbed else '否'}")
        result.section_graph_feedback_summary = "；".join(feedback_parts)
        expected_section_absorption = injected_count
        if expected_section_absorption:
            result.section_graph_absorption_count = absorbed_count
            result.section_graph_absorption_rate = round(absorbed_count / expected_section_absorption, 4)
        else:
            result.section_graph_absorption_count = 0
            result.section_graph_absorption_rate = 0.0
        result.section_graph_low_absorption_count = len(low_absorption_labels)
        result.section_graph_low_absorption_sections = "、".join(low_absorption_labels)
        result.section_graph_refinement_triggered = result.section_graph_query_refined_count > 0
        result.section_graph_refinement_coverage = (
            round(result.section_graph_query_refined_count / result.section_graph_low_absorption_count, 4)
            if result.section_graph_low_absorption_count > 0 else 0.0
        )
        result.section_graph_refinement_improvement_rate = (
            round(result.section_graph_refinement_improved_count / result.section_graph_query_refined_count, 4)
            if result.section_graph_query_refined_count > 0 else 0.0
        )
        comparison_text = result.section_graph_refinement_comparison_summary
        comparison_by_label: dict[str, str] = {}
        for item in [part.strip() for part in comparison_text.split("；") if part.strip()]:
            label, _, metrics = item.partition("=")
            comparison_by_label[label] = metrics
        for label in low_absorption_labels:
            metrics = comparison_by_label.get(label, "")
            if not metrics:
                result.section_graph_low_absorption_only_count += 1
                low_improvement_parts.append(f"{label}=低吸收")
                continue
            if "->0" in metrics:
                result.section_graph_no_hit_count += 1
                low_improvement_parts.append(f"{label}=无命中")
                continue
            if "(Δ0)" in metrics:
                result.section_graph_no_gain_count += 1
                low_improvement_parts.append(f"{label}=有命中但无增量")
                continue
            if result.section_graph_refinement_triggered and "Δ" in metrics:
                continue
            result.section_graph_low_absorption_only_count += 1
            low_improvement_parts.append(f"{label}=低吸收")
        result.section_graph_low_improvement_summary = "；".join(low_improvement_parts)
        result.memory_usefulness_score = round((min(result.memory_hit_count, 5) / 5 + result.historical_delta_coverage + (1 - min(result.duplicate_memory_injection_rate, 1.0)) + result.thesis_stability_score) / 4, 4)
        result.consistency_issues = check_report_consistency(report, state)
        memory_issue_count = sum(1 for issue in result.consistency_issues if "长期记忆" in issue or "历史" in issue or "评级变化" in issue or "估值演变" in issue or "风险演化" in issue)
        expected_memory_checks = 1 if result.memory_hit_count > 0 else 0
        result.memory_reference_present = result.memory_hit_count <= 0 or memory_issue_count == 0
        result.memory_reference_coverage = 1.0 if expected_memory_checks == 0 else round(max(0, expected_memory_checks - memory_issue_count) / expected_memory_checks, 4)
        result.consistency_issue_count = len(result.consistency_issues)
        result.consistency_passed = result.consistency_issue_count == 0
        rating = state.sections.get("rating", "")
        dcf = state.dcf
        if dcf and rating:
            if dcf.upside > 0 and rating in ("强烈推荐", "推荐"):
                result.rating_consistent = True
            elif dcf.upside < 0 and rating in ("谨慎", "回避"):
                result.rating_consistent = True
            elif rating == "中性":
                result.rating_consistent = True

    # 5. LLM-as-Judge
    if use_llm_judge:
        try:
            from app.llm import chat_json

            scores = chat_json(build_judge_prompt(report), temperature=0.1, max_tokens=512)
            if isinstance(scores, dict) and "completeness" in scores:
                result.completeness = min(5, max(1, int(scores.get("completeness", 3))))
                result.data_support = min(5, max(1, int(scores.get("data_support", 3))))
                result.reasoning_quality = min(5, max(1, int(scores.get("reasoning_quality", 3))))
                result.readability = min(5, max(1, int(scores.get("readability", 3))))
        except Exception as e:
            logger.warning(f"LLM 评分失败: {e}")
            result.completeness = 3
            result.data_support = 3
            result.reasoning_quality = 3
            result.readability = 3
    else:
        result.completeness = 0
        result.data_support = 0
        result.reasoning_quality = 0
        result.readability = 0

    # 6. 综合评分
    rule_score = (
        result.section_coverage * 30 +
        (10 if result.has_tables else 0) +
        (10 if result.has_numbers else 0) +
        (5 if result.rating_consistent else 0)
    )
    llm_score = 0.0
    if use_llm_judge:
        llm_score = (
            result.completeness + result.data_support +
            result.reasoning_quality + result.readability
        ) / 20 * 45  # 最高 45 分
    result.overall_score = round(rule_score + llm_score, 1)

    return result


def evaluate_report_with_metrics(report: str, state=None, stock_code: str = "", *, use_llm_judge: bool = True) -> dict:
    result = evaluate_report(report, state=state, stock_code=stock_code, use_llm_judge=use_llm_judge)
    payload = asdict(result)
    payload["summary"] = result.summary()
    if state is not None and getattr(state, "run_metrics", None):
        payload["run_metrics"] = dict(state.run_metrics)
    return payload


def format_eval_report(result: EvalResult) -> str:
    """格式化评测报告为 Markdown"""
    return format_eval_markdown(result)
