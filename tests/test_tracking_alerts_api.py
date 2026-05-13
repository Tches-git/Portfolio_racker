from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import EventCollection, MarketEvent
from tests.helpers import authenticated_client


def test_alerts_endpoint_returns_alert_summary(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="e1", stock_code="600519", title="监管问询", impact_level="high", sentiment="negative", impact_scope="risk")],
        total=1,
        high_impact_count=1,
        source_count=1,
    )
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: collection)

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/alerts?stock_codes=600519").json()

    assert payload["total"] >= 2
    assert payload["high_severity_count"] >= 1
    assert payload["risk_alert_count"] >= 1
    assert payload["manual_review_count"] >= 1
    assert payload["severity_counts"]["high"] >= 1
    assert payload["alert_type_counts"]["risk_watch"] >= 1
    assert payload["rule_counts"]["high_impact"] >= 1


def test_alerts_endpoint_filters_processed_status(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="e1", stock_code="600519", title="已复核风险", impact_level="high", status="reviewed")],
        total=1,
        high_impact_count=1,
        source_count=1,
    )
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: collection)

    with authenticated_client() as (client, _user):
        reviewed = client.get("/api/v1/alerts?stock_codes=600519&status=reviewed").json()
        open_alerts = client.get("/api/v1/alerts?stock_codes=600519&status=open").json()

    assert reviewed["total"] == 1
    assert reviewed["items"][0]["status"] == "reviewed"
    assert open_alerts["total"] == 0


def test_alert_rules_endpoint_returns_builtin_rules():
    payload = TestClient(app).get("/api/v1/alerts/rules").json()

    assert payload["total"] >= 6
    assert {item["rule_id"] for item in payload["items"]} >= {"high_impact", "manual_review", "regulation_risk"}


def test_alerts_endpoint_filters_by_mode_severity_type_and_rule(monkeypatch):
    collection = EventCollection(
        items=[
            MarketEvent(event_id="e1", stock_code="600519", title="重大公告", impact_level="high", confidence=0.4),
            MarketEvent(event_id="e2", stock_code="600519", title="来源占位", retrieval_mode="placeholder", is_placeholder=True),
        ],
        total=2,
        high_impact_count=1,
        source_count=2,
    )
    monkeypatch.setattr("app.api.server.list_user_events", lambda db, user_id, stock_codes=None, limit=100, **kwargs: collection)

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/alerts?mode=history&severity=high&alert_type=manual_review&rule_id=manual_review").json()

    assert payload["total"] == 1
    assert payload["items"][0]["rule_id"] == "manual_review"
    assert payload["items"][0]["severity"] == "high"


def test_daily_briefing_endpoint_returns_key_events(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="e1", stock_code="600519", title="高影响事件", impact_level="high", sentiment="positive")],
        total=1,
        high_impact_count=1,
        source_count=1,
    )
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: collection)

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/briefing/daily?stock_codes=600519").json()

    assert payload["total_events"] == 1
    assert payload["key_events"][0]["event_id"] == "e1"
    assert payload["suggested_actions"]
