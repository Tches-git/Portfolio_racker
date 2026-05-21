"""最小兼容的浏览器触发分析运行管理。"""
from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Condition, Lock, Thread
from typing import Iterable
from uuid import uuid4

from app.api.mappers import build_run_response
from app.api.schemas import AnalysisRunListResponse, AnalysisRunResponse, RunStockGroupDTO, WorkspaceSnapshotDTO
from app.config import OUTPUT_DIR, REDIS_URL
from app.memory.db_store import UserMemoryStore
from app.memory.store import get_memory_store
from app.db.session import SessionLocal
from app.db.repositories import save_user_run
from app.engine import ReportEngine
from app.evals.rag_eval import evaluate_rag_citations
from app.models import AnalysisState
from app.exports.storage import save_output_files


@dataclass
class AnalysisRun:
    run_id: str
    stock_code: str
    user_id: str = ''
    status: str = 'queued'
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    detail: str = '等待启动分析'
    last_event: str = ''
    error: str = ''
    owner: str = ''
    owner_role: str = ''
    archived: bool = False
    retry_of_run_id: str = ''
    canceled: bool = False
    state: AnalysisState | None = None
    run_metrics: dict[str, float | int | bool] = field(default_factory=dict)
    multi_agent_trace: dict[str, object] = field(default_factory=dict)
    event_context: dict[str, object] = field(default_factory=dict)
    event_report_summary: dict[str, object] = field(default_factory=dict)
    exports: list[dict[str, str]] = field(default_factory=list)
    events: list[dict[str, str]] = field(default_factory=list)
    audit_events: list[dict[str, str]] = field(default_factory=list)
    latest_report_url: str = ''
    history_url: str = ''
    recovery_status: str = 'normal'
    stale_after_restart: bool = False
    attempts: int = 0
    max_attempts: int = 2
    priority: int = 0
    worker_id: str = ''
    locked_at: str = ''
    next_retry_at: str = ''


class RunNotFoundError(RuntimeError):
    """运行不存在。"""


class RunActionError(RuntimeError):
    """运行动作不合法。"""


