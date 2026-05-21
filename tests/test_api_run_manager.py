from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import time

import pytest

from app.api.mappers import build_run_response
from app.api.run_manager import AnalysisRun, AnalysisRunManager, RunNotFoundError


class FlakyEngine:
    calls = 0

    def __init__(self, on_step=None):
        self.on_step = on_step

    def run(self, stock_code: str, *, uploaded_items=None, event_context=None):
        FlakyEngine.calls += 1
        if FlakyEngine.calls == 1:
            raise RuntimeError('temporary failure')
        return SimpleNamespace(
            final_report='# report',
            stock_code=stock_code,
            run_metrics={'duration_s': 1.0, 'llm_calls': 1, 'tool_calls': 1, 'total_tokens': 10, 'success': True},
            sections={'report_export': f'report_{stock_code}_retry.md'},
        )


class DummyEngine:
    calls = 0
    last_event_context = None

    def __init__(self, on_step=None):
        self.on_step = on_step

    def run(self, stock_code: str, *, uploaded_items=None, event_context=None):
        DummyEngine.calls += 1
        DummyEngine.last_event_context = dict(event_context or {})
        state = SimpleNamespace(
            final_report='# report',
            stock_code=stock_code,
            run_metrics={'duration_s': 1.2, 'llm_calls': 2, 'tool_calls': 3, 'total_tokens': 42, 'success': True},
            sections={
                'report_export': f'report_{stock_code}_demo.md',
                'trace_export': f'trace_{stock_code}_demo.log',
                'report_html_export': f'report_{stock_code}_demo.html',
                'source_refs_export': f'sources_{stock_code}_demo.json',
                'rating': '推荐',
                'rating_detail': '事件影响可控',
            },
        )
        if self.on_step:
            self.on_step('planning', '正在规划分析任务', state)
        return state


class TraceEngine:
    def __init__(self, on_step=None):
        self.on_step = on_step

    def run(self, stock_code: str, *, uploaded_items=None, event_context=None):
        state = SimpleNamespace(
            final_report='# report',
            stock_code=stock_code,
            run_metrics={'duration_s': 1.0, 'llm_calls': 1, 'tool_calls': 2, 'total_tokens': 20, 'success': True},
            run_payload={
                'multi_agent_trace': {
                    'mode': 'autogen_graphflow',
                    'role_count': 7,
                    'completed_role_count': 6,
                    'failed_role_count': 0,
                    'roles': [{'role_id': 'planner', 'role_name': 'PlannerAgent', 'status': 'completed'}],
                }
            },
            sections={'report_export': f'report_{stock_code}_trace.md'},
            source_refs=[],
        )
        if self.on_step:
            self.on_step('research_done', '多智能体研究完成: 6 个角色', state)
        return state


def test_build_run_response_maps_metrics_and_exports():
    run = AnalysisRun(run_id='run_demo', stock_code='600519', status='completed')
    run.detail = 'done'
    run.exports = [{'kind': 'markdown', 'filename': 'report_600519_demo.md', 'path': 'output/report_600519_demo.md', 'download_url': '/api/v1/exports/report_600519_demo.md'}]
    run.events = [{'timestamp': '2026-05-07T11:00:00', 'status': 'completed', 'event': 'run_completed', 'detail': 'done'}]
    run.event_context = {'event_id': 'e1', 'title': '重大公告', 'impact_level': 'high'}
    run.event_report_summary = {'trigger_label': '重大公告', 'priority': 'P0 高优先级', 'event_commentary_url': '/api/v1/exports/event_commentary.md'}
    run.multi_agent_trace = {'mode': 'autogen_graphflow', 'role_count': 6, 'completed_role_count': 6, 'failed_role_count': 0, 'roles': []}
    run.state = SimpleNamespace(run_metrics={'duration_s': 1.5, 'llm_calls': 2, 'tool_calls': 4, 'total_tokens': 88, 'success': True})

    payload = build_run_response(run)

    assert payload.run_id == 'run_demo'
    assert payload.status == 'completed'
    assert payload.exports[0].filename == 'report_600519_demo.md'
    assert payload.events[0].event == 'run_completed'
    assert payload.run_metrics.total_tokens == 88
    assert payload.event_context.event_id == 'e1'
    assert payload.event_context.title == '重大公告'
    assert payload.event_report_summary.trigger_label == '重大公告'
    assert payload.event_report_summary.event_commentary_url.endswith('event_commentary.md')
    assert payload.multi_agent_trace.role_count == 6
    assert payload.actions.product_route == '/stocks/600519'
    assert payload.actions.suggested_next_action == '查看导出物'
    assert payload.observability.event_count == 1
    assert payload.observability.artifact_count == 1
    assert payload.observability.recovery_status == 'normal'
    assert payload.observability.stale_after_restart is False
    assert payload.observability.max_attempts == 2
    assert payload.audit_events == []


