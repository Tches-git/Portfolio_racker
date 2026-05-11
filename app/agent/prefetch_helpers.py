from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.models import AnalysisState, ToolCallRecord

LIVE_TOOL_KEYS = ("announcement", "filing", "quote", "broker_report", "fund_holding")
LIVE_TOOL_ERROR_LABELS = {
    "announcement": "公告",
    "filing": "交易所披露",
    "quote": "行情",
    "broker_report": "券商观点",
    "fund_holding": "基金持仓",
}


def format_profile_observation(profile) -> str:
    return (
        f"公司: {profile.name} ({profile.code})\n"
        f"行业: {profile.industry}\n"
        f"市值: {profile.market_cap:.0f}亿\n"
        f"PE: {profile.pe_ratio:.1f} | PB: {profile.pb_ratio:.1f}\n"
        f"总股本: {profile.total_shares:.2f}亿股"
    )


def format_financials_observation(metrics: list) -> str:
    if not metrics:
        return "未获取到财务数据"
    lines = [f"获取到 {len(metrics)} 期财务数据:"]
    for metric in metrics[:8]:
        lines.append(metric.summary())
    return "\n".join(lines)


def format_peers_observation(peers: list, industry: str) -> str:
    if not peers:
        return f"未找到{industry}行业的可比公司"
    lines = [f"找到 {len(peers)} 家{industry}行业可比公司:"]
    for peer in peers:
        lines.append(f"  {peer.name}({peer.code}): 市值{peer.market_cap:.0f}亿 PE={peer.pe_ratio:.1f} ROE={peer.roe:.1f}%")
    return "\n".join(lines)


def format_news_observation(news: list[dict]) -> str:
    if not news:
        return "未获取到新闻"
    lines = [f"获取到 {len(news)} 条新闻:"]
    for item in news[:5]:
        lines.append(f"  · {item['title']}")
    return "\n".join(lines)


def format_live_quote_summary(quote: dict) -> str:
    if not quote:
        return ""
    return (
        f"{quote.get('title', '快照')} | PE {quote.get('pe_ratio', 0):.1f} | "
        f"PB {quote.get('pb_ratio', 0):.1f} | 市值 {quote.get('market_cap', 0):.0f}亿"
    )


def build_quote_source_ref(stock_code: str, quote: dict) -> dict:
    return {
        "source_id": f"quote_{stock_code}",
        "title": quote.get("title", "实时行情快照"),
        "source_type": "quote",
        "summary": format_live_quote_summary(quote),
        "time": quote.get("time", ""),
        "source": quote.get("source", "live_quote"),
        "provider": quote.get("provider", "unknown"),
        "channel": quote.get("channel", "live_quote"),
        "retrieval_mode": quote.get("retrieval_mode", "api"),
        "evidence_type": quote.get("evidence_type", "quote"),
        "link": quote.get("link", ""),
        "parse_status": "success",
        "is_placeholder": bool(quote.get("is_placeholder", False)),
    }


def build_live_source_refs(items: list[dict], *, source_type: str, default_title: str, default_retrieval_mode: str, default_evidence_type: str) -> list[dict]:
    refs: list[dict] = []
    for item in items:
        refs.append({
            "source_id": item.get("id", ""),
            "title": item.get("title", default_title),
            "source_type": source_type,
            "summary": item.get("summary", ""),
            "time": item.get("time", ""),
            "source": item.get("source", ""),
            "provider": item.get("provider", ""),
            "channel": item.get("channel", source_type),
            "retrieval_mode": item.get("retrieval_mode", default_retrieval_mode),
            "evidence_type": item.get("evidence_type", default_evidence_type),
            "link": item.get("link", ""),
            "parse_status": "success",
            "is_placeholder": bool(item.get("is_placeholder", False)),
        })
    return refs


def build_document_source_ref(document, *, summary: dict, table_count: int) -> dict:
    return {
        "source_id": document.source_id,
        "title": document.title,
        "source_type": document.source_type,
        "summary": summary.get("summary", ""),
        "time": document.extracted_at,
        "source": document.metadata.get("file_name", document.title),
        "provider": "upload",
        "channel": "upload",
        "retrieval_mode": "user_upload",
        "evidence_type": "document_extract",
        "link": "",
        "parse_status": summary.get("parse_status", "success"),
        "table_count": str(table_count),
        "is_placeholder": False,
    }


def build_prefetch_runtime_payload(state: AnalysisState) -> dict:
    return {
        "profile_ready": bool(state.profile),
        "metrics_count": len(state.metrics),
        "peers_count": len(state.peers),
        "news_count": len(state.news),
    }


