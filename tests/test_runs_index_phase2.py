from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runs_index_page_exists_and_uses_recent_runs_api():
    page = (ROOT / 'frontend/src/app/runs/page.tsx').read_text(encoding='utf-8')
    center = (ROOT / 'frontend/src/components/workbench/task-delivery-center.tsx').read_text(encoding='utf-8')

    assert 'fetchRunWorkbench' in page
    assert '多智能体研报任务台' in page
    assert '可信度审计和交付物' in page
    assert '研报任务队列' in center
    assert 'CREATE' in center
    assert 'CURRENT MISSION' in center
    assert 'currentAgentRole' in center
    assert 'RunActionControls' in center
    assert 'BatchRunLauncher' in center
    assert 'run-create-panel' in center
    assert 'runCreatePanelTarget' in center
    assert '批量多股票运行' in (ROOT / 'frontend/src/components/batch-run-launcher.tsx').read_text(encoding='utf-8')
    assert 'data-run-launcher-input' in (ROOT / 'frontend/src/components/batch-run-launcher.tsx').read_text(encoding='utf-8')
    assert 'data.runs.workspace.tracked_stocks' in center
    assert '/runs#run-create-panel' in (ROOT / 'app/api/server.py').read_text(encoding='utf-8')


def test_global_run_center_links_to_runs_index():
    run_center = (ROOT / 'frontend/src/components/global-run-center.tsx').read_text(encoding='utf-8')
    recent_runs = (ROOT / 'frontend/src/components/recent-runs-panel.tsx').read_text(encoding='utf-8')

    assert '查看全部任务' in run_center
    assert 'globalRunStats' in run_center
    assert 'href="/runs"' in recent_runs or "href='/runs'" in recent_runs


def test_homepage_and_workspace_link_to_run_center():
    home = (ROOT / 'frontend/src/app/page.tsx').read_text(encoding='utf-8')
    dashboard = (ROOT / 'frontend/src/components/workbench/dashboard-overview.tsx').read_text(encoding='utf-8')

    assert 'fetchDashboard' in home
    assert 'DashboardOverview' in home
    assert 'SetupWizard' in dashboard
    assert '组合风险' in dashboard
    assert '任务交付' in dashboard
    assert '/runs' in dashboard
