"""Agent 工具模块单元测试"""
from __future__ import annotations

from app.models import AnalysisState, FinancialMetrics, PeerCompany, StockProfile
from app.agent.tools import Tool, execute_tool


def _make_tool(name: str = "test_tool", retryable: bool = True,
               cacheable: bool = True, fn=None) -> Tool:
    """创建测试用工具"""
    if fn is None:
        fn = lambda **kwargs: f"result_{kwargs.get('x', 'default')}"
    return Tool(
        name=name,
        description="测试工具",
        parameters_schema={"type": "object", "properties": {}, "required": []},
        function=fn,
        retryable=retryable,
        cacheable=cacheable,
    )


class TestExecuteTool:
    """execute_tool 函数测试"""

    def test_basic_execution(self):
        tool = _make_tool(fn=lambda **kw: "hello")
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state)
        assert result == "hello"
        assert len(state.tool_memory) == 1
        assert state.tool_memory[0].success is True

    def test_unknown_tool(self):
        result = execute_tool([], "nonexistent", {})
        assert "未知工具" in result

    def test_cache_hit(self):
        call_count = 0

        def counting_fn(**kw):
            nonlocal call_count
            call_count += 1
            return "cached_result"

        tool = _make_tool(fn=counting_fn, cacheable=True)
        state = AnalysisState()

        result1 = execute_tool([tool], "test_tool", {}, state=state)
        assert result1 == "cached_result"
        assert call_count == 1

        result2 = execute_tool([tool], "test_tool", {}, state=state)
        assert "[缓存]" in result2
        assert call_count == 1

    def test_no_cache_when_disabled(self):
        call_count = 0

        def counting_fn(**kw):
            nonlocal call_count
            call_count += 1
            return "result"

        tool = _make_tool(fn=counting_fn, cacheable=False)
        state = AnalysisState()

        execute_tool([tool], "test_tool", {}, state=state)
        execute_tool([tool], "test_tool", {}, state=state)
        assert call_count == 2

    def test_retry_on_failure(self):
        attempt_count = 0

        def failing_fn(**kw):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise RuntimeError("模拟失败")
            return "success"

        tool = _make_tool(fn=failing_fn, retryable=True)
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state, max_retries=2)
        assert result == "success"

    def test_all_retries_fail(self):
        def always_fail(**kw):
            raise RuntimeError("永远失败")

        tool = _make_tool(fn=always_fail, retryable=True)
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state, max_retries=1)
        assert "失败" in result
        assert state.tool_memory[-1].success is False

    def test_records_tool_memory(self):
        tool = _make_tool(fn=lambda **kw: "ok")
        state = AnalysisState()
        execute_tool([tool], "test_tool", {"x": "1"}, state=state)
        assert len(state.tool_memory) == 1
        rec = state.tool_memory[0]
        assert rec.tool_name == "test_tool"
        assert rec.args == {"x": "1"}
        assert rec.observation == "ok"


def test_make_tools_exposes_phase1_tools():
    from app.agent.tools import _make_tools

    tools = _make_tools(AnalysisState(stock_code="600519"))
    names = {tool.name for tool in tools}

    assert "fetch_announcements" in names
    assert "fetch_live_quotes" in names
    assert "extract_document_summary" in names
    assert "extract_document_tables" in names


def test_fetch_tools_share_prefetch_formatters(monkeypatch):
    from app.agent.tools import _make_tools

    state = AnalysisState(stock_code="600519")
    tools = {tool.name: tool for tool in _make_tools(state)}
    monkeypatch.setattr("app.data_source.akshare_client.get_stock_profile", lambda code: StockProfile(code=code, name="茅台", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=10, total_shares=12))
    monkeypatch.setattr("app.data_source.akshare_client.get_financial_metrics", lambda code: [FinancialMetrics(code=code, period="2024Q4", revenue=100, net_profit=50, roe=20, gross_margin=80, debt_ratio=20)])
    monkeypatch.setattr("app.data_source.akshare_client.get_peer_companies", lambda industry, exclude_code=None: [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)])
    monkeypatch.setattr("app.data_source.akshare_client.get_recent_news", lambda name: [{"title": "新闻1"}, {"title": "新闻2"}])

    profile_text = tools["fetch_stock_profile"].function()
    financials_text = tools["fetch_financials"].function()
    peers_text = tools["fetch_peers"].function(industry="白酒")
    news_text = tools["fetch_news"].function(name="茅台")

    assert "公司: 茅台 (600519)" in profile_text
    assert "获取到 1 期财务数据" in financials_text
    assert "找到 1 家白酒行业可比公司" in peers_text
    assert "获取到 2 条新闻" in news_text


def test_fetch_live_quotes_tool_updates_runtime_payload(monkeypatch):
    from app.agent.tools import _make_tools

    state = AnalysisState(stock_code="600519")
    tools = {tool.name: tool for tool in _make_tools(state)}
    monkeypatch.setattr("app.agent.tools.fetch_live_quotes", lambda stock_code: {"title": "快照", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000, "time": "2026-01-03"})

    text = tools["fetch_live_quotes"].function()

    assert "标题: 快照" in text
    assert state.runtime_input_payload["live_tools"]["quote_snapshot"] == {"title": "快照", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000, "time": "2026-01-03"}
    assert state.runtime_input_payload["live_tools"]["quote_summary"] == "快照 | PE 20.0 | PB 5.0 | 市值 1000亿"
    assert state.runtime_input_payload["live_tools"]["source_ref_count"] == 1
    assert state.runtime_input_payload["live_tools"]["success_count"] == 1
    assert state.runtime_input_payload["live_tools"]["tool_count"] == 5
    assert state.runtime_input_payload["live_tools"]["failed_count"] == 0
    assert state.runtime_input_payload["live_tools"]["success_rate"] == "0.20"
    assert "success_map" not in state.runtime_input_payload["live_tools"]
    assert len(state.source_refs) == 1
    assert state.sections["live_quote_snapshot"]


