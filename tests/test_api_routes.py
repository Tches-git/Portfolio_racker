from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.server import app


def test_latest_report_returns_404_for_unknown_stock():
    client = TestClient(app)

    response = client.get('/api/v1/reports/latest/000001')

    assert response.status_code == 404
    assert '未找到股票 000001 的历史分析记录' in response.json()['detail']


def test_stock_history_returns_404_for_unknown_stock():
    client = TestClient(app)

    response = client.get('/api/v1/history/000001')

    assert response.status_code == 404
    assert '未找到股票 000001 的历史分析记录' in response.json()['detail']


def test_export_download_returns_404_for_unknown_file():
    client = TestClient(app)

    response = client.get('/api/v1/exports/report_missing_demo.html')

    assert response.status_code == 404
    assert '未找到导出物' in response.json()['detail']


def test_get_run_returns_404_for_unknown_run():
    client = TestClient(app)

    response = client.get('/api/v1/runs/run_missing')

    assert response.status_code == 404
    assert '未找到运行任务' in response.json()['detail']


def test_retry_run_returns_404_for_unknown_run():
    client = TestClient(app)

    response = client.post('/api/v1/runs/run_missing/retry')

    assert response.status_code == 404
    assert '未找到运行任务' in response.json()['detail']
