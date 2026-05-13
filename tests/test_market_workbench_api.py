from __future__ import annotations

import time

import app.api.server as server
from tests.helpers import database_client, multi_user_client


def _headers(username: str) -> dict[str, str]:
    return {"X-Test-User": username}


def _bars(count: int) -> list[dict]:
    return [
        {
            "date": f"2026-03-{index + 1:02d}",
            "open": 100 + index,
            "high": 102 + index,
            "low": 99 + index,
            "close": 101 + index,
            "volume": 10000 + index,
            "amount": 2000000 + index,
            "change_pct": 1.2,
            "turnover": 0.8,
        }
        for index in range(count)
    ]


def test_market_workbench_requires_login():
    with database_client() as (client, _Session):
        response = client.get("/api/v1/ui/markets/600519")

    assert response.status_code == 401
    assert response.json()["detail"] == "请先登录"


def test_market_workbench_returns_quote_and_limited_bars(monkeypatch):
    monkeypatch.setattr(
        server,
        "fetch_live_quotes",
        lambda stock_code: {
            "title": "贵州茅台 实时行情快照",
            "time": "2026-05-12T10:00:00",
            "provider": "akshare",
            "price": 1500.5,
            "pe_ratio": 28.2,
            "pb_ratio": 8.1,
            "market_cap": 1880000000000,
            "stock_code": stock_code,
        },
    )
    monkeypatch.setattr(server, "get_stock_daily_bars", lambda stock_code, days=90: _bars(days + 8))

    with multi_user_client() as (client, _users, _Session):
        response = client.get("/api/v1/ui/markets/600519?range=30d", headers=_headers("alice"))

    payload = response.json()
    assert response.status_code == 200
    assert payload["range"] == "30d"
    assert payload["stock_name"] == "贵州茅台"
    assert payload["quote"]["price"] == 1500.5
    assert payload["quote"]["source_status"] == "ok"
    assert len(payload["daily_bars"]) == 30
    assert payload["actions"][0]["href"] == "/stocks/600519"


def test_market_workbench_degrades_when_data_source_fails(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("source down")

    monkeypatch.setattr(server, "fetch_live_quotes", fail)
    monkeypatch.setattr(server, "get_stock_daily_bars", fail)

    with multi_user_client() as (client, _users, _Session):
        response = client.get("/api/v1/ui/markets/600519", headers=_headers("alice"))

    payload = response.json()
    assert response.status_code == 200
    assert payload["daily_bars"] == []
    assert payload["quote"]["source_status"] == "degraded"
    assert "暂不可用" in payload["fallback_message"]


def test_market_workbench_rejects_invalid_stock_code():
    with multi_user_client() as (client, _users, _Session):
        response = client.get("/api/v1/ui/markets/ABC", headers=_headers("alice"))

    assert response.status_code == 422
    assert response.json()["detail"] == "请输入 6 位 A 股股票代码"


def test_market_data_call_timeout_degrades_quickly():
    started = time.monotonic()
    result, message = server._safe_market_call("日线", lambda: time.sleep(0.2), timeout=0.01)

    assert result is None
    assert "响应超时" in message
    assert time.monotonic() - started < 0.1
