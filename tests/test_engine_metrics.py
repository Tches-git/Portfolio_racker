from __future__ import annotations

import app.engine as engine_mod
from app.models import AnalysisState


class DummyOrchestrator:
    def __init__(self, on_step=None):
        self.on_step = on_step
        self.tracer = self
        self.agent_trace = []
        self.rag_trace = []

    def run(self, stock_code: str) -> AnalysisState:
        state = AnalysisState(stock_code=stock_code, final_report="# report")
        state.sections["agent_steps"] = "5"
        state.sections["rag_hits"] = "2"
        return state

    def summary(self) -> dict:
        return {"trace_id": "trace-1", "tool_calls": 7, "errors": 1}


class DummyTokenStats:
    def __init__(self):
        self.calls = 0

    def snapshot(self):
        self.calls += 1
        if self.calls == 1:
            return {
                "total_calls": 1,
                "total_prompt_tokens": 10,
                "total_completion_tokens": 5,
                "total_tokens": 15,
            }
        return {
            "total_calls": 4,
            "total_prompt_tokens": 40,
            "total_completion_tokens": 25,
            "total_tokens": 65,
        }


def test_report_engine_collects_run_metrics(monkeypatch):
    monkeypatch.setattr(engine_mod, "AgentOrchestrator", DummyOrchestrator)
    monkeypatch.setattr(engine_mod, "token_stats", DummyTokenStats())

    engine = engine_mod.ReportEngine()
    state = engine.run("600519")

    assert state.run_metrics["success"] is True
    assert state.run_metrics["llm_calls"] == 3
    assert state.run_metrics["total_tokens"] == 50
    assert state.run_metrics["tool_calls"] == 7
    assert state.run_metrics["errors"] == 1
    assert engine.last_run_metrics["trace_id"] == "trace-1"
