from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app
from app.tracking.models import Watchlist


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
