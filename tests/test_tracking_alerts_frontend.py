from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_alerts_page_and_api_client_are_wired():
    page = (ROOT / "frontend/src/app/alerts/page.tsx").read_text(encoding="utf-8")
    status_controls = (ROOT / "frontend/src/components/event-status-controls.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")
    event_page = (ROOT / "frontend/src/app/events/page.tsx").read_text(encoding="utf-8")
    event_workbench = (ROOT / "frontend/src/components/workbench/event-workbench.tsx").read_text(encoding="utf-8")
    risk_queue = (ROOT / "frontend/src/components/workbench/risk-queue.tsx").read_text(encoding="utf-8")

    assert "view: 'alerts'" in page
    assert "fetchEventWorkbench" in event_page
    assert "预警处理" in event_workbench
    assert "manual_review_count" in event_workbench
    assert "rule_id" in page
    assert "RiskQueue" in event_workbench
    assert "EventStatusControls" in event_workbench
    assert "update('reviewed'" in status_controls
    assert "标记已复核" in status_controls
    assert "/api/v1/alerts" in api
    assert "/api/v1/alerts/rules" in api
    assert "TrackingAlertFilters" in api
    assert "AlertRuleListResponse" in types
    assert "TrackingAlertListResponse" in types
    assert "rule_counts" in types
    assert "/events" in sidebar
    assert "待处理预警" in risk_queue


def test_briefing_page_and_api_client_are_wired():
    page = (ROOT / "frontend/src/app/briefing/page.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")

    assert "BriefingRedirect" in page
    assert "redirect(query.toString() ? `/events?" in page
    assert "/api/v1/briefing/daily" in api
    assert "DailyBriefingResponse" in types
    assert "/events" in sidebar
