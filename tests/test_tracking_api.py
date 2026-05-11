from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import EventCollection, MarketEvent


def test_events_endpoint_returns_tracking_contract(monkeypatch):
    event = MarketEvent(event_id="e1", stock_code="600519", title="高影响公告", impact_level="high", provider="cninfo")
    monkeypatch.setattr("app.api.server.collect_market_events", lambda stock_codes=None, limit_per_stock=4: EventCollection(items=[event], total=1, high_impact_count=1, source_count=1))

    payload = TestClient(app).get("/api/v1/events?stock_codes=600519").json()

    assert payload["total"] == 1
    assert payload["high_impact_count"] == 1
    assert payload["items"][0]["event_id"] == "e1"
    assert payload["mode"] == "realtime"


def test_stock_events_endpoint_returns_timeline_contract(monkeypatch):
    event = MarketEvent(event_id="e2", stock_code="000858", stock_name="五粮液", title="券商点评", event_type="broker_view")
    monkeypatch.setattr("app.api.server.collect_stock_events", lambda stock_code, limit=6, include_history=False: EventCollection(items=[event], total=1, source_count=1))

    payload = TestClient(app).get("/api/v1/stocks/000858/events").json()

    assert payload["stock_code"] == "000858"
    assert payload["stock_name"] == "五粮液"
    assert payload["items"][0]["event_type"] == "broker_view"


def test_events_endpoint_supports_history_mode(monkeypatch):
    event = MarketEvent(event_id="h1", stock_code="600519", title="历史事件")
    captured = {}

    def fake_collect(**kwargs):
        captured.update(kwargs)
        return EventCollection(items=[event], total=1, source_count=1)

    monkeypatch.setattr("app.api.server.collect_historical_events", fake_collect)

    payload = TestClient(app).get("/api/v1/events?mode=history&stock_codes=600519&status=new").json()

    assert payload["mode"] == "history"
    assert payload["items"][0]["event_id"] == "h1"
    assert captured["status"] == "new"


def test_event_detail_endpoint_returns_single_event(monkeypatch):
    event = MarketEvent(event_id="e3", stock_code="600519", title="事件详情")
    monkeypatch.setattr("app.api.server.find_market_event", lambda event_id, stock_codes=None: event if event_id == "e3" else None)

    payload = TestClient(app).get("/api/v1/events/e3").json()

    assert payload["event_id"] == "e3"
    assert payload["title"] == "事件详情"


def test_event_analyze_endpoint_starts_run(monkeypatch):
    event = MarketEvent(event_id="e4", stock_code="600519", title="重大公告", provider="cninfo")
    monkeypatch.setattr("app.api.server.find_market_event", lambda event_id, stock_codes=None: event)
    monkeypatch.setattr("app.api.server.save_events", lambda events: None)
    monkeypatch.setattr("app.api.server.update_event_status", lambda event_id, status, note="": event)

    class FakeRun:
        run_id = "run_event"

    class FakeRunManager:
        def start_event_run(self, stock_code, *, event_context, actor="system", role="admin"):
            assert stock_code == "600519"
            assert event_context["event_id"] == "e4"
            return FakeRun()

        def get_run_response(self, run_id):
            return {"run_id": run_id, "stock_code": "600519", "detail": "由事件触发研报更新"}

    monkeypatch.setattr("app.api.server.run_manager", FakeRunManager())

    payload = TestClient(app).post("/api/v1/events/e4/analyze", json={}).json()

    assert payload["run_id"] == "run_event"
    assert payload["stock_code"] == "600519"


def test_event_status_endpoint_updates_event(monkeypatch):
    event = MarketEvent(event_id="e5", stock_code="600519", title="待复核事件")
    updated = MarketEvent(event_id="e5", stock_code="600519", title="待复核事件", status="reviewed", status_note="已看")
    captured = {}
    monkeypatch.setattr("app.api.server.find_market_event", lambda event_id, stock_codes=None: event)
    monkeypatch.setattr("app.api.server.save_events", lambda events: captured.setdefault("saved", [item.event_id for item in events]))
    monkeypatch.setattr("app.api.server.update_event_status", lambda event_id, status, note="": captured.update({"event_id": event_id, "status": status, "note": note}) or updated)

    payload = TestClient(app).patch("/api/v1/events/e5/status", json={"status": "reviewed", "note": "已看"}).json()

    assert captured["saved"] == ["e5"]
    assert captured["status"] == "reviewed"
    assert payload["status"] == "reviewed"
