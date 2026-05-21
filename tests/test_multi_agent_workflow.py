from __future__ import annotations

import sys
import types

import app.agent.autogen_adapter as adapter_mod
import app.agent.multi_agent as multi_mod
from app.agent.autogen_adapter import AutoGenRuntime
from app.agent.multi_agent import AutoGenMultiAgentWorkflow
from app.agent.role_specs import MULTI_AGENT_ROLES, get_role_spec
from app.models import AnalysisState, FinancialMetrics, PeerCompany, StockProfile


def test_autogen_runtime_falls_back_without_api_key(monkeypatch):
    monkeypatch.setattr(adapter_mod, "OPENAI_API_KEY", "")

    runtime = adapter_mod.create_autogen_runtime()

    assert runtime.available is False
    assert runtime.mode == "autogen_graphflow_fallback"
    assert "OPENAI_API_KEY" in runtime.error


def test_autogen_runtime_uses_openai_compatible_config(monkeypatch):
    captured: dict[str, object] = {}

    class FakeOpenAIChatCompletionClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    class FakeAssistantAgent:
        def __init__(self, **kwargs):
            self.name = kwargs["name"]

    fake_openai_module = types.ModuleType("autogen_ext.models.openai")
    fake_openai_module.OpenAIChatCompletionClient = FakeOpenAIChatCompletionClient
    fake_agent_module = types.ModuleType("autogen_agentchat.agents")
    fake_agent_module.AssistantAgent = FakeAssistantAgent
    monkeypatch.setitem(sys.modules, "autogen_ext", types.ModuleType("autogen_ext"))
    monkeypatch.setitem(sys.modules, "autogen_ext.models", types.ModuleType("autogen_ext.models"))
    monkeypatch.setitem(sys.modules, "autogen_ext.models.openai", fake_openai_module)
    monkeypatch.setitem(sys.modules, "autogen_agentchat", types.ModuleType("autogen_agentchat"))
    monkeypatch.setitem(sys.modules, "autogen_agentchat.agents", fake_agent_module)
    monkeypatch.setattr(adapter_mod, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(adapter_mod, "OPENAI_BASE_URL", "https://example.test/v1")
    monkeypatch.setattr(adapter_mod, "LLM_MODEL", "gpt-test")

    runtime = adapter_mod.create_autogen_runtime()

    assert runtime.available is True
    assert runtime.mode == "autogen_graphflow"
    assert captured["model"] == "gpt-test"
    assert captured["api_key"] == "test-key"
    assert captured["base_url"] == "https://example.test/v1"
    assert captured["model_info"]["function_calling"] is True
    assert len(runtime.agents or []) == 7


def test_multi_agent_workflow_records_fixed_role_trace():
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    workflow = AutoGenMultiAgentWorkflow(runtime=AutoGenRuntime(available=True, mode="autogen_graphflow", model="test"))

    result = workflow.run("600519", state)

    assert result.trace.role_count == 7
    assert result.trace.completed_role_count == 6
    assert result.trace.failed_role_count == 0
    assert [role.role_id for role in result.trace.roles] == [
        "planner",
        "market_data",
        "fundamental_valuation",
        "event_analysis",
        "risk_review",
        "report_writer",
    ]
    assert "citation_audit" not in [role.role_id for role in result.trace.roles]
    assert state.run_payload["multi_agent_trace"]["mode"] == "autogen_graphflow"
    assert "多智能体研究结论" in state.analysis_payload["research_conclusion"]


def test_roles_have_structured_contracts():
    assert len(MULTI_AGENT_ROLES) == 7
    for spec in MULTI_AGENT_ROLES:
        assert spec.system_message
        assert spec.objective
        assert spec.input_contract
        assert spec.output_contract
        assert spec.failure_policy
        assert spec.quality_checks
    assert get_role_spec("citation_audit").phase == "post_write"


def test_market_and_fundamental_agents_have_separate_tool_boundaries(monkeypatch):
    called: list[str] = []

    monkeypatch.setattr(multi_mod, "_make_tools", lambda state: [])
    monkeypatch.setattr(multi_mod, "execute_tool", lambda tools, name, args, state=None: called.append(name) or "ok")

    state = AnalysisState(
        stock_code="600519",
        stock_name="测试公司",
        profile=StockProfile(code="600519", name="测试公司", industry="测试行业"),
        metrics=[FinancialMetrics(code="600519", period="2025Q4", revenue=100)],
        peers=[PeerCompany(code="000001", name="同行")],
    )
    workflow = AutoGenMultiAgentWorkflow(runtime=AutoGenRuntime(available=True, mode="autogen_graphflow", model="test"))

    workflow.run("600519", state)

    market_spec = get_role_spec("market_data")
    valuation_spec = get_role_spec("fundamental_valuation")
    assert market_spec.allowed_tools == ("trend_analysis",)
    assert "dcf_valuation" not in market_spec.allowed_tools
    assert "dcf_valuation" in valuation_spec.allowed_tools
    assert "dupont_analysis" in called
    assert "dcf_valuation" in called
    assert "comparable_valuation" in called
    assert "trend_analysis" in called


def test_citation_audit_runs_after_final_report(monkeypatch):
    monkeypatch.setattr(multi_mod, "evaluate_rag_citations", lambda report, refs, stock_code="": {
        "citation_coverage_rate": 0.5,
        "unsupported_claim_count": 1,
        "source_reference_count": len(refs),
        "retrieval_topk_hit_rate": 0.4,
        "rerank_selected_count": 2,
    })
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    state.final_report = "# 正式研报\n观点来自来源[1]"
    state.source_refs = [{"title": "来源1"}]
    workflow = AutoGenMultiAgentWorkflow(runtime=AutoGenRuntime(available=True, mode="autogen_graphflow", model="test"))
    workflow.run("600519", state)

    trace = workflow.run_post_write_audit(state)

    assert trace.role_count == 7
    assert trace.completed_role_count == 7
    assert [role.role_id for role in trace.roles][-1] == "citation_audit"
    assert trace.roles[-1].phase == "post_write"
    assert state.analysis_payload["citation_audit"]["citation_coverage_rate"] == 0.5


def test_citation_audit_degrades_when_final_report_empty():
    state = AnalysisState(stock_code="600519", stock_name="测试公司")
    workflow = AutoGenMultiAgentWorkflow(runtime=AutoGenRuntime(available=True, mode="autogen_graphflow", model="test"))
    workflow.run("600519", state)

    trace = workflow.run_post_write_audit(state)

    audit_role = trace.roles[-1]
    assert audit_role.role_id == "citation_audit"
    assert audit_role.status == "degraded"
    assert audit_role.fallback_used is True
    assert "正式报告为空" in audit_role.summary
