"""内部状态到 API DTO 的映射。"""
from __future__ import annotations

from pathlib import Path

from app.api.schemas import (
    AnalysisRunResponse,
    DeliverySummaryDTO,
    ExportArtifactDTO,
    RunActionAvailabilityDTO,
    HealthResponse,
    RunAuditEventDTO,
    HistoryInsightDTO,
    HistoryRecordDTO,
    LatestReportResponse,
    QualitySummaryDTO,
    ReportSummaryDTO,
    RunEventDTO,
    RunMetricsDTO,
    RunObservabilityDTO,
    StockHistoryResponse,
    StockIdentityDTO,
    StockMemoryDTO,
    ValuationSummaryDTO,
)
from app.memory.store import AnalysisRecord, StockMemorySnapshot


def build_health_response() -> HealthResponse:
    return HealthResponse()


def _stock_identity(*, code: str, name: str = "", industry: str = "") -> StockIdentityDTO:
    return StockIdentityDTO(code=code, name=name, industry=industry)


def _export_artifacts(output_dir: Path, stock_code: str, timestamp: str) -> list[ExportArtifactDTO]:
    patterns = [
        ("markdown", f"report_{stock_code}_{timestamp}.md"),
        ("html", f"report_{stock_code}_{timestamp}.html"),
        ("pdf", f"report_{stock_code}_{timestamp}.pdf"),
        ("trace", f"trace_{stock_code}_{timestamp}.log"),
        ("sources", f"sources_{stock_code}_{timestamp}.json"),
    ]
    items: list[ExportArtifactDTO] = []
    for kind, filename in patterns:
        path = output_dir / filename
        if path.exists():
            items.append(
                ExportArtifactDTO(
                    kind=kind,
                    filename=filename,
                    path=str(path),
                    download_url=f"/api/v1/exports/{filename}",
                )
            )
    return items


def map_latest_record(record: AnalysisRecord, *, output_dir: Path) -> LatestReportResponse:
    exports = _export_artifacts(output_dir, record.stock_code, record.timestamp.replace("-", "").replace(":", "").replace("T", "_")[:15])
    previewable_count = sum(1 for item in exports if item.kind in {'markdown', 'html', 'sources'})
    return LatestReportResponse(
        stock=_stock_identity(code=record.stock_code, name=record.stock_name, industry=record.industry),
        summary=ReportSummaryDTO(
            rating=record.rating,
            rating_score=record.rating_score,
            conclusion_brief=record.conclusion,
        ),
        valuation=ValuationSummaryDTO(
            per_share_value=record.dcf_per_share,
            current_price=record.current_price,
            upside=record.dcf_upside,
        ),
        quality=QualitySummaryDTO(
            source_reference_count=record.source_reference_count,
            placeholder_source_count=record.placeholder_source_count,
        ),
        run_metrics=RunMetricsDTO(success=True),
        exports=exports,
        delivery=DeliverySummaryDTO(
            available_kinds=[item.kind for item in exports],
            previewable_count=previewable_count,
            downloadable_count=len(exports),
            latest_export_filename=exports[0].filename if exports else '',
        ),
        generated_at=record.timestamp,
    )


def map_history_record(record: AnalysisRecord) -> HistoryRecordDTO:
    return HistoryRecordDTO(
        stock_code=record.stock_code,
        stock_name=record.stock_name,
        timestamp=record.timestamp,
        rating=record.rating,
        rating_score=record.rating_score,
        conclusion=record.conclusion,
        risk_count=record.risk_count,
        risk_summary=record.risk_summary,
        source_reference_count=record.source_reference_count,
        placeholder_source_count=record.placeholder_source_count,
        dcf_per_share=record.dcf_per_share,
        dcf_upside=record.dcf_upside,
    )


def map_stock_memory(snapshot: StockMemorySnapshot) -> StockMemoryDTO:
    return StockMemoryDTO(
        timestamp=snapshot.timestamp,
        thesis=snapshot.thesis,
        rating=snapshot.rating,
        target_range=snapshot.target_range,
        valuation_summary=snapshot.valuation_summary,
        historical_delta=snapshot.historical_delta,
        conflict_flag=snapshot.conflict_flag,
        conflict_reason=snapshot.conflict_reason,
        key_risks=list(snapshot.key_risks),
        catalysts=list(snapshot.catalysts),
    )


