from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_frontend_stock_page_contains_analysis_launcher():
    page = (ROOT / 'frontend/src/app/stocks/[stockCode]/page.tsx').read_text(encoding='utf-8')
    workbench = (ROOT / 'frontend/src/components/workbench/stock-workbench.tsx').read_text(encoding='utf-8')

    assert 'fetchStockWorkbench' in page
    assert 'StockWorkbench' in page
    assert 'AnalysisLauncher' in workbench
    assert '生成研报' in workbench


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
    stock_workbench = (ROOT / 'frontend/src/components/workbench/stock-workbench.tsx').read_text(encoding='utf-8')

    assert 'redirect(`/stocks/${stockCode}?tab=exports`)' in exports_page
    assert 'redirect(`/stocks/${stockCode}?tab=summary`)' in history_page
    assert 'ExportsTab' in stock_workbench
    assert 'BacktestTab' in stock_workbench
    assert '事件影响回测' in stock_workbench
    assert '代表性事件' in stock_workbench
    assert '交付中心' in stock_workbench
    assert 'sameOriginApiUrl' in stock_workbench
    assert 'previewExportUrl' in stock_workbench
    assert '预览' in stock_workbench
    assert '下载' in stock_workbench
