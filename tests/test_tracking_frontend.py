from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_events_page_uses_tracking_api_contract():
    page = (ROOT / "frontend/src/app/events/page.tsx").read_text(encoding="utf-8")
    detail_page = (ROOT / "frontend/src/app/events/[eventId]/page.tsx").read_text(encoding="utf-8")
    status_controls = (ROOT / "frontend/src/components/event-status-controls.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    workbench = (ROOT / "frontend/src/components/workbench/event-workbench.tsx").read_text(encoding="utf-8")

    assert "事件预警处理台" in page
    assert "fetchEventWorkbench" in page
    assert "selected_event_id" in page
    assert "EventStatusControls" in workbench
    assert "fetchEventDetail" in detail_page
    assert "fetchMarketWorkbench" in detail_page
    assert "事件详情" in detail_page
    assert "事件正文" in detail_page
    assert "来源证据" in detail_page
    assert "行情快照" in detail_page
    assert "updateEventStatus" in status_controls
    assert "处理闭环" in status_controls
    assert "status_actor" in types
    assert "X-Actor" in api
    assert "/api/v1/events" in api
    assert "/api/v1/ui/events" in api
    assert "/api/v1/events/${eventId}/status" in api
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
    workbench = (ROOT / "frontend/src/components/workbench/stock-workbench.tsx").read_text(encoding="utf-8")

    assert "redirect(`/stocks/${stockCode}?tab=timeline`)" in timeline_page
    assert "fetchStockWorkbench" in stock_page
    assert "历史事件不会隐式沉淀" in stock_page
    assert "所属组合" in workbench
    assert "事件台" in workbench
    assert "AnalysisLauncher" in workbench
    assert "?tab=timeline" in sidebar
    assert "timeline" in workbench


def test_event_detail_page_and_analyze_action_are_wired():
    detail_page = (ROOT / "frontend/src/app/events/[eventId]/page.tsx").read_text(encoding="utf-8")
    analyze_button = (ROOT / "frontend/src/components/event-analyze-button.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    alerts_page = (ROOT / "frontend/src/app/alerts/page.tsx").read_text(encoding="utf-8")
    briefing_page = (ROOT / "frontend/src/app/briefing/page.tsx").read_text(encoding="utf-8")
    workbench = (ROOT / "frontend/src/components/workbench/event-workbench.tsx").read_text(encoding="utf-8")

    assert "EventAnalyzeButton" in detail_page
    assert "返回事件队列定位" in detail_page
    assert "打开原文" in detail_page
    assert "EventAnalyzeButton" in workbench
    assert "eventTapeConsole" in workbench
    assert "eventDetailDock" in workbench
    assert "新闻式详情" in workbench
    assert "analyzeEvent" in analyze_button
    assert "/api/v1/events/${eventId}/analyze" in api
    assert "view: 'alerts'" in alerts_page
    assert "redirect(query.toString() ? `/events?" in briefing_page