def test_run_manager_raises_for_missing_run(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)

    with pytest.raises(RunNotFoundError):
        manager.get_run('missing')


def test_run_manager_starts_batch_runs(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)

    runs = manager.start_batch(['600519', '000858', '600519', ''], actor='lead', role='admin')

    assert len(runs) == 2
    assert {item.stock_code for item in runs} == {'600519', '000858'}
    assert all(item.audit_events[0]['actor'] == 'lead' for item in runs)


def test_run_manager_executes_run_and_persists_completion(monkeypatch, tmp_path):
    DummyEngine.calls = 0
    DummyEngine.last_event_context = None
    manager = AnalysisRunManager(output_dir=tmp_path)
    monkeypatch.setattr('app.api.run_manager.ReportEngine', DummyEngine)
    monkeypatch.setattr('app.api.run_manager.save_output_files', lambda state, timestamp=None: (tmp_path / 'report.md', tmp_path / 'trace.log'))

    run = manager.start_run('600519')
    for _ in range(50):
        current = manager.get_run(run.run_id)
        if current.status in {'completed', 'failed'}:
            break
        time.sleep(0.02)
    else:
        raise AssertionError('run did not finish in time')

    current = manager.get_run(run.run_id)
    assert current.status == 'completed'
    assert current.latest_report_url == '/api/v1/reports/latest/600519'
    assert any(item['kind'] == 'markdown' for item in current.exports)
    assert current.attempts == 1
    assert current.worker_id == ''


def test_run_manager_persists_partial_multi_agent_trace(monkeypatch, tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)
    monkeypatch.setattr('app.api.run_manager.ReportEngine', TraceEngine)
    monkeypatch.setattr('app.api.run_manager.save_output_files', lambda state, root=None, timestamp=None: None)

    run = manager.start_run('600519')
    manager.execute_queued_once(worker_id='worker-test')
    reloaded = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)
    current = reloaded.get_run(run.run_id)

    assert current.status == 'completed'
    assert current.multi_agent_trace['role_count'] == 7
    assert current.multi_agent_trace['roles'][0]['role_id'] == 'planner'


def test_run_manager_executes_event_run_with_context(monkeypatch, tmp_path):
    DummyEngine.calls = 0
    DummyEngine.last_event_context = None
    manager = AnalysisRunManager(output_dir=tmp_path)
    monkeypatch.setattr('app.api.run_manager.ReportEngine', DummyEngine)
    monkeypatch.setattr('app.api.run_manager.save_output_files', lambda state, timestamp=None: (tmp_path / 'report.md', tmp_path / 'trace.log'))

    run = manager.start_event_run('600519', event_context={'event_id': 'e4', 'title': '重大公告', 'impact_level': 'high'})
    for _ in range(50):
        current = manager.get_run(run.run_id)
        if current.status in {'completed', 'failed'}:
            break
        time.sleep(0.02)
    else:
        raise AssertionError('event run did not finish in time')

    assert current.status == 'completed'
    assert current.event_context['event_id'] == 'e4'
    assert DummyEngine.last_event_context['event_id'] == 'e4'
    assert current.event_report_summary['trigger_label'] == '重大公告'
    assert current.event_report_summary['event_commentary_url'].startswith('/api/v1/exports/event_commentary_')
    assert any(item['kind'] == 'event_commentary' for item in current.exports)
    assert (tmp_path / current.event_report_summary['event_commentary_filename']).exists()
    assert build_run_response(current).event_context.impact_level == 'high'
    assert build_run_response(current).event_report_summary.priority == 'P0 高优先级'


