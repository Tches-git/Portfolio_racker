from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_events_page_uses_tracking_api_contract():
    page = (ROOT / "frontend/src/app/events/page.tsx").read_text(encoding="utf-8")
    detail_page = (ROOT / "frontend/src/app/events/[eventId]/page.tsx").read_text(encoding="utf-8")
    status_controls = (ROOT / "frontend/src/components/event-status-controls.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")

    assert "金融事件追踪" in page
    assert "fetchMarketEvents" in page
    assert "status=new" in page
    assert "EventStatusControls" in page
    assert "EventStatusControls" in detail_page
    assert "updateEventStatus" in status_controls
    assert "处理闭环" in status_controls
    assert "status_actor" in types
    assert "X-Actor" in api
    assert "/api/v1/events" in api
    assert "/api/v1/events/${eventId}/status" in api
    assert "mode=history" in page
    assert "stock_codes" in page
    assert "MarketEventListResponse" in types
    assert "high_impact_count" in types
    assert "converted_to_report" in types
    assert "EventImpactReviewResponse" in types
    assert "fetchEventImpactReview" in api
    assert "/api/v1/stocks/${stockCode}/event-impact-review" in api


def test_stock_timeline_page_and_nav_are_wired():
    timeline_page = (ROOT / "frontend/src/app/stocks/[stockCode]/timeline/page.tsx").read_text(encoding="utf-8")
    stock_page = (ROOT / "frontend/src/app/stocks/[stockCode]/page.tsx").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")
    workspace_nav = (ROOT / "frontend/src/components/stock-workspace-nav.tsx").read_text(encoding="utf-8")

    assert "fetchStockEvents" in timeline_page
    assert "事件时间线" in timeline_page
    assert "fetchStockEvents" in stock_page
    assert "fetchWatchlists" in stock_page
    assert "所属组合" in stock_page
    assert "事件详情" in stock_page
    assert "今日简报" in stock_page
    assert "/timeline" in sidebar
    assert "timeline" in workspace_nav


def test_event_detail_page_and_analyze_action_are_wired():
    detail_page = (ROOT / "frontend/src/app/events/[eventId]/page.tsx").read_text(encoding="utf-8")
    analyze_button = (ROOT / "frontend/src/components/event-analyze-button.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    alerts_page = (ROOT / "frontend/src/app/alerts/page.tsx").read_text(encoding="utf-8")
    briefing_page = (ROOT / "frontend/src/app/briefing/page.tsx").read_text(encoding="utf-8")

    assert "fetchEventDetail" in detail_page
    assert "EventAnalyzeButton" in detail_page
    assert "analyzeEvent" in analyze_button
    assert "/api/v1/events/${eventId}/analyze" in api
    assert "EventAnalyzeButton" in alerts_page
    assert "review_required_events" in briefing_page
