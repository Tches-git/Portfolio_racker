from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.server import app
from tests.helpers import authenticated_client


def test_health_endpoint_returns_ok():
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"].startswith("application/json")


def test_export_download_returns_file(monkeypatch, tmp_path):
    export_path = tmp_path / 'report_600519_demo.html'
    export_path.write_text('<html></html>', encoding='utf-8')
    monkeypatch.setattr('app.api.server.get_user_export_artifact', lambda db, user_id, filename: SimpleNamespace(path=str(export_path)))

    with authenticated_client() as (client, _user):
        response = client.get('/api/v1/exports/report_600519_demo.html')

    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/html')
    assert 'attachment; filename="report_600519_demo.html"' in response.headers.get('content-disposition', '')


def test_list_runs_endpoint_returns_items(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.list_run_objects', lambda **kwargs: [])
    monkeypatch.setattr('app.api.server.run_manager.list_runs', lambda limit=10, **kwargs: {
        'items': [{
            'run_id': 'run_recent',
            'stock_code': '600519',
            'status': 'completed',
            'created_at': '',
            'updated_at': '',
            'detail': 'done',
            'last_event': 'run_completed',
            'error': '',
            'latest_report_url': '/api/v1/reports/latest/600519',
            'history_url': '/api/v1/history/600519',
            'exports': [],
            'events': [{'timestamp': '', 'status': 'completed', 'event': 'run_completed', 'detail': 'done'}],
            'run_metrics': {'duration_s': 1.0, 'llm_calls': 1, 'tool_calls': 1, 'total_tokens': 10, 'success': True},
        }],
        'total': 1,
        'queued_count': 0,
        'running_count': 0,
        'completed_count': 1,
        'failed_count': 0,
        'stock_groups': [{'stock_code': '600519', 'total': 1, 'active_count': 0, 'failed_count': 0, 'archived_count': 0, 'latest_run_id': 'run_recent', 'latest_status': 'completed', 'latest_updated_at': ''}],
        'workspace': {'tracked_stocks': ['600519'], 'most_active_stock': '600519', 'latest_completed_stock': '600519', 'failed_stock_count': 0, 'history_backed_stock_count': 1, 'recommended_concurrency': 3, 'active_limit_reached': False, 'observability_status': 'enhanced', 'collaboration_ready': True, 'collaborator_count': 1, 'audited_action_count': 1, 'archived_run_count': 0, 'stale_run_count': 0, 'recovery_status': 'normal', 'worker_count': 2, 'retry_scheduled_count': 0, 'queue_mode': 'worker_queue'}, 
    })

    with authenticated_client() as (client, _user):
        response = client.get('/api/v1/runs?limit=5')

    assert response.status_code == 200
    assert response.json()['items'][0]['run_id'] == 'run_recent'
    assert response.json()['completed_count'] == 1
    assert response.json()['total'] == 1
    assert response.json()['stock_groups'][0]['stock_code'] == '600519'
    assert response.json()['workspace']['most_active_stock'] == '600519'
    assert response.json()['workspace']['collaborator_count'] == 1


def test_stock_news_endpoint_returns_recent_news(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr('app.api.server.get_recent_news', lambda stock_code, count=8: [{'title': '新闻A', 'content': '摘要A', 'time': '2026-01-01', 'source': '东财', 'url': 'http://news', 'channel': 'eastmoney'}])

    response = client.get('/api/v1/news/600519?limit=3')

    assert response.status_code == 200
    assert response.json()['stock_code'] == '600519'
    assert response.json()['total'] == 1
    assert response.json()['items'][0]['title'] == '新闻A'


def test_store_health_backup_and_ops_endpoints(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.store_health', lambda: {'backend': 'sqlite-wal', 'integrity': 'ok', 'schema_version': 3, 'journal_mode': 'wal', 'row_count': 1, 'backup_available': False, 'last_backup_path': ''})
    monkeypatch.setattr('app.api.server.run_manager.ops_metrics', lambda: {'ops_status': 'healthy', 'total_runs': 1, 'active_runs': 0, 'failed_runs': 0, 'failure_rate': 0.0, 'avg_duration_s': 1.0, 'p95_duration_s': 1.0, 'alert_count': 0, 'alerts': [], 'recent_events': []})
    monkeypatch.setattr('app.api.server.run_manager.backup_store', lambda: 'output/api_run_backups/api_runs_demo.db')

    with authenticated_client(role="admin") as (client, _user):
        health = client.get('/api/v1/store/health')
        ops = client.get('/api/v1/ops/metrics')
        backup = client.post('/api/v1/store/backup')

    assert health.status_code == 200
    assert health.json()['integrity'] == 'ok'
    assert ops.status_code == 200
    assert ops.json()['ops_status'] == 'healthy'
    assert backup.status_code == 200
    assert backup.json()['backup_path'].endswith('api_runs_demo.db')


def test_batch_run_endpoint_returns_created_items(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.start_batch', lambda stock_codes, **kwargs: [type('Run', (), {'run_id': f'run_{index}'})() for index, _ in enumerate(stock_codes)])
    monkeypatch.setattr('app.api.server._sync_user_run', lambda db, user, run: None)
    monkeypatch.setattr('app.api.server.run_manager.get_run_response', lambda run_id: {
        'run_id': run_id,
        'stock_code': '600519',
        'status': 'queued',
        'created_at': '',
        'updated_at': '',
        'detail': 'queued',
        'last_event': '',
        'error': '',
        'latest_report_url': '',
        'history_url': '',
        'exports': [],
        'events': [],
        'audit_events': [],
        'run_metrics': {'duration_s': 0.0, 'llm_calls': 0, 'tool_calls': 0, 'total_tokens': 0, 'success': False},
    })

    with authenticated_client() as (client, _user):
        response = client.post('/api/v1/runs/batch', json={'stock_codes': ['600519', '000858']})

    assert response.status_code == 202
    assert response.json()['total'] == 2


def test_create_run_endpoint_returns_accepted(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.start_run', lambda stock_code, **kwargs: type('Run', (), {'run_id': 'run_demo'})())
    monkeypatch.setattr('app.api.server._sync_user_run', lambda db, user, run: None)
    monkeypatch.setattr('app.api.server.run_manager.get_run_response', lambda run_id: {
        'run_id': run_id,
        'stock_code': '600519',
        'status': 'queued',
        'created_at': '',
        'updated_at': '',
        'detail': 'queued',
        'last_event': '',
        'error': '',
        'latest_report_url': '',
        'history_url': '',
        'exports': [],
        'events': [],
        'run_metrics': {'duration_s': 0.0, 'llm_calls': 0, 'tool_calls': 0, 'total_tokens': 0, 'success': False},
    })

    with authenticated_client() as (client, _user):
        response = client.post('/api/v1/runs', json={'stock_code': '600519'})

    assert response.status_code == 202
    assert response.json()['run_id'] == 'run_demo'


def test_retry_run_endpoint_returns_accepted(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.get_run', lambda run_id: SimpleNamespace(run_id=run_id, user_id='user-test'))
    monkeypatch.setattr('app.api.server.run_manager.retry_run', lambda run_id, **kwargs: type('Run', (), {'run_id': 'run_retry'})())
    monkeypatch.setattr('app.api.server._sync_user_run', lambda db, user, run: None)
    monkeypatch.setattr('app.api.server.run_manager.get_run_response', lambda run_id: {
        'run_id': run_id,
        'stock_code': '600519',
        'status': 'queued',
        'created_at': '',
        'updated_at': '',
        'detail': 'retry',
        'last_event': 'run_created',
        'error': '',
        'latest_report_url': '',
        'history_url': '',
        'exports': [],
        'events': [],
        'run_metrics': {'duration_s': 0.0, 'llm_calls': 0, 'tool_calls': 0, 'total_tokens': 0, 'success': False},
    })

    with authenticated_client() as (client, _user):
        response = client.post('/api/v1/runs/run_old/retry')

    assert response.status_code == 202
    assert response.json()['run_id'] == 'run_retry'


def test_cancel_run_endpoint_returns_updated_run(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.get_run', lambda run_id: SimpleNamespace(run_id=run_id, user_id='user-test'))
    monkeypatch.setattr('app.api.server.run_manager.cancel_run', lambda run_id, **kwargs: type('Run', (), {'run_id': run_id})())
    monkeypatch.setattr('app.api.server._sync_user_run', lambda db, user, run: None)
    monkeypatch.setattr('app.api.server.run_manager.get_run_response', lambda run_id: {
        'run_id': run_id,
        'stock_code': '600519',
        'status': 'failed',
        'created_at': '',
        'updated_at': '',
        'detail': '任务已取消',
        'last_event': 'run_canceled',
        'error': '任务已取消',
        'owner': '',
        'archived': False,
        'retry_of_run_id': '',
        'latest_report_url': '',
        'history_url': '',
        'exports': [],
        'events': [],
        'run_metrics': {'duration_s': 0.0, 'llm_calls': 0, 'tool_calls': 0, 'total_tokens': 0, 'success': False},
    })

    with authenticated_client() as (client, _user):
        response = client.post('/api/v1/runs/run_live/cancel')

    assert response.status_code == 200
    assert response.json()['last_event'] == 'run_canceled'


def test_assign_and_archive_run_endpoints(monkeypatch):
    monkeypatch.setattr('app.api.server.run_manager.get_run', lambda run_id: SimpleNamespace(run_id=run_id, user_id='user-test'))
    monkeypatch.setattr('app.api.server.run_manager.assign_owner', lambda run_id, owner, **kwargs: type('Run', (), {'run_id': run_id})())
    monkeypatch.setattr('app.api.server.run_manager.archive_run', lambda run_id, **kwargs: type('Run', (), {'run_id': run_id})())
    monkeypatch.setattr('app.api.server._sync_user_run', lambda db, user, run: None)
    monkeypatch.setattr('app.api.server.run_manager.get_run_response', lambda run_id: {
        'run_id': run_id,
        'stock_code': '600519',
        'status': 'completed',
        'created_at': '',
        'updated_at': '',
        'detail': 'done',
        'last_event': 'run_archived',
        'error': '',
        'owner': 'alice',
        'owner_role': 'analyst',
        'archived': True,
        'retry_of_run_id': '',
        'latest_report_url': '',
        'history_url': '',
        'exports': [],
        'events': [],
        'run_metrics': {'duration_s': 0.0, 'llm_calls': 0, 'tool_calls': 0, 'total_tokens': 0, 'success': True},
    })

    with authenticated_client(username="alice") as (client, _user):
        assign_response = client.post('/api/v1/runs/run_demo/assign', json={'owner': 'alice'})
        archive_response = client.post('/api/v1/runs/run_demo/archive')

    assert assign_response.status_code == 200
    assert assign_response.json()['owner'] == 'alice'
    assert archive_response.status_code == 200
    assert archive_response.json()['archived'] is True
