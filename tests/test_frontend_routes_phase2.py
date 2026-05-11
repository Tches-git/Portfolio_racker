from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_frontend_stock_page_contains_analysis_launcher():
    page = (ROOT / 'frontend/src/app/stocks/[stockCode]/page.tsx').read_text(encoding='utf-8')

    assert 'AnalysisLauncher' in page
    assert 'StockNewsPanel' in page
    assert 'fetchStockNews' in page
    assert '浏览器分析' in page or '开始分析' in page


def test_frontend_api_client_contains_run_endpoints():
    api_file = (ROOT / 'frontend/src/lib/api.ts').read_text(encoding='utf-8')

    assert 'createAnalysisRun' in api_file
    assert '/api/v1/runs' in api_file
    assert 'fetchAnalysisRun' in api_file
    assert 'retryAnalysisRun' in api_file
    assert 'cancelAnalysisRun' in api_file
    assert 'assignAnalysisRun' in api_file
    assert 'archiveAnalysisRun' in api_file
    assert 'fetchWorkspaceStocks' in api_file
    assert 'fetchRecentRuns' in api_file
    assert 'createBatchAnalysisRuns' in api_file
    assert 'fetchReportDiff' in api_file
    assert 'fetchStockNews' in api_file
    assert '/api/v1/news' in api_file


def test_frontend_detail_routes_include_deeper_product_states():
    exports_page = (ROOT / 'frontend/src/app/stocks/[stockCode]/exports/page.tsx').read_text(encoding='utf-8')
    history_page = (ROOT / 'frontend/src/app/stocks/[stockCode]/history/page.tsx').read_text(encoding='utf-8')

    assert 'inlineMeta' in exports_page
    assert '交付概览' in exports_page
    assert '关联任务' in exports_page
    assert '设为当前' in exports_page
    assert '导出预览' in exports_page
    assert 'previewMode' in exports_page
    assert 'EXPORT_CATEGORIES' in exports_page
    assert 'mergeArtifacts' in exports_page
    assert 'artifactCategory' in exports_page
    assert 'event_commentary' in exports_page
    assert '事件点评' in exports_page
    assert 'recordTone' in history_page
    assert '变化解释' in history_page
    assert '版本 Diff' in history_page
    assert 'fetchReportDiff' in history_page
    assert '任务联动' in history_page
    assert '设为当前' in history_page
    assert '来源引用' in history_page
