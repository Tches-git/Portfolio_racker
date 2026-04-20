from __future__ import annotations

from app.ui.callbacks import build_stage_overview, get_progress_state


def test_get_progress_state_for_stage_events():
    rag_ready = get_progress_state("rag_ready")
    writer_done = get_progress_state("writer_done")

    assert rag_ready is not None
    assert rag_ready["progress"] > 0
    assert rag_ready["label"] == "知识库就绪"
    assert writer_done is not None
    assert writer_done["progress"] == 1.0


def test_get_progress_state_for_unknown_event_returns_none():
    assert get_progress_state("unknown_event") is None


def test_build_stage_overview_renders_table():
    markdown = build_stage_overview({"knowledge": "done", "data": "running", "research": "pending", "write": "pending"})

    assert "阶段状态" in markdown
    assert "知识准备" in markdown
    assert "✅ 已完成" in markdown
    assert "🔄 进行中" in markdown
