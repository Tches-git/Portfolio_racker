from __future__ import annotations

from dataclasses import dataclass

import app.agent.orchestrator as orch_mod
from app.agent.multi_agent import MultiAgentRoleTrace, MultiAgentTrace
from app.models import AblationConfig, AnalysisState, FinancialMetrics, PeerCompany, RiskItem, StockProfile, ToolCallRecord


@dataclass
class DummyRecord:
    stock_name: str = "茅台"
    timestamp: str = "2026-01-01T00:00:00"
    rating: str = "推荐"
    rating_score: float = 80
    revenue: float = 100
    net_profit: float = 50
    roe: float = 20
    gross_margin: float = 80
    debt_ratio: float = 20
    dcf_per_share: float = 1000
    dcf_upside: float = 10
    conclusion: str = "历史结论"
    industry: str = "白酒"
    stock_code: str = "600519"
    pe_ratio: float = 30


class DummyMemoryStore:
    def get_latest(self, stock_code):
        return None

    def save_analysis(self, state):
        return DummyRecord()

    def get_history(self, limit=100):
        return []

    def get_stock_memory(self, stock_code, limit=6):
        from app.memory.store import StockMemorySnapshot
        return [
            StockMemorySnapshot(
                stock_code=stock_code,
                timestamp="2026-04-21T10:00:00",
                thesis="盈利韧性延续。",
                rating="推荐",
                target_range="1950-2050元",
                key_risks=["需求波动", "新品节奏"],
                catalysts=["渠道修复"],
                valuation_summary="DCF每股价值 2010.00元，上涨空间 +9.0%",
                confidence_signals={"rating_score": 82, "source_reference_count": 4, "placeholder_source_ratio": 0.25},
                historical_delta="评级 中性→推荐",
                conflict_flag=True,
                conflict_reason="评分变化 75.0→82.0；新增风险 新品节奏",
            ),
            StockMemorySnapshot(
                stock_code=stock_code,
                timestamp="2026-04-18T10:00:00",
                thesis="盈利稳健。",
                rating="中性",
                target_range="1800-1900元",
                key_risks=["需求波动"],
                catalysts=["渠道修复"],
                valuation_summary="DCF每股价值 1850.00元，上涨空间 +3.0%",
                confidence_signals={"rating_score": 75, "source_reference_count": 2, "placeholder_source_ratio": 0.5},
            ),
        ]

    def get_ranked_stock_memory(self, stock_code, limit=6):
        return self.get_stock_memory(stock_code, limit=limit)

    def build_memory_context(self, stock_code):
        return {
            "summary": "长期记忆摘要",
            "timeline": "- 2026-01-01 | 推荐 | thesis",
            "memory_hit_count": 1,
            "historical_delta_coverage": 1.0,
            "duplicate_memory_injection_rate": 0.0,
            "memory_conflict_count": 1,
            "governance_notes": "去重 1 条；衰减低权重 0 条；保留冲突 1 条",
            "repeated_risk_patterns": "需求波动",
            "repeated_catalyst_patterns": "渠道修复",
            "repeated_risk_pattern_count": 1,
            "repeated_catalyst_pattern_count": 1,
            "thesis_stability_score": 0.5,
            "rating_drift_summary": "中性→推荐",
            "rating_drift_count": 1,
            "memory_pattern_summary": "重复风险：需求波动；重复催化：渠道修复；thesis稳定度：50%；评级漂移：中性→推荐",
        }


class DummyKB:
    def __init__(self):
        self.store = type("Store", (), {"size": 3})()
        self.saved = False

    def init(self):
        return None

    def build_stock_knowledge(self, *args, **kwargs):
        return None

    def add_documents(self, docs):
        return None

    def save(self):
        self.saved = True

    def query(self, *args, **kwargs):
        return []

    def format_context(self, results):
        return ""


class DummyResearchAgent:
    def __init__(self, role="research", on_step=None):
        self.on_step = on_step or (lambda *args, **kwargs: None)

    def run(self, task, state):
        self.on_step("action", "调用工具: fetch_stock_profile", {"tool": "fetch_stock_profile"})
        return orch_mod.AgentResult(
            answer="研究结论",
            total_steps=2,
            plan=[],
            reflection="反思摘要",
        )


class DummyMultiAgentWorkflow:
    def __init__(self, on_role_step=None):
        self.on_role_step = on_role_step or (lambda *args, **kwargs: None)

    def run(self, stock_code, state):
        self.on_role_step("role_done", "MarketDataAgent completed", {"role_id": "market_data"})
        trace = MultiAgentTrace(
            mode="autogen_graphflow",
            role_count=6,
            completed_role_count=6,
            failed_role_count=0,
            roles=[
                MultiAgentRoleTrace(
                    role_id="market_data",
                    role_name="MarketDataAgent",
                    status="completed",
                    summary="研究结论",
                    tool_call_count=1,
                    duration_s=0.1,
                )
            ],
        )
        return orch_mod.AgentResult(
            answer="研究结论",
            total_steps=6,
            trace=trace,
            plan=[type("Plan", (), {"step_id": "1", "objective": "看财务", "preferred_tool": "MarketDataAgent"})()],
            reflection="反思摘要",
        )


def test_wrap_external_data_marks_prompt_boundary():
    orchestrator = orch_mod.AgentOrchestrator()

    wrapped = orchestrator._wrap_external_data("外部数据\n第二行")

    assert wrapped.startswith("<external_data>")
    assert wrapped.endswith("</external_data>")
    assert "外部数据" in wrapped


def test_build_research_memory_context_remains_plain_text():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    state.sections["memory_hit_count"] = "1"
    state.sections["memory_comparison_summary"] = "本次 vs 上次"
    state.sections["memory_comparison_risk"] = "风险演化"
    state.sections["repeated_risk_patterns"] = "需求波动"
    state.sections["rating_drift_summary"] = "中性→推荐"
    state.sections["memory_governance_notes"] = "治理说明"

    context = orchestrator._build_research_memory_context(state)

    assert "<external_data>" not in context
    assert "本次 vs 上次" in context


def test_build_research_task_wraps_memory_context():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    state.sections["memory_hit_count"] = "1"
    state.sections["memory_comparison_summary"] = "本次 vs 上次"
    state.sections["memory_comparison_risk"] = "风险演化"
    state.sections["repeated_risk_patterns"] = "需求波动"
    state.sections["rating_drift_summary"] = "中性→推荐"
    state.sections["memory_governance_notes"] = "治理说明"

    task = orchestrator._build_research_task("600519", state)

    assert "<external_data>" in task
    assert "长期记忆使用规则" in task