def map_stock_history(*, code: str, name: str, industry: str, records: list[AnalysisRecord], memory: list[StockMemorySnapshot], insights: dict[str, str | int | float]) -> StockHistoryResponse:
    return StockHistoryResponse(
        stock=_stock_identity(code=code, name=name, industry=industry),
        records=[map_history_record(item) for item in records],
        memory=[map_stock_memory(item) for item in memory],
        insights=HistoryInsightDTO(
            conflict_count=int(insights.get('memory_conflict_count', 0) or 0),
            latest_conflict_reason=next((item.conflict_reason for item in memory if item.conflict_reason), ''),
            rating_drift_summary=str(insights.get('rating_drift_summary', '') or ''),
            thesis_stability_score=float(insights.get('thesis_stability_score', 0.0) or 0.0),
            repeated_risk_patterns=[part for part in str(insights.get('repeated_risk_patterns', '') or '').split('；') if part and part != '暂无'],
            repeated_catalyst_patterns=[part for part in str(insights.get('repeated_catalyst_patterns', '') or '').split('；') if part and part != '暂无'],
            memory_pattern_summary=str(insights.get('memory_pattern_summary', '') or ''),
        ),
    )


def build_run_response(run) -> AnalysisRunResponse:
    metrics = dict(getattr(run, 'run_metrics', {}) or {})
    if not metrics and getattr(run, 'state', None) is not None:
        metrics = dict(getattr(run.state, 'run_metrics', {}) or {})
    exports = list(getattr(run, 'exports', []) or [])
    events = list(getattr(run, 'events', []) or [])
    audit_events = list(getattr(run, 'audit_events', []) or [])
    stock_code = str(getattr(run, 'stock_code', '') or '')
    status = str(getattr(run, 'status', '') or '')
    owner = str(getattr(run, 'owner', '') or '')
    archived = bool(getattr(run, 'archived', False))
    can_retry = status == 'failed'
    can_cancel = status in {'queued', 'running'}
    latest_signal = str(getattr(run, 'last_event', '') or '') or (events[-1].get('event', '') if events else '')
    return AnalysisRunResponse(
        run_id=run.run_id,
        stock_code=run.stock_code,
        status=run.status,
        created_at=run.created_at,
        updated_at=run.updated_at,
        detail=run.detail,
        last_event=run.last_event,
        error=run.error,
        owner=owner,
        owner_role=str(getattr(run, 'owner_role', '') or ''),
        archived=archived,
        retry_of_run_id=getattr(run, 'retry_of_run_id', ''),
        latest_report_url=run.latest_report_url,
        history_url=run.history_url,
        exports=[ExportArtifactDTO(**item) for item in exports],
        events=[RunEventDTO(**item) for item in events],
        audit_events=[RunAuditEventDTO(**item) for item in audit_events],
        run_metrics=RunMetricsDTO(
            duration_s=float(metrics.get('duration_s', 0.0) or 0.0),
            llm_calls=int(metrics.get('llm_calls', 0) or 0),
            tool_calls=int(metrics.get('tool_calls', 0) or 0),
            total_tokens=int(metrics.get('total_tokens', 0) or 0),
            success=bool(metrics.get('success', False)),
        ),
        actions=RunActionAvailabilityDTO(
            can_retry=can_retry,
            can_cancel=can_cancel,
            can_assign=True,
            can_archive=not archived,
            can_change_owner=True,
            can_view_audit=True,
            suggested_next_action='重试失败任务' if can_retry else '取消活跃任务' if can_cancel else '查看导出物' if status == 'completed' else '分配负责人',
            product_route=f'/stocks/{stock_code}' if stock_code else '',
            history_route=f'/stocks/{stock_code}/history' if stock_code else '',
            exports_route=f'/stocks/{stock_code}/exports' if stock_code else '',
        ),
        observability=RunObservabilityDTO(
            event_count=len(events),
            artifact_count=len(exports),
            has_error=bool(getattr(run, 'error', '') or status == 'failed'),
            latest_signal=latest_signal,
            owner_label=owner or '未分配',
            archive_label='已归档' if archived else '活跃',
            retry_lineage=str(getattr(run, 'retry_of_run_id', '') or ''),
            recovery_status=str(getattr(run, 'recovery_status', 'normal') or 'normal'),
            stale_after_restart=bool(getattr(run, 'stale_after_restart', False)),
            attempts=int(getattr(run, 'attempts', 0) or 0),
            max_attempts=int(getattr(run, 'max_attempts', 2) or 2),
            worker_id=str(getattr(run, 'worker_id', '') or ''),
            locked_at=str(getattr(run, 'locked_at', '') or ''),
            next_retry_at=str(getattr(run, 'next_retry_at', '') or ''),
        ),
    )
