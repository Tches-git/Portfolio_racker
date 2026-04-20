"""网页端会话状态辅助函数。"""
from __future__ import annotations

RESULT_STATE_KEYS = ("state", "engine", "run_error", "last_stock_code")


def set_workspace_view(session_state, view: str) -> None:
    session_state["workspace_view"] = view


def clear_result_state(session_state) -> None:
    for key in RESULT_STATE_KEYS:
        session_state.pop(key, None)
    session_state["running"] = False


def queue_run(session_state, stock_code: str) -> None:
    session_state["pending_run_code"] = stock_code.strip()
    session_state["stock_code_input"] = stock_code.strip()
    set_workspace_view(session_state, "run")


def consume_queued_run(session_state) -> str:
    return str(session_state.pop("pending_run_code", "") or "").strip()


def make_retry_callback(session_state, stock_code: str):
    def _retry() -> None:
        if stock_code:
            queue_run(session_state, stock_code)
    return _retry