def test_run_manager_requeues_transient_failures(monkeypatch, tmp_path):
    FlakyEngine.calls = 0
    manager = AnalysisRunManager(output_dir=tmp_path)
    monkeypatch.setattr('app.api.run_manager.ReportEngine', FlakyEngine)
    monkeypatch.setattr('app.api.run_manager.save_output_files', lambda state, timestamp=None: (tmp_path / 'report.md', tmp_path / 'trace.log'))

    run = manager.start_run('600519')
    for _ in range(80):
        current = manager.get_run(run.run_id)
        if current.status == 'completed':
            break
        time.sleep(0.02)
    else:
        raise AssertionError('retrying run did not finish in time')

    assert current.status == 'completed'
    assert current.attempts == 2
    assert any(item['event'] == 'run_retry_scheduled' for item in current.events)


def test_run_manager_claims_priority_runs_without_worker_thread(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)
    low = AnalysisRun(run_id='run_low', stock_code='600519', priority=0, created_at='2026-05-07T10:00:00')
    high = AnalysisRun(run_id='run_high', stock_code='000858', priority=5, created_at='2026-05-07T11:00:00')
    manager._runs[low.run_id] = low
    manager._runs[high.run_id] = high

    claimed = manager._claim_next_run('worker-test')

    assert claimed.run_id == 'run_high'
    assert claimed.status == 'running'
    assert claimed.worker_id == 'worker-test'
    assert claimed.attempts == 1


