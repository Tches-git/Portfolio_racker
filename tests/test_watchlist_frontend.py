from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_watchlist_page_and_client_are_wired():
    page = (ROOT / "frontend/src/app/watchlist/page.tsx").read_text(encoding="utf-8")
    detail_page = (ROOT / "frontend/src/app/watchlist/[watchlistId]/page.tsx").read_text(encoding="utf-8")
    market_center = (ROOT / "frontend/src/components/workbench/watchlist-market-center.tsx").read_text(encoding="utf-8")
    dashboard = (ROOT / "frontend/src/components/workbench/dashboard-overview.tsx").read_text(encoding="utf-8")
    refresh_button = (ROOT / "frontend/src/components/watchlist-refresh-button.tsx").read_text(encoding="utf-8")
    form = (ROOT / "frontend/src/components/watchlist-create-form.tsx").read_text(encoding="utf-8")
    manager = (ROOT / "frontend/src/components/watchlist-management-panel.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "组合监控终端" in page
    assert "fetchDashboard" in page
    assert "fetchMarketEvents" not in page
    assert "WatchlistManagementPanel" in page
    assert "/watchlist/${watchlist.watchlist_id}" in manager
    assert "fetchUiWatchlistDetail" in detail_page
    assert "WatchlistMarketCenter" in detail_page
    assert "组合行情数据中心" in detail_page
    assert "PortfolioQuoteTable" in market_center
    assert "PortfolioTrendChart" in market_center
    assert "日 K 走势" in market_center
    assert "portfolioCandleBody" in market_center
    assert "buildPriceTicks" in market_center
    assert "buildDateTicks" in market_center
    assert "组合股票日 K 走势图" in market_center
    assert "MarketSuggestionDock" in market_center
    assert "setInterval" in market_center
    assert "document.visibilityState === 'hidden'" in market_center
    assert "router.refresh()" in market_center
    assert "刷新行情" in market_center
    assert "WatchlistRefreshButton" in market_center
    assert "我的组合" in dashboard
    assert "data.watchlists.total" in dashboard
    assert "href={`/watchlist/${watchlist.watchlist_id}`}" in dashboard
    assert "新账号只显示当前用户创建的数据" in page
    assert "删除组合" in manager
    assert "调整股票池" in manager
    assert "updateWatchlistFromForm" in manager
    assert "deleteWatchlistFromForm" in manager
    assert "router.push(`/watchlist/${created.watchlist_id}`)" in form
    assert "refreshWatchlist" in refresh_button
    assert "createWatchlist" in form
    assert "fetchStockSearch" in form
    assert "搜索股票名称 / 代码" in form
    assert "已选股票" in form
    assert "updateWatchlist" in api
    assert "deleteWatchlist" in api
    assert "/api/v1/stocks/search" in api
    assert "/api/v1/ui/watchlists/${encodeURIComponent(watchlistId)}" in api
    assert "/api/v1/watchlists" in api
    assert "/api/v1/watchlists/${encodeURIComponent(watchlistId)}/refresh" in api
    assert "/api/v1/watchlists/${encodeURIComponent(watchlistId)}" in api
    assert "WatchlistListResponse" in types
    assert "WatchlistDetailResponse" in types
    assert "WatchlistMarketSnapshot" in types
    assert "market_snapshots" in types
    assert "market_updated_at" in types
    assert "market_fallback_message" in types
    assert "WatchlistUpdateRequest" in types
    assert "StockSearchResponse" in types
    assert "href: '/watchlist'" in sidebar


def test_homepage_actions_are_executable_and_setup_has_no_demo_stocks():
    setup = (ROOT / "frontend/src/components/workbench/setup-wizard.tsx").read_text(encoding="utf-8")
    action_buttons = (ROOT / "frontend/src/components/workbench/workbench-action-buttons.tsx").read_text(encoding="utf-8")
    shell = (ROOT / "frontend/src/components/workbench/workspace-shell.tsx").read_text(encoding="utf-8")
    primitives = (ROOT / "frontend/src/components/workbench/primitives.tsx").read_text(encoding="utf-8")
    search_shell = (ROOT / "frontend/src/components/search-shell.tsx").read_text(encoding="utf-8")
    workspace_insights = (ROOT / "frontend/src/components/workspace-insights.tsx").read_text(encoding="utf-8")

    assert "PageShell" in shell
    assert "WorkbenchActionButtons" in primitives
    assert "refreshWatchlist(action.target_id)" in action_buttons
    assert "router.refresh()" in action_buttons
    assert "suggested_stock_codes.map" not in setup
    assert "WatchlistCreateForm" in setup
    assert "POPULAR" not in search_shell
    assert "FAVORITES" not in workspace_insights
    for demo_code in ["600519", "000858", "300750", "600036"]:
        assert demo_code not in setup
        assert demo_code not in search_shell
        assert demo_code not in workspace_insights