def build_document_runtime_payload(*, summary_text: str, parse_rate: str, table_rate: str, failure_count: int) -> dict:
    return {
        "summary": summary_text,
        "parse_success_rate": parse_rate,
        "table_extraction_success_rate": table_rate,
        "failure_count": failure_count,
    }


def sync_document_parse_payload(state: AnalysisState, *, summary_text: str, parse_rate: str, table_rate: str, failure_count: int) -> dict:
    state.sections["document_parse_summary"] = summary_text
    state.sections["document_parse_success_rate"] = parse_rate
    state.sections["table_extraction_success_rate"] = table_rate
    state.sections["document_parse_failure_count"] = str(failure_count)
    payload = build_document_runtime_payload(
        summary_text=summary_text,
        parse_rate=parse_rate,
        table_rate=table_rate,
        failure_count=failure_count,
    )
    state.runtime_input_payload["documents"] = payload
    return payload


def format_document_parse_summary(documents: list) -> str:
    if not documents:
        return "未提供文档"
    lines = []
    for document in documents:
        parse_status = document.metadata.get("parse_status", "success")
        lines.append(
            f"- {document.title} | 类型={document.source_type} | 文本块={len(document.text_blocks)} | 表格={len(document.tables)} | 状态={parse_status}"
        )
    return "\n".join(lines)


def summarize_uploaded_documents(documents: list, *, extract_document_summary, extract_document_tables) -> dict:
    source_refs: list[dict] = []
    parse_success = 0
    table_success = 0
    for document in documents:
        summary = extract_document_summary(document)
        tables = extract_document_tables(document)
        if summary.get("parse_status") != "partial":
            parse_success += 1
        if tables:
            table_success += 1
        source_refs.append(build_document_source_ref(document, summary=summary, table_count=len(tables)))

    total = len(documents) or 1
    failure_count = total - parse_success
    return {
        "parse_success": parse_success,
        "table_success": table_success,
        "source_refs": source_refs,
        "summary_text": format_document_parse_summary(documents),
        "parse_rate": f"{parse_success / total:.2f}",
        "table_rate": f"{table_success / total:.2f}",
        "failure_count": failure_count,
    }


def ingest_uploaded_documents(state: AnalysisState, uploaded_items: list[dict], *, parse_uploaded_items=None, extract_document_summary=None, extract_document_tables=None) -> dict:
    if not uploaded_items:
        state.documents = []
        payload = sync_document_parse_payload(
            state,
            summary_text="未提供多模态文档，继续走默认单股票路径。",
            parse_rate="1.00",
            table_rate="0.00",
            failure_count=0,
        )
        return {
            "documents": [],
            "source_refs": [],
            "summary_text": payload["summary"],
            "parse_success": 0,
            "table_success": 0,
            "failure_count": 0,
            "parse_rate": payload["parse_success_rate"],
            "table_rate": payload["table_extraction_success_rate"],
            "payload": payload,
        }

    if parse_uploaded_items is None:
        from app.data_source.multimodal import parse_uploaded_items as default_parse_uploaded_items

        parse_uploaded_items = default_parse_uploaded_items
    if extract_document_summary is None or extract_document_tables is None:
        from app.data_source.live_tools import (
            extract_document_summary as default_extract_document_summary,
            extract_document_tables as default_extract_document_tables,
        )

        extract_document_summary = extract_document_summary or default_extract_document_summary
        extract_document_tables = extract_document_tables or default_extract_document_tables

    documents = parse_uploaded_items(uploaded_items)
    state.documents = documents
    summary = summarize_uploaded_documents(
        documents,
        extract_document_summary=extract_document_summary,
        extract_document_tables=extract_document_tables,
    )
    state.source_refs.extend(summary["source_refs"])
    payload = sync_document_parse_payload(
        state,
        summary_text=summary["summary_text"],
        parse_rate=summary["parse_rate"],
        table_rate=summary["table_rate"],
        failure_count=summary["failure_count"],
    )
    return {
        "documents": documents,
        **summary,
        "payload": payload,
    }


def format_live_tool_error_summary(errors: dict[str, str]) -> str:
    if not errors:
        return ""
    return "；".join(
        f"{LIVE_TOOL_ERROR_LABELS.get(key, key)}: {message}"
        for key, message in errors.items()
        if message
    )


