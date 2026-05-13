from __future__ import annotations

from app.auth.rate_limit import _memory_events
from app.config import AUTH_COOKIE_NAME
from tests.helpers import database_client


def test_register_sets_httponly_session_cookie_and_me_reads_login_state():
    _memory_events.clear()
    with database_client() as (client, _Session):
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "first@example.com", "username": "first", "password": "Secret123!"},
        )

        assert response.status_code == 201
        assert response.json()["user"]["role"] == "admin"
        assert AUTH_COOKIE_NAME in response.cookies
        assert "httponly" in response.headers.get("set-cookie", "").lower()

        me = client.get("/api/v1/me")
        assert me.status_code == 200
        assert me.json()["email"] == "first@example.com"

        logout = client.post("/api/v1/auth/logout")
        assert logout.status_code == 200
        assert client.get("/api/v1/me").status_code == 401


def test_login_reuses_session_cookie_and_rejects_wrong_password():
    _memory_events.clear()
    with database_client() as (client, _Session):
        client.post(
            "/api/v1/auth/register",
            json={"email": "alice-login@example.com", "username": "alice-login", "password": "Secret123!"},
        )
        client.post("/api/v1/auth/logout")

        response = client.post(
            "/api/v1/auth/login",
            json={"email_or_username": "alice-login", "password": "Secret123!"},
        )
        assert response.status_code == 200
        assert AUTH_COOKIE_NAME in response.cookies
        assert client.get("/api/v1/me").json()["username"] == "alice-login"

        failed = client.post(
            "/api/v1/auth/login",
            json={"email_or_username": "alice-login", "password": "wrong-password"},
        )
        assert failed.status_code == 401
        assert failed.json()["detail"] == "邮箱/用户名或密码不正确"


def test_register_can_be_disabled(monkeypatch):
    _memory_events.clear()
    monkeypatch.setattr("app.auth.service.ENABLE_SIGNUP", False)

    with database_client() as (client, _Session):
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "closed@example.com", "username": "closed", "password": "Secret123!"},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "当前服务未开放注册"


def test_signup_rate_limit_returns_429(monkeypatch):
    _memory_events.clear()
    monkeypatch.setattr("app.api.server.SIGNUP_RATE_LIMIT_PER_HOUR", 1)

    with database_client() as (client, _Session):
        first = client.post(
            "/api/v1/auth/register",
            json={"email": "rate-limit@example.com", "username": "rate-limit", "password": "Secret123!"},
        )
        second = client.post(
            "/api/v1/auth/register",
            json={"email": "rate-limit@example.com", "username": "rate-limit-2", "password": "Secret123!"},
        )

    assert first.status_code == 201
    assert second.status_code == 429
    assert second.json()["detail"] == "请求过于频繁，请稍后再试"
