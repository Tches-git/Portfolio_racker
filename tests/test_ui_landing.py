from __future__ import annotations

from app.ui.landing import POPULAR_STOCK_PILLS, _WORKSPACE_HINTS


def test_popular_stock_pills_contains_core_examples():
    assert "600519" in POPULAR_STOCK_PILLS
    assert "300750" in POPULAR_STOCK_PILLS


def test_workspace_hints_cover_all_views():
    assert set(_WORKSPACE_HINTS) == {"home", "run", "result"}
    assert "工作台" in _WORKSPACE_HINTS["run"]
    assert "结果浏览" in _WORKSPACE_HINTS["result"]
