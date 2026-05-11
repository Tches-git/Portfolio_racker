from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import EventCollection, MarketEvent, Watchlist


def test_watchlists_endpoint_returns_contract(monkeypatch):
    watchlist = Watchlist(watchlist_id="wl1", name="核心组合", stock_codes=["600519"])
    monkeypatch.setattr("app.api.server.list_watchlists", lambda: [watchlist])

    payload = TestClient(app).get("/api/v1/watchlists").json()

    assert payload["total"] == 1
    assert payload["items"][0]["watchlist_id"] == "wl1"


def test_create_watchlist_endpoint_dedupes_codes(monkeypatch):
    captured = {}

    def fake_create(name, stock_codes, *, description=""):
        captured["stock_codes"] = stock_codes
        return Watchlist(watchlist_id="wl2", name=name, stock_codes=["600519", "000858"], description=description)

    monkeypatch.setattr("app.api.server.create_watchlist", fake_create)

    payload = TestClient(app).post(
        "/api/v1/watchlists",
        json={"name": "自选组合", "stock_codes": ["600519", "600519", "000858"], "description": "测试"},
    ).json()

    assert captured["stock_codes"] == ["600519", "600519", "000858"]
    assert payload["stock_codes"] == ["600519", "000858"]


def test_watchlist_detail_endpoint_returns_portfolio_context(monkeypatch):
    watchlist = Watchlist(
        watchlist_id="wl1",
        name="核心组合",
        stock_codes=["600519"],
        last_refreshed_at="2026-05-11T09:30:00",
    )
    event = MarketEvent(event_id="e1", stock_code="600519", title="高影响公告", impact_level="high", provider="cninfo")
    monkeypatch.setattr("app.api.server.get_watchlist", lambda watchlist_id: watchlist if watchlist_id == "wl1" else None)
    monkeypatch.setattr("app.api.server.collect_historical_events", lambda stock_codes=None, limit=80: EventCollection(items=[event], total=1, high_impact_count=1, source_count=1))

    payload = TestClient(app).get("/api/v1/watchlists/wl1").json()

    assert payload["watchlist"]["watchlist_id"] == "wl1"
    assert payload["events"]["mode"] == "history"
    assert payload["summary"]["event_count"] == 1
    assert payload["summary"]["impacted_stocks"][0]["stock_code"] == "600519"


def test_watchlist_detail_endpoint_returns_404_for_missing_watchlist(monkeypatch):
    monkeypatch.setattr("app.api.server.get_watchlist", lambda watchlist_id: None)

    response = TestClient(app).get("/api/v1/watchlists/missing")

    assert response.status_code == 404


def test_watchlist_refresh_endpoint_collects_events_and_updates_timestamp(monkeypatch):
    watchlist = Watchlist(watchlist_id="wl1", name="核心组合", stock_codes=["600519"])
    updated = Watchlist(
        watchlist_id="wl1",
        name="核心组合",
        stock_codes=["600519"],
        last_refreshed_at="2026-05-11T10:00:00",
    )
    event = MarketEvent(event_id="e2", stock_code="600519", title="实时事件", provider="quote")
    captured = {}

    def fake_collect(stock_codes=None, limit_per_stock=4):
        captured["stock_codes"] = stock_codes
        captured["limit_per_stock"] = limit_per_stock
        return EventCollection(items=[event], total=1, source_count=1)

    monkeypatch.setattr("app.api.server.get_watchlist", lambda watchlist_id: watchlist)
    monkeypatch.setattr("app.api.server.collect_market_events", fake_collect)
    monkeypatch.setattr("app.api.server.mark_watchlist_refreshed", lambda watchlist_id: updated)

    response = TestClient(app).post("/api/v1/watchlists/wl1/refresh")
    payload = response.json()

    assert response.status_code == 202
    assert captured["stock_codes"] == ["600519"]
    assert payload["watchlist"]["last_refreshed_at"] == "2026-05-11T10:00:00"
    assert payload["events"]["mode"] == "realtime"
