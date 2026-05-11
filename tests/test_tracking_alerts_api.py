from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import EventCollection, MarketEvent


def test_alerts_endpoint_returns_alert_summary(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="e1", stock_code="600519", title="监管问询", impact_level="high", sentiment="negative", impact_scope="risk")],
        total=1,
        high_impact_count=1,
        source_count=1,
    )
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: collection)

    payload = TestClient(app).get("/api/v1/alerts").json()

    assert payload["total"] >= 2
    assert payload["high_severity_count"] >= 1
    assert payload["risk_alert_count"] >= 1


def test_daily_briefing_endpoint_returns_key_events(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="e1", stock_code="600519", title="高影响事件", impact_level="high", sentiment="positive")],
        total=1,
        high_impact_count=1,
        source_count=1,
    )
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: collection)

    payload = TestClient(app).get("/api/v1/briefing/daily").json()

    assert payload["total_events"] == 1
    assert payload["key_events"][0]["event_id"] == "e1"
    assert payload["suggested_actions"]
