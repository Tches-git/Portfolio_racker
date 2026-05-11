from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_alerts_page_and_api_client_are_wired():
    page = (ROOT / "frontend/src/app/alerts/page.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "金融预警中心" in page
    assert "fetchTrackingAlerts" in page
    assert "/api/v1/alerts" in api
    assert "TrackingAlertListResponse" in types
    assert "/alerts" in sidebar


def test_briefing_page_and_api_client_are_wired():
    page = (ROOT / "frontend/src/app/briefing/page.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "Daily Briefing" in page
    assert "fetchDailyBriefing" in page
    assert "/api/v1/briefing/daily" in api
    assert "DailyBriefingResponse" in types
    assert "/briefing" in sidebar
