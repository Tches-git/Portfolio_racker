from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_market_workbench_route_and_api_are_wired():
    index_page = (ROOT / "frontend/src/app/markets/page.tsx").read_text(encoding="utf-8")
    page = (ROOT / "frontend/src/app/markets/[stockCode]/page.tsx").read_text(encoding="utf-8")
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")

    assert "fetchWatchlists" in index_page
    assert "safeFetchWatchlists" in index_page
    assert "MarketSearchForm" in index_page
    assert "只读展示" in index_page
    assert "fetchMarketWorkbench" in page
    assert "serverApiOptions" in page
    assert "fallbackMarketData" in page
    assert "行情服务暂时不可用" in page
    assert "行情展示" in page
    assert "/api/v1/ui/markets" in api
    assert "timeoutMs" in api
    assert "MarketWorkbenchResponse" in types
    assert "MarketDailyBar" in types
    assert "MarketQuote" in types


def test_market_workbench_component_contains_svg_chart_and_chinese_states():
    component = (ROOT / "frontend/src/components/workbench/market-workbench.tsx").read_text(encoding="utf-8")

    assert "<svg" in component
    assert "30日" in component
    assert "90日" in component
    assert "180日" in component
    assert "fallback_message" in component
    assert "行情快照" in component
    assert "关键交易指标" in component
    assert "暂无可展示的日线数据" in component


def test_market_workbench_navigation_is_wired():
    app_shell = (ROOT / "frontend/src/components/app-shell.tsx").read_text(encoding="utf-8")
    sidebar = (ROOT / "frontend/src/components/sidebar-nav.tsx").read_text(encoding="utf-8")
    stock_workbench = (ROOT / "frontend/src/components/workbench/stock-workbench.tsx").read_text(encoding="utf-8")

    assert "{ label: '行情', href: '/markets' }" in app_shell
    assert "行情展示" in sidebar
    assert "/(?:stocks|markets)" in sidebar
    assert "/markets/${stockCode}" in sidebar
    assert "/markets/${data.stock_code}" in stock_workbench
    assert "行情" in stock_workbench


def test_market_search_form_validates_and_routes_stock_code():
    form = (ROOT / "frontend/src/components/market-search-form.tsx").read_text(encoding="utf-8")

    assert "请输入 6 位 A 股股票代码" in form
    assert "router.push(`/markets/${normalized}`)" in form
    assert "查看行情" in form
    assert "replace(/\\D/g, '')" in form
