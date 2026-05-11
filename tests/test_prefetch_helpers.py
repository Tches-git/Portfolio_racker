from __future__ import annotations

from app.agent.prefetch_helpers import (
    build_document_runtime_payload,
    build_document_source_ref,
    build_live_source_refs,
    build_live_tools_runtime_payload,
    build_prefetch_runtime_payload,
    build_quote_source_ref,
    fetch_orchestrator_live_sources,
    format_document_parse_summary,
    format_financials_observation,
    format_live_quote_summary,
    format_live_tool_error_summary,
    format_news_observation,
    format_peers_observation,
    format_profile_observation,
    ingest_uploaded_documents,
    initialize_live_tools_payload,
    prefetch_core_data,
    prefetch_market_context,
    summarize_uploaded_documents,
    sync_document_parse_payload,
    sync_live_tools_status,
    update_live_tools_payload,
)
from app.models import AnalysisState, FinancialMetrics, PeerCompany, StockProfile


class DummyLogger:
    @staticmethod
    def warning(*args, **kwargs):
        return None


def test_format_helpers_match_expected_text_shape():
    profile = StockProfile(code="600519", name="茅台", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=10, total_shares=12)
    metrics = [FinancialMetrics(code="600519", period="2024Q4", revenue=100, net_profit=50, roe=20, gross_margin=80, debt_ratio=20)]
    peers = [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)]
    news = [{"title": "新闻1"}, {"title": "新闻2"}]
    quote = {"title": "快照", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000}

    assert "公司: 茅台 (600519)" in format_profile_observation(profile)
    assert "获取到 1 期财务数据" in format_financials_observation(metrics)
    assert "找到 1 家白酒行业可比公司" in format_peers_observation(peers, "白酒")
    assert "获取到 2 条新闻" in format_news_observation(news)
    assert format_live_quote_summary(quote) == "快照 | PE 20.0 | PB 5.0 | 市值 1000亿"


def test_prefetch_core_data_populates_state_and_tool_memory():
    state = AnalysisState(stock_code="600519")

    prefetch_core_data(
        state,
        get_stock_profile=lambda code: StockProfile(code=code, name="茅台", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=10, total_shares=10),
        get_financial_metrics=lambda code: [FinancialMetrics(code=code, period="2024Q4", revenue=100, net_profit=50, roe=20, gross_margin=80, debt_ratio=20)],
        logger=DummyLogger(),
    )

    assert state.profile is not None
    assert state.stock_name == "茅台"
    assert len(state.metrics) == 1
    assert [record.tool_name for record in state.tool_memory] == ["fetch_stock_profile", "fetch_financials"]


def test_prefetch_market_context_populates_state_and_tool_memory():
    state = AnalysisState(
        stock_code="600519",
        profile=StockProfile(code="600519", name="茅台", industry="白酒"),
        stock_name="茅台",
    )

    prefetch_market_context(
        state,
        get_peer_companies=lambda industry, exclude_code=None: [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)],
        get_recent_news=lambda name: [{"title": "新闻1"}, {"title": "新闻2"}],
        logger=DummyLogger(),
    )

    assert len(state.peers) == 1
    assert len(state.news) == 2
    assert [record.tool_name for record in state.tool_memory] == ["fetch_peers", "fetch_news"]


def test_prefetch_market_context_skips_when_profile_missing():
    state = AnalysisState(stock_code="600519")

    prefetch_market_context(
        state,
        get_peer_companies=lambda industry, exclude_code=None: [PeerCompany(code="000858", name="五粮液")],
        get_recent_news=lambda name: [{"title": "新闻1"}],
        logger=DummyLogger(),
    )

    assert state.peers == []
    assert state.news == []
    assert state.tool_memory == []


