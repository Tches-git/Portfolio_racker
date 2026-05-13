from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_watchlist_page_and_client_are_wired():
    page = (ROOT / "frontend/src/app/watchlist/page.tsx").read_text(encoding="utf-8")
    detail_page = (ROOT / "frontend/src/app/watchlist/[watchlistId]/page.tsx").read_text(encoding="utf-8")
    refresh_button = (ROOT / "frontend/src/components/watchlist-refresh-button.tsx").read_text(encoding="utf-8")
    form = (ROOT / "frontend/src/components/watchlist-create-form.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "组合跟踪" in page
    assert "fetchDashboard" in page
    assert "fetchMarketEvents" not in page
    assert "/watchlist/${watchlist.watchlist_id}" in page
    assert "fetchUiWatchlistDetail" in detail_page
    assert "WatchlistRefreshButton" in detail_page
    assert "组合驾驶舱" in detail_page
    assert "risk_score" in detail_page
    assert "priority_actions" in detail_page
    assert "新账号不会加载旧数据" in page
    assert "只有你创建并刷新过的组合" in page
    assert "router.push(`/watchlist/${created.watchlist_id}`)" in form
    assert "refreshWatchlist" in refresh_button
    assert "createWatchlist" in form
    assert "/api/v1/ui/watchlists/${encodeURIComponent(watchlistId)}" in api
    assert "/api/v1/watchlists" in api
    assert "/api/v1/watchlists/${encodeURIComponent(watchlistId)}/refresh" in api
    assert "WatchlistListResponse" in types
    assert "WatchlistDetailResponse" in types
    assert "href: '/watchlist'" in sidebar


def test_homepage_actions_are_executable_and_setup_has_no_demo_stocks():
    setup = (ROOT / "frontend/src/components/workbench/setup-wizard.tsx").read_text(encoding="utf-8")
    action_buttons = (ROOT / "frontend/src/components/workbench/workbench-action-buttons.tsx").read_text(encoding="utf-8")
    shell = (ROOT / "frontend/src/components/workbench/workspace-shell.tsx").read_text(encoding="utf-8")
    search_shell = (ROOT / "frontend/src/components/search-shell.tsx").read_text(encoding="utf-8")
    workspace_insights = (ROOT / "frontend/src/components/workspace-insights.tsx").read_text(encoding="utf-8")

    assert "WorkbenchActionButtons" in shell
    assert "refreshWatchlist(action.target_id)" in action_buttons
    assert "router.refresh()" in action_buttons
    assert "suggested_stock_codes.map" in setup
    assert "POPULAR" not in search_shell
    assert "FAVORITES" not in workspace_insights
    for demo_code in ["600519", "000858", "300750", "600036"]:
        assert demo_code not in setup
        assert demo_code not in search_shell
        assert demo_code not in workspace_insights
