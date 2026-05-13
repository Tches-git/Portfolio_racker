from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_frontend_api_client_carries_credentials_and_auth_contract():
    api = read("frontend/src/lib/api.ts")
    types = read("frontend/src/lib/types.ts")

    assert "apiFetch" in api
    assert "credentials: init.credentials ?? 'include'" in api
    assert "/api/v1/auth/login" in api
    assert "/api/v1/auth/register" in api
    assert "/api/v1/auth/logout" in api
    assert "/api/v1/me" in api
    assert "fetchCurrentUser" in api
    assert "sameOriginApiUrl" in api
    assert "AuthUser" in types
    assert "AuthLoginRequest" in types
    assert "AuthRegisterRequest" in types


def test_login_register_pages_and_user_menu_are_wired():
    login_page = read("frontend/src/app/login/page.tsx")
    register_page = read("frontend/src/app/register/page.tsx")
    auth_forms = read("frontend/src/components/auth-forms.tsx")
    user_menu = read("frontend/src/components/user-menu.tsx")
    shell = read("frontend/src/components/app-shell.tsx")

    assert "LoginForm" in login_page
    assert "RegisterForm" in register_page
    assert "login({" in auth_forms
    assert "register({" in auth_forms
    assert "登录研究中枢" in auth_forms
    assert "创建研究账号" in auth_forms
    assert "logout()" in user_menu
    assert "退出登录" in user_menu
    assert "user: AuthUser | null" in shell
    assert "UserMenu" in shell
    assert "多用户工作区" in shell


def test_frontend_middleware_and_server_cookie_forwarding_are_wired():
    middleware = read("frontend/src/middleware.ts")
    server_auth = read("frontend/src/lib/server-auth.ts")
    layout = read("frontend/src/app/layout.tsx")
    home_page = read("frontend/src/app/page.tsx")

    assert "portfolio_session" in middleware
    assert "/login" in middleware
    assert "/register" in middleware
    assert "pathname.startsWith('/api/v1')" in middleware
    assert "pathname.startsWith('/_next')" in middleware
    assert "getCurrentUserFromServer" in server_auth
    assert "serverApiOptions" in server_auth
    assert "cookieStore.toString()" in server_auth
    assert "getCurrentUserFromServer" in layout
    assert "user={user}" in layout
    assert "serverApiOptions" in home_page


def test_download_links_use_same_origin_api_paths():
    run_page = read("frontend/src/app/runs/[runId]/page.tsx")
    stock_workbench = read("frontend/src/components/workbench/stock-workbench.tsx")
    dashboard = read("frontend/src/components/report-dashboard.tsx")

    assert "sameOriginApiUrl" in run_page
    assert "sameOriginApiUrl" in stock_workbench
    assert "sameOriginApiUrl" in dashboard
    assert "${API_BASE}" not in run_page
    assert "${API_BASE}" not in stock_workbench
    assert "${API_BASE}" not in dashboard