def test_source_ref_builders_share_contract_shape():
    quote_ref = build_quote_source_ref("600519", {"title": "快照", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000, "time": "2026-01-01", "source": "live", "provider": "akshare", "channel": "live_quote", "retrieval_mode": "api", "evidence_type": "quote", "link": ""})
    live_refs = build_live_source_refs([{"id": "a", "title": "公告", "summary": "摘要", "time": "2026-01-01", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "retrieval_mode": "api", "evidence_type": "announcement_update", "link": "http://a", "is_placeholder": False}], source_type="announcement", default_title="", default_retrieval_mode="fallback_news", default_evidence_type="announcement")
    document = type("Document", (), {"source_id": "doc1", "title": "材料A", "source_type": "pdf", "extracted_at": "2026-01-02", "metadata": {"file_name": "材料A.pdf"}})()
    document_ref = build_document_source_ref(document, summary={"summary": "文档摘要", "parse_status": "success"}, table_count=2)
    state = AnalysisState(stock_code="600519", profile=StockProfile(code="600519", name="茅台", industry="白酒"), metrics=[FinancialMetrics(code="600519", period="2024Q4")], peers=[PeerCompany(code="000858", name="五粮液")], news=[{"title": "新闻1"}])
    prefetch_payload = build_prefetch_runtime_payload(state)
    document_payload = build_document_runtime_payload(summary_text="文档摘要", parse_rate="0.80", table_rate="0.60", failure_count=1)
    live_tools_payload = build_live_tools_runtime_payload(success_count=3, tool_count=4, announcement_count=1, filing_count=1, broker_report_count=0, source_ref_count=3, quote_snapshot={"title": "快照", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000}, errors={"broker_report": "broker down"}, error_summary="券商观点: broker down")

    assert quote_ref["source_id"] == "quote_600519"
    assert quote_ref["summary"] == "快照 | PE 20.0 | PB 5.0 | 市值 1000亿"
    assert live_refs[0]["source_id"] == "a"
    assert live_refs[0]["source_type"] == "announcement"
    assert document_ref["source_id"] == "doc1"
    assert document_ref["evidence_type"] == "document_extract"
    assert document_ref["table_count"] == "2"
    assert prefetch_payload == {"profile_ready": True, "metrics_count": 1, "peers_count": 1, "news_count": 1}
    assert document_payload == {"summary": "文档摘要", "parse_success_rate": "0.80", "table_extraction_success_rate": "0.60", "failure_count": 1}
    assert live_tools_payload["success_rate"] == "0.75"
    assert live_tools_payload["quote_summary"] == "快照 | PE 20.0 | PB 5.0 | 市值 1000亿"
    assert live_tools_payload["error_summary"] == "券商观点: broker down"


def test_document_helpers_build_shared_summary_and_payload():
    state = AnalysisState(stock_code="600519")
    document = type("Document", (), {
        "source_id": "doc1",
        "title": "材料A",
        "source_type": "pdf",
        "extracted_at": "2026-01-02",
        "metadata": {"file_name": "材料A.pdf", "parse_status": "success"},
        "tables": [{"headers": ["a"], "rows": [["1"]]}],
        "text_blocks": ["正文"],
    })()

    summary = summarize_uploaded_documents(
        [document],
        extract_document_summary=lambda doc: {"summary": "文档摘要", "parse_status": "success"},
        extract_document_tables=lambda doc: list(doc.tables),
    )
    payload = sync_document_parse_payload(
        state,
        summary_text=summary["summary_text"],
        parse_rate=summary["parse_rate"],
        table_rate=summary["table_rate"],
        failure_count=summary["failure_count"],
    )

    assert summary["parse_success"] == 1
    assert summary["table_success"] == 1
    assert summary["source_refs"][0]["source_id"] == "doc1"
    assert format_document_parse_summary([document]).startswith("- 材料A")
    assert payload == {
        "summary": summary["summary_text"],
        "parse_success_rate": "1.00",
        "table_extraction_success_rate": "1.00",
        "failure_count": 0,
    }
    assert state.sections["document_parse_success_rate"] == "1.00"
    assert state.runtime_input_payload["documents"] == payload


def test_ingest_uploaded_documents_helper_updates_state_for_empty_and_nonempty_inputs():
    empty_state = AnalysisState(stock_code="600519")
    empty_summary = ingest_uploaded_documents(empty_state, [])
    assert empty_state.documents == []
    assert empty_state.runtime_input_payload["documents"]["parse_success_rate"] == "1.00"
    assert empty_summary["documents"] == []
    assert empty_summary["failure_count"] == 0

    state = AnalysisState(stock_code="600519")
    document = type("Document", (), {
        "source_id": "doc2",
        "title": "材料B",
        "source_type": "pdf",
        "extracted_at": "2026-01-03",
        "metadata": {"file_name": "材料B.pdf", "parse_status": "success"},
        "tables": [{"headers": ["x"], "rows": [["2"]]}],
        "text_blocks": ["正文B"],
    })()
    summary = ingest_uploaded_documents(
        state,
        [{"name": "材料B.pdf"}],
        parse_uploaded_items=lambda items: [document],
        extract_document_summary=lambda doc: {"summary": "B摘要", "parse_status": "success"},
        extract_document_tables=lambda doc: list(doc.tables),
    )
    assert state.documents == [document]
    assert len(state.source_refs) == 1
    assert state.runtime_input_payload["documents"]["parse_success_rate"] == "1.00"
    assert summary["documents"] == [document]
    assert summary["source_refs"][0]["source_id"] == "doc2"


def test_ingest_uploaded_documents_helper_uses_default_callbacks_when_omitted(monkeypatch):
    state = AnalysisState(stock_code="600519")
    document = type("Document", (), {
        "source_id": "doc3",
        "title": "材料C",
        "source_type": "pdf",
        "extracted_at": "2026-01-04",
        "metadata": {"file_name": "材料C.pdf", "parse_status": "success"},
        "tables": [{"headers": ["y"], "rows": [["3"]]}],
        "text_blocks": ["正文C"],
    })()
    monkeypatch.setattr("app.data_source.multimodal.parse_uploaded_items", lambda items: [document])
    monkeypatch.setattr("app.data_source.live_tools.extract_document_summary", lambda doc: {"summary": "C摘要", "parse_status": "success"})
    monkeypatch.setattr("app.data_source.live_tools.extract_document_tables", lambda doc: list(doc.tables))

    summary = ingest_uploaded_documents(state, [{"name": "材料C.pdf"}])

    assert state.documents == [document]
    assert summary["documents"] == [document]
    assert summary["source_refs"][0]["source_id"] == "doc3"
    assert state.runtime_input_payload["documents"]["parse_success_rate"] == "1.00"


