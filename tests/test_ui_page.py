from __future__ import annotations

from app.ui.page import build_result_summary, build_workspace_options, resolve_workspace_view
from app.models import AnalysisState


def test_build_result_summary_extracts_core_metrics():
    state = AnalysisState(stock_code="600519", stock_name="贵州茅台", sections={"agent_steps": "8", "rag_hits": "3"})
    run_metrics = {"duration_s": 12.34, "total_tokens": 5678}

    summary = build_result_summary(state, run_metrics)

    assert summary["stock"] == "贵州茅台 (600519)"
    assert summary["agent_steps"] == "8"
    assert summary["rag_hits"] == "3"
    assert summary["duration"] == "12.34s"
    assert summary["tokens"] == "5678"


def test_build_workspace_options_hides_result_when_no_report():
    options = build_workspace_options(False)

    assert [item["key"] for item in options] == ["home", "run"]


def test_resolve_workspace_view_prefers_run_while_running():
    assert resolve_workspace_view("result", has_result=True, running=True) == "run"
    assert resolve_workspace_view("", has_result=True, running=False) == "result"
