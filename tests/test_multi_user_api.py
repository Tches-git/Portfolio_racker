from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

import app.api.server as server
from app.api.server import app
from app.db.models import ExportArtifactRecord
from app.db.repositories import create_user_watchlist, save_user_events
from app.tracking.models import EventCollection, MarketEvent
from tests.helpers import multi_user_client


def _headers(username: str) -> dict[str, str]:
    return {"X-Test-User": username}


def test_expanded_business_api_surface_requires_login():
    client = TestClient(app)

    requests = [
        ("get", "/api/v1/watchlists", None),
        ("post", "/api/v1/watchlists", {"name": "组合", "stock_codes": ["600519"]}),
        ("get", "/api/v1/events?mode=history", None),
        ("get", "/api/v1/events/event_missing", None),
        ("patch", "/api/v1/events/event_missing/status", {"status": "reviewed"}),
        ("post", "/api/v1/events/event_missing/analyze", {"note": "跟进"}),
        ("get", "/api/v1/alerts?mode=history", None),
        ("get", "/api/v1/briefing/daily", None),
        ("get", "/api/v1/runs", None),
        ("post", "/api/v1/runs", {"stock_code": "600519"}),
        ("get", "/api/v1/exports/report_missing.md", None),
        ("get", "/api/v1/reports/latest/600519", None),
        ("get", "/api/v1/history/600519", None),
        ("get", "/api/v1/reports/diff/600519", None),
        ("get", "/api/v1/workspace/stocks", None),
        ("get", "/api/v1/store/health", None),
        ("get", "/api/v1/ops/metrics", None),
        ("post", "/api/v1/store/backup", None),
    ]

    for method, url, body in requests:
        response = getattr(client, method)(url, json=body) if body is not None else getattr(client, method)(url)
        assert response.status_code == 401, url
        assert response.json()["detail"] == "请先登录"

    assert client.get("/api/v1/alerts/rules").status_code == 200


def test_watchlist_api_isolated_between_users():
    with multi_user_client() as (client, _users, _Session):
        alice_created = client.post(
            "/api/v1/watchlists",
            headers=_headers("alice"),
            json={"name": "Alice 组合", "stock_codes": ["600519"], "description": "A"},
        )
        bob_created = client.post(
            "/api/v1/watchlists",
            headers=_headers("bob"),
            json={"name": "Bob 组合", "stock_codes": ["000858"], "description": "B"},
        )

        assert alice_created.status_code == 201
        assert bob_created.status_code == 201

        alice_list = client.get("/api/v1/watchlists", headers=_headers("alice")).json()
        bob_list = client.get("/api/v1/watchlists", headers=_headers("bob")).json()

        assert alice_list["total"] == 1
        assert alice_list["items"][0]["name"] == "Alice 组合"
        assert alice_list["items"][0]["stock_codes"] == ["600519"]
        assert bob_list["total"] == 1
        assert bob_list["items"][0]["name"] == "Bob 组合"
        assert bob_list["items"][0]["stock_codes"] == ["000858"]

        bob_watchlist_id = bob_created.json()["watchlist_id"]
        denied = client.get(f"/api/v1/watchlists/{bob_watchlist_id}", headers=_headers("alice"))
        assert denied.status_code == 404


def test_new_user_workspace_starts_empty_and_does_not_collect_default_stocks(monkeypatch):
    def fail_collect(*args, **kwargs):
        raise AssertionError("空用户不应该隐式采集默认股票池")

    monkeypatch.setattr(server, "collect_market_events", fail_collect)

    with multi_user_client() as (client, _users, _Session):
        watchlists = client.get("/api/v1/watchlists", headers=_headers("alice")).json()
        events = client.get("/api/v1/events", headers=_headers("alice")).json()
        alerts = client.get("/api/v1/alerts", headers=_headers("alice")).json()
        briefing = client.get("/api/v1/briefing/daily", headers=_headers("alice")).json()
        workspace = client.get("/api/v1/workspace/stocks", headers=_headers("alice")).json()

    assert watchlists == {"items": [], "total": 0}
    assert events["total"] == 0
    assert events["items"] == []
    assert alerts["total"] == 0
    assert alerts["items"] == []
    assert briefing["total_events"] == 0
    assert briefing["key_events"] == []
    assert workspace["items"] == []


def test_event_history_and_status_are_isolated_between_users():
    with multi_user_client() as (client, users, Session):
        with Session() as db:
            create_user_watchlist(db, user_id=users["alice"].id, name="Alice 组合", stock_codes=["600519"])
            create_user_watchlist(db, user_id=users["bob"].id, name="Bob 组合", stock_codes=["000858"])
            save_user_events(
                db,
                user_id=users["alice"].id,
                events=[MarketEvent(event_id="event_alice", stock_code="600519", title="Alice 高影响公告", impact_level="high")],
            )
            save_user_events(
                db,
                user_id=users["bob"].id,
                events=[MarketEvent(event_id="event_bob", stock_code="000858", title="Bob 行业新闻", impact_level="medium")],
            )

        alice_events = client.get("/api/v1/events?mode=history", headers=_headers("alice")).json()
        bob_events = client.get("/api/v1/events?mode=history", headers=_headers("bob")).json()

        assert alice_events["total"] == 1
        assert alice_events["items"][0]["event_id"] == "event_alice"
        assert bob_events["total"] == 1
        assert bob_events["items"][0]["event_id"] == "event_bob"

        assert client.get("/api/v1/events/event_alice", headers=_headers("bob")).status_code == 404
        reviewed = client.patch(
            "/api/v1/events/event_alice/status",
            headers=_headers("alice"),
            json={"status": "reviewed", "note": "已看过"},
        )
        assert reviewed.status_code == 200
        assert reviewed.json()["status"] == "reviewed"

        denied = client.patch(
            "/api/v1/events/event_alice/status",
            headers=_headers("bob"),
            json={"status": "ignored"},
        )
        assert denied.status_code == 404