def test_prepare_runtime_inputs_calls_stages(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519")
    calls: list[str] = []
    monkeypatch.setattr(orchestrator, "_prefetch_data", lambda state_obj: calls.append("prefetch"))
    monkeypatch.setattr(orchestrator, "_ingest_uploaded_documents", lambda state_obj, uploaded_items: calls.append("ingest"))
    monkeypatch.setattr(orchestrator, "_hydrate_live_sources", lambda state_obj: calls.append("hydrate"))
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)

    orchestrator._prepare_runtime_inputs(state, [{"name": "doc"}])

    assert calls == ["prefetch", "ingest", "hydrate"]
    assert "prefetch_done" in events


def test_prefetch_data_populates_tool_memory(monkeypatch):
    monkeypatch.setattr(orch_mod, "logger", type("L", (), {"warning": staticmethod(lambda *a, **k: None)})())
    monkeypatch.setattr("app.data_source.akshare_client.get_stock_profile", lambda code: StockProfile(code=code, name="茅台", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=10, total_shares=10))
    monkeypatch.setattr("app.data_source.akshare_client.get_financial_metrics", lambda code: [FinancialMetrics(code=code, period="2024Q4", revenue=100, net_profit=50, revenue_yoy=10, profit_yoy=8, roe=20, gross_margin=80, debt_ratio=20)])
    monkeypatch.setattr("app.data_source.akshare_client.get_peer_companies", lambda industry, exclude_code=None: [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)])
    monkeypatch.setattr("app.data_source.akshare_client.get_recent_news", lambda name: [{"title": "新闻1"}, {"title": "新闻2"}])

    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    orchestrator._prefetch_data(state)

    tool_names = [record.tool_name for record in state.tool_memory]
    assert state.profile is not None
    assert len(state.metrics) == 1
    assert len(state.peers) == 1
    assert len(state.news) == 2
    assert tool_names == ["fetch_stock_profile", "fetch_financials", "fetch_peers", "fetch_news"]


