"""Agent 工具集 — 供 ReAct Agent 自主调用（支持 function calling schema + 重试 + 缓存）"""
from __future__ import annotations
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from app.models import AnalysisState, ToolCallRecord
from app.data_source.live_tools import (
    extract_document_summary,
    extract_document_tables,
    fetch_announcements,
    fetch_broker_reports,
    fetch_exchange_filings,
    fetch_fund_holdings,
    fetch_live_quotes,
)
from app.agent.prefetch_helpers import (
    build_live_source_refs,
    build_quote_source_ref,
    format_financials_observation,
    format_live_quote_summary,
    format_news_observation,
    format_peers_observation,
    format_profile_observation,
    initialize_live_tools_payload,
    sync_live_tools_status,
    update_live_tools_payload,
)
from app.utils.tracer import get_active_tracer

logger = logging.getLogger("fin.agent.tools")


@dataclass
class Tool:
    """Agent 工具定义（含 function calling schema）"""
    name: str
    description: str
    parameters_schema: dict[str, Any]  # JSON Schema 格式
    function: Callable[..., str]
    retryable: bool = True
    cacheable: bool = True
    critical: bool = False  # 关键工具标记：失败将严重影响分析质量


def _make_tools(state: AnalysisState) -> list[Tool]:
    """根据当前状态创建工具列表"""

    initial_live_tools_payload = initialize_live_tools_payload(state)
    live_tools_success_state: dict[str, bool] = dict(initial_live_tools_payload.get("success_map", {})) if isinstance(initial_live_tools_payload.get("success_map", {}), dict) else {}

    def _build_quote_source_ref(quote: dict[str, Any]) -> dict[str, Any]:
        return build_quote_source_ref(state.stock_code, quote)

    def _build_live_source_refs(items: list[dict[str, Any]], *, source_type: str, default_title: str, default_retrieval_mode: str, default_evidence_type: str) -> list[dict[str, Any]]:
        return build_live_source_refs(items, source_type=source_type, default_title=default_title, default_retrieval_mode=default_retrieval_mode, default_evidence_type=default_evidence_type)

    def fetch_stock_profile(code: str = "") -> str:
        """获取公司基本信息"""
        from app.data_source.akshare_client import get_stock_profile
        target = code or state.stock_code
        try:
            profile = get_stock_profile(target)
            if target == state.stock_code:
                state.profile = profile
                state.stock_name = profile.name
            return format_profile_observation(profile)
        except Exception as e:
            return f"获取失败: {e}"

    def fetch_financials(code: str = "") -> str:
        """获取多年财务数据"""
        from app.data_source.akshare_client import get_financial_metrics
        target = code or state.stock_code
        try:
            metrics = get_financial_metrics(target)
            if target == state.stock_code:
                state.metrics = metrics
            return format_financials_observation(metrics)
        except Exception as e:
            return f"获取失败: {e}"

    def fetch_peers(industry: str = "") -> str:
        """获取同行业公司"""
        from app.data_source.akshare_client import get_peer_companies
        ind = industry or (state.profile.industry if state.profile else "")
        if not ind:
            return "需要先获取公司信息以确定行业"
        try:
            peers = get_peer_companies(ind, exclude_code=state.stock_code)
            state.peers = peers
            return format_peers_observation(peers, ind)
        except Exception as e:
            return f"获取失败: {e}"

    def fetch_news(name: str = "") -> str:
        """获取近期新闻"""
        from app.data_source.akshare_client import get_recent_news
        target = name or state.stock_name
        if not target:
            return "需要先获取公司名称"
        try:
            news = get_recent_news(target)
            state.news = news
            return format_news_observation(news)
        except Exception as e:
            return f"获取失败: {e}"

    def run_dupont_analysis(**kwargs) -> str:
        """执行杜邦分析"""
        from app.finance.dupont import analyze_dupont, format_dupont_table, dupont_summary
        if not state.metrics:
            return "需要先获取财务数据"
        state.dupont = analyze_dupont(state.metrics)
        table = format_dupont_table(state.dupont)
        summary = dupont_summary(state.dupont)
        state.sections["dupont_table"] = table
        state.sections["dupont_summary"] = summary
        return f"{table}\n\n{summary}"

    def run_dcf_valuation(**kwargs) -> str:
        """执行DCF估值 + 蒙特卡洛模拟 + 敏感性分析"""
        from app.finance.valuation import (
            dcf_valuation, format_dcf_table,
            run_monte_carlo_dcf, build_sensitivity_table, format_monte_carlo_summary,
        )
        if not state.metrics or not state.profile:
            return "需要先获取财务数据和公司信息"
        # 基础 DCF
        state.dcf = dcf_valuation(state.metrics, state.profile)
        if not state.dcf:
            return "数据不足，无法进行DCF估值（可能现金流和利润均为负）"
        table = format_dcf_table(state.dcf)
        state.sections["dcf_table"] = table
        result_parts = [
            f"每股内在价值: {state.dcf.per_share_value:.2f}元",
            f"当前股价: {state.dcf.current_price:.2f}元",
            f"上涨空间: {state.dcf.upside:+.1f}%",
            "", table,
        ]
        # 蒙特卡洛模拟
        try:
            from app.config import MC_SIMULATIONS
            mc = run_monte_carlo_dcf(state.metrics, state.profile, simulations=MC_SIMULATIONS)
            if mc:
                state.dcf.monte_carlo_summary = mc
                mc_text = format_monte_carlo_summary(mc)
                state.sections["dcf_monte_carlo"] = mc_text
                result_parts.append(f"\n{mc_text}")
        except Exception as e:
            logger.warning(f"蒙特卡洛模拟失败: {e}")
        # 敏感性分析
        try:
            sens = build_sensitivity_table(state.metrics, state.profile)
            if sens:
                state.dcf.sensitivity_matrix = sens["matrix"]
                state.dcf.sensitivity_waccs = sens["waccs"]
                state.dcf.sensitivity_growth_rates = sens["growth_rates"]
                state.sections["dcf_sensitivity"] = sens["table_md"]
                result_parts.append(f"\n### 敏感性分析\n{sens['table_md']}")
        except Exception as e:
            logger.warning(f"敏感性分析失败: {e}")
        return "\n".join(result_parts)

    def run_comparable_valuation(**kwargs) -> str:
        """执行可比公司估值"""
        from app.finance.valuation import comparable_valuation
        if not state.profile or not state.peers:
            return "需要先获取公司信息和同行数据"
        result = comparable_valuation(state.profile, state.peers)
        state.sections["comparable_summary"] = result.get("summary", "")
        return result.get("summary", "无结果")

    def run_trend_analysis(**kwargs) -> str:
        """执行趋势分析"""
        from app.finance.trend import analyze_trends, format_trend_table, trend_summary
        if not state.metrics:
            return "需要先获取财务数据"
        state.trends = analyze_trends(state.metrics)
        table = format_trend_table(state.trends)
        summary = trend_summary(state.trends)
        state.sections["trend_table"] = table
        state.sections["trend_summary"] = summary
        return f"{table}\n\n{summary}"

    def run_risk_assessment(**kwargs) -> str:
        """执行风险评估"""
        from app.finance.risk_model import assess_financial_risks, assess_news_risks
        risks = []
        if state.profile and state.metrics:
            risks.extend(assess_financial_risks(state.profile, state.metrics))
        if state.news:
            risks.extend(assess_news_risks(state.news, state.stock_name))
        state.risks = risks
        if not risks:
            return "未发现明显风险"
        lines = [f"识别到 {len(risks)} 项风险:"]
        for r in risks:
            lines.append(f"  [{r.level.upper()}][{r.category}] {r.description}")
            if r.evidence:
                lines.append(f"    证据: {r.evidence}")
            if r.transmission_path:
                lines.append(f"    传导路径: {r.transmission_path}")
            if r.impact:
                lines.append(f"    影响指标: {r.impact}")
        return "\n".join(lines)

    def run_quantitative_scoring(**kwargs) -> str:
        """执行量化评分"""
        from app.finance.metrics import score_profitability, score_safety, score_valuation, overall_rating
        if not state.metrics:
            return "需要先获取财务数据"
        profit = score_profitability(state.metrics)
        industry = state.profile.industry if state.profile else ""
        safety = score_safety(state.metrics, industry=industry)
        val = score_valuation(state.profile) if state.profile else {"score": 0, "details": "无数据"}
        rating, detail = overall_rating(profit["score"], safety["score"], val["score"])
        state.sections["rating"] = rating
        state.sections["rating_detail"] = detail
        state.sections["scores"] = f"盈利 {profit['score']} | 安全 {safety['score']} | 估值 {val['score']}"
        return (
            f"盈利能力: {profit['score']}/100 — {profit['details']}\n"
            f"安全性: {safety['score']}/100 — {safety['details']}\n"
            f"估值: {val['score']}/100 — {val['details']}\n"
            f"综合评级: {rating} ({detail})"
        )

    def rag_query(question: str = "") -> str:
        """从知识库检索相关信息（含重排序）"""
        from app.rag.knowledge_base import get_knowledge_base
        if not question:
            return "请提供检索问题"
        kb = get_knowledge_base()
        results = kb.query(question, top_k=5, candidate_k=15, use_rerank=True)
        return kb.format_context(results)

    def fetch_announcements_tool(limit: int = 5) -> str:
        try:
            items = fetch_announcements(state.stock_code, state.stock_name, limit=limit)
        except Exception as exc:
            message = str(exc)
            state.sections["announcement_error"] = message
            sync_live_tools_status(state, live_tools_success_state, success_key="announcement", succeeded=False, error_key="announcement", error_message=message)
            return f"获取失败: {message}"
        state.announcements = items
        state.source_refs.extend(_build_live_source_refs(items, source_type="announcement", default_title="", default_retrieval_mode="fallback_news", default_evidence_type="announcement"))
        update_live_tools_payload(state, announcement_count=len(items), source_ref_count=len(state.source_refs))
        sync_live_tools_status(state, live_tools_success_state, success_key="announcement", succeeded=True, error_key="announcement")
        if not items:
            return "未获取到公告"
        return "\n".join(f"- {item['title']} | {item.get('time', '')} | {item.get('source', '')}" for item in items)

    def fetch_live_quotes_tool(**kwargs) -> str:
        try:
            quote = fetch_live_quotes(state.stock_code)
        except Exception as exc:
            message = str(exc)
            state.sections["quote_error"] = message
            sync_live_tools_status(state, live_tools_success_state, success_key="quote", succeeded=False, error_key="quote", error_message=message)
            return f"获取失败: {message}"
        quote_summary = format_live_quote_summary(quote)
        state.source_refs.append(_build_quote_source_ref(quote))
        update_live_tools_payload(
            state,
            quote_snapshot=dict(quote),
            quote_summary=quote_summary,
            source_ref_count=len(state.source_refs),
        )
        sync_live_tools_status(state, live_tools_success_state, success_key="quote", succeeded=True, error_key="quote")
        state.sections["live_quote_snapshot"] = str(quote)
        return (
            f"标题: {quote.get('title', '')}\n"
            f"PE: {quote.get('pe_ratio', 0):.1f} | PB: {quote.get('pb_ratio', 0):.1f}\n"
            f"市值: {quote.get('market_cap', 0):.0f}亿"
        )

    def fetch_exchange_filings_tool(limit: int = 5) -> str:
        try:
            items = fetch_exchange_filings(state.stock_code, state.stock_name, limit=limit)
        except Exception as exc:
            message = str(exc)
            state.sections["filing_error"] = message
            sync_live_tools_status(state, live_tools_success_state, success_key="filing", succeeded=False, error_key="filing", error_message=message)
            return f"获取失败: {message}"
        state.filings = items
        state.source_refs.extend(_build_live_source_refs(items, source_type="filing", default_title="", default_retrieval_mode="fallback_news", default_evidence_type="filing"))
        update_live_tools_payload(state, filing_count=len(items), source_ref_count=len(state.source_refs))
        sync_live_tools_status(state, live_tools_success_state, success_key="filing", succeeded=True, error_key="filing")
        if not items:
            return "未获取到交易所文件"
        return "\n".join(f"- {item['title']} | {item.get('time', '')} | {item.get('source', '')}" for item in items)

    def fetch_broker_reports_tool(limit: int = 3) -> str:
        try:
            items = fetch_broker_reports(state.stock_code, state.stock_name, limit=limit)
        except Exception as exc:
            message = str(exc)
            state.sections["broker_report_error"] = message
            sync_live_tools_status(state, live_tools_success_state, success_key="broker_report", succeeded=False, error_key="broker_report", error_message=message)
            return f"获取失败: {message}"
        state.source_refs.extend(_build_live_source_refs(items, source_type="broker_report", default_title="券商观点", default_retrieval_mode="placeholder", default_evidence_type="broker_view"))
        update_live_tools_payload(state, broker_report_count=len(items), source_ref_count=len(state.source_refs))
        sync_live_tools_status(state, live_tools_success_state, success_key="broker_report", succeeded=True, error_key="broker_report")
        if not items:
            return "未获取到券商研报"
        return "\n".join(f"- {item['title']} | {item.get('summary', '')}" for item in items)

    def fetch_fund_holdings_tool(limit: int = 5) -> str:
        try:
            items = fetch_fund_holdings(state.stock_code, limit=limit)
        except Exception as exc:
            message = str(exc)
            state.sections["fund_holding_error"] = message
            sync_live_tools_status(state, live_tools_success_state, success_key="fund_holding", succeeded=False, error_key="fund_holding", error_message=message)
            return f"获取失败: {message}"
        state.source_refs.extend(_build_live_source_refs(items, source_type="fund_holding", default_title="基金持仓", default_retrieval_mode="api", default_evidence_type="institutional_holding"))
        update_live_tools_payload(state, fund_holding_count=len(items), source_ref_count=len(state.source_refs))
        sync_live_tools_status(state, live_tools_success_state, success_key="fund_holding", succeeded=True, error_key="fund_holding")
        if not items:
            return "未获取到基金持仓"
        return "\n".join(f"- {item['title']} | {item.get('summary', '')}" for item in items)

    def extract_document_tables_tool(source_id: str = "") -> str:
        if not state.documents:
            return "暂无已上传文档"
        document = next((doc for doc in state.documents if not source_id or doc.source_id == source_id), state.documents[0])
        tables = extract_document_tables(document)
        if not tables:
            return f"文档《{document.title}》未识别到表格"
        summaries = []
        for idx, table in enumerate(tables, 1):
            headers = " / ".join(table.get("headers", [])[:5])
            summaries.append(f"表{idx}: {len(table.get('rows', []))}行 | {headers}")
        return "\n".join(summaries)

    def extract_document_summary_tool(source_id: str = "") -> str:
        if not state.documents:
            return "暂无已上传文档"
        document = next((doc for doc in state.documents if not source_id or doc.source_id == source_id), state.documents[0])
        summary = extract_document_summary(document)
        return (
            f"标题: {summary.get('title', '')}\n"
            f"类型: {summary.get('source_type', '')} | 状态: {summary.get('parse_status', '')}\n"
            f"摘要: {summary.get('summary', '')}"
        )

    # ── 工具注册（含 function calling schema）──

    return [
        Tool("fetch_stock_profile", "获取公司基本信息（名称、行业、市值、PE、PB）",
             {"type": "object", "properties": {"code": {"type": "string", "description": "股票代码,默认当前股票"}}, "required": []},
             fetch_stock_profile, critical=True),
        Tool("fetch_financials", "获取多年财务数据（营收、利润、ROE、毛利率等,覆盖3-5年）",
             {"type": "object", "properties": {"code": {"type": "string", "description": "股票代码,默认当前股票"}}, "required": []},
             fetch_financials, critical=True),
        Tool("fetch_peers", "获取同行业可比公司及其关键财务指标",
             {"type": "object", "properties": {"industry": {"type": "string", "description": "行业名称,默认当前公司行业"}}, "required": []},
             fetch_peers),
        Tool("fetch_news", "获取公司近期新闻",
             {"type": "object", "properties": {"name": {"type": "string", "description": "公司名称,默认当前公司"}}, "required": []},
             fetch_news),
        Tool("fetch_announcements", "获取近期公告/公告摘要（带来源元信息）",
             {"type": "object", "properties": {"limit": {"type": "integer", "description": "返回条数,默认5"}}, "required": []},
             fetch_announcements_tool),
        Tool("fetch_live_quotes", "获取实时行情快照与估值相关字段（带来源元信息）",
             {"type": "object", "properties": {}, "required": []},
             fetch_live_quotes_tool),
        Tool("fetch_exchange_filings", "获取交易所文件/披露线索（带来源元信息）",
             {"type": "object", "properties": {"limit": {"type": "integer", "description": "返回条数,默认5"}}, "required": []},
             fetch_exchange_filings_tool),
        Tool("fetch_broker_reports", "获取东方财富券商研报列表，失败后回退新闻观点来源",
             {"type": "object", "properties": {"limit": {"type": "integer", "description": "返回条数,默认3"}}, "required": []},
             fetch_broker_reports_tool),
        Tool("fetch_fund_holdings", "获取基金持仓/机构持股线索（带来源元信息）",
             {"type": "object", "properties": {"limit": {"type": "integer", "description": "返回条数,默认5"}}, "required": []},
             fetch_fund_holdings_tool),
        Tool("extract_document_tables", "提取已上传文档中的结构化表格摘要",
             {"type": "object", "properties": {"source_id": {"type": "string", "description": "文档 source_id，默认取第一份"}}, "required": []},
             extract_document_tables_tool),
        Tool("extract_document_summary", "提取已上传文档的文本摘要与解析状态",
             {"type": "object", "properties": {"source_id": {"type": "string", "description": "文档 source_id，默认取第一份"}}, "required": []},
             extract_document_summary_tool),
        Tool("dupont_analysis", "执行杜邦分析：将ROE分解为净利率×资产周转率×权益乘数",
             {"type": "object", "properties": {}, "required": []},
             run_dupont_analysis, cacheable=False),
        Tool("dcf_valuation", "执行DCF现金流折现估值+蒙特卡洛模拟+敏感性分析",
             {"type": "object", "properties": {}, "required": []},
             run_dcf_valuation, cacheable=False),
        Tool("comparable_valuation", "执行可比公司估值,用同行PE/PB均值推算隐含价值",
             {"type": "object", "properties": {}, "required": []},
             run_comparable_valuation, cacheable=False),
        Tool("trend_analysis", "执行多年趋势分析,计算CAGR和趋势方向",
             {"type": "object", "properties": {}, "required": []},
             run_trend_analysis, cacheable=False),
        Tool("risk_assessment", "评估财务风险和舆情风险",
             {"type": "object", "properties": {}, "required": []},
             run_risk_assessment, cacheable=False),
        Tool("quantitative_scoring", "量化评分(盈利/安全/估值)并给出综合评级",
             {"type": "object", "properties": {}, "required": []},
             run_quantitative_scoring, cacheable=False),
        Tool("rag_query", "从金融知识库检索相关专业知识（含LLM重排序）",
             {"type": "object", "properties": {"question": {"type": "string", "description": "检索问题"}}, "required": ["question"]},
             rag_query),
    ]


