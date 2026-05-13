from __future__ import annotations

from app.api.schemas import AnalysisRunListResponse
import app.api.server as server
from app.db.repositories import create_user_watchlist, save_user_events
from app.tracking.models import MarketEvent
from tests.helpers import multi_user_client


def _headers(username: str) -> dict[str, str]:
    return {"X-Test-User": username}


def test_ui_dashboard_new_user_returns_setup_without_collecting_defaults(monkeypatch):
    def fail_collect(*args, **kwargs):
        raise AssertionError("UI 驾驶舱不应该隐式采集默认股票池")

    monkeypatch.setattr(server, "collect_market_events", fail_collect)
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=8, user_id="": AnalysisRunListResponse())

    with multi_user_client() as (client, _users, Session):
        payload = client.get("/api/v1/ui/dashboard", headers=_headers("alice")).json()
        with Session() as db:
            events = server.list_user_events(db, user_id="user-alice").total
            watchlists = server.list_user_watchlists(db, user_id="user-alice")

    assert payload["mode"] == "setup"
    assert payload["setup"]["title"] == "创建第一个组合"
    assert payload["setup"]["suggested_stock_codes"] == []
    assert payload["watchlists"]["total"] == 0
    assert payload["latest_events"]["total"] == 0
    assert events == 0
    assert watchlists == []


def test_ui_dashboard_active_user_returns_portfolio_risk(monkeypatch):
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=8, user_id="": AnalysisRunListResponse())

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            create_user_watchlist(db, user_id="user-alice", name="核心组合", stock_codes=["600519"])
            save_user_events(
                db,
                user_id="user-alice",
                events=[MarketEvent(event_id="event_a", stock_code="600519", title="高影响事件", impact_level="high", confidence=0.6)],
            )
            create_user_watchlist(db, user_id="user-bob", name="Bob 组合", stock_codes=["000858"])
            save_user_events(
                db,
                user_id="user-bob",
                events=[MarketEvent(event_id="event_b", stock_code="000858", title="Bob 事件", impact_level="high")],
            )

        alice = client.get("/api/v1/ui/dashboard", headers=_headers("alice")).json()
        bob = client.get("/api/v1/ui/dashboard", headers=_headers("bob")).json()

    assert alice["mode"] == "active"
    assert alice["portfolio_summary"]["watchlist_count"] == 1
    assert alice["portfolio_summary"]["event_count"] == 1
    assert alice["risk_queue"]["total"] >= 1
    assert alice["latest_events"]["items"][0]["event_id"] == "event_a"
    assert bob["latest_events"]["items"][0]["event_id"] == "event_b"


def test_ui_events_supports_alert_view_filters_and_selected_event(monkeypatch):
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=8, user_id="": AnalysisRunListResponse())

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            create_user_watchlist(db, user_id="user-alice", name="核心组合", stock_codes=["600519"])
            save_user_events(
                db,
                user_id="user-alice",
                events=[MarketEvent(event_id="event_review", stock_code="600519", title="低置信高影响", impact_level="high", confidence=0.5)],
            )

        payload = client.get(
            "/api/v1/ui/events?view=alerts&severity=high&selected_event_id=event_review",
            headers=_headers("alice"),
        ).json()

    assert payload["view"] == "alerts"
    assert payload["alerts"]["total"] >= 1
    assert payload["selected_event"]["event_id"] == "event_review"
    assert payload["filters"]["severity"] == "high"


def test_ui_stock_workbench_is_readonly_for_untracked_stock(monkeypatch):
    monkeypatch.setattr(server, "collect_stock_events", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("UI 股票台不应该实时采集")))
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=50, user_id="": AnalysisRunListResponse())
    monkeypatch.setattr(server.run_manager, "list_event_runs", lambda stock_code="", limit=40, user_id="": [])

    with multi_user_client() as (client, _users, Session):
        response = client.get("/api/v1/ui/stocks/600519", headers=_headers("alice"))
        with Session() as db:
            events = server.list_user_events(db, user_id="user-alice").total

    assert response.status_code == 200
    assert response.json()["is_tracked"] is False
    assert response.json()["timeline"]["total"] == 0
    assert events == 0
