from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sidebar_nav_is_stock_aware_and_not_hardcoded():
    sidebar = (ROOT / 'frontend/src/components/sidebar-nav.tsx').read_text(encoding='utf-8')
    shell = (ROOT / 'frontend/src/components/app-shell.tsx').read_text(encoding='utf-8')

    assert 'stockCodeFromPath' in sidebar
    assert '/stocks/${stockCode}' in sidebar
    assert '当前任务详情' in sidebar
    assert '组合管理' in sidebar
    assert '?tab=timeline' in sidebar
    assert 'SidebarNav' in shell


def test_stock_page_fetches_recent_runs_panel():
    page = (ROOT / 'frontend/src/app/stocks/[stockCode]/page.tsx').read_text(encoding='utf-8')
    workbench = (ROOT / 'frontend/src/components/workbench/stock-workbench.tsx').read_text(encoding='utf-8')

    assert 'fetchStockWorkbench' in page
    assert 'related_runs' in workbench
    assert 'AnalysisLauncher' in workbench
