from __future__ import annotations

from types import SimpleNamespace

import app.agent.orchestrator as orch_mod
import web_app
from app.models import AnalysisState
from app.ui.callbacks import make_callback


def test_compact_report_context_keeps_head_and_tail():
    orch = orch_mod.AgentOrchestrator()
    text = "A" * 600 + "中间内容" + "B" * 600
    compacted = orch._compact_report_context(text, 500, "测试上下文")

    assert "已截断" in compacted
    assert compacted.startswith("A" * 200)
    assert compacted.endswith("B" * 120)
    assert len(compacted) < len(text)


def test_make_callback_updates_progress_and_logs():
    events: list[tuple[str, object]] = []

    class DummyProgress:
        def progress(self, value):
            events.append(("progress", value))

    class DummySlot:
        def info(self, text):
            events.append(("info", text))

        def success(self, text):
            events.append(("success", text))

        def markdown(self, text):
            events.append(("markdown", text))

        def caption(self, text):
            events.append(("caption", text))

    callback = make_callback(
        progress_bar=DummyProgress(),
        status_placeholder=DummySlot(),
        log_placeholder=DummySlot(),
        metrics_placeholder=DummySlot(),
        stage_placeholder=DummySlot(),
    )
    state = AnalysisState(stock_code="600519", sections={"agent_steps": "2", "rag_hits": "1"}, run_metrics={"llm_calls": 3, "tool_calls": 4})

    callback("rag_init", "正在初始化", state)
    callback("thinking", "正在分析估值逻辑", state)
    callback("writer_done", "撰写完成", state)

    assert ("progress", 0.10) in events
    assert ("progress", 1.0) in events
    assert any(item[0] == "info" and "知识库初始化" in item[1] for item in events)
    assert any(item[0] == "success" and "研报撰写完成" in item[1] for item in events)
    assert any(item[0] == "markdown" and "实时进展" in item[1] for item in events)
    assert any(item[0] == "caption" and "LLM调用: 3" in item[1] for item in events)


def test_render_run_metrics_shows_postprocess_fix_metadata(monkeypatch):
    calls: list[tuple[str, object]] = []

    class DummyColumn:
        def metric(self, label, value):
            calls.append((label, value))

    class DummyExpander:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(web_app.st, "subheader", lambda text: calls.append(("subheader", text)))
    monkeypatch.setattr(web_app.st, "info", lambda text: calls.append(("info", text)))
    monkeypatch.setattr(web_app.st, "columns", lambda n: [DummyColumn() for _ in range(n)])
    monkeypatch.setattr(web_app.st, "caption", lambda text: calls.append(("caption", text)))
    monkeypatch.setattr(web_app.st, "expander", lambda label, expanded=False: DummyExpander())
    monkeypatch.setattr(web_app.st, "markdown", lambda text: calls.append(("markdown", text)))
    monkeypatch.setattr(web_app.st, "code", lambda text, language=None: calls.append(("code", language)))

    state = AnalysisState(
        stock_code="600519",
        final_report="# 研报\n数据降级说明：新闻数据不足。",
        run_metrics={"duration_s": 1.23, "llm_calls": 2, "tool_calls": 3, "total_tokens": 456, "errors": 0},
        sections={
            "agent_steps": "5",
            "rag_hits": "2",
            "postprocess_fix_count": "3",
            "postprocess_fixes": "missing_section:七、核心风险与跟踪指标\ninvestment_section_enriched",
            "data_gaps": "新闻/舆情数据不足，事件驱动与风险提示需降级",
        },
    )
    engine = SimpleNamespace(last_run_metrics={"trace_id": "trace-1"})

    class DummyEvalResult:
        consistency_issue_count = 2
        risk_evidence_count = 1
        risk_transmission_count = 1
        data_gap_disclosure_count = 1
        consistency_issues = ["报告正文未引用 state 中的 DCF 每股价值：555.57元"]

    monkeypatch.setattr(web_app, "evaluate_report", lambda report, state=None, use_llm_judge=True: DummyEvalResult())

    web_app.render_run_metrics(state, engine)

    assert ("自动修补", "3") in calls
    assert ("一致性问题", "2") in calls
    assert ("数据降级披露", "1") in calls
    assert any(item[0] == "markdown" and "新闻/舆情数据不足" in item[1] for item in calls)
    assert any(item[0] == "markdown" and "DCF 每股价值" in item[1] for item in calls)
    assert any(item[0] == "markdown" and "missing_section:七、核心风险与跟踪指标" in item[1] for item in calls)
    assert ("caption", "trace_id: trace-1") in calls
