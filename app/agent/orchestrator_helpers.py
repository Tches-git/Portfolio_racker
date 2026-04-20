"""AgentOrchestrator 的可复用辅助函数。"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import MAX_REPORT_RAG_CONTEXTS
from app.models import AnalysisState


def parallel_rag_queries(orchestrator, kb, queries: list[str], logger) -> list[str]:
    rag_contexts: list[str] = []
    with ThreadPoolExecutor(max_workers=min(len(queries), MAX_REPORT_RAG_CONTEXTS)) as pool:
        future_map = {
            pool.submit(kb.query, q, top_k=3, candidate_k=10, use_rerank=True): q
            for q in queries[:MAX_REPORT_RAG_CONTEXTS]
        }
        for future in as_completed(future_map):
            query = future_map[future]
            try:
                results = future.result()
            except Exception as e:
                logger.warning(f"RAG 查询失败 [{query}]: {e}")
                continue
            if results:
                rag_contexts.append(kb.format_context(results))
                for item in results:
                    orchestrator._rag_hits.append({
                        "query": query,
                        "content": item["content"][:100],
                        "score": item.get("rerank_score", item.get("score", 0)),
                        "source": item.get("metadata", {}).get("source_file", ""),
                        "page": item.get("metadata", {}).get("source_page", ""),
                    })
    return rag_contexts


def compact_report_context(text: str, limit: int, label: str) -> str:
    if len(text) <= limit:
        return text
    head = max(limit // 2, 200)
    tail = max(limit - head - len(label) - 32, 120)
    return f"{text[:head]}\n\n[{label} 已截断，保留前后关键信息]\n\n{text[-tail:]}"


def extract_section_body(report: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(report)
    return match.group(1).strip() if match else ""


def upsert_section(report: str, heading: str, body: str) -> str:
    section_text = f"## {heading}\n{body.strip()}".strip()
    pattern = re.compile(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(report):
        return pattern.sub(section_text + "\n\n", report, count=1).rstrip()
    return report.rstrip() + "\n\n" + section_text + "\n"


def collect_data_gaps(state: AnalysisState) -> list[str]:
    gaps: list[str] = []
    if not state.profile:
        gaps.append("公司基础信息不足，行业/市值/估值口径可能不完整")
    if not state.metrics:
        gaps.append("财务数据不足，无法支撑核心财务与盈利质量判断")
    else:
        latest = state.metrics[0]
        if latest.cash_flow == 0:
            gaps.append("经营现金流数据不足，现金流质量结论需降级")
        if latest.total_assets == 0 or latest.total_equity == 0:
            gaps.append("资产负债表字段不完整，杜邦和杠杆解读需降级")
    if not state.peers:
        gaps.append("同行可比数据不足，相对估值与竞争格局判断需降级")
    if not state.news:
        gaps.append("新闻/舆情数据不足，事件驱动与风险提示需降级")
    if not state.dcf:
        gaps.append("DCF 估值结果不足，目标价锚需降级为区间或谨慎表述")
    return gaps


def build_tracking_indicators(state: AnalysisState) -> list[str]:
    indicators: list[str] = []
    if state.metrics:
        latest = state.metrics[0]
        if latest.revenue_yoy:
            indicators.append(f"营收增速（最新 {latest.revenue_yoy:+.1f}%）")
        else:
            indicators.append("营收增速")
        if latest.profit_yoy:
            indicators.append(f"净利润增速（最新 {latest.profit_yoy:+.1f}%）")
        else:
            indicators.append("净利润增速")
        if latest.roe:
            indicators.append(f"ROE（最新 {latest.roe:.1f}%）")
        if latest.cash_flow:
            indicators.append(f"经营现金流（最新 {latest.cash_flow:.1f}亿）")
        else:
            indicators.append("经营现金流")
    if state.dcf and state.dcf.per_share_value > 0:
        indicators.append(f"DCF 估值锚（每股价值 {state.dcf.per_share_value:.2f}元）")
    if state.peers:
        indicators.append("同行估值溢价/折价变化")
    if state.news:
        indicators.append("监管与舆情事件进展")
    seen: list[str] = []
    for item in indicators:
        if item not in seen:
            seen.append(item)
    return seen[:5] or ["营收增速", "净利润增速", "ROE", "经营现金流", "估值中枢变化"]


def build_investment_advice_block(state: AnalysisState, *, tracking_indicators: list[str] | None = None) -> str:
    rating = state.sections.get("rating", "中性")
    rating_detail = state.sections.get("rating_detail", "现有证据下维持审慎判断")
    if state.dcf and state.dcf.per_share_value > 0 and state.dcf.current_price > 0:
        anchor_text = (
            f"估值锚：DCF 对应每股价值 {state.dcf.per_share_value:.2f} 元，当前股价 {state.dcf.current_price:.2f} 元，"
            f"对应上涨空间 {state.dcf.upside:+.1f}%。"
        )
    else:
        anchor_text = "估值锚：现有数据不足以形成稳定目标价锚，建议等待更多财务与行业数据验证后再更新判断。"
    tracking = "；".join(tracking_indicators or build_tracking_indicators(state))
    return (
        f"当前评级：{rating}（{rating_detail}）。\n\n"
        f"{anchor_text}\n\n"
        f"后续跟踪指标：{tracking}。"
    )


def build_missing_section_body(orchestrator, heading: str, state: AnalysisState) -> str:
    research_conclusion = state.sections.get("research_conclusion", "现有数据不足以支持进一步判断。")
    if heading == "一、投资要点":
        body = research_conclusion[:280] or "现有数据不足以支持进一步判断。"
        gaps = collect_data_gaps(state)
        if gaps:
            body += "\n\n数据降级说明：" + "；".join(gaps[:2])
        return body
    if heading == "七、核心风险与跟踪指标":
        body = f"### 风险证据与传导路径\n{orchestrator._format_risks(state)}\n\n### 后续跟踪指标\n- " + "\n- ".join(build_tracking_indicators(state))
        gaps = collect_data_gaps(state)
        if gaps:
            body += "\n\n### 数据降级说明\n- " + "\n- ".join(gaps)
        return body
    if heading == "八、投资建议":
        return build_investment_advice_block(state)
    return "现有数据不足以支持进一步判断，本节暂以已有研究结论和已披露数据为基础，后续需结合更多财务与行业信息补充。"


def post_process_report(orchestrator, report: str, state: AnalysisState) -> str:
    report = (report or "").strip()
    if not report:
        return report
    expected_title = f"# {state.stock_name}（{state.stock_code}）深度研究报告"
    if report.startswith("# "):
        lines = report.splitlines()
        if lines:
            lines[0] = expected_title
            report = "\n".join(lines)
        else:
            report = expected_title
    else:
        report = expected_title + "\n\n" + report

    required_sections = [
        "一、投资要点",
        "二、公司概况与商业模式",
        "三、财务与盈利质量分析",
        "四、杜邦分析与经营效率",
        "五、估值分析",
        "六、行业格局与可比公司对比",
        "七、核心风险与跟踪指标",
        "八、投资建议",
    ]
    fixes: list[str] = []
    for heading in required_sections:
        if not re.search(rf"^## {re.escape(heading)}$", report, re.MULTILINE):
            report = upsert_section(report, heading, build_missing_section_body(orchestrator, heading, state))
            fixes.append(f"missing_section:{heading}")

    risk_heading = "七、核心风险与跟踪指标"
    risk_body = extract_section_body(report, risk_heading)
    tracking_indicators = build_tracking_indicators(state)
    if state.risks and ("证据：" not in risk_body or "传导路径：" not in risk_body):
        supplement = f"### 风险证据与传导路径\n{orchestrator._format_risks(state)}\n\n### 后续跟踪指标\n- " + "\n- ".join(tracking_indicators)
        if "### 风险证据与传导路径" not in risk_body:
            risk_body = (risk_body + "\n\n" + supplement).strip() if risk_body else supplement
            fixes.append("risk_section_enriched")
        report = upsert_section(report, risk_heading, risk_body)

    gaps = collect_data_gaps(state)
    if gaps and "数据降级说明" not in risk_body:
        risk_body = extract_section_body(report, risk_heading)
        risk_body = (risk_body + "\n\n### 数据降级说明\n- " + "\n- ".join(gaps)).strip()
        report = upsert_section(report, risk_heading, risk_body)
        fixes.append("data_gap_disclosure")

    advice_heading = "八、投资建议"
    advice_body = extract_section_body(report, advice_heading)
    if any(keyword not in advice_body for keyword in ("评级", "估值锚", "后续跟踪指标")):
        supplement = build_investment_advice_block(state, tracking_indicators=tracking_indicators)
        if supplement not in advice_body:
            advice_body = (advice_body + "\n\n" + supplement).strip() if advice_body else supplement
            report = upsert_section(report, advice_heading, advice_body)
            fixes.append("investment_section_enriched")

    state.sections["postprocess_fix_count"] = str(len(fixes))
    state.sections["postprocess_fixes"] = "\n".join(fixes)
    return report.strip()