def build_live_tools_runtime_payload(*, success_count: int, tool_count: int, announcement_count: int, filing_count: int, broker_report_count: int, source_ref_count: int, quote_snapshot: dict, errors: dict[str, str], error_summary: str, fund_holding_count: int = 0) -> dict:
    return {
        "success_rate": f"{success_count / tool_count:.2f}" if tool_count > 0 else "0.00",
        "success_count": success_count,
        "tool_count": tool_count,
        "failed_count": max(tool_count - success_count, 0),
        "announcement_count": announcement_count,
        "filing_count": filing_count,
        "broker_report_count": broker_report_count,
        "fund_holding_count": fund_holding_count,
        "source_ref_count": source_ref_count,
        "quote_snapshot": quote_snapshot,
        "quote_summary": format_live_quote_summary(quote_snapshot),
        "errors": errors,
        "error_count": len(errors),
        "error_summary": error_summary,
    }


def initialize_live_tools_payload(state: AnalysisState) -> dict:
    payload = state.runtime_input_payload.get("live_tools", {})
    return payload if isinstance(payload, dict) else {}


def update_live_tools_payload(state: AnalysisState, *, remove_keys: tuple[str, ...] = (), **updates) -> dict:
    payload = dict(initialize_live_tools_payload(state))
    for key in remove_keys:
        payload.pop(key, None)
    payload.update(updates)
    state.runtime_input_payload["live_tools"] = payload
    return payload


def sync_live_tools_status(state: AnalysisState, live_tools_success_state: dict[str, bool], *, success_key: str | None = None, succeeded: bool, error_key: str | None = None, error_message: str = "") -> dict:
    payload = initialize_live_tools_payload(state)
    errors = dict(payload.get("errors", {})) if isinstance(payload.get("errors", {}), dict) else {}
    if success_key:
        live_tools_success_state[success_key] = succeeded
    if error_key:
        if error_message:
            errors[error_key] = error_message
        else:
            errors.pop(error_key, None)
    success_count = sum(1 for key in LIVE_TOOL_KEYS if live_tools_success_state.get(key))
    tool_count = max(int(payload.get("tool_count", 0) or 0), len(LIVE_TOOL_KEYS))
    updates = {
        "errors": errors,
        "tool_count": tool_count,
        "success_count": success_count,
        "failed_count": sum(1 for key in LIVE_TOOL_KEYS if key in errors),
        "error_count": len(errors),
        "error_summary": format_live_tool_error_summary(errors),
    }
    if tool_count > 0:
        updates["success_rate"] = f"{success_count / tool_count:.2f}"
    return update_live_tools_payload(state, remove_keys=("success_map",), **updates)


def fetch_orchestrator_live_sources(state: AnalysisState, *, fetch_announcements=None, fetch_exchange_filings=None, fetch_live_quotes=None, fetch_broker_reports=None, fetch_fund_holdings=None) -> dict:
    if fetch_announcements is None or fetch_exchange_filings is None or fetch_live_quotes is None or fetch_broker_reports is None or fetch_fund_holdings is None:
        from app.data_source.live_tools import (
            fetch_announcements as default_fetch_announcements,
            fetch_broker_reports as default_fetch_broker_reports,
            fetch_exchange_filings as default_fetch_exchange_filings,
            fetch_fund_holdings as default_fetch_fund_holdings,
            fetch_live_quotes as default_fetch_live_quotes,
        )

        fetch_announcements = fetch_announcements or default_fetch_announcements
        fetch_exchange_filings = fetch_exchange_filings or default_fetch_exchange_filings
        fetch_live_quotes = fetch_live_quotes or default_fetch_live_quotes
        fetch_broker_reports = fetch_broker_reports or default_fetch_broker_reports
        fetch_fund_holdings = fetch_fund_holdings or default_fetch_fund_holdings

    success_count = 0
    live_tool_errors: dict[str, str] = {}
    live_quote_snapshot: dict | None = None
    broker_reports: list[dict] = []
    fund_holdings: list[dict] = []

    try:
        state.announcements = fetch_announcements(state.stock_code, state.stock_name)
        success_count += 1
    except Exception as exc:
        live_tool_errors["announcement"] = str(exc)
        state.sections["announcement_error"] = str(exc)

    try:
        state.filings = fetch_exchange_filings(state.stock_code, state.stock_name)
        success_count += 1
    except Exception as exc:
        live_tool_errors["filing"] = str(exc)
        state.sections["filing_error"] = str(exc)

    try:
        quote = fetch_live_quotes(state.stock_code)
        live_quote_snapshot = dict(quote)
        state.sections["live_quote_snapshot"] = str(quote)
        state.source_refs.append(build_quote_source_ref(state.stock_code, quote))
        success_count += 1
    except Exception as exc:
        live_tool_errors["quote"] = str(exc)
        state.sections["quote_error"] = str(exc)

    try:
        broker_reports = fetch_broker_reports(state.stock_code, state.stock_name)
        state.source_refs.extend(build_live_source_refs(broker_reports, source_type="broker_report", default_title="券商观点", default_retrieval_mode="placeholder", default_evidence_type="broker_view"))
        success_count += 1
    except Exception as exc:
        live_tool_errors["broker_report"] = str(exc)
        state.sections["broker_report_error"] = str(exc)

    try:
        fund_holdings = fetch_fund_holdings(state.stock_code)
        state.source_refs.extend(build_live_source_refs(fund_holdings, source_type="fund_holding", default_title="基金持仓", default_retrieval_mode="api", default_evidence_type="institutional_holding"))
        success_count += 1
    except Exception as exc:
        live_tool_errors["fund_holding"] = str(exc)
        state.sections["fund_holding_error"] = str(exc)

    for items, source_type in ((state.announcements, "announcement"), (state.filings, "filing")):
        state.source_refs.extend(build_live_source_refs(items, source_type=source_type, default_title="", default_retrieval_mode="fallback_news", default_evidence_type=source_type))

    live_tools_payload = build_live_tools_runtime_payload(
        success_count=success_count,
        tool_count=len(LIVE_TOOL_KEYS),
        announcement_count=len(state.announcements),
        filing_count=len(state.filings),
        broker_report_count=len(broker_reports),
        fund_holding_count=len(fund_holdings),
        source_ref_count=len(state.source_refs),
        quote_snapshot=live_quote_snapshot or {},
        errors=live_tool_errors,
        error_summary=format_live_tool_error_summary(live_tool_errors),
    )
    state.sections["live_tool_success_rate"] = live_tools_payload["success_rate"]
    state.runtime_input_payload["live_tools"] = live_tools_payload
    return live_tools_payload