def test_prefetch_data_delegates_to_helper_stages(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    calls: list[str] = []

    monkeypatch.setattr(orch_mod, "prefetch_core_data", lambda state_obj, **kwargs: calls.append("core"))
    monkeypatch.setattr(orch_mod, "prefetch_market_context", lambda state_obj, **kwargs: calls.append("market"))

    orchestrator._prefetch_data(state)

    assert calls == ["core", "market"]


def test_populate_memory_sections_sets_structured_payload():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    memory_context = DummyMemoryStore().build_memory_context("600519")
    stock_memory = DummyMemoryStore().get_ranked_stock_memory("600519")

    orchestrator._populate_memory_sections(state, memory_context=memory_context, stock_memory=stock_memory)

    assert state.memory_payload["summary"] == "长期记忆摘要"
    assert state.memory_payload["memory_hit_count"] == 1
    assert state.memory_payload["comparison_rating"] == "中性 → 推荐"
    assert state.memory_payload["risk_evolution_count"] == 2
    assert state.memory_payload["research_memory_context"].startswith("仅把长期记忆当作待验证线索")
    assert state.sections["stock_memory_summary"] == "长期记忆摘要"


def test_prepare_runtime_inputs_sets_structured_runtime_payload(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519")
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒")
    state.metrics = [FinancialMetrics(code="600519", period="2024Q4")]
    state.peers = [PeerCompany(code="000858", name="五粮液")]
    state.news = [{"title": "新闻1"}]
    monkeypatch.setattr(orchestrator, "_prefetch_data", lambda state_obj: None)
    monkeypatch.setattr(orchestrator, "_ingest_uploaded_documents", lambda state_obj, uploaded_items: state_obj.runtime_input_payload.__setitem__("documents", {"summary": "文档摘要"}))
    monkeypatch.setattr(orchestrator, "_hydrate_live_sources", lambda state_obj: state_obj.runtime_input_payload.__setitem__("live_tools", {"success_rate": "1.00"}))
    orchestrator.on_step = lambda *args: None

    orchestrator._prepare_runtime_inputs(state, [])

    assert state.runtime_input_payload["prefetch"]["profile_ready"] is True
    assert state.runtime_input_payload["documents"]["summary"] == "文档摘要"
    assert state.runtime_input_payload["live_tools"]["success_rate"] == "1.00"


def test_hydrate_live_sources_sets_structured_runtime_payload(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    events: list[str] = []
    orchestrator.on_step = lambda event, *_: events.append(event)

    monkeypatch.setattr("app.data_source.live_tools.fetch_announcements", lambda stock_code, stock_name: [{"id": "a", "title": "公告A", "summary": "摘要", "time": "2026-01-01", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "retrieval_mode": "api", "evidence_type": "announcement", "link": "http://a", "is_placeholder": False}])
    monkeypatch.setattr("app.data_source.live_tools.fetch_exchange_filings", lambda stock_code, stock_name: [{"id": "f", "title": "披露A", "summary": "摘要", "time": "2026-01-02", "source": "sse", "provider": "sse", "channel": "filing", "retrieval_mode": "api", "evidence_type": "filing", "link": "http://f", "is_placeholder": False}])
    monkeypatch.setattr("app.data_source.live_tools.fetch_live_quotes", lambda stock_code: {"title": "快照", "time": "2026-01-03", "source": "live", "provider": "akshare", "channel": "live_quote", "retrieval_mode": "api", "evidence_type": "quote", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000})
    monkeypatch.setattr("app.data_source.live_tools.fetch_broker_reports", lambda stock_code, stock_name: (_ for _ in ()).throw(RuntimeError("broker down")))
    monkeypatch.setattr("app.data_source.live_tools.fetch_fund_holdings", lambda stock_code: [{"id": "h", "title": "基金持仓", "summary": "持仓摘要", "time": "2026-01-04", "source": "eastmoney_fund_hold", "provider": "eastmoney_fund_hold", "channel": "fund_holding", "retrieval_mode": "api", "evidence_type": "institutional_holding", "link": "", "is_placeholder": False}])

    orchestrator._hydrate_live_sources(state)

    assert state.runtime_input_payload["live_tools"] == {
        "success_rate": "0.80",
        "success_count": 4,
        "tool_count": 5,
        "failed_count": 1,
        "announcement_count": 1,
        "filing_count": 1,
        "broker_report_count": 0,
        "fund_holding_count": 1,
        "source_ref_count": 4,
        "quote_snapshot": {"title": "快照", "time": "2026-01-03", "source": "live", "provider": "akshare", "channel": "live_quote", "retrieval_mode": "api", "evidence_type": "quote", "pe_ratio": 20, "pb_ratio": 5, "market_cap": 1000},
        "quote_summary": "快照 | PE 20.0 | PB 5.0 | 市值 1000亿",
        "errors": {"broker_report": "broker down"},
        "error_count": 1,
        "error_summary": "券商观点: broker down",
    }
    assert state.sections["live_tool_success_rate"] == "0.80"
    assert state.sections["live_quote_snapshot"]
    assert state.sections["broker_report_error"] == "broker down"
    assert events == ["live_tools_start", "live_tools_done"]


def test_prepare_memory_context_populates_memory_and_returns_prev_record():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519")
    memory = DummyMemoryStore()

    prev_record = orchestrator._prepare_memory_context(state, memory, "600519")

    assert prev_record is None
    assert state.memory_payload["summary"] == "长期记忆摘要"
    assert state.sections["stock_memory_summary"] == "长期记忆摘要"


def test_initialize_knowledge_base_emits_ready_event():
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519")
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)

    kb = DummyKB()
    orch_mod.get_knowledge_base = lambda: kb

    returned = orchestrator._initialize_knowledge_base(state)

    assert returned is kb
    assert "rag_init" in events
    assert "rag_ready" in events


def test_run_research_phase_updates_sections_and_events(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519")
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)
    monkeypatch.setattr(orch_mod, "AutoGenMultiAgentWorkflow", DummyMultiAgentWorkflow)
    orchestrator._run_research_phase("600519", state)

    assert state.analysis_payload["research_conclusion"] == "研究结论"
    assert "看财务" in state.analysis_payload["research_plan"]
    assert state.analysis_payload["research_reflection"] == "反思摘要"
    assert state.sections["research_conclusion"] == "研究结论"
    assert state.run_payload["multi_agent_trace"]["role_count"] == 6
    assert "research_start" in events
    assert "research_done" in events


def test_prepare_writer_state_refreshes_graph_and_data_gaps(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒")
    state.metrics = [FinancialMetrics(code="600519", period="2024Q4", revenue=100)]
    state.news = [{"title": "新闻1"}]
    state.documents = [type("Doc", (), {"title": "补充材料"})()]
    kb = DummyKB()
    graph_summary = type("Summary", (), {"summary": "图摘要", "relationship_coverage": 0.5, "risk_path_completeness": 0.6})()
    captured = {}

    monkeypatch.setattr(orchestrator, "_enrich_knowledge", lambda state_obj, kb_obj: captured.__setitem__("enriched", True))
    monkeypatch.setattr(orch_mod, "build_graph_summary", lambda state_obj: graph_summary)
    monkeypatch.setattr(orchestrator, "_build_section_graph_queries", lambda state_obj: {"risk": "r", "industry": "i", "valuation": "v"})
    monkeypatch.setattr(orchestrator, "_build_section_graph_query_refinements", lambda state_obj: {"risk": "", "industry": "", "valuation": ""})
    monkeypatch.setattr(orchestrator, "_refresh_graph_context", lambda state_obj, summary_obj, section_query_overrides, section_query_refinements: captured.update({"summary": summary_obj, "queries": section_query_overrides, "refinements": section_query_refinements}))
    monkeypatch.setattr(orch_mod, "collect_data_gaps", lambda state_obj: ["现金流数据不足"])

    returned_summary, overrides, refinements = orchestrator._prepare_writer_state(state, kb)

    assert returned_summary is graph_summary
    assert overrides["risk"] == "r"
    assert refinements["valuation"] == ""
    assert captured["enriched"] is True
    assert captured["summary"] is graph_summary
    assert state.analysis_payload["data_gaps"] == ["现金流数据不足"]
    assert state.analysis_payload["data_gap_count"] == 1
    assert state.sections["data_gaps"] == "现金流数据不足"
    assert state.sections["data_gap_count"] == "1"


def test_run_writer_phase_writes_report_and_emits_done(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    kb = DummyKB()
    graph_summary = type("Summary", (), {"summary": "图摘要", "relationship_coverage": 0.5, "risk_path_completeness": 0.6})()
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)

    monkeypatch.setattr(orchestrator, "_write_report_with_rag", lambda state_obj, kb_obj, prev_record=None: "# 初稿")
    monkeypatch.setattr(orch_mod, "post_process_report", lambda orch, report, state_obj: "# 最终报告")
    monkeypatch.setattr(orchestrator, "_build_section_graph_query_refinements", lambda state_obj: {"risk": "", "industry": "", "valuation": ""})

    orchestrator._run_writer_phase(state, kb, None, graph_summary, {"risk": "r", "industry": "i", "valuation": "v"}, {"risk": "", "industry": "", "valuation": ""})

    assert state.final_report == "# 最终报告"
    assert "writer_start" in events
    assert "writer_done" in events


def test_run_writer_phase_falls_back_when_llm_fails(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.analysis_payload["multi_agent_role_outputs"] = {"planner": "已完成规划", "report_writer": "已形成 brief"}
    kb = DummyKB()
    graph_summary = type("Summary", (), {"summary": "图摘要", "relationship_coverage": 0.5, "risk_path_completeness": 0.6})()
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)

    monkeypatch.setattr(orchestrator, "_write_report_with_rag", lambda state_obj, kb_obj, prev_record=None: (_ for _ in ()).throw(RuntimeError("LLM timeout")))
    monkeypatch.setattr(orch_mod, "post_process_report", lambda orch, report, state_obj: report)
    monkeypatch.setattr(orchestrator, "_build_section_graph_query_refinements", lambda state_obj: {"risk": "", "industry": "", "valuation": ""})

    orchestrator._run_writer_phase(state, kb, None, graph_summary, {"risk": "r", "industry": "i", "valuation": "v"}, {"risk": "", "industry": "", "valuation": ""})

    assert "多智能体降级研报" in state.final_report
    assert "LLM timeout" in state.sections["writer_fallback_error"]
    assert "writer_fallback" in events
    assert "writer_done" in events


def test_run_writer_phase_falls_back_when_writer_timeout(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    kb = DummyKB()
    graph_summary = type("Summary", (), {"summary": "图摘要", "relationship_coverage": 0.5, "risk_path_completeness": 0.6})()
    events: list[str] = []
    orchestrator.on_step = lambda event, detail, state_obj: events.append(event)

    monkeypatch.setattr(orch_mod, "WRITER_PHASE_TIMEOUT_SECONDS", 0.01)
    monkeypatch.setattr(orchestrator, "_write_report_with_rag", lambda state_obj, kb_obj, prev_record=None: __import__("time").sleep(1))
    monkeypatch.setattr(orch_mod, "post_process_report", lambda orch, report, state_obj: report)
    monkeypatch.setattr(orchestrator, "_build_section_graph_query_refinements", lambda state_obj: {"risk": "", "industry": "", "valuation": ""})

    orchestrator._run_writer_phase(state, kb, None, graph_summary, {"risk": "r", "industry": "i", "valuation": "v"}, {"risk": "", "industry": "", "valuation": ""})

    assert "多智能体降级研报" in state.final_report
    assert "Report Agent 写作阶段超过" in state.sections["writer_fallback_error"]
    assert "writer_fallback" in events
    assert "writer_done" in events


def test_build_report_history_text_prefers_structured_memory_payload():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.memory_payload["writing_memory_context"] = "结构化长期记忆"
    state.sections["writing_memory_context"] = "旧长期记忆"

    history_text = orchestrator._build_report_history_text(state)

    assert history_text.startswith("<external_data>")
    assert "结构化长期记忆" in history_text
    assert "旧长期记忆" not in history_text


def test_build_report_history_text_appends_peer_history(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.memory_payload["writing_memory_context"] = "结构化长期记忆"
    prev_record = DummyRecord(stock_name="测试公司", industry="白酒", stock_code="600519")
    peer_record = DummyRecord(stock_name="五粮液", stock_code="000858", rating="中性", roe=18, pe_ratio=24)

    monkeypatch.setattr(orch_mod, "get_memory_store", lambda: type("Memory", (), {"get_history": staticmethod(lambda limit=100: [peer_record])})())
    monkeypatch.setattr(orch_mod, "find_peer_from_history", lambda records, industry, exclude_code=None: [peer_record])

    history_text = orchestrator._build_report_history_text(state, prev_record)

    assert "上次分析日期" in history_text
    assert "历史分析过的同行业公司" in history_text
    assert "五粮液(000858)" in history_text


def test_build_report_graph_context_prefers_structured_payload():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.sections["graph_context"] = "旧图摘要"
    state.sections["hybrid_graph_context"] = "旧混合摘要"
    state.sections["graph_query_focus"] = "旧焦点"
    state.sections["graph_focus_summary"] = "旧多焦点摘要"
    state.sections["section_graph_summary"] = "旧章节摘要"
    state.sections["section_graph_context"] = "旧章节图摘要"
    state.sections["section_graph_context_risk"] = "风险章节 Graph Context：\n- 旧未命中"
    state.sections["section_graph_context_industry"] = "行业章节 Graph Context：\n- 旧未命中"
    state.sections["section_graph_context_valuation"] = "估值章节 Graph Context：\n- 旧未命中"
    state.graph_payload = {
        "graph_context": "图摘要",
        "hybrid_graph_context": "混合摘要",
        "graph_query_focus": "风险传导",
        "graph_focus_summary": "多焦点摘要",
        "section_graph_summary": "章节摘要",
        "section_graph_context": "章节图摘要",
        "section_graph_context_map": {
            "risk": "风险章节 Graph Context：\n- 未命中",
            "industry": "行业章节 Graph Context：\n- 未命中",
            "valuation": "估值章节 Graph Context：\n- 未命中",
        },
    }

    context = orchestrator._build_report_graph_context(state)

    assert "风险传导" in context["graph_focus_text"]
    assert "图摘要" in context["graph_text"]
    assert "旧图摘要" not in context["graph_text"]
    assert "风险章节 Graph Context：\n- 未命中" in context["risk_graph_context"]
    assert "旧未命中" not in context["risk_graph_context"]


def test_build_report_context_wraps_external_materials(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=8, total_shares=10)
    state.sections["research_conclusion"] = "研究结论"
    state.sections["writing_memory_context"] = "旧长期记忆"
    state.sections["dcf_monte_carlo"] = "MC"
    state.sections["dcf_sensitivity"] = "敏感性"
    state.memory_payload["writing_memory_context"] = "长期记忆"
    state.graph_payload = {
        "graph_context": "图摘要",
        "hybrid_graph_context": "混合摘要",
        "graph_query_focus": "风险传导",
        "graph_focus_summary": "多焦点摘要",
        "section_graph_summary": "章节摘要",
        "section_graph_context": "章节图摘要",
        "section_graph_context_map": {
            "risk": "风险章节 Graph Context：\n- 未命中",
            "industry": "行业章节 Graph Context：\n- 未命中",
            "valuation": "估值章节 Graph Context：\n- 未命中",
        },
    }
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_parallel_rag_queries", lambda self, kb, queries: ["知识1", "知识2"])
    monkeypatch.setattr("app.utils.tables.build_metrics_table", lambda state: "财务表")
    monkeypatch.setattr("app.utils.tables.build_peers_table", lambda state: "同行表")

    context = orchestrator._build_report_context(state, DummyKB(), None)

    assert "<external_data>" in context["metrics_table"]
    assert "<external_data>" in context["history_text"]
    assert "长期记忆" in context["history_text"]
    assert "旧长期记忆" not in context["history_text"]
    assert "风险传导" in context["graph_focus_text"]
    assert "图摘要" in context["graph_text"]
    assert "MC" in context["mc_text"]
    assert "敏感性" in context["sensitivity_text"]
    assert "研究结论" in context["research_conclusion"]
    assert "风险章节 Graph Context：\n- 未命中" in context["risk_graph_context"]
    assert context["rag_text"].startswith("知识1")


def test_build_report_context_skips_rag_when_ablation_disables_it(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司", ablation_config=AblationConfig(enable_rag=False))
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=8, total_shares=10)
    state.analysis_payload["research_conclusion"] = "研究结论"
    state.sections["dcf_monte_carlo"] = "MC"
    state.sections["dcf_sensitivity"] = "敏感性"
    state.memory_payload["writing_memory_context"] = "长期记忆"
    state.graph_payload = {
        "graph_context": "图摘要",
        "hybrid_graph_context": "混合摘要",
        "graph_query_focus": "风险传导",
        "graph_focus_summary": "多焦点摘要",
        "section_graph_summary": "章节摘要",
        "section_graph_context": "章节图摘要",
        "section_graph_context_map": {
            "risk": "风险章节 Graph Context：\n- 未命中",
            "industry": "行业章节 Graph Context：\n- 未命中",
            "valuation": "估值章节 Graph Context：\n- 未命中",
        },
    }

    called = {"rag": False}

    def _parallel_rag_queries(*args, **kwargs):
        called["rag"] = True
        return ["知识1"]

    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_parallel_rag_queries", _parallel_rag_queries)
    monkeypatch.setattr("app.utils.tables.build_metrics_table", lambda state: "财务表")
    monkeypatch.setattr("app.utils.tables.build_peers_table", lambda state: "同行表")

    context = orchestrator._build_report_context(state, DummyKB(), None)

    assert called["rag"] is False
    assert context["rag_text"] == "无额外知识"


def test_build_report_prompt_prefers_structured_memory_payload(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=8, total_shares=10)
    state.memory_payload["writing_memory_context"] = "结构化长期记忆"
    state.sections["writing_memory_context"] = "旧长期记忆"
    state.sections["dupont_table"] = "杜邦表"
    state.sections["dupont_summary"] = "杜邦总结"
    state.sections["dcf_table"] = "DCF表"
    state.sections["comparable_summary"] = "可比总结"
    state.sections["trend_table"] = "趋势表"
    state.sections["trend_summary"] = "趋势总结"
    state.sections["scores"] = "评分卡"
    state.sections["rating"] = "推荐"
    state.sections["rating_detail"] = "盈利质量稳健"

    report_context = {
        "metrics_table": "<external_data>财务表</external_data>",
        "history_text": "<external_data>历史</external_data>",
        "mc_text": "<external_data>MC</external_data>",
        "sensitivity_text": "<external_data>敏感性</external_data>",
        "research_conclusion": "<external_data>研究结论</external_data>",
        "source_reference_text": "<external_data>来源</external_data>",
        "multimodal_text": "<external_data>多模态</external_data>",
        "graph_text": "<external_data>图摘要</external_data>",
        "hybrid_graph_text": "<external_data>混合检索</external_data>",
        "graph_focus_text": "<external_data>风险传导</external_data>",
        "graph_focus_summary": "<external_data>多焦点摘要</external_data>",
        "section_graph_summary": "<external_data>章节摘要</external_data>",
        "section_graph_context": "<external_data>章节图摘要</external_data>",
        "risk_graph_context": "<external_data>风险图</external_data>",
        "industry_graph_context": "<external_data>行业图</external_data>",
        "valuation_graph_context": "<external_data>估值图</external_data>",
        "rag_text": "知识1",
        "peers_table": "<external_data>同行表</external_data>",
    }

    prompt = orchestrator._build_report_prompt(state, report_context, orchestrator._memory_value(state, "writing_memory_context", "无长期记忆"))

    assert "结构化长期记忆" in prompt
    assert "旧长期记忆" not in prompt
    assert "杜邦表" in prompt
    assert "DCF表" in prompt
    assert "推荐" in prompt
    assert "测试公司（600519）" in prompt
    assert prompt.count("<external_data>") >= 2



def test_build_report_external_data_block_contains_expected_sections():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.profile = StockProfile(code="600519", name="测试公司", industry="白酒", market_cap=1000, pe_ratio=30, pb_ratio=8, total_shares=10)
    state.sections["dupont_table"] = "杜邦表"
    state.sections["dcf_table"] = "DCF表"
    state.sections["rating"] = "推荐"
    state.sections["rating_detail"] = "盈利质量稳健"
    report_context = {
        "metrics_table": "<external_data>财务表</external_data>",
        "history_text": "<external_data>历史</external_data>",
        "mc_text": "<external_data>MC</external_data>",
        "sensitivity_text": "<external_data>敏感性</external_data>",
        "research_conclusion": "<external_data>研究结论</external_data>",
        "source_reference_text": "<external_data>来源</external_data>",
        "multimodal_text": "<external_data>多模态</external_data>",
        "graph_text": "<external_data>图摘要</external_data>",
        "hybrid_graph_text": "<external_data>混合检索</external_data>",
        "graph_focus_text": "<external_data>风险传导</external_data>",
        "graph_focus_summary": "<external_data>多焦点摘要</external_data>",
        "section_graph_summary": "<external_data>章节摘要</external_data>",
        "section_graph_context": "<external_data>章节图摘要</external_data>",
        "risk_graph_context": "<external_data>风险图</external_data>",
        "industry_graph_context": "<external_data>行业图</external_data>",
        "valuation_graph_context": "<external_data>估值图</external_data>",
        "rag_text": "知识1",
        "peers_table": "<external_data>同行表</external_data>",
    }

    block = orchestrator._build_report_external_data_block(state, report_context, "结构化长期记忆")

    assert block.startswith("<external_data>")
    assert block.endswith("</external_data>")
    assert "杜邦表" in block
    assert "DCF表" in block
    assert "结构化长期记忆" in block


def test_build_report_prompt_requirements_and_quality_bar():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    event_state = AnalysisState(stock_code="600519", stock_name="测试公司", event_context={"event_id": "e1", "title": "重大公告"})

    requirements = orchestrator._build_report_prompt_requirements(state)
    event_requirements = orchestrator._build_report_prompt_requirements(event_state)
    quality_bar = orchestrator._build_report_prompt_quality_bar()

    assert "## 输出要求（必须严格遵守）" in requirements
    assert "# 测试公司（600519）深度研究报告" in requirements
    assert "不要机械重复" in requirements
    assert "禁止评级前后自相矛盾" in requirements
    assert "事件触发研究" in event_requirements
    assert "## 质量标准" in quality_bar
    assert "优先做“分析+判断”" in quality_bar


def test_event_context_is_formatted_and_injected_into_prompts():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(
        stock_code="600519",
        stock_name="测试公司",
        event_context={
            "event_id": "e1",
            "title": "高影响公告",
            "summary": "公司披露重大事项",
            "source": "交易所公告",
            "impact_level": "high",
            "impact_scope": "fundamentals",
            "confidence": 0.82,
            "related_sources": [{"title": "公告原文", "url": "https://example.com/a"}],
        },
    )

    orchestrator._hydrate_event_context(state)
    research_task = orchestrator._build_research_task("600519", state)

    assert "事件ID: e1" in state.sections["event_context"]
    assert "高影响公告" in state.runtime_input_payload["event_context"]["title"]
    assert "触发事件材料" in research_task
    assert "fundamentals" in research_task


def test_write_report_with_rag_calls_chat_with_built_prompt(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    monkeypatch.setattr(orchestrator, "_build_report_context", lambda *args, **kwargs: {"metrics_table": "A", "history_text": "B", "mc_text": "C", "sensitivity_text": "D", "research_conclusion": "E", "source_reference_text": "F", "multimodal_text": "G", "graph_text": "H", "hybrid_graph_text": "I", "graph_focus_text": "J", "graph_focus_summary": "K", "section_graph_summary": "L", "section_graph_context": "M", "risk_graph_context": "N", "industry_graph_context": "O", "valuation_graph_context": "P", "rag_text": "Q", "peers_table": "R"})
    monkeypatch.setattr(orchestrator, "_build_report_prompt", lambda *args, **kwargs: "PROMPT")
    captured = {}
    monkeypatch.setattr(orch_mod, "chat", lambda prompt, **kwargs: captured.setdefault("prompt", prompt) or "# 报告")

    orchestrator._write_report_with_rag(state, DummyKB())

    assert captured["prompt"] == "PROMPT"


def test_build_report_prompt_reduces_persona_and_calls_out_natural_progression():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    prompt = orchestrator._build_report_prompt(
        state,
        {
            "metrics_table": "<external_data>财务表</external_data>",
            "history_text": "<external_data>历史</external_data>",
            "mc_text": "<external_data>MC</external_data>",
            "sensitivity_text": "<external_data>敏感性</external_data>",
            "research_conclusion": "<external_data>研究结论</external_data>",
            "source_reference_text": "<external_data>来源</external_data>",
            "multimodal_text": "<external_data>多模态</external_data>",
            "graph_text": "<external_data>图摘要</external_data>",
            "hybrid_graph_text": "<external_data>混合检索</external_data>",
            "graph_focus_text": "<external_data>焦点</external_data>",
            "graph_focus_summary": "<external_data>摘要</external_data>",
            "section_graph_summary": "<external_data>章节摘要</external_data>",
            "section_graph_context": "<external_data>章节图</external_data>",
            "risk_graph_context": "<external_data>风险图</external_data>",
            "industry_graph_context": "<external_data>行业图</external_data>",
            "valuation_graph_context": "<external_data>估值图</external_data>",
            "rag_text": "知识1",
            "peers_table": "<external_data>同行表</external_data>",
        },
        "长期记忆",
    )

    assert "你是张明" not in prompt
    assert "判断先行、证据跟进、段落推进自然" in prompt
    assert "避免机械同义复述" in prompt


def test_refresh_graph_context_applies_payload(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    summary = type("Summary", (), {"summary": "图摘要", "relationship_coverage": 0.5, "risk_path_completeness": 0.6})()

    monkeypatch.setattr(orch_mod, "build_hybrid_context", lambda *args, **kwargs: {
        "graph_context": "图上下文",
        "hybrid_context": "混合上下文",
        "graph_hit_count": 2,
        "hybrid_retrieval_hit_rate": 1.0,
        "graph_query_focus": "风险传导",
        "graph_focus_coverage": 0.8,
        "graph_focus_summary": "风险传导=命中(causes_risk)",
        "section_graph_hit_count": 1,
        "section_graph_focus_coverage": 0.5,
        "section_graph_summary": "风险章节=命中(causes_risk)",
        "section_graph_context": "章节图上下文",
        "section_graph_query_summary": "query",
        "section_graph_query_refinement_summary": "未触发",
        "section_graph_query_refined_count": 0,
        "section_graph_refinement_comparison_summary": "",
        "section_graph_refinement_improved_count": 0,
        "section_graph_query_map": {"risk": "r", "industry": "i", "valuation": "v"},
        "section_graph_context_map": {"risk": "rr", "industry": "ii", "valuation": "vv"},
    })

    orchestrator._refresh_graph_context(
        state,
        summary,
        section_query_overrides={"risk": "x", "industry": "y", "valuation": "z"},
        section_query_refinements={"risk": "", "industry": "", "valuation": ""},
    )

    assert state.sections["graph_context"] == "图上下文"
    assert state.sections["section_graph_context_risk"] == "rr"
    assert state.sections["relationship_coverage"] == "0.5"
    assert state.graph_payload["graph_context"] == "图上下文"
    assert state.graph_payload["graph_hit_count"] == 2
    assert state.graph_payload["section_graph_context_map"]["risk"] == "rr"
    assert state.graph_payload["relationship_coverage"] == 0.5


def test_finalize_run_updates_memory_sections(monkeypatch):
    orchestrator = orch_mod.AgentOrchestrator()
    orchestrator._tracer = orch_mod.Tracer()
    orchestrator._agent_steps.append({"agent": "research"})
    orchestrator._rag_hits.append({"tool": "rag_query"})
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    memory = DummyMemoryStore()
    kb = DummyKB()

    monkeypatch.setattr(orchestrator, "_persist_knowledge", lambda kb_obj: setattr(kb_obj, "saved", True))
    monkeypatch.setattr(orchestrator, "_save_memory_record", lambda state_obj, memory_obj, prev_record: state_obj.sections.__setitem__("memory_saved", "1"))
    monkeypatch.setattr(orchestrator, "_refresh_memory_sections", lambda state_obj, memory_obj, stock_code: state_obj.sections.__setitem__("memory_refreshed", stock_code))

    orchestrator._finalize_run(state, kb, memory, None, "600519")

    assert kb.saved is True
    assert state.sections["memory_saved"] == "1"
    assert state.sections["memory_refreshed"] == "600519"
    assert state.sections["agent_steps"] == "1"
    assert state.sections["rag_hits"] == "1"
    assert state.run_payload["agent_steps"] == 1
    assert state.run_payload["rag_hits"] == 1
    assert isinstance(state.run_payload["trace_summary"], dict)
    assert state.run_payload["trace_summary"]["phase_total_ms"] >= 0


def test_run_traced_collects_sections(monkeypatch):
    monkeypatch.setattr(orch_mod, "get_memory_store", lambda: DummyMemoryStore())
    monkeypatch.setattr(orch_mod, "get_knowledge_base", lambda: DummyKB())
    monkeypatch.setattr(orch_mod, "AutoGenMultiAgentWorkflow", DummyMultiAgentWorkflow)
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_prefetch_data", lambda self, state: state.tool_memory.append(ToolCallRecord(tool_name="fetch_stock_profile", observation="ok")))
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_enrich_knowledge", lambda self, state, kb: None)
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_write_report_with_rag", lambda self, state, kb, prev_record=None: "# 研报")
    monkeypatch.setattr(orch_mod, "compare_with_history", lambda record, prev_record: "")
    monkeypatch.setattr(orch_mod, "find_peer_from_history", lambda records, industry, exclude_code=None: [])

    events: list[str] = []
    orchestrator = orch_mod.AgentOrchestrator(on_step=lambda event, detail, state: events.append(event))
    orchestrator._tracer = orch_mod.Tracer()
    state = orchestrator._run_traced("600519", AnalysisState(stock_code="600519", stock_name="测试公司"), uploaded_items=[])

    assert state.final_report.startswith("# 测试公司（600519）深度研究报告")
    assert state.sections["research_conclusion"] == "研究结论"
    assert state.sections["research_reflection"] == "反思摘要"
    assert state.run_payload["multi_agent_trace"]["completed_role_count"] == 6
    assert state.sections["stock_memory_summary"] == "长期记忆摘要"
    assert state.sections["memory_hit_count"] == "1"
    assert state.sections["memory_conflict_count"] == "1"
    assert "去重 1 条" in state.sections["memory_governance_notes"]
    assert state.sections["repeated_risk_pattern_count"] == "1"
    assert state.sections["rating_drift_count"] == "1"
    assert state.sections["graph_hit_count"] != "0"
    assert float(state.sections["hybrid_retrieval_hit_rate"]) >= 0.0
    assert float(state.sections["relationship_coverage"]) > 0
    assert state.sections["graph_query_focus"] == "风险传导"
    assert float(state.sections["graph_focus_coverage"]) > 0
    assert state.sections["section_graph_hit_count"] != "0"
    assert float(state.sections["section_graph_focus_coverage"]) > 0
    assert "风险传导=命中" in state.sections["graph_focus_summary"]
    assert "风险章节=命中" in state.sections["section_graph_summary"]
    assert "测试公司" in state.sections["section_graph_query_summary"]
    assert state.sections["section_graph_query_risk"]
    assert int(state.sections["section_graph_query_refined_count"]) >= 0
    assert state.sections["section_graph_refinement_decision"]
    assert state.sections.get("section_graph_refinement_strategy_summary", "")
    assert "风险章节 Graph Context：" in state.sections["section_graph_context_risk"]
    assert "行业章节 Graph Context：" in state.sections["section_graph_context_industry"]
    assert "估值章节 Graph Context：" in state.sections["section_graph_context_valuation"]
    assert state.sections["hybrid_graph_context"]
    assert "Query Focus：风险传导" in state.sections["hybrid_graph_context"]
    assert "多焦点关系摘要" in state.sections["hybrid_graph_context"]
    assert "仅把长期记忆当作待验证线索" in state.sections["research_memory_context"]
    assert "记忆治理" in state.sections["research_memory_context"]
    assert "重复风险模式" in state.sections["research_memory_context"]
    assert "评级变化" in state.sections["writing_memory_context"]
    assert "重复催化模式" in state.sections["writing_memory_context"]
    assert "模式摘要" in state.sections["writing_memory_context"]
    assert "冲突原因" in state.sections["writing_memory_context"]
    assert "推荐" in state.sections["memory_comparison_rating"]
    assert "<external_data>" not in state.sections["research_memory_context"]
    assert "<external_data>" not in state.sections["writing_memory_context"]
    assert state.sections["risk_evolution_count"] == "2"
    assert state.sections["valuation_rating_timeline_count"] == "2"
    assert state.sections["agent_steps"] == "1"
    assert state.run_payload["agent_steps"] == 1
    assert state.run_payload["rag_hits"] == int(state.sections.get("rag_hits", "0"))
    assert state.run_payload["postprocess"]["fix_count"] >= 1
    assert state.run_payload["phase_breakdown"]
    assert int(state.sections["postprocess_fix_count"]) >= 1
    assert "rag_ready" in events
    assert "writer_done" in events


def test_build_section_graph_query_refinements_tightens_only_low_absorption_sections():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.peers = [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)]
    state.risks = [RiskItem(category="news", level="high", description="需求波动加剧")]
    state.sections["section_graph_context_risk"] = "旧风险章节 Graph Context：\n- 测试公司 --causes_risk--> 旧需求波动"
    state.sections["section_graph_context_industry"] = "旧行业章节 Graph Context：\n- 测试公司 --compares_with--> 旧五粮液"
    state.sections["section_graph_context_valuation"] = "旧估值章节 Graph Context：\n- 未命中"
    state.graph_payload["section_graph_context_map"] = {
        "risk": "风险章节 Graph Context：\n- 测试公司 --causes_risk--> 需求波动",
        "industry": "行业章节 Graph Context：\n- 测试公司 --compares_with--> 五粮液",
        "valuation": "估值章节 Graph Context：\n- 未命中",
    }
    state.final_report = """
## 六、行业格局与可比公司对比
公司所处行业竞争格局稳定，与同行可比维度清晰。

## 七、核心风险与跟踪指标
公司经营稳健，但相关不确定性仍需后续跟踪。
"""

    refinements = orchestrator._build_section_graph_query_refinements(state)

    assert "风险结论" in refinements["risk"]
    assert refinements["industry"] == ""
    assert "估值 目标价 DCF" in refinements["valuation"]
    assert "风险章节=低吸收→贴正文表达" in state.sections["section_graph_refinement_decision"]
    assert "风险章节=低吸收→贴正文表达" in state.sections["section_graph_refinement_strategy_summary"]
    assert "估值章节=无命中→扩词召回" in state.sections["section_graph_refinement_strategy_summary"]
    assert "行业章节=注入是/吸收是" in state.sections["section_graph_feedback_summary"]
    assert "风险章节=低吸收→贴正文表达" in state.graph_payload["section_graph_refinement_decision"]
    assert "行业章节=注入是/吸收是" in state.graph_payload["section_graph_feedback_summary"]


def test_build_section_graph_query_refinements_uses_no_hit_and_no_gain_strategies():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.peers = [PeerCompany(code="000858", name="五粮液", market_cap=800, pe_ratio=25, roe=18)]
    state.risks = [RiskItem(category="news", level="high", description="需求波动加剧")]
    state.sections["section_graph_context_risk"] = "旧风险章节 Graph Context：\n- 已命中"
    state.sections["section_graph_context_industry"] = "旧行业章节 Graph Context：\n- 测试公司 --compares_with--> 旧五粮液"
    state.sections["section_graph_context_valuation"] = "旧估值章节 Graph Context：\n- 已命中"
    state.sections["section_graph_refinement_comparison_summary"] = "旧风险章节=9->9 (Δ9)"
    state.graph_payload["section_graph_context_map"] = {
        "risk": "风险章节 Graph Context：\n- 未命中",
        "industry": "行业章节 Graph Context：\n- 测试公司 --compares_with--> 五粮液",
        "valuation": "估值章节 Graph Context：\n- 未命中",
    }
    state.graph_payload["section_graph_refinement_comparison_summary"] = "风险章节=0->0 (Δ0)；行业章节=1->1 (Δ0)；估值章节=0->0 (Δ0)"
    state.final_report = """
## 六、行业格局与可比公司对比
公司所处行业竞争格局稳定，但未形成新增可比结论。

## 七、核心风险与跟踪指标
公司经营稳健，但相关不确定性仍需后续跟踪。
"""

    refinements = orchestrator._build_section_graph_query_refinements(state)

    assert "新闻 公告 指标" in refinements["risk"]
    assert "估值 目标价 DCF" in refinements["valuation"]
    assert refinements["industry"] == ""
    assert "风险章节=无命中→扩词召回" in state.sections["section_graph_refinement_strategy_summary"]
    assert "估值章节=无命中→扩词召回" in state.sections["section_graph_refinement_strategy_summary"]


def test_format_risks_includes_evidence_and_path():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(
        stock_code="600519",
        risks=[
            RiskItem(
                category="news",
                level="high",
                description="监管或合规负面事件升温，可能扰动经营节奏与市场预期",
                evidence="新闻标题：公司收到监管问询函",
                transmission_path="监管处置或合规整改 → 利润率与估值承压",
                impact="净利率、估值中枢",
                source="东财",
                time="2026-01-02",
            )
        ],
    )

    text = orchestrator._format_risks(state)

    assert "证据：" in text
    assert "传导路径：" in text
    assert "来源：东财 | 2026-01-02" in text


def test_ingest_uploaded_documents_updates_state_and_metrics():
    events: list[str] = []
    orchestrator = orch_mod.AgentOrchestrator(on_step=lambda event, *_: events.append(event))
    state = AnalysisState(stock_code="600519")

    orchestrator._ingest_uploaded_documents(
        state,
        [{"name": "notes.txt", "content": "标题\n|列A|列B|\n|---|---|\n|1|2|".encode("utf-8"), "content_type": "text/plain"}],
    )

    assert len(state.documents) == 1
    assert len(state.source_refs) == 1
    assert state.source_refs[0]["provider"] == "upload"
    assert state.source_refs[0]["retrieval_mode"] == "user_upload"
    assert state.sections["document_parse_success_rate"] == "1.00"
    assert state.sections["table_extraction_success_rate"] == "1.00"
    assert state.sections["document_parse_failure_count"] == "0"
    assert events == ["document_parse_start", "document_parse_done"]


def test_post_process_report_fills_missing_sections_and_metadata():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        sections={"rating": "推荐", "rating_detail": "盈利质量稳健"},
        risks=[
            RiskItem(
                category="news",
                level="high",
                description="监管或合规负面事件升温，可能扰动经营节奏与市场预期",
                evidence="新闻标题：公司收到监管问询函",
                transmission_path="监管处置或合规整改 → 利润率与估值承压",
                impact="净利率、估值中枢",
                source="东财",
                time="2026-01-02",
            )
        ],
        metrics=[FinancialMetrics(code="600519", period="2025-12-31", revenue_yoy=8.5, profit_yoy=6.2, roe=24.5, cash_flow=120)],
    )

    report = "# 错误标题\n\n## 一、投资要点\n已有内容。"
    processed = orchestrator._post_process_report(report, state)

    assert processed.startswith("# 贵州茅台（600519）深度研究报告")
    assert "## 七、核心风险与跟踪指标" in processed
    assert "证据：" in processed
    assert "传导路径：" in processed
    assert "## 八、投资建议" in processed
    assert "估值锚：" in processed
    assert state.sections["postprocess_fix_count"] != "0"


def test_collect_data_gaps_and_disclosure():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        metrics=[FinancialMetrics(code="600519", period="2025-12-31", revenue=100, net_profit=30, cash_flow=0, total_assets=0, total_equity=0)],
        sections={"rating": "推荐", "rating_detail": "数据待补充"},
    )

    gaps = orchestrator._collect_data_gaps(state)
    processed = orchestrator._post_process_report("# 标题\n\n## 七、核心风险与跟踪指标\n已有内容。", state)

    assert any("经营现金流数据不足" in gap for gap in gaps)
    assert any("资产负债表字段不完整" in gap for gap in gaps)
    assert "数据降级说明" in processed
    assert "data_gap_disclosure" in state.sections["postprocess_fixes"]
    assert "data_gap_disclosure" in state.run_payload["postprocess"]["fixes"]
    assert "data_gap_disclosure" in state.run_payload["postprocess"]["fix_summary"]


def test_post_process_report_aligns_investment_rating_text():
    orchestrator = orch_mod.AgentOrchestrator()
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        sections={"rating": "推荐", "rating_detail": "盈利质量稳健"},
    )

    report = "# 标题\n\n## 八、投资建议\n**投资评级：减持**\n\n核心理由：估值需观察。\n\n当前评级：中性。"
    processed = orchestrator._post_process_report(report, state)

    assert "**投资评级：推荐**" in processed
    assert "当前评级：推荐（盈利质量稳健）。" in processed
    assert "investment_rating_aligned" in state.run_payload["postprocess"]["fixes"]