def test_run_manager_lists_recent_runs(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_1'] = AnalysisRun(run_id='run_1', stock_code='600519', status='failed', updated_at='2026-05-07T10:00:00')
    manager._runs['run_2'] = AnalysisRun(run_id='run_2', stock_code='000858', status='running', updated_at='2026-05-07T11:00:00')
    manager._save_runs()

    payload = manager.list_runs(limit=1)

    assert len(payload.items) == 1
    assert payload.items[0].run_id == 'run_2'
    assert payload.total == 2
    assert payload.running_count == 1
    assert payload.failed_count == 1
    assert payload.stock_groups[0].stock_code == '000858'
    assert payload.workspace.failed_stock_count == 1
    assert payload.workspace.recommended_concurrency == 3
    assert payload.workspace.observability_status == 'enhanced'
    assert payload.workspace.stale_run_count == 0
    assert payload.workspace.recovery_status == 'normal'
    assert payload.workspace.queue_mode == 'worker_queue'
    assert payload.workspace.worker_count == 2


def test_run_manager_marks_loaded_active_runs_as_interrupted(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_live'] = AnalysisRun(run_id='run_live', stock_code='600519', status='running', updated_at='2026-05-07T11:00:00')
    manager._save_runs()

    reloaded = AnalysisRunManager(output_dir=tmp_path)
    recovered = reloaded.get_run('run_live')
    payload = reloaded.list_runs()

    assert recovered.status == 'failed'
    assert recovered.stale_after_restart is True
    assert recovered.recovery_status == 'interrupted_after_restart'
    assert recovered.last_event == 'run_interrupted_after_restart'
    assert payload.workspace.stale_run_count == 1
    assert payload.workspace.recovery_status == 'needs_attention'


def test_run_manager_supports_retry_and_cancel(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_fail'] = AnalysisRun(run_id='run_fail', stock_code='600519', status='failed', updated_at='2026-05-07T10:00:00')
    manager._runs['run_live'] = AnalysisRun(run_id='run_live', stock_code='000858', status='running', updated_at='2026-05-07T11:00:00')
    manager._save_runs()

    retried = manager.retry_run('run_fail')
    canceled = manager.cancel_run('run_live')

    assert retried.stock_code == '600519'
    assert retried.retry_of_run_id == 'run_fail'
    assert canceled.last_event == 'run_canceled'


def test_run_manager_supports_assignment_and_archive(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_done'] = AnalysisRun(run_id='run_done', stock_code='600519', status='completed', updated_at='2026-05-07T11:00:00')
    manager._save_runs()

    assigned = manager.assign_owner('run_done', 'alice')
    archived = manager.archive_run('run_done')

    assert assigned.owner == 'alice'
    assert archived.archived is True
    assert archived.audit_events[-1]['action'] == 'archive_run'


def test_run_manager_enforces_roles_for_archiving(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_done'] = AnalysisRun(run_id='run_done', stock_code='600519', status='completed')

    with pytest.raises(Exception):
        manager.archive_run('run_done', actor='bob', role='analyst')


def test_run_manager_tracks_collaboration_summary(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_done'] = AnalysisRun(run_id='run_done', stock_code='600519', status='completed')
    manager.assign_owner('run_done', 'alice', actor='lead', role='admin', owner_role='analyst')

    payload = manager.list_runs()

    assert payload.items[0].owner == 'alice'
    assert payload.items[0].owner_role == 'analyst'
    assert payload.items[0].audit_events[-1].actor == 'lead'
    assert payload.workspace.collaborator_count == 1
    assert payload.workspace.audited_action_count == 1


def test_run_manager_reports_ops_metrics(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)
    manager._runs['run_failed'] = AnalysisRun(run_id='run_failed', stock_code='600519', status='failed', run_metrics={'duration_s': 400})
    manager._runs['run_running'] = AnalysisRun(run_id='run_running', stock_code='000858', status='running', run_metrics={'duration_s': 10})

    metrics = manager.ops_metrics()
    payload = manager.list_runs()

    assert metrics['ops_status'] == 'degraded'
    assert metrics['alert_count'] >= 1
    assert metrics['failure_rate'] == 0.5
    assert payload.workspace.ops_status == 'degraded'
    assert payload.workspace.p95_duration_s == 400


def test_run_manager_reports_store_health_and_backup(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path, auto_start_workers=False)
    manager._runs['run_done'] = AnalysisRun(run_id='run_done', stock_code='600519', status='completed')
    manager._save_runs()

    health = manager.store_health()
    backup_path = manager.backup_store()
    payload = manager.list_runs()

    assert health['backend'] == 'sqlite-wal'
    assert health['integrity'] == 'ok'
    assert health['schema_version'] == 7
    assert Path(backup_path).exists()
    assert payload.workspace.store_backend == 'sqlite-wal'
    assert payload.workspace.backup_available is True


def test_run_manager_persists_runs_in_sqlite(tmp_path):
    manager = AnalysisRunManager(output_dir=tmp_path)
    manager._runs['run_done'] = AnalysisRun(
        run_id='run_done',
        stock_code='600519',
        status='completed',
        updated_at='2026-05-07T11:00:00',
        owner='alice',
        archived=True,
        retry_of_run_id='run_old',
        latest_report_url='/api/v1/reports/latest/600519',
        history_url='/api/v1/history/600519',
        exports=[{'kind': 'markdown', 'filename': 'report_600519_demo.md', 'path': 'output/report_600519_demo.md', 'download_url': '/api/v1/exports/report_600519_demo.md'}],
        events=[{'timestamp': '2026-05-07T11:00:00', 'status': 'completed', 'event': 'run_completed', 'detail': 'done'}],
        event_context={'event_id': 'e9', 'title': '业绩预告', 'impact_level': 'medium'},
        event_report_summary={'trigger_label': '业绩预告', 'priority': 'P1 持续跟踪'},
        multi_agent_trace={'mode': 'autogen_graphflow', 'role_count': 6, 'completed_role_count': 6, 'failed_role_count': 0, 'roles': []},
        run_metrics={'duration_s': 1.5, 'llm_calls': 2, 'tool_calls': 4, 'total_tokens': 88, 'success': True},
    )
    manager._save_runs()

    reloaded = AnalysisRunManager(output_dir=tmp_path).get_run('run_done')

    assert reloaded.owner == 'alice'
    assert reloaded.archived is True
    assert reloaded.retry_of_run_id == 'run_old'
    assert reloaded.exports[0]['filename'] == 'report_600519_demo.md'
    assert reloaded.events[0]['event'] == 'run_completed'
    assert reloaded.event_context['event_id'] == 'e9'
    assert reloaded.event_report_summary['trigger_label'] == '业绩预告'
    assert reloaded.run_metrics['total_tokens'] == 88
    assert reloaded.multi_agent_trace['role_count'] == 6


def test_run_manager_migrates_legacy_json_store(tmp_path):
    legacy_path = tmp_path / 'api_runs.json'
    legacy_path.write_text(
        '[{"run_id": "run_legacy", "stock_code": "600519", "status": "completed", "created_at": "2026-05-07T10:00:00", "updated_at": "2026-05-07T11:00:00", "detail": "done", "last_event": "run_completed", "error": "", "owner": "alice", "archived": true, "retry_of_run_id": "", "canceled": false, "exports": [], "events": [], "latest_report_url": "/api/v1/reports/latest/600519", "history_url": "/api/v1/history/600519"}]',
        encoding='utf-8',
    )

    manager = AnalysisRunManager(output_dir=tmp_path)
    legacy = manager.get_run('run_legacy')

    assert legacy.owner == 'alice'
    assert (tmp_path / 'api_runs.db').exists()
