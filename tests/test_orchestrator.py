from __future__ import annotations

from dataclasses import dataclass

import app.agent.orchestrator as orch_mod
from app.models import AnalysisState, FinancialMetrics, PeerCompany, RiskItem, StockProfile, ToolCallRecord


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


def test_run_traced_collects_sections(monkeypatch):
    monkeypatch.setattr(orch_mod, "get_memory_store", lambda: DummyMemoryStore())
    monkeypatch.setattr(orch_mod, "get_knowledge_base", lambda: DummyKB())
    monkeypatch.setattr(orch_mod, "ReActAgent", DummyResearchAgent)
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_prefetch_data", lambda self, state: state.tool_memory.append(ToolCallRecord(tool_name="fetch_stock_profile", observation="ok")))
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_enrich_knowledge", lambda self, state, kb: None)
    monkeypatch.setattr(orch_mod.AgentOrchestrator, "_write_report_with_rag", lambda self, state, kb, prev_record=None: "# 研报")
    monkeypatch.setattr(orch_mod, "compare_with_history", lambda record, prev_record: "")
    monkeypatch.setattr(orch_mod, "find_peer_from_history", lambda records, industry, exclude_code=None: [])

    events: list[str] = []
    orchestrator = orch_mod.AgentOrchestrator(on_step=lambda event, detail, state: events.append(event))
    orchestrator._tracer = orch_mod.Tracer()
    state = orchestrator._run_traced("600519", AnalysisState(stock_code="600519", stock_name="测试公司"))

    assert state.final_report.startswith("# 测试公司（600519）深度研究报告")
    assert state.sections["research_conclusion"] == "研究结论"
    assert state.sections["research_reflection"] == "反思摘要"
    assert state.sections["agent_steps"] == "1"
    assert int(state.sections["postprocess_fix_count"]) >= 1
    assert "rag_ready" in events
    assert "writer_done" in events


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
