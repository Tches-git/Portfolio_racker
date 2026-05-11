from __future__ import annotations

from app.tracking.alerts import build_tracking_alerts
from app.tracking.briefing import build_daily_briefing
from app.tracking.models import EventCollection, MarketEvent


def test_build_tracking_alerts_flags_high_impact_and_risk():
    events = EventCollection(items=[
        MarketEvent(event_id="e1", stock_code="600519", title="收到监管问询", impact_level="high", sentiment="negative", impact_scope="risk", summary="问询函"),
        MarketEvent(event_id="e2", stock_code="000858", title="来源占位", is_placeholder=True, retrieval_mode="placeholder"),
    ], total=2, high_impact_count=1, placeholder_count=1)

    alerts = build_tracking_alerts(events)

    assert {alert.alert_type for alert in alerts} >= {"high_impact", "risk_watch", "source_degraded"}
    assert any(alert.severity == "high" for alert in alerts)


def test_build_daily_briefing_prioritizes_key_events_and_actions():
    collection = EventCollection(items=[
        MarketEvent(event_id="e1", stock_code="600519", title="高影响事件", impact_level="high", sentiment="positive", confidence=0.9),
        MarketEvent(event_id="e2", stock_code="000858", title="低影响事件", impact_level="low", sentiment="neutral", confidence=0.5),
    ], total=2, high_impact_count=1, source_count=2)

    briefing = build_daily_briefing(collection)

    assert briefing.total_events == 2
    assert briefing.key_events[0].event_id == "e1"
    assert "高影响" in briefing.summary
    assert briefing.suggested_actions
