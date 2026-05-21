from __future__ import annotations

from app.api.schemas import AnalysisRunListResponse, AnalysisRunResponse
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


def test_ui_events_hide_saved_events_when_user_has_no_tracking_scope(monkeypatch):
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=8, user_id="": AnalysisRunListResponse())

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            save_user_events(
                db,
                user_id="user-alice",
                events=[MarketEvent(event_id="old_event", stock_code="600519", title="旧组合事件", impact_level="high")],
            )

        payload = client.get("/api/v1/ui/events?view=alerts", headers=_headers("alice")).json()
        events = client.get("/api/v1/events?mode=history", headers=_headers("alice")).json()
        alerts = client.get("/api/v1/alerts?mode=history", headers=_headers("alice")).json()

    assert payload["events"]["total"] == 0
    assert payload["alerts"]["total"] == 0
    assert events["items"] == []
    assert alerts["items"] == []


def test_ui_watchlist_detail_returns_market_snapshots_without_collecting_events(monkeypatch):
    def fail_collect(*args, **kwargs):
        raise AssertionError("组合行情 BFF 不应该触发事件采集")

    def fake_quote(stock_code):
        return {
            "stock_name": "测试股份",
            "price": 12.8,
            "market_cap": 1200000000,
            "pe_ratio": 18.5,
            "pb_ratio": 2.1,
            "provider": "mock",
            "time": "2026-05-20T10:30:00",
        }

    def fake_bars(stock_code, days=180):
        return [
            {
                "date": f"2026-05-{day:02d}",
                "open": 10 + day / 10,
                "high": 10.5 + day / 10,
                "low": 9.8 + day / 10,
                "close": 10.2 + day / 10,
                "volume": 10000 + day,
                "amount": 1000000 + day,
                "change_pct": 0.5,
                "turnover": 1.2,
            }
            for day in range(1, 21)
        ]

    monkeypatch.setattr(server, "collect_market_events", fail_collect)
    monkeypatch.setattr(server, "fetch_live_quotes", fake_quote)
    monkeypatch.setattr(server, "get_stock_daily_bars", fake_bars)

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            watchlist = create_user_watchlist(db, user_id="user-alice", name="核心组合", stock_codes=["600519"])

        payload = client.get(f"/api/v1/ui/watchlists/{watchlist.watchlist_id}", headers=_headers("alice")).json()

    assert payload["watchlist"]["watchlist_id"] == watchlist.watchlist_id
    assert payload["market_snapshots"][0]["stock_code"] == "600519"
    assert payload["market_snapshots"][0]["stock_name"] == "测试股份"
    assert payload["market_snapshots"][0]["quote"]["price"] == 12.8
    assert payload["market_snapshots"][0]["trend_30d"]
    assert payload["market_snapshots"][0]["trend_90d"]
    assert payload["market_updated_at"]


def test_ui_watchlist_detail_marks_single_stock_market_degraded(monkeypatch):
    monkeypatch.setattr(server, "fetch_live_quotes", lambda stock_code: (_ for _ in ()).throw(RuntimeError("quote down")))
    monkeypatch.setattr(server, "get_stock_daily_bars", lambda stock_code, days=180: (_ for _ in ()).throw(RuntimeError("bars down")))

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            watchlist = create_user_watchlist(db, user_id="user-alice", name="核心组合", stock_codes=["600519"])
            bob_watchlist = create_user_watchlist(db, user_id="user-bob", name="Bob 组合", stock_codes=["000858"])

        payload = client.get(f"/api/v1/ui/watchlists/{watchlist.watchlist_id}", headers=_headers("alice")).json()
        denied = client.get(f"/api/v1/ui/watchlists/{bob_watchlist.watchlist_id}", headers=_headers("alice"))

    assert denied.status_code == 404
    assert payload["market_snapshots"][0]["source_status"] == "degraded"
    assert "数据源" in payload["market_snapshots"][0]["fallback_message"]
    assert payload["market_fallback_message"]


def test_ui_runs_hide_saved_runs_when_user_has_no_tracking_scope(monkeypatch):
    def fail_list_runs(*args, **kwargs):
        raise AssertionError("无组合用户不应该从任务历史反推出追踪范围")

    monkeypatch.setattr(server.run_manager, "list_runs", fail_list_runs)

    with multi_user_client() as (client, _users, _Session):
        payload = client.get("/api/v1/ui/runs", headers=_headers("alice")).json()

    assert payload["runs"]["total"] == 0
    assert payload["runs"]["items"] == []
    assert payload["runs"]["workspace"]["tracked_stocks"] == []


def test_ui_runs_filter_to_current_watchlist_scope(monkeypatch):
    def fake_list_runs(limit=1000, user_id=""):
        return AnalysisRunListResponse(
            items=[
                AnalysisRunResponse(run_id="run_old", stock_code="600519", status="completed", detail="旧组合任务"),
                AnalysisRunResponse(run_id="run_active", stock_code="000858", status="failed", detail="当前组合任务"),
            ],
            total=2,
            completed_count=1,
            failed_count=1,
        )

    monkeypatch.setattr(server.run_manager, "list_runs", fake_list_runs)

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            create_user_watchlist(db, user_id="user-alice", name="当前组合", stock_codes=["000858"])

        payload = client.get("/api/v1/ui/runs", headers=_headers("alice")).json()

    assert payload["runs"]["total"] == 1
    assert [item["run_id"] for item in payload["runs"]["items"]] == ["run_active"]
    assert payload["runs"]["completed_count"] == 0
    assert payload["runs"]["failed_count"] == 1
    assert payload["runs"]["workspace"]["tracked_stocks"] == ["000858"]


def test_ui_stock_workbench_is_readonly_for_untracked_stock(monkeypatch):
    monkeypatch.setattr(server, "collect_stock_events", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("UI 股票台不应该实时采集")))
    monkeypatch.setattr(server.run_manager, "list_runs", lambda limit=50, user_id="": AnalysisRunListResponse())
    monkeypatch.setattr(server.run_manager, "list_event_runs", lambda stock_code="", limit=40, user_id="": [])

    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            save_user_events(
                db,
                user_id="user-alice",
                events=[MarketEvent(event_id="old_stock_event", stock_code="600519", title="已移出组合事件", impact_level="high")],
            )
        response = client.get("/api/v1/ui/stocks/600519", headers=_headers("alice"))
        with Session() as db:
            events = server.list_user_events(db, user_id="user-alice").total

    assert response.status_code == 200
    assert response.json()["is_tracked"] is False
    assert response.json()["timeline"]["total"] == 0
    assert response.json()["related_runs"]["total"] == 0
    assert events == 1