def test_live_tools_helper_keeps_payload_sync_and_hides_success_map():
    state = AnalysisState(stock_code="600519")
    state.runtime_input_payload["live_tools"] = {"success_map": {"announcement": True}}
    success_state = {"announcement": True}

    update_live_tools_payload(state, announcement_count=1, source_ref_count=2)
    payload = sync_live_tools_status(state, success_state, success_key="quote", succeeded=True, error_key="quote")

    assert initialize_live_tools_payload(state)["announcement_count"] == 1
    assert payload["success_count"] == 2
    assert payload["tool_count"] == 5
    assert payload["failed_count"] == 0
    assert payload["success_rate"] == "0.40"
    assert "success_map" not in payload


def test_fetch_orchestrator_live_sources_builds_runtime_payload_and_sections():
    state = AnalysisState(stock_code="600519", stock_name="测试公司")

    payload = fetch_orchestrator_live_sources(
        state,
        fetch_announcements=lambda stock_code, stock_name: [{"id": "a", "title": "公告A", "summary": "摘要", "time": "2026-01-01", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "retrieval_mode": "api", "evidence_type": "announcement", "link": "http://a", "is_placeholder": False}],
        fetch_exchange_filings=lambda stock_code, stock_name: [{"id": "f", "title": "披露A", "summary": "摘要", "time": "2026-01-02", "source": "sse", "provider": "sse", "channel": "filing", "retrieval_mode": "api", "evidence_type": "filing", "link": "http://f", "is_placeholder": False}],
        fetch_live_quotes=lambda stock_code: {"title": "快照", "time": "2026-01-03", "source": "live", "provider": "akshare", "channel": "live_quote", "retrieval_mode": "api", "evidence_type": "quote", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000},
        fetch_broker_reports=lambda stock_code, stock_name: (_ for _ in ()).throw(RuntimeError("broker down")),
        fetch_fund_holdings=lambda stock_code: [{"id": "h", "title": "基金持仓", "summary": "持仓摘要", "time": "2026-01-04", "source": "eastmoney_fund_hold", "provider": "eastmoney_fund_hold", "channel": "fund_holding", "retrieval_mode": "api", "evidence_type": "institutional_holding", "link": "", "is_placeholder": False}],
    )

    assert payload["success_count"] == 4
    assert payload["tool_count"] == 5
    assert payload["source_ref_count"] == 4
    assert payload["fund_holding_count"] == 1
    assert payload["error_summary"] == "券商观点: broker down"
    assert state.sections["live_tool_success_rate"] == "0.80"
    assert state.sections["broker_report_error"] == "broker down"
    assert state.sections["live_quote_snapshot"]


def test_fetch_orchestrator_live_sources_uses_default_fetchers_when_omitted(monkeypatch):
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    monkeypatch.setattr("app.data_source.live_tools.fetch_announcements", lambda stock_code, stock_name: [{"id": "a2", "title": "公告B", "summary": "摘要B", "time": "2026-01-05", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "retrieval_mode": "api", "evidence_type": "announcement", "link": "http://a2", "is_placeholder": False}])
    monkeypatch.setattr("app.data_source.live_tools.fetch_exchange_filings", lambda stock_code, stock_name: [{"id": "f2", "title": "披露B", "summary": "摘要B", "time": "2026-01-06", "source": "sse", "provider": "sse", "channel": "filing", "retrieval_mode": "api", "evidence_type": "filing", "link": "http://f2", "is_placeholder": False}])
    monkeypatch.setattr("app.data_source.live_tools.fetch_live_quotes", lambda stock_code: {"title": "快照B", "time": "2026-01-07", "source": "live", "provider": "akshare", "channel": "live_quote", "retrieval_mode": "api", "evidence_type": "quote", "pe_ratio": 21, "pb_ratio": 6, "market_cap": 1100})
    monkeypatch.setattr("app.data_source.live_tools.fetch_broker_reports", lambda stock_code, stock_name: [])
    monkeypatch.setattr("app.data_source.live_tools.fetch_fund_holdings", lambda stock_code: [])

    payload = fetch_orchestrator_live_sources(state)

    assert payload["success_count"] == 5
    assert payload["tool_count"] == 5
    assert payload["announcement_count"] == 1
    assert payload["filing_count"] == 1
    assert payload["broker_report_count"] == 0
    assert payload["quote_snapshot"]["title"] == "快照B"


def test_format_live_tool_error_summary_uses_shared_labels():
    assert format_live_tool_error_summary({"announcement": "ann down", "quote": "quote down"}) == "公告: ann down；行情: quote down"