def prefetch_core_data(state: AnalysisState, *, get_stock_profile, get_financial_metrics, logger) -> None:
    code = state.stock_code
    profile_result = None
    metrics_result = None
    profile_obs = ""
    metrics_obs = ""

    def fetch_profile():
        nonlocal profile_result, profile_obs
        try:
            profile = get_stock_profile(code)
            state.profile = profile
            state.stock_name = profile.name
            profile_result = profile
            profile_obs = format_profile_observation(profile)
        except Exception as exc:
            logger.warning(f"预取 profile 失败: {exc}")
            profile_obs = f"获取失败: {exc}"

    def fetch_financials():
        nonlocal metrics_result, metrics_obs
        try:
            metrics = get_financial_metrics(code)
            state.metrics = metrics
            metrics_result = metrics
            metrics_obs = format_financials_observation(metrics)
        except Exception as exc:
            logger.warning(f"预取 financials 失败: {exc}")
            metrics_obs = f"获取失败: {exc}"

    with ThreadPoolExecutor(max_workers=2) as pool:
        future_profile = pool.submit(fetch_profile)
        future_financials = pool.submit(fetch_financials)
        future_profile.result()
        future_financials.result()

    if profile_result:
        state.tool_memory.append(ToolCallRecord(tool_name="fetch_stock_profile", args={}, observation=profile_obs, success=True, from_cache=False, attempts=1))
    if metrics_result:
        state.tool_memory.append(ToolCallRecord(tool_name="fetch_financials", args={}, observation=metrics_obs, success=True, from_cache=False, attempts=1))


def prefetch_market_context(state: AnalysisState, *, get_peer_companies, get_recent_news, logger) -> None:
    profile = state.profile
    if not profile:
        return
    peers_obs = ""
    news_obs = ""

    def fetch_peers():
        nonlocal peers_obs
        try:
            peers = get_peer_companies(profile.industry, exclude_code=state.stock_code)
            state.peers = peers
            peers_obs = format_peers_observation(peers, profile.industry)
        except Exception as exc:
            logger.warning(f"预取 peers 失败: {exc}")
            peers_obs = f"获取失败: {exc}"

    def fetch_news():
        nonlocal news_obs
        try:
            news = get_recent_news(profile.name)
            state.news = news
            news_obs = format_news_observation(news)
        except Exception as exc:
            logger.warning(f"预取 news 失败: {exc}")
            news_obs = f"获取失败: {exc}"

    with ThreadPoolExecutor(max_workers=2) as pool:
        future_peers = pool.submit(fetch_peers)
        future_news = pool.submit(fetch_news)
        future_peers.result()
        future_news.result()

    if state.peers:
        state.tool_memory.append(ToolCallRecord(tool_name="fetch_peers", args={}, observation=peers_obs, success=True, from_cache=False, attempts=1))
    if state.news:
        state.tool_memory.append(ToolCallRecord(tool_name="fetch_news", args={}, observation=news_obs, success=True, from_cache=False, attempts=1))