def tools_to_function_specs(tools: list[Tool]) -> list[dict]:
    """将工具列表转换为智谱 function calling 格式"""
    specs = []
    for t in tools:
        specs.append({
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters_schema,
            },
        })
    return specs


def format_tools_prompt(tools: list[Tool]) -> str:
    """生成工具列表说明供 Agent System Prompt 使用（兼容 ReAct 文本模式）"""
    lines = ["你可以使用以下工具：\n"]
    for t in tools:
        params_desc = ", ".join(
            f"{k}({v.get('description', '')})"
            for k, v in t.parameters_schema.get("properties", {}).items()
        )
        lines.append(f"- **{t.name}**: {t.description}。参数: {params_desc or '无'}")
    return "\n".join(lines)


def execute_tool(
    tools: list[Tool],
    name: str,
    args: dict[str, Any],
    state: AnalysisState | None = None,
    max_retries: int = 2,
) -> str:
    """执行指定工具（支持重试和缓存）"""
    tool = None
    for t in tools:
        if t.name == name:
            tool = t
            break
    if not tool:
        return f"未知工具: {name}"

    # 查找缓存（相同工具+相同参数 → 复用观察结果）
    if tool.cacheable and state:
        args_key = json.dumps(args, sort_keys=True, ensure_ascii=False)
        for record in state.tool_memory:
            cached_key = json.dumps(record.args, sort_keys=True, ensure_ascii=False)
            if record.tool_name == name and cached_key == args_key and record.success:
                logger.info(f"工具缓存命中: {name}")
                return f"[缓存] {record.observation}"

    # 执行（带重试）
    retries = max_retries if tool.retryable else 0
    last_error = ""
    tracer = get_active_tracer()
    for attempt in range(retries + 1):
        try:
            if tracer:
                with tracer.span(name, "tool", args=str(args)[:200]):
                    result = tool.function(**args)
            else:
                result = tool.function(**args)
            # 记录到 memory
            if state:
                state.tool_memory.append(ToolCallRecord(
                    tool_name=name, args=args, observation=result,
                    success=True, attempts=attempt + 1,
                ))
            return result
        except Exception as e:
            last_error = str(e)
            logger.warning(f"工具 {name} 执行失败 (attempt={attempt+1}): {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)

    # 记录失败
    if state:
        state.tool_memory.append(ToolCallRecord(
            tool_name=name, args=args, observation=f"失败: {last_error}",
            success=False, attempts=retries + 1,
        ))
    if tool.critical:
        return f"[关键工具失败] 工具执行失败({retries + 1}次尝试): {last_error}"
    return f"[非关键] 工具执行失败({retries + 1}次尝试): {last_error}（不影响研报核心内容生成）"
