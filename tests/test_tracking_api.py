from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import EventCollection, MarketEvent
from tests.helpers import authenticated_client


def test_events_endpoint_returns_tracking_contract(monkeypatch):
    event = MarketEvent(event_id="e1", stock_code="600519", title="高影响公告", impact_level="high", provider="cninfo")
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: EventCollection(items=[event], total=1, high_impact_count=1, source_count=1))

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/events?stock_codes=600519").json()

    assert payload["total"] == 1
    assert payload["high_impact_count"] == 1
    assert payload["items"][0]["event_id"] == "e1"
    assert payload["mode"] == "realtime"


def test_stock_events_endpoint_returns_timeline_contract(monkeypatch):
    event = MarketEvent(event_id="e2", stock_code="000858", stock_name="五粮液", title="券商点评", event_type="broker_view")
    monkeypatch.setattr("app.api.server.collect_stock_events", lambda stock_code, limit=6, include_history=False: EventCollection(items=[event], total=1, source_count=1))

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/stocks/000858/events").json()

    assert payload["stock_code"] == "000858"
    assert payload["stock_name"] == "五粮液"
    assert payload["items"][0]["event_type"] == "broker_view"


def test_stock_event_impact_review_endpoint_links_event_runs(monkeypatch):
    event = MarketEvent(
        event_id="e_review",
        stock_code="600519",
        stock_name="贵州茅台",
        title="高影响公告",
        event_type="announcement",
        impact_level="high",
        sentiment="negative",
        status="converted_to_report",
    )
    monkeypatch.setattr("app.api.server.list_user_events", lambda db, user_id, stock_codes=None, limit=20, **kwargs: EventCollection(items=[event], total=1, high_impact_count=1, source_count=1))
    monkeypatch.setattr("app.api.server._sync_user_run", lambda db, user, run: None)

    class FakeRun:
        run_id = "run_review"
        stock_code = "600519"
        status = "completed"
        updated_at = "2026-05-08T10:00:00"
        created_at = "2026-05-08T09:00:00"
        event_context = {"event_id": "e_review"}
        event_report_summary = {"report_delta_hint": "评级维持推荐", "event_commentary_url": "/api/v1/exports/event_commentary.md"}
        exports = []

    class FakeRunManager:
        def list_event_runs(self, *, stock_code="", limit=40, user_id=""):
            assert stock_code == "600519"
            return [FakeRun()]

    monkeypatch.setattr("app.api.server.run_manager", FakeRunManager())

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/stocks/600519/event-impact-review").json()

    assert payload["stock_code"] == "600519"
    assert payload["high_impact_count"] == 1
    assert payload["converted_count"] == 1
    assert payload["event_driven_run_count"] == 1
    assert payload["dominant_event_types"] == ["announcement"]
    assert payload["replay_items"][0]["run_id"] == "run_review"
    assert payload["replay_items"][0]["event_commentary_url"].endswith("event_commentary.md")


def test_events_endpoint_supports_history_mode(monkeypatch):
    event = MarketEvent(event_id="h1", stock_code="600519", title="历史事件")
    captured = {}

    def fake_list(db, user_id, **kwargs):
        captured.update(kwargs)
        return EventCollection(items=[event], total=1, source_count=1)

    monkeypatch.setattr("app.api.server.list_user_events", fake_list)

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/events?mode=history&stock_codes=600519&status=new").json()

    assert payload["mode"] == "history"
    assert payload["items"][0]["event_id"] == "h1"
    assert captured["status"] == "new"


def test_event_detail_endpoint_returns_single_event(monkeypatch):
    event = MarketEvent(event_id="e3", stock_code="600519", title="事件详情")
    monkeypatch.setattr("app.api.server.get_user_event", lambda db, user_id, event_id: event if event_id == "e3" else None)

    with authenticated_client() as (client, _user):
        payload = client.get("/api/v1/events/e3").json()

    assert payload["event_id"] == "e3"
    assert payload["title"] == "事件详情"


def test_event_analyze_endpoint_starts_run(monkeypatch):
    event = MarketEvent(event_id="e4", stock_code="600519", title="重大公告", provider="cninfo", impact_level="high", event_type="announcement")
    monkeypatch.setattr("app.api.server.get_user_event", lambda db, user_id, event_id: event)
    monkeypatch.setattr("app.api.server.save_user_events", lambda db, user_id, events: None)
    monkeypatch.setattr("app.api.server.update_user_event_status", lambda db, user_id, event_id, status, note="", actor="system": event)
    monkeypatch.setattr("app.api.server._sync_user_run", lambda db, user, run: None)

    class FakeRun:
        run_id = "run_event"

    class FakeRunManager:
        def start_event_run(self, stock_code, *, event_context, actor="system", role="admin", user_id=""):
            assert stock_code == "600519"
            assert event_context["event_id"] == "e4"
            assert event_context["impact_level"] == "high"
            assert event_context["event_type"] == "announcement"
            assert user_id
            return FakeRun()

        def get_run_response(self, run_id):
            return {"run_id": run_id, "stock_code": "600519", "detail": "由事件触发研报更新"}

    monkeypatch.setattr("app.api.server.run_manager", FakeRunManager())

    with authenticated_client() as (client, _user):
        payload = client.post("/api/v1/events/e4/analyze", json={}).json()

    assert payload["run_id"] == "run_event"
    assert payload["stock_code"] == "600519"


def test_event_status_endpoint_updates_event(monkeypatch):
    event = MarketEvent(event_id="e5", stock_code="600519", title="待复核事件")
    updated = MarketEvent(event_id="e5", stock_code="600519", title="待复核事件", status="reviewed", status_note="已看", status_actor="alice")
    captured = {}
    monkeypatch.setattr("app.api.server.get_user_event", lambda db, user_id, event_id: event)
    monkeypatch.setattr("app.api.server.update_user_event_status", lambda db, user_id, event_id, status, note="", actor="system": captured.update({"event_id": event_id, "status": status, "note": note, "actor": actor}) or updated)

    with authenticated_client(username="alice") as (client, _user):
        payload = client.patch("/api/v1/events/e5/status", json={"status": "reviewed", "note": "已看"}, headers={"X-Actor": "alice"}).json()

    assert captured["status"] == "reviewed"
    assert captured["actor"] == "alice"
    assert payload["status"] == "reviewed"
    assert payload["status_actor"] == "alice"
