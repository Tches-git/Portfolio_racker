from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sidebar_nav_is_stock_aware_and_not_hardcoded():
    sidebar = (ROOT / 'frontend/src/components/sidebar-nav.tsx').read_text(encoding='utf-8')
    shell = (ROOT / 'frontend/src/components/app-shell.tsx').read_text(encoding='utf-8')

    assert 'stockCodeFromPath' in sidebar
    assert '/stocks/${stockCode}' in sidebar
    assert '当前任务详情' in sidebar
    assert '组合跟踪' in sidebar
    assert 'SidebarNav' in shell


def test_stock_page_fetches_recent_runs_panel():
    page = (ROOT / 'frontend/src/app/stocks/[stockCode]/page.tsx').read_text(encoding='utf-8')

    assert 'fetchRecentRuns' in page
    assert 'RecentRunsPanel' in page
