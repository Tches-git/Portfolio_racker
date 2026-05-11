from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_run_detail_page_exists_and_uses_run_api():
    page = (ROOT / 'frontend/src/app/runs/[runId]/page.tsx').read_text(encoding='utf-8')

    assert 'fetchAnalysisRun' in page
    assert 'RunActionControls' in page
    assert '负责人' in page
    assert '阶段事件时间线' in page
    assert '运行任务中心' in page
    assert '任务路径' in page
    assert '返回任务中心' in page
    assert '复用统一导出 contract' in page
    assert 'actions.suggested_next_action' in page
    assert 'observability.retry_lineage' in page
    assert 'observability.recovery_status' in page
    assert 'observability.stale_after_restart' in page
    assert 'detailStatusBar' in page


def test_recent_runs_and_launcher_link_to_run_detail():
    recent_runs = (ROOT / 'frontend/src/components/recent-runs-panel.tsx').read_text(encoding='utf-8')
    launcher = (ROOT / 'frontend/src/components/analysis-launcher.tsx').read_text(encoding='utf-8')

    assert '/runs/${run.run_id}' in recent_runs
    assert '/runs/${run.run_id}' in launcher


def test_history_page_has_master_detail_snapshot_hint():
    history_page = (ROOT / 'frontend/src/app/stocks/[stockCode]/history/page.tsx').read_text(encoding='utf-8')

    assert 'selectedRecord' in history_page
    assert 'searchParams' in history_page
    assert '当前选中记录' in history_page
