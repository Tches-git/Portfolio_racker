from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_layout_includes_global_run_center():
    layout = (ROOT / 'frontend/src/app/layout.tsx').read_text(encoding='utf-8')
    run_center = (ROOT / 'frontend/src/components/global-run-center.tsx').read_text(encoding='utf-8')

    assert 'GlobalRunCenter' in layout
    assert '全局运行中心' in run_center
    assert 'fetchRecentRuns' in run_center
    assert 'globalRunStats' in run_center


def test_homepage_includes_rebuilt_command_center():
    home = (ROOT / 'frontend/src/app/page.tsx').read_text(encoding='utf-8')
    dashboard = (ROOT / 'frontend/src/components/workbench/dashboard-overview.tsx').read_text(encoding='utf-8')
    setup = (ROOT / 'frontend/src/components/workbench/setup-wizard.tsx').read_text(encoding='utf-8')

    assert 'DashboardOverview' in home
    assert 'fetchDashboard' in home
    assert '组合风险驾驶舱' in home
    assert '创建第一个组合' in setup
    assert '最新关键事件' in dashboard
    assert '今日主题' in dashboard
    assert '新工作区' in setup


def test_exports_page_has_master_detail_snapshot():
    exports_page = (ROOT / 'frontend/src/app/stocks/[stockCode]/exports/page.tsx').read_text(encoding='utf-8')
    stock_workbench = (ROOT / 'frontend/src/components/workbench/stock-workbench.tsx').read_text(encoding='utf-8')

    assert 'redirect(`/stocks/${stockCode}?tab=exports`)' in exports_page
    assert 'ExportsTab' in stock_workbench
    assert '导出物' in stock_workbench
