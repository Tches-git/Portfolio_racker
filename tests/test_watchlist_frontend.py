from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_watchlist_page_and_client_are_wired():
    page = (ROOT / "frontend/src/app/watchlist/page.tsx").read_text(encoding="utf-8")
    form = (ROOT / "frontend/src/components/watchlist-create-form.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "组合跟踪" in page
    assert "fetchWatchlists" in page
    assert "createWatchlist" in form
    assert "/api/v1/watchlists" in api
    assert "WatchlistListResponse" in types
    assert "href: '/watchlist'" in sidebar