class AnalysisRunManager:
    _LEGACY_PERSIST_PATH = 'api_runs.json'
    _DB_PATH = 'api_runs.db'
    _SCHEMA_VERSION = 7

    def __init__(self, *, output_dir: Path, worker_count: int = 2, auto_start_workers: bool = True) -> None:
        self._output_dir = output_dir
        self._runs: dict[str, AnalysisRun] = {}
        self._lock = Lock()
        self._queue_condition = Condition(self._lock)
        self._worker_count = max(1, worker_count)
        self._workers_started = False
        self._mark_interrupted_on_load = auto_start_workers
        self._legacy_store_path = output_dir / self._LEGACY_PERSIST_PATH
        self._db_path = output_dir / self._DB_PATH
        self._backup_dir = output_dir / 'api_run_backups'
        self._last_backup_path = ''
        self._initialize_store()
        self._load_runs()
        if auto_start_workers:
            self.start_workers()

    def start_run(self, stock_code: str, *, retry_of_run_id: str = '', actor: str = 'system', role: str = 'admin', user_id: str = '') -> AnalysisRun:
        run = AnalysisRun(
            run_id=f'run_{uuid4().hex}',
            stock_code=stock_code.strip(),
            user_id=user_id,
            detail='已创建分析任务，准备启动引擎',
            retry_of_run_id=retry_of_run_id,
            owner=actor if actor != 'system' else '',
            owner_role=role if actor != 'system' else '',
        )
        run.events.append(self._event_payload(run.status, 'run_created', run.detail))
        run.audit_events.append(self._audit_payload(actor, role, 'create_run', f'创建 {run.stock_code} 分析任务'))
        with self._queue_condition:
            self._runs[run.run_id] = run
            self._save_run(run)
            self._enqueue_run(run.run_id)
            self._queue_condition.notify()
        return run

    def start_event_run(self, stock_code: str, *, event_context: dict[str, object], actor: str = 'system', role: str = 'admin', retry_of_run_id: str = '', user_id: str = '') -> AnalysisRun:
        context = dict(event_context or {})
        title = context.get('title', '') or context.get('event_id', '')
        source = context.get('source', '') or context.get('provider', '')
        detail = f'由事件触发研报更新：{title}'
        if source:
            detail = f'{detail}（来源：{source}）'
        run = AnalysisRun(
            run_id=f'run_{uuid4().hex}',
            stock_code=stock_code.strip(),
            user_id=user_id,
            detail=detail,
            last_event='event_analysis_requested',
            retry_of_run_id=retry_of_run_id,
            event_context=context,
            priority=1,
            owner=actor if actor != 'system' else '',
            owner_role=role if actor != 'system' else '',
        )
        run.events.append(self._event_payload(run.status, 'run_created', '已创建事件触发分析任务'))
        run.events.append(self._event_payload(run.status, run.last_event, detail))
        run.audit_events.append(self._audit_payload(actor, role, 'create_run', f'创建 {run.stock_code} 事件触发分析任务'))
        run.audit_events.append(self._audit_payload(actor, role, 'event_analyze', f"事件 {context.get('event_id', '')} 触发分析"))
        with self._queue_condition:
            self._runs[run.run_id] = run
            self._save_run(run)
            self._enqueue_run(run.run_id)
            self._queue_condition.notify()
            return run

    def get_run(self, run_id: str) -> AnalysisRun:
        self.refresh_from_store()
        with self._lock:
            run = self._runs.get(run_id)
        if run is None:
            raise RunNotFoundError(f'未找到运行任务: {run_id}')
        return run

    def assign_owner(self, run_id: str, owner: str, *, actor: str = 'system', role: str = 'admin', owner_role: str = 'analyst') -> AnalysisRun:
        self._ensure_permission(role, 'assign_owner')
        with self._lock:
            run = self._runs.get(run_id)
            if run is None:
                raise RunNotFoundError(f'未找到运行任务: {run_id}')
            run.owner = owner.strip()
            run.owner_role = owner_role.strip() or 'analyst'
            run.updated_at = datetime.now().isoformat()
            run.events.append(self._event_payload(run.status, 'run_assigned', f'已分配给 {run.owner}'))
            run.audit_events.append(self._audit_payload(actor, role, 'assign_owner', f'分配给 {run.owner}'))
            self._save_run(run)
            return run

    def archive_run(self, run_id: str, *, actor: str = 'system', role: str = 'admin') -> AnalysisRun:
        self._ensure_permission(role, 'archive_run')
        with self._lock:
            run = self._runs.get(run_id)
            if run is None:
                raise RunNotFoundError(f'未找到运行任务: {run_id}')
            run.archived = True
            run.updated_at = datetime.now().isoformat()
            run.events.append(self._event_payload(run.status, 'run_archived', '任务已归档'))
            run.audit_events.append(self._audit_payload(actor, role, 'archive_run', '任务已归档'))
            self._save_run(run)
            return run

    def cancel_run(self, run_id: str, *, actor: str = 'system', role: str = 'admin') -> AnalysisRun:
        self._ensure_permission(role, 'cancel_run')
        with self._lock:
            run = self._runs.get(run_id)
            if run is None:
                raise RunNotFoundError(f'未找到运行任务: {run_id}')
            if run.status not in {'queued', 'running'}:
                raise RunActionError('仅排队中或运行中的任务可以取消')
            run.canceled = True
            run.status = 'failed'
            run.detail = '任务已取消'
            run.last_event = 'run_canceled'
            run.error = '任务已取消'
            run.updated_at = datetime.now().isoformat()
            run.events.append(self._event_payload(run.status, run.last_event, run.detail))
            run.audit_events.append(self._audit_payload(actor, role, 'cancel_run', '任务已取消'))
            self._save_run(run)
            self._queue_condition.notify_all()
            return run

    def retry_run(self, run_id: str, *, actor: str = 'system', role: str = 'admin') -> AnalysisRun:
        self._ensure_permission(role, 'retry_run')
        run = self.get_run(run_id)
        if run.status != 'failed':
            raise RunActionError('仅失败任务支持重试')
        if run.event_context:
            retried = self.start_event_run(run.stock_code, event_context=run.event_context, retry_of_run_id=run.run_id, actor=actor, role=role, user_id=run.user_id)
        else:
            retried = self.start_run(run.stock_code, retry_of_run_id=run.run_id, actor=actor, role=role, user_id=run.user_id)
        retried.audit_events.append(self._audit_payload(actor, role, 'retry_run', f'重试来源 {run.run_id}'))
        self._save_run(retried)
        return retried

    def start_batch(self, stock_codes: list[str], *, actor: str = 'system', role: str = 'admin', user_id: str = '') -> list[AnalysisRun]:
        runs = []
        seen = set()
        for code in stock_codes:
            normalized = code.strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            runs.append(self.start_run(normalized, actor=actor, role=role, user_id=user_id))
        return runs

    def get_run_response(self, run_id: str) -> AnalysisRunResponse:
        return build_run_response(self.get_run(run_id))

    def start_workers(self) -> None:
        with self._lock:
            if self._workers_started:
                return
            self._workers_started = True
        for index in range(self._worker_count):
            Thread(target=self._worker_loop, args=(f'worker-{index + 1}',), daemon=True).start()

    def list_run_objects(self, *, limit: int = 1000, owner: str = '', user_id: str = '') -> list[AnalysisRun]:
        self.refresh_from_store()
        with self._lock:
            ordered_runs = sorted(self._runs.values(), key=lambda item: item.updated_at or item.created_at, reverse=True)
            if user_id:
                ordered_runs = [item for item in ordered_runs if item.user_id == user_id]
            if owner:
                ordered_runs = [item for item in ordered_runs if item.owner == owner]
            return ordered_runs[: max(1, limit)]

    def list_runs(self, limit: int = 10, *, owner: str = '', user_id: str = '') -> AnalysisRunListResponse:
        ordered_runs = self.list_run_objects(limit=10_000, owner=owner, user_id=user_id)
        runs = ordered_runs[: max(1, limit)]
        ops_metrics = self._ops_metrics_from_runs(ordered_runs)
        with self._lock:
            status_counts = {
                'queued': sum(1 for item in ordered_runs if item.status == 'queued'),
                'running': sum(1 for item in ordered_runs if item.status == 'running'),
                'completed': sum(1 for item in ordered_runs if item.status == 'completed'),
                'failed': sum(1 for item in ordered_runs if item.status == 'failed'),
            }
            stock_groups = self._stock_groups(ordered_runs)
            archived_run_count = sum(1 for item in ordered_runs if item.archived)
            stale_run_count = sum(1 for item in ordered_runs if item.stale_after_restart)
            retry_scheduled_count = sum(1 for item in ordered_runs if item.status == 'queued' and item.next_retry_at)
            collaborator_count = len({item.owner for item in ordered_runs if item.owner})
            audited_action_count = sum(len(item.audit_events) for item in ordered_runs)
            history_backed_stock_count = (
                len({item.stock_code for item in ordered_runs if item.status == 'completed'})
                if user_id
                else len(get_memory_store().get_all_stocks())
            )
        return AnalysisRunListResponse(
            items=[build_run_response(run) for run in runs],
            total=len(ordered_runs),
            queued_count=status_counts['queued'],
            running_count=status_counts['running'],
            completed_count=status_counts['completed'],
            failed_count=status_counts['failed'],
            stock_groups=stock_groups,
            workspace=WorkspaceSnapshotDTO(
                tracked_stocks=[group.stock_code for group in stock_groups],
                most_active_stock=stock_groups[0].stock_code if stock_groups else '',
                latest_completed_stock=next((item.stock_code for item in ordered_runs if item.status == 'completed'), ''),
                failed_stock_count=sum(1 for group in stock_groups if group.failed_count),
                history_backed_stock_count=history_backed_stock_count,
                recommended_concurrency=3,
                active_limit_reached=status_counts['queued'] + status_counts['running'] >= 3,
                observability_status='enhanced',
                collaboration_ready=True,
                collaborator_count=collaborator_count,
                audited_action_count=audited_action_count,
                archived_run_count=archived_run_count,
                stale_run_count=stale_run_count,
                recovery_status='needs_attention' if stale_run_count else 'normal',
                worker_count=self._worker_count,
                retry_scheduled_count=retry_scheduled_count,
                queue_mode='worker_queue',
                store_backend='sqlite-wal',
                schema_version=self._SCHEMA_VERSION,
                wal_enabled=True,
                backup_available=bool(self._last_backup_path),
                last_backup_path=self._last_backup_path,
                ops_status=str(ops_metrics['ops_status']),
                alert_count=int(ops_metrics['alert_count']),
                failure_rate=float(ops_metrics['failure_rate']),
                avg_duration_s=float(ops_metrics['avg_duration_s']),
                p95_duration_s=float(ops_metrics['p95_duration_s']),
            ),
        )

    def list_event_runs(self, *, stock_code: str = '', limit: int = 20, owner: str = '', user_id: str = '') -> list[AnalysisRun]:
        with self._lock:
            runs = [
                run for run in self._runs.values()
                if run.event_context and (not stock_code or run.stock_code == stock_code)
                and (not owner or run.owner == owner)
                and (not user_id or run.user_id == user_id)
            ]
        return sorted(runs, key=lambda item: item.updated_at or item.created_at, reverse=True)[: max(1, limit)]

    def find_run_by_export(self, filename: str, *, owner: str = '', user_id: str = '') -> AnalysisRun | None:
        with self._lock:
            for run in self._runs.values():
                if user_id and run.user_id != user_id:
                    continue
                if owner and run.owner != owner:
                    continue
                for export in run.exports:
                    if export.get('filename') == filename:
                        return run
        return None

    @staticmethod
    def _stock_groups(runs: list[AnalysisRun]) -> list[RunStockGroupDTO]:
        grouped: dict[str, dict[str, str | int]] = {}
        for run in runs:
            entry = grouped.setdefault(run.stock_code, {
                'stock_code': run.stock_code,
                'total': 0,
                'active_count': 0,
                'failed_count': 0,
                'archived_count': 0,
                'latest_run_id': run.run_id,
                'latest_status': run.status,
                'latest_updated_at': run.updated_at,
            })
            entry['total'] = int(entry['total']) + 1
            if run.status in {'queued', 'running'}:
                entry['active_count'] = int(entry['active_count']) + 1
            if run.status == 'failed':
                entry['failed_count'] = int(entry['failed_count']) + 1
            if run.archived:
                entry['archived_count'] = int(entry['archived_count']) + 1
        return [RunStockGroupDTO(**item) for item in grouped.values()]

    def _worker_loop(self, worker_id: str) -> None:
        while True:
            with self._queue_condition:
                run = self._claim_next_run(worker_id)
                if run is None:
                    self._queue_condition.wait(timeout=1.0)
                    continue
            self._execute_run(run.run_id)

    def execute_queued_once(self, worker_id: str = 'external-worker') -> AnalysisRun | None:
        """供独立 worker 进程调用：刷新共享任务库，领取并执行一个任务。"""
        self.refresh_from_store(mark_interrupted=False)
        with self._queue_condition:
            run = self._claim_next_run(worker_id)
        if run is None:
            return None
        self._execute_run(run.run_id)
        return self.get_run(run.run_id)

    def run_external_worker(self, *, worker_id: str = 'external-worker', poll_interval: float = 1.0) -> None:
        """Redis 通知优先、SQLite 轮询兜底的单机 worker 循环。"""
        print(f'{worker_id} 已启动，等待研报任务')
        while True:
            self._wait_for_queue_signal(timeout=max(1, int(poll_interval)))
            run = self.execute_queued_once(worker_id)
            if run is None:
                time.sleep(poll_interval)

    def _claim_next_run(self, worker_id: str) -> AnalysisRun | None:
        now = datetime.now().isoformat()
        candidates = [
            run for run in self._runs.values()
            if run.status == 'queued' and not run.canceled and (not run.next_retry_at or run.next_retry_at <= now)
        ]
        if not candidates:
            return None
        run = sorted(candidates, key=lambda item: (-item.priority, item.created_at))[0]
        run.status = 'running'
        run.attempts += 1
        run.worker_id = worker_id
        run.locked_at = now
        run.updated_at = now
        run.detail = f'{worker_id} 已领取任务，启动分析引擎'
        run.last_event = 'run_claimed'
        run.events.append(self._event_payload(run.status, run.last_event, run.detail))
        self._save_run(run)
        return run

    def _execute_run(self, run_id: str) -> None:
        run = self.get_run(run_id)
        db = None
        memory_store = None
        if run.user_id:
            db = SessionLocal()
            memory_store = UserMemoryStore(db, run.user_id)
        output_root = self._run_output_dir(run)

        def on_step(event: str, detail: str, state: AnalysisState) -> None:
            if self.get_run(run_id).canceled:
                raise RuntimeError('任务已取消')
            partial_trace = dict(getattr(state, 'run_payload', {}).get('multi_agent_trace', {}) or {})
            partial_metrics = dict(getattr(state, 'run_metrics', {}) or {})
            self._update_run(
                run_id,
                status='running',
                detail=detail,
                last_event=event,
                run_metrics=partial_metrics or None,
                multi_agent_trace=partial_trace or None,
            )

        self._update_run(run_id, status='running', detail='分析引擎已启动', last_event='run_started')
        if self.get_run(run_id).canceled:
            if db is not None:
                db.close()
            return
        try:
            engine = ReportEngine(on_step=on_step, memory_store=memory_store)
        except TypeError:
            engine = ReportEngine(on_step=on_step)
        try:
            state = engine.run(run.stock_code, event_context=run.event_context or None)
            if not state.final_report:
                self._update_run(run_id, status='failed', detail='分析未生成最终报告', last_event='run_failed', error='分析未生成最终报告')
                return
            try:
                save_output_files(state, root=output_root, timestamp=self._export_timestamp(state))
            except TypeError:
                save_output_files(state, timestamp=self._export_timestamp(state))
            self._update_completed_run(run_id, state)
            if db is not None:
                save_user_run(db, user_id=run.user_id, run=self.get_run(run_id))
        except Exception as exc:
            self._handle_run_failure(run_id, str(exc))
        finally:
            if db is not None:
                db.close()

    def _handle_run_failure(self, run_id: str, error: str) -> None:
        with self._queue_condition:
            run = self._runs[run_id]
            run.error = error
            run.worker_id = ''
            run.locked_at = ''
            run.updated_at = datetime.now().isoformat()
            if run.canceled or error == '任务已取消' or run.attempts >= run.max_attempts:
                run.status = 'failed'
                run.detail = '分析运行失败'
                run.last_event = 'run_failed'
                run.events.append(self._event_payload(run.status, run.last_event, run.detail))
            else:
                run.status = 'queued'
                run.detail = f'分析失败，已自动重新排队（{run.attempts}/{run.max_attempts}）'
                run.last_event = 'run_retry_scheduled'
                run.next_retry_at = datetime.now().isoformat()
                run.events.append(self._event_payload(run.status, run.last_event, run.detail))
                self._queue_condition.notify()
            self._save_run(run)

    @staticmethod
    def _export_timestamp(state: AnalysisState) -> str:
        if getattr(state, 'run_metrics', None):
            return datetime.now().strftime('%Y%m%d_%H%M%S')
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def _update_completed_run(self, run_id: str, state: AnalysisState) -> None:
        run = self.get_run(run_id)
        output_root = self._run_output_dir(run)
        exports = []
        for key, kind in (
            ('report_export', 'markdown'),
            ('report_html_export', 'html'),
            ('report_pdf_export', 'pdf'),
            ('trace_export', 'trace'),
            ('source_refs_export', 'sources'),
        ):
            filename = str(state.sections.get(key, '') or '').strip()
            if filename:
                exports.append({
                    'kind': kind,
                    'filename': filename,
                    'path': str(output_root / filename),
                    'download_url': f'/api/v1/exports/{filename}',
                })
        event_summary = {}
        if run.event_context:
            event_summary = self._build_event_report_summary(run, state)
            commentary_filename = self._write_event_commentary_export(run, state, event_summary)
            if commentary_filename:
                event_summary['event_commentary_filename'] = commentary_filename
                event_summary['event_commentary_url'] = f'/api/v1/exports/{commentary_filename}'
                exports.append({
                    'kind': 'event_commentary',
                    'filename': commentary_filename,
                    'path': str(output_root / commentary_filename),
                    'download_url': f'/api/v1/exports/{commentary_filename}',
                })
        with self._lock:
            current = self._runs[run_id]
            current.status = 'completed'
            current.updated_at = datetime.now().isoformat()
            current.detail = '分析已完成，可查看最新摘要与导出物'
            current.last_event = 'run_completed'
            current.error = ''
            current.worker_id = ''
            current.locked_at = ''
            current.next_retry_at = ''
            current.state = state
            current.run_metrics = dict(getattr(state, 'run_metrics', {}) or {})
            citation_metrics = evaluate_rag_citations(
                getattr(state, 'final_report', '') or '',
                list(getattr(state, 'source_refs', []) or []),
                stock_code=current.stock_code,
            )
            current.run_metrics.update(citation_metrics)
            current.run_metrics['citation_audit_coverage_rate'] = float(citation_metrics.get('citation_coverage_rate', 0.0) or 0.0)
            current.multi_agent_trace = dict(getattr(state, 'run_payload', {}).get('multi_agent_trace', {}) or {})
            current.event_report_summary = event_summary
            current.exports = exports
            current.latest_report_url = f'/api/v1/reports/latest/{current.stock_code}'
            current.history_url = f'/api/v1/history/{current.stock_code}'
            current.events.append(self._event_payload(current.status, current.last_event, current.detail))
            self._save_run(current)

    def _build_event_report_summary(self, run: AnalysisRun, state: AnalysisState) -> dict[str, object]:
        context = dict(run.event_context or {})
        sections = dict(getattr(state, 'sections', {}) or {})
        title = str(context.get('title') or context.get('event_id') or '事件触发研报')
        sentiment = str(context.get('sentiment') or 'neutral')
        impact_level = str(context.get('impact_level') or 'low')
        impact_scope = str(context.get('impact_scope') or 'sentiment')
        direction = {
            'positive': '利好验证',
            'negative': '风险复核',
            'uncertain': '不确定性复核',
            'neutral': '中性跟踪',
        }.get(sentiment, '中性跟踪')
        priority = {
            'high': 'P0 高优先级',
            'medium': 'P1 持续跟踪',
            'low': 'P2 观察',
        }.get(impact_level, 'P2 观察')
        rating = str(sections.get('rating') or '').strip()
        rating_detail = str(sections.get('rating_detail') or '').strip()
        trigger_line = str(context.get('summary') or context.get('reason') or title)
        thesis = f'本次研报由“{title}”触发，重点复核 {impact_scope} 传导路径。'
        if trigger_line and trigger_line != title:
            thesis = f'{thesis} 事件摘要：{trigger_line[:160]}'
        report_delta_hint = '研报已生成，建议结合导出正文复核投资要点、核心风险与后续跟踪指标。'
        if rating or rating_detail:
            report_delta_hint = f'当前研报评级 {rating or "--"}；{rating_detail or "需结合正文确认评级依据"}'
        action = '查看事件点评导出并回到事件详情复核来源。'
        if impact_level == 'high':
            action = '优先复核事件点评导出，并检查研报中风险/估值锚是否已更新。'
        related_sources = context.get('related_sources') if isinstance(context.get('related_sources'), list) else []
        return {
            'trigger_label': title,
            'thesis': thesis,
            'impact_direction': direction,
            'impact_level': impact_level,
            'impact_scope': impact_scope,
            'priority': priority,
            'review_status': 'completed',
            'action': action,
            'report_delta_hint': report_delta_hint,
            'related_source_count': len(related_sources),
            'event_commentary_filename': '',
            'event_commentary_url': '',
        }

    def _write_event_commentary_export(self, run: AnalysisRun, state: AnalysisState, summary: dict[str, object]) -> str:
        context = dict(run.event_context or {})
        if not context:
            return ''
        output_root = self._run_output_dir(run)
        output_root.mkdir(parents=True, exist_ok=True)
        safe_event_id = ''.join(ch for ch in str(context.get('event_id') or run.run_id) if ch.isalnum() or ch in {'_', '-'})[:48] or run.run_id
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'event_commentary_{run.stock_code}_{safe_event_id}_{run.run_id[-8:]}_{timestamp}.md'
        path = output_root / filename
        sections = dict(getattr(state, 'sections', {}) or {})
        report_excerpt = str(getattr(state, 'final_report', '') or '').strip()[:1000]
        source = str(context.get('source') or context.get('provider') or '未知来源')
        published_at = str(context.get('published_at') or context.get('collected_at') or '')
        related_sources = context.get('related_sources') if isinstance(context.get('related_sources'), list) else []
        related_lines = []
        for item in related_sources[:5]:
            if not isinstance(item, dict):
                continue
            title = str(item.get('title') or item.get('source') or item.get('url') or '').strip()
            url = str(item.get('url') or '').strip()
            related_lines.append(f"- {title or '相关来源'}{f'：{url}' if url else ''}")
        content = f"""# 事件点评：{context.get('title') or context.get('event_id') or '事件触发研报'}

## 触发事件
- 股票：{context.get('stock_name') or run.stock_code}（{run.stock_code}）
- 事件 ID：{context.get('event_id') or ''}
- 来源：{source}
- 时间：{published_at or '待补充'}
- 类型：{context.get('event_type') or 'other'}
- 影响等级：{context.get('impact_level') or 'low'}
- 情绪方向：{context.get('sentiment') or 'neutral'}
- 影响范围：{context.get('impact_scope') or 'sentiment'}
- 置信度：{context.get('confidence') or 0}

## 事件摘要
{context.get('summary') or context.get('reason') or '暂无摘要'}

## 事件驱动研报摘要卡
- 触发判断：{summary.get('thesis') or ''}
- 影响方向：{summary.get('impact_direction') or ''}
- 优先级：{summary.get('priority') or ''}
- 研报变化提示：{summary.get('report_delta_hint') or ''}
- 建议动作：{summary.get('action') or ''}

## 研报关联
- 任务 ID：{run.run_id}
- 任务状态：completed
- 正文导出：{sections.get('report_export') or '暂无'}
- HTML 导出：{sections.get('report_html_export') or '暂无'}

## 相关来源
{chr(10).join(related_lines) if related_lines else '- 暂无相关来源'}

## 正文摘录
{report_excerpt or '暂无正文摘录'}
"""
        path.write_text(content, encoding='utf-8')
        sections['event_commentary_export'] = filename
        if hasattr(state, 'sections'):
            state.sections['event_commentary_export'] = filename
        return filename

    def _run_output_dir(self, run: AnalysisRun) -> Path:
        if run.user_id:
            return self._output_dir / 'users' / run.user_id
        return self._output_dir

    def _update_run(
        self,
        run_id: str,
        *,
        status: str | None = None,
        detail: str | None = None,
        last_event: str | None = None,
        error: str | None = None,
        run_metrics: dict[str, object] | None = None,
        multi_agent_trace: dict[str, object] | None = None,
    ) -> None:
        with self._lock:
            run = self._runs[run_id]
            if status is not None:
                run.status = status
            if detail is not None:
                run.detail = detail
            if last_event is not None:
                run.last_event = last_event
            if error is not None:
                run.error = error
            if run_metrics is not None:
                run.run_metrics = dict(run_metrics)
            if multi_agent_trace is not None:
                run.multi_agent_trace = dict(multi_agent_trace)
            run.updated_at = datetime.now().isoformat()
            if detail is not None or last_event is not None or status is not None:
                run.events.append(self._event_payload(run.status, run.last_event, run.detail))
            self._save_run(run)

    def _initialize_store(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as conn:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA foreign_keys=ON')
            conn.execute(f'PRAGMA user_version = {self._SCHEMA_VERSION}')
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS api_runs (
                    run_id TEXT PRIMARY KEY,
                    stock_code TEXT NOT NULL,
                    user_id TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    detail TEXT NOT NULL,
                    last_event TEXT NOT NULL,
                    error TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    owner_role TEXT NOT NULL DEFAULT '',
                    archived INTEGER NOT NULL,
                    retry_of_run_id TEXT NOT NULL,
                    canceled INTEGER NOT NULL,
                    latest_report_url TEXT NOT NULL,
                    history_url TEXT NOT NULL,
                    recovery_status TEXT NOT NULL DEFAULT 'normal',
                    stale_after_restart INTEGER NOT NULL DEFAULT 0,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL DEFAULT 2,
                    priority INTEGER NOT NULL DEFAULT 0,
                    worker_id TEXT NOT NULL DEFAULT '',
                    locked_at TEXT NOT NULL DEFAULT '',
                    next_retry_at TEXT NOT NULL DEFAULT '',
                    run_metrics_json TEXT NOT NULL DEFAULT '{}',
                    multi_agent_trace_json TEXT NOT NULL DEFAULT '{}',
                    event_context_json TEXT NOT NULL DEFAULT '{}',
                    event_report_summary_json TEXT NOT NULL DEFAULT '{}',
                    exports_json TEXT NOT NULL,
                    events_json TEXT NOT NULL,
                    audit_events_json TEXT NOT NULL DEFAULT '[]'
                )
                '''
            )
            columns = {item[1] for item in conn.execute("PRAGMA table_info(api_runs)").fetchall()}
            if 'owner_role' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN owner_role TEXT NOT NULL DEFAULT '' ")
            if 'user_id' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN user_id TEXT NOT NULL DEFAULT '' ")
            if 'run_metrics_json' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN run_metrics_json TEXT NOT NULL DEFAULT '{}' ")
            if 'multi_agent_trace_json' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN multi_agent_trace_json TEXT NOT NULL DEFAULT '{}' ")
            if 'recovery_status' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN recovery_status TEXT NOT NULL DEFAULT 'normal' ")
            if 'stale_after_restart' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN stale_after_restart INTEGER NOT NULL DEFAULT 0 ")
            for column, ddl in {
                'attempts': 'ALTER TABLE api_runs ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0',
                'max_attempts': 'ALTER TABLE api_runs ADD COLUMN max_attempts INTEGER NOT NULL DEFAULT 2',
                'priority': 'ALTER TABLE api_runs ADD COLUMN priority INTEGER NOT NULL DEFAULT 0',
                'worker_id': "ALTER TABLE api_runs ADD COLUMN worker_id TEXT NOT NULL DEFAULT ''",
                'locked_at': "ALTER TABLE api_runs ADD COLUMN locked_at TEXT NOT NULL DEFAULT ''",
                'next_retry_at': "ALTER TABLE api_runs ADD COLUMN next_retry_at TEXT NOT NULL DEFAULT ''",
            }.items():
                if column not in columns:
                    conn.execute(ddl)
            if 'audit_events_json' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN audit_events_json TEXT NOT NULL DEFAULT '[]' ")
            if 'event_context_json' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN event_context_json TEXT NOT NULL DEFAULT '{}' ")
            if 'event_report_summary_json' not in columns:
                conn.execute("ALTER TABLE api_runs ADD COLUMN event_report_summary_json TEXT NOT NULL DEFAULT '{}' ")
            conn.execute('CREATE INDEX IF NOT EXISTS idx_api_runs_status_updated ON api_runs(status, updated_at)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_api_runs_stock_updated ON api_runs(stock_code, updated_at)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_api_runs_owner ON api_runs(owner)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_api_runs_user_id ON api_runs(user_id)')
            conn.commit()

    def _load_runs(self) -> None:
        loaded_from_db = False
        recovery_changed = False
        if self._db_path.exists():
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(
                    '''
                    SELECT run_id, stock_code, status, created_at, updated_at, detail, last_event,
                           error, owner, owner_role, archived, retry_of_run_id, canceled, latest_report_url,
                           history_url, recovery_status, stale_after_restart, attempts, max_attempts,
                           priority, worker_id, locked_at, next_retry_at, run_metrics_json, multi_agent_trace_json, event_context_json,
                           event_report_summary_json, exports_json, events_json, audit_events_json, user_id
                    FROM api_runs
                    ORDER BY updated_at DESC
                    '''
                ).fetchall()
            for row in rows:
                run = self._run_from_row(row, mark_interrupted=self._mark_interrupted_on_load)
                self._runs[run.run_id] = run
                recovery_changed = recovery_changed or (str(row[2]) in {'queued', 'running'} and run.stale_after_restart)
            if recovery_changed:
                self._save_runs()
            loaded_from_db = bool(rows)
        if loaded_from_db or not self._legacy_store_path.exists():
            return
        try:
            data = json.loads(self._legacy_store_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return
        for item in data:
            payload = dict(item)
            payload['state'] = None
            payload.setdefault('recovery_status', 'normal')
            payload.setdefault('stale_after_restart', False)
            payload.setdefault('owner_role', '')
            payload.setdefault('user_id', '')
            payload.setdefault('audit_events', [])
            payload.setdefault('multi_agent_trace', {})
            payload.setdefault('attempts', 0)
            payload.setdefault('max_attempts', 2)
            payload.setdefault('priority', 0)
            payload.setdefault('worker_id', '')
            payload.setdefault('locked_at', '')
            payload.setdefault('next_retry_at', '')
            payload.setdefault('event_context', {})
            payload.setdefault('event_report_summary', {})
            if payload.get('status') in {'queued', 'running'}:
                payload['status'] = 'failed'
                payload['recovery_status'] = 'interrupted_after_restart'
                payload['stale_after_restart'] = True
                payload['detail'] = '服务重启后检测到未完成任务，请重试恢复分析'
                payload['last_event'] = 'run_interrupted_after_restart'
                payload['error'] = '任务在服务重启前未完成'
                payload['worker_id'] = ''
                payload['locked_at'] = ''
                payload.setdefault('events', []).append(self._event_payload('failed', 'run_interrupted_after_restart', payload['detail']))
            run = AnalysisRun(**payload)
            self._runs[run.run_id] = run
        self._save_runs()

    def ops_metrics(self) -> dict[str, object]:
        with self._lock:
            runs = list(self._runs.values())
        return self._ops_metrics_from_runs(runs)

    def _ops_metrics_from_runs(self, runs: list[AnalysisRun]) -> dict[str, object]:
        total_runs = len(runs)
        active_runs = sum(1 for item in runs if item.status in {'queued', 'running'})
        failed_runs = sum(1 for item in runs if item.status == 'failed')
        durations = sorted(float(item.run_metrics.get('duration_s', 0.0) or 0.0) for item in runs if item.run_metrics)
        recent_events = []
        for run in runs:
            for event in run.events[-3:]:
                recent_events.append({**event, 'run_id': run.run_id, 'stock_code': run.stock_code})
        failure_rate = (failed_runs / total_runs) if total_runs else 0.0
        avg_duration_s = (sum(durations) / len(durations)) if durations else 0.0
        p95_duration_s = durations[min(len(durations) - 1, int(len(durations) * 0.95))] if durations else 0.0
        alerts = []
        if failure_rate >= 0.5 and total_runs >= 2:
            alerts.append('失败率超过 50%')
        if active_runs >= self._worker_count:
            alerts.append('活跃任务达到 worker 容量')
        if p95_duration_s >= 300:
            alerts.append('P95 运行耗时超过 300s')
        recent_events = sorted(recent_events, key=lambda item: item.get('timestamp', ''), reverse=True)[:8]
        return {
            'ops_status': 'degraded' if alerts else 'healthy',
            'total_runs': total_runs,
            'active_runs': active_runs,
            'failed_runs': failed_runs,
            'failure_rate': round(failure_rate, 4),
            'avg_duration_s': round(avg_duration_s, 2),
            'p95_duration_s': round(p95_duration_s, 2),
            'alert_count': len(alerts),
            'alerts': alerts,
            'recent_events': recent_events,
        }

    def backup_store(self) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self._backup_dir / f'api_runs_{timestamp}.db'
        with self._lock:
            with sqlite3.connect(self._db_path) as source:
                with sqlite3.connect(backup_path) as target:
                    source.backup(target)
            self._last_backup_path = str(backup_path)
        return self._last_backup_path

    def store_health(self) -> dict[str, str | int | bool]:
        with sqlite3.connect(self._db_path) as conn:
            integrity = str(conn.execute('PRAGMA integrity_check').fetchone()[0])
            user_version = int(conn.execute('PRAGMA user_version').fetchone()[0])
            journal_mode = str(conn.execute('PRAGMA journal_mode').fetchone()[0])
            row_count = int(conn.execute('SELECT COUNT(*) FROM api_runs').fetchone()[0])
        return {
            'backend': 'sqlite-wal',
            'integrity': integrity,
            'schema_version': user_version,
            'journal_mode': journal_mode,
            'row_count': row_count,
            'backup_available': bool(self._last_backup_path),
            'last_backup_path': self._last_backup_path,
        }

    def _save_runs(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            self._write_runs(conn, self._runs.values())

    def _save_run(self, run: AnalysisRun) -> None:
        with sqlite3.connect(self._db_path) as conn:
            self._write_runs(conn, [run])

    def _write_runs(self, conn: sqlite3.Connection, runs: Iterable[AnalysisRun]) -> None:
        conn.executemany(
            '''
            INSERT OR REPLACE INTO api_runs (
                run_id, stock_code, user_id, status, created_at, updated_at, detail, last_event,
                error, owner, owner_role, archived, retry_of_run_id, canceled, latest_report_url,
                history_url, recovery_status, stale_after_restart, attempts, max_attempts, priority,
                worker_id, locked_at, next_retry_at, run_metrics_json, multi_agent_trace_json, event_context_json, event_report_summary_json,
                exports_json, events_json, audit_events_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            [self._run_to_row(run) for run in runs],
        )
        conn.commit()

    @staticmethod
    def _run_to_row(run: AnalysisRun) -> tuple[object, ...]:
        return (
            run.run_id,
            run.stock_code,
            run.user_id,
            run.status,
            run.created_at,
            run.updated_at,
            run.detail,
            run.last_event,
            run.error,
            run.owner,
            run.owner_role,
            int(run.archived),
            run.retry_of_run_id,
            int(run.canceled),
            run.latest_report_url,
            run.history_url,
            run.recovery_status,
            int(run.stale_after_restart),
            run.attempts,
            run.max_attempts,
            run.priority,
            run.worker_id,
            run.locked_at,
            run.next_retry_at,
            json.dumps(run.run_metrics, ensure_ascii=False),
            json.dumps(run.multi_agent_trace, ensure_ascii=False),
            json.dumps(run.event_context, ensure_ascii=False),
            json.dumps(run.event_report_summary, ensure_ascii=False),
            json.dumps(run.exports, ensure_ascii=False),
            json.dumps(run.events, ensure_ascii=False),
            json.dumps(run.audit_events, ensure_ascii=False),
        )

    def refresh_from_store(self, *, mark_interrupted: bool = False) -> None:
        if not self._db_path.exists():
            return
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                '''
                SELECT run_id, stock_code, status, created_at, updated_at, detail, last_event,
                       error, owner, owner_role, archived, retry_of_run_id, canceled, latest_report_url,
                       history_url, recovery_status, stale_after_restart, attempts, max_attempts,
                       priority, worker_id, locked_at, next_retry_at, run_metrics_json, multi_agent_trace_json, event_context_json,
                       event_report_summary_json, exports_json, events_json, audit_events_json, user_id
                FROM api_runs
                ORDER BY updated_at DESC
                '''
            ).fetchall()
        with self._lock:
            for row in rows:
                incoming = self._run_from_row(row, mark_interrupted=mark_interrupted)
                current = self._runs.get(incoming.run_id)
                if current is None or incoming.updated_at >= current.updated_at:
                    self._runs[incoming.run_id] = incoming

    def _redis_client(self):
        if not REDIS_URL:
            return None
        try:
            import redis

            return redis.Redis.from_url(REDIS_URL, socket_connect_timeout=0.5, socket_timeout=1.0)
        except Exception:
            return None

    def _enqueue_run(self, run_id: str) -> None:
        client = self._redis_client()
        if client is None:
            return
        try:
            client.lpush('analysis_runs:queue', run_id)
        except Exception:
            return

    def _wait_for_queue_signal(self, *, timeout: int = 1) -> str:
        client = self._redis_client()
        if client is None:
            time.sleep(timeout)
            return ''
        try:
            item = client.brpop('analysis_runs:queue', timeout=timeout)
            if not item:
                return ''
            value = item[1]
            return value.decode('utf-8') if isinstance(value, bytes) else str(value)
        except Exception:
            time.sleep(timeout)
            return ''

    @staticmethod
    def _run_from_row(row: tuple[object, ...], *, mark_interrupted: bool = True) -> AnalysisRun:
        status = str(row[2])
        recovery_status = str(row[15] or 'normal')
        stale_after_restart = bool(row[16])
        detail = str(row[5])
        last_event = str(row[6])
        error = str(row[7])
        if mark_interrupted and status in {'queued', 'running'}:
            status = 'failed'
            recovery_status = 'interrupted_after_restart'
            stale_after_restart = True
            detail = '服务重启后检测到未完成任务，请重试恢复分析'
            last_event = 'run_interrupted_after_restart'
            error = '任务在服务重启前未完成'
        attempts = int(row[17] or 0)
        max_attempts = int(row[18] or 2)
        priority = int(row[19] or 0)
        worker_id = str(row[20] or '')
        locked_at = str(row[21] or '')
        next_retry_at = str(row[22] or '')
        run_metrics = dict(json.loads(str(row[23]) or '{}'))
        multi_agent_trace = dict(json.loads(str(row[24]) or '{}'))
        event_context = dict(json.loads(str(row[25]) or '{}'))
        event_report_summary = dict(json.loads(str(row[26]) or '{}'))
        exports = list(json.loads(str(row[27]) or '[]'))
        events = list(json.loads(str(row[28]) or '[]'))
        audit_events = list(json.loads(str(row[29]) or '[]'))
        if stale_after_restart and not any(item.get('event') == 'run_interrupted_after_restart' for item in events):
            events.append({
                'timestamp': datetime.now().isoformat(),
                'status': status,
                'event': 'run_interrupted_after_restart',
                'detail': detail,
            })
        return AnalysisRun(
            run_id=str(row[0]),
            stock_code=str(row[1]),
            user_id=str(row[30] or '') if len(row) > 30 else '',
            status=status,
            created_at=str(row[3]),
            updated_at=str(row[4]),
            detail=detail,
            last_event=last_event,
            error=error,
            owner=str(row[8]),
            owner_role=str(row[9]),
            archived=bool(row[10]),
            retry_of_run_id=str(row[11]),
            canceled=bool(row[12]),
            latest_report_url=str(row[13]),
            history_url=str(row[14]),
            recovery_status=recovery_status,
            stale_after_restart=stale_after_restart,
            attempts=attempts,
            max_attempts=max_attempts,
            priority=priority,
            worker_id=worker_id if status == 'running' else '',
            locked_at=locked_at if status == 'running' else '',
            next_retry_at=next_retry_at,
            run_metrics=run_metrics,
            multi_agent_trace=multi_agent_trace,
            event_context=event_context,
            event_report_summary=event_report_summary,
            exports=exports,
            events=events,
            audit_events=audit_events,
            state=None,
        )

    @staticmethod
    def _ensure_permission(role: str, action: str) -> None:
        role_actions = {
            'viewer': set(),
            'analyst': {'retry_run', 'cancel_run', 'assign_owner'},
            'admin': {'retry_run', 'cancel_run', 'assign_owner', 'archive_run'},
        }
        if action not in role_actions.get(role, role_actions['viewer']):
            raise RunActionError(f'角色 {role} 无权执行 {action}')

    @staticmethod
    def _event_payload(status: str, event: str, detail: str) -> dict[str, str]:
        return {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'event': event,
            'detail': detail,
        }

    @staticmethod
    def _audit_payload(actor: str, role: str, action: str, detail: str) -> dict[str, str]:
        return {
            'timestamp': datetime.now().isoformat(),
            'actor': actor or 'system',
            'role': role or 'viewer',
            'action': action,
            'detail': detail,
        }


run_manager = AnalysisRunManager(
    output_dir=OUTPUT_DIR,
    auto_start_workers=os.getenv('RUN_MANAGER_AUTO_START', 'true').lower() in {'1', 'true', 'yes', 'on'},
)
