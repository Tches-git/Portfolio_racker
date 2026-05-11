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
    assert "fetchWatchlists" in page
    assert "/watchlist/${watchlist.watchlist_id}" in page
    assert "fetchWatchlistDetail" in detail_page
    assert "WatchlistRefreshButton" in detail_page
    assert "组合风险驾驶舱" in detail_page
    assert "risk_score" in detail_page
    assert "priority_actions" in detail_page
    assert "portfolioRiskScore" in page
    assert "最高风险" in page
    assert "refreshWatchlist" in refresh_button
    assert "createWatchlist" in form
    assert "/api/v1/watchlists" in api
    assert "/api/v1/watchlists/${encodeURIComponent(watchlistId)}/refresh" in api
    assert "WatchlistListResponse" in types
    assert "WatchlistDetailResponse" in types
    assert "href: '/watchlist'" in sidebar
