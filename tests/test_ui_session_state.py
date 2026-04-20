from __future__ import annotations

from app.ui.session_state import clear_result_state, consume_queued_run, make_retry_callback, queue_run, set_workspace_view


def test_queue_and_consume_run_code():
    session = {}
    queue_run(session, "600519")

    assert session["pending_run_code"] == "600519"
    assert consume_queued_run(session) == "600519"
    assert "pending_run_code" not in session


def test_clear_result_state_resets_running_and_payload():
    session = {"state": object(), "engine": object(), "run_error": "err", "last_stock_code": "600519", "running": True}

    clear_result_state(session)

    assert session["running"] is False
    assert "state" not in session
    assert "engine" not in session


def test_make_retry_callback_queues_previous_code():
    session = {}
    callback = make_retry_callback(session, "300750")
    callback()

    assert session["pending_run_code"] == "300750"


def test_set_workspace_view_updates_session_state():
    session = {}

    set_workspace_view(session, "result")

    assert session["workspace_view"] == "result"
