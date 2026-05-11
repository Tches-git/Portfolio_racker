from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runs_index_page_exists_and_uses_recent_runs_api():
    page = (ROOT / 'frontend/src/app/runs/page.tsx').read_text(encoding='utf-8')

    assert 'fetchRecentRuns' in page
    assert '全局任务中心' in page
    assert '运行队列' in page
    assert '按股票聚合' in page
    assert '已归档' in page
    assert '推荐并发' in page
    assert '运行分布' in page
    assert 'selectionHint' in page
    assert '时间线' in page
    assert 'actions.suggested_next_action' in page
    assert 'observability.event_count' in page
    assert 'BatchRunLauncher' in page
    assert '批量多股票运行' in (ROOT / 'frontend/src/components/batch-run-launcher.tsx').read_text(encoding='utf-8')
    assert 'filterBar' in page
    assert 'masterDetailPreview' in page
    assert 'recovery_status' in page


def test_global_run_center_links_to_runs_index():
    run_center = (ROOT / 'frontend/src/components/global-run-center.tsx').read_text(encoding='utf-8')
    recent_runs = (ROOT / 'frontend/src/components/recent-runs-panel.tsx').read_text(encoding='utf-8')

    assert '查看全部任务' in run_center
    assert 'globalRunStats' in run_center
    assert 'href="/runs"' in recent_runs or "href='/runs'" in recent_runs


def test_homepage_and_workspace_link_to_run_center():
    home = (ROOT / 'frontend/src/app/page.tsx').read_text(encoding='utf-8')
    insights = (ROOT / 'frontend/src/components/workspace-insights.tsx').read_text(encoding='utf-8')

    assert 'RecentRunsPanel' in home
    assert 'fetchWorkspaceStocks' in home
    assert 'StockCardGrid' in home
    assert 'QuickActions' in home
    assert '组合工作区' in insights
    assert '任务中心' in insights