def test_untracked_stock_page_does_not_persist_realtime_events(monkeypatch):
    collection = EventCollection(
        items=[MarketEvent(event_id="stock_page_event", stock_code="600519", title="实时事件")],
        total=1,
        high_impact_count=0,
        placeholder_count=0,
        duplicate_count=0,
        source_count=1,
    )
    monkeypatch.setattr(server, "collect_stock_events", lambda stock_code, limit=6, include_history=False: collection)

    with multi_user_client() as (client, _users, _Session):
        realtime = client.get("/api/v1/stocks/600519/events", headers=_headers("alice")).json()
        history = client.get("/api/v1/events?mode=history", headers=_headers("alice")).json()

        assert realtime["total"] == 1
        assert history["items"] == []

        client.post(
            "/api/v1/watchlists",
            headers=_headers("alice"),
            json={"name": "Alice 组合", "stock_codes": ["600519"]},
        )
        client.get("/api/v1/stocks/600519/events", headers=_headers("alice"))
        tracked_history = client.get("/api/v1/events?mode=history", headers=_headers("alice")).json()

    assert tracked_history["total"] == 1
    assert tracked_history["items"][0]["event_id"] == "stock_page_event"


def test_run_detail_is_hidden_from_other_users(monkeypatch):
    with multi_user_client() as (client, users, _Session):
        alice_run = SimpleNamespace(run_id="run_alice", user_id=users["alice"].id)
        monkeypatch.setattr(server.run_manager, "get_run", lambda run_id: alice_run)
        monkeypatch.setattr(server, "_sync_user_run", lambda db, user, run: None)
        monkeypatch.setattr(
            server.run_manager,
            "get_run_response",
            lambda run_id: {
                "run_id": run_id,
                "stock_code": "600519",
                "status": "completed",
                "created_at": "",
                "updated_at": "",
                "detail": "done",
                "last_event": "run_completed",
                "error": "",
                "latest_report_url": "/api/v1/reports/latest/600519",
                "history_url": "/api/v1/history/600519",
                "exports": [],
                "events": [],
                "audit_events": [],
                "run_metrics": {"duration_s": 1.0, "llm_calls": 0, "tool_calls": 0, "total_tokens": 0, "success": True},
            },
        )

        assert client.get("/api/v1/runs/run_alice", headers=_headers("alice")).status_code == 200
        denied = client.get("/api/v1/runs/run_alice", headers=_headers("bob"))
        assert denied.status_code == 404
        assert denied.json()["detail"] == "未找到运行任务: run_alice"


def test_export_download_uses_current_user_artifact(tmp_path):
    export_path = tmp_path / "alice_report.md"
    export_path.write_text("# Alice report\n", encoding="utf-8")

    with multi_user_client() as (client, users, Session):
        with Session() as db:
            db.add(
                ExportArtifactRecord(
                    user_id=users["alice"].id,
                    run_id="run_alice",
                    stock_code="600519",
                    kind="markdown",
                    filename=export_path.name,
                    path=str(export_path),
                    download_url=f"/api/v1/exports/{export_path.name}",
                )
            )
            db.commit()

        alice_response = client.get(f"/api/v1/exports/{export_path.name}", headers=_headers("alice"))
        bob_response = client.get(f"/api/v1/exports/{export_path.name}", headers=_headers("bob"))

        assert alice_response.status_code == 200
        assert alice_response.text == "# Alice report\n"
        assert bob_response.status_code == 404


def test_admin_ops_endpoints_reject_normal_users(monkeypatch):
    monkeypatch.setattr(
        server.run_manager,
        "store_health",
        lambda: {"backend": "sqlite-wal", "integrity": "ok", "schema_version": 6, "journal_mode": "wal", "row_count": 0, "backup_available": False, "last_backup_path": ""},
    )
    monkeypatch.setattr(
        server.run_manager,
        "ops_metrics",
        lambda: {"ops_status": "healthy", "total_runs": 0, "active_runs": 0, "failed_runs": 0, "failure_rate": 0.0, "avg_duration_s": 0.0, "p95_duration_s": 0.0, "alert_count": 0, "alerts": [], "recent_events": []},
    )
    monkeypatch.setattr(server.run_manager, "backup_store", lambda: "output/api_run_backups/api_runs_demo.db")

    with multi_user_client() as (client, _users, _Session):
        assert client.get("/api/v1/store/health", headers=_headers("alice")).status_code == 403
        assert client.get("/api/v1/ops/metrics", headers=_headers("alice")).status_code == 403
        assert client.post("/api/v1/store/backup", headers=_headers("alice")).status_code == 403

        assert client.get("/api/v1/store/health", headers=_headers("admin")).status_code == 200
        assert client.get("/api/v1/ops/metrics", headers=_headers("admin")).status_code == 200
        assert client.post("/api/v1/store/backup", headers=_headers("admin")).status_code == 200