def test_live_source_tools_sync_runtime_payload_and_source_refs(monkeypatch):
    from app.agent.tools import _make_tools

    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    tools = {tool.name: tool for tool in _make_tools(state)}
    monkeypatch.setattr("app.agent.tools.fetch_announcements", lambda stock_code, stock_name, limit=5: [{"id": "a1", "title": "公告A", "summary": "摘要A", "time": "2026-01-01", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "retrieval_mode": "api", "evidence_type": "announcement", "link": "http://a"}])
    monkeypatch.setattr("app.agent.tools.fetch_exchange_filings", lambda stock_code, stock_name, limit=5: [{"id": "f1", "title": "披露A", "summary": "摘要F", "time": "2026-01-02", "source": "sse", "provider": "sse", "channel": "filing", "retrieval_mode": "api", "evidence_type": "filing", "link": "http://f"}])
    monkeypatch.setattr("app.agent.tools.fetch_broker_reports", lambda stock_code, stock_name, limit=3: [{"id": "b1", "title": "券商A", "summary": "观点A", "time": "2026-01-03", "source": "broker", "provider": "broker", "channel": "broker_report", "retrieval_mode": "api", "evidence_type": "broker_view", "link": "http://b"}])

    announcements_text = tools["fetch_announcements"].function()
    filings_text = tools["fetch_exchange_filings"].function()
    broker_text = tools["fetch_broker_reports"].function()

    assert "公告A" in announcements_text
    assert "披露A" in filings_text
    assert "券商A" in broker_text
    assert state.runtime_input_payload["live_tools"]["announcement_count"] == 1
    assert state.runtime_input_payload["live_tools"]["filing_count"] == 1
    assert state.runtime_input_payload["live_tools"]["broker_report_count"] == 1
    assert state.runtime_input_payload["live_tools"]["source_ref_count"] == 3
    assert state.runtime_input_payload["live_tools"]["success_count"] == 3
    assert state.runtime_input_payload["live_tools"]["tool_count"] == 5
    assert state.runtime_input_payload["live_tools"]["failed_count"] == 0
    assert state.runtime_input_payload["live_tools"]["success_rate"] == "0.60"
    assert "success_map" not in state.runtime_input_payload["live_tools"]
    assert len(state.source_refs) == 3


def test_live_source_tools_track_failures_in_runtime_payload(monkeypatch):
    from app.agent.tools import _make_tools

    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    tools = {tool.name: tool for tool in _make_tools(state)}
    monkeypatch.setattr("app.agent.tools.fetch_announcements", lambda stock_code, stock_name, limit=5: (_ for _ in ()).throw(RuntimeError("ann down")))
    monkeypatch.setattr("app.agent.tools.fetch_exchange_filings", lambda stock_code, stock_name, limit=5: [{"id": "f1", "title": "披露A", "summary": "摘要F", "time": "2026-01-02", "source": "sse", "provider": "sse", "channel": "filing", "retrieval_mode": "api", "evidence_type": "filing", "link": "http://f"}])
    monkeypatch.setattr("app.agent.tools.fetch_broker_reports", lambda stock_code, stock_name, limit=3: (_ for _ in ()).throw(RuntimeError("broker down")))
    monkeypatch.setattr("app.agent.tools.fetch_live_quotes", lambda stock_code: (_ for _ in ()).throw(RuntimeError("quote down")))

    announcements_text = tools["fetch_announcements"].function()
    filings_text = tools["fetch_exchange_filings"].function()
    broker_text = tools["fetch_broker_reports"].function()
    quote_text = tools["fetch_live_quotes"].function()

    assert "获取失败: ann down" == announcements_text
    assert "披露A" in filings_text
    assert "获取失败: broker down" == broker_text
    assert "获取失败: quote down" == quote_text
    assert state.runtime_input_payload["live_tools"]["success_count"] == 1
    assert state.runtime_input_payload["live_tools"]["tool_count"] == 5
    assert state.runtime_input_payload["live_tools"]["failed_count"] == 3
    assert state.runtime_input_payload["live_tools"]["error_count"] == 3
    assert state.runtime_input_payload["live_tools"]["success_rate"] == "0.20"
    assert "success_map" not in state.runtime_input_payload["live_tools"]
    assert state.runtime_input_payload["live_tools"]["errors"] == {
        "announcement": "ann down",
        "broker_report": "broker down",
        "quote": "quote down",
    }
    error_summary = state.runtime_input_payload["live_tools"]["error_summary"]
    assert "公告: ann down" in error_summary
    assert "券商观点: broker down" in error_summary
    assert "行情: quote down" in error_summary
    assert state.sections["announcement_error"] == "ann down"
    assert state.sections["broker_report_error"] == "broker down"
    assert state.sections["quote_error"] == "quote down"
