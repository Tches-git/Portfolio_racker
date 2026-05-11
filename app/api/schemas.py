"""对外 API DTO。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class StoreHealthResponse(BaseModel):
    backend: str = ""
    integrity: str = ""
    schema_version: int = 0
    journal_mode: str = ""
    row_count: int = 0
    backup_available: bool = False
    last_backup_path: str = ""


class StoreBackupResponse(BaseModel):
    backup_path: str = ""


class OpsMetricsResponse(BaseModel):
    ops_status: str = "healthy"
    total_runs: int = 0
    active_runs: int = 0
    failed_runs: int = 0
    failure_rate: float = 0.0
    avg_duration_s: float = 0.0
    p95_duration_s: float = 0.0
    alert_count: int = 0
    alerts: list[str] = Field(default_factory=list)
    recent_events: list[dict[str, str]] = Field(default_factory=list)


class StockIdentityDTO(BaseModel):
    code: str
    name: str = ""
    industry: str = ""


class ReportSummaryDTO(BaseModel):
    rating: str = ""
    rating_score: float = 0.0
    conclusion_brief: str = ""


class ValuationSummaryDTO(BaseModel):
    per_share_value: float = 0.0
    current_price: float = 0.0
    upside: float = 0.0


class QualitySummaryDTO(BaseModel):
    source_reference_count: int = 0
    placeholder_source_count: int = 0


class RunMetricsDTO(BaseModel):
    duration_s: float = 0.0
    llm_calls: int = 0
    tool_calls: int = 0
    total_tokens: int = 0
    success: bool = False


class ExportArtifactDTO(BaseModel):
    kind: str
    filename: str
    path: str
    download_url: str = ""


class DeliverySummaryDTO(BaseModel):
    available_kinds: list[str] = Field(default_factory=list)
    previewable_count: int = 0
    downloadable_count: int = 0
    latest_export_filename: str = ""
    contract_path: str = "/api/v1/exports/{filename}"


class LatestReportResponse(BaseModel):
    stock: StockIdentityDTO
    summary: ReportSummaryDTO
    valuation: ValuationSummaryDTO
    quality: QualitySummaryDTO
    run_metrics: RunMetricsDTO
    exports: list[ExportArtifactDTO] = Field(default_factory=list)
    delivery: DeliverySummaryDTO = Field(default_factory=DeliverySummaryDTO)
    generated_at: str = ""


class HistoryRecordDTO(BaseModel):
    stock_code: str
    stock_name: str
    timestamp: str
    rating: str = ""
    rating_score: float = 0.0
    conclusion: str = ""
    risk_count: int = 0
    risk_summary: str = ""
    source_reference_count: int = 0
    placeholder_source_count: int = 0
    dcf_per_share: float = 0.0
    dcf_upside: float = 0.0


class StockMemoryDTO(BaseModel):
    timestamp: str
    thesis: str = ""
    rating: str = ""
    target_range: str = ""
    valuation_summary: str = ""
    historical_delta: str = ""
    conflict_flag: bool = False
    conflict_reason: str = ""
    key_risks: list[str] = Field(default_factory=list)
    catalysts: list[str] = Field(default_factory=list)


class HistoryInsightDTO(BaseModel):
    conflict_count: int = 0
    latest_conflict_reason: str = ""
    rating_drift_summary: str = ""
    thesis_stability_score: float = 0.0
    repeated_risk_patterns: list[str] = Field(default_factory=list)
    repeated_catalyst_patterns: list[str] = Field(default_factory=list)
    memory_pattern_summary: str = ""


class StockHistoryResponse(BaseModel):
    stock: StockIdentityDTO
    records: list[HistoryRecordDTO] = Field(default_factory=list)
    memory: list[StockMemoryDTO] = Field(default_factory=list)
    insights: HistoryInsightDTO = Field(default_factory=HistoryInsightDTO)


class StockNewsItemDTO(BaseModel):
    title: str = ""
    content: str = ""
    time: str = ""
    source: str = ""
    url: str = ""
    channel: str = ""


class StockNewsResponse(BaseModel):
    stock_code: str
    items: list[StockNewsItemDTO] = Field(default_factory=list)
    total: int = 0


class MarketEventDTO(BaseModel):
    event_id: str
    stock_code: str
    stock_name: str = ""
    title: str = ""
    summary: str = ""
    source: str = ""
    provider: str = ""
    url: str = ""
    published_at: str = ""
    collected_at: str = ""
    event_type: str = "other"
    sentiment: str = "neutral"
    impact_level: str = "low"
    impact_scope: str = "sentiment"
    confidence: float = 0.0
    reason: str = ""
    channel: str = ""
    retrieval_mode: str = ""
    evidence_type: str = ""
    is_placeholder: bool = False
    related_sources: list[dict[str, str]] = Field(default_factory=list)
    is_duplicate: bool = False
    parent_event_id: str = ""
    status: str = "new"
    status_updated_at: str = ""
    status_note: str = ""


class MarketEventListResponse(BaseModel):
    items: list[MarketEventDTO] = Field(default_factory=list)
    total: int = 0
    high_impact_count: int = 0
    placeholder_count: int = 0
    duplicate_count: int = 0
    source_count: int = 0
    mode: str = "realtime"


class StockEventTimelineResponse(MarketEventListResponse):
    stock_code: str
    stock_name: str = ""


class TrackingAlertDTO(BaseModel):
    alert_id: str
    stock_code: str
    event_id: str
    alert_type: str = "high_impact"
    title: str = ""
    message: str = ""
    severity: str = "medium"
    status: str = "open"
    created_at: str = ""
    suggested_action: str = ""


class TrackingAlertListResponse(BaseModel):
    items: list[TrackingAlertDTO] = Field(default_factory=list)
    total: int = 0
    high_severity_count: int = 0
    risk_alert_count: int = 0
    source_degraded_count: int = 0


class DailyBriefingResponse(BaseModel):
    title: str = ""
    summary: str = ""
    generated_at: str = ""
    total_events: int = 0
    high_impact_count: int = 0
    negative_event_count: int = 0
    source_count: int = 0
    key_events: list[MarketEventDTO] = Field(default_factory=list)
    alerts: list[TrackingAlertDTO] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    review_required_events: list[MarketEventDTO] = Field(default_factory=list)


class WatchlistDTO(BaseModel):
    watchlist_id: str
    name: str
    stock_codes: list[str] = Field(default_factory=list)
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    last_refreshed_at: str = ""


class WatchlistListResponse(BaseModel):
    items: list[WatchlistDTO] = Field(default_factory=list)
    total: int = 0


class WatchlistImpactStockDTO(BaseModel):
    stock_code: str
    stock_name: str = ""
    event_count: int = 0
    high_impact_count: int = 0
    latest_event_at: str = ""


class WatchlistSummaryDTO(BaseModel):
    stock_count: int = 0
    event_count: int = 0
    high_impact_count: int = 0
    alert_count: int = 0
    high_severity_count: int = 0
    source_count: int = 0
    placeholder_count: int = 0
    last_refreshed_at: str = ""
    impacted_stocks: list[WatchlistImpactStockDTO] = Field(default_factory=list)


class WatchlistDetailResponse(BaseModel):
    watchlist: WatchlistDTO
    events: MarketEventListResponse = Field(default_factory=MarketEventListResponse)
    alerts: TrackingAlertListResponse = Field(default_factory=TrackingAlertListResponse)
    briefing: DailyBriefingResponse = Field(default_factory=DailyBriefingResponse)
    summary: WatchlistSummaryDTO = Field(default_factory=WatchlistSummaryDTO)


class WatchlistCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    stock_codes: list[str] = Field(min_length=1)
    description: str = ""


class EventAnalyzeRequest(BaseModel):
    note: str = ""


class EventStatusUpdateRequest(BaseModel):
    status: str = Field(min_length=1)
    note: str = ""


class AnalysisRunCreateRequest(BaseModel):
    stock_code: str = Field(min_length=1)


class BatchRunCreateRequest(BaseModel):
    stock_codes: list[str] = Field(min_length=1)


class BatchRunCreateResponse(BaseModel):
    items: list['AnalysisRunResponse'] = Field(default_factory=list)
    total: int = 0


class RunAssignmentRequest(BaseModel):
    owner: str = Field(min_length=1)


class RunActorDTO(BaseModel):
    actor: str = "system"
    role: str = "admin"


class RunAuditEventDTO(BaseModel):
    timestamp: str = ""
    actor: str = ""
    role: str = ""
    action: str = ""
    detail: str = ""


class RunEventDTO(BaseModel):
    timestamp: str = ""
    status: str = ""
    event: str = ""
    detail: str = ""


class RunActionAvailabilityDTO(BaseModel):
    can_retry: bool = False
    can_cancel: bool = False
    can_assign: bool = True
    can_archive: bool = True
    can_change_owner: bool = True
    can_view_audit: bool = True
    suggested_next_action: str = ""
    product_route: str = ""
    history_route: str = ""
    exports_route: str = ""


class RunObservabilityDTO(BaseModel):
    event_count: int = 0
    artifact_count: int = 0
    has_error: bool = False
    latest_signal: str = ""
    owner_label: str = "未分配"
    archive_label: str = "活跃"
    retry_lineage: str = ""
    recovery_status: str = "normal"
    stale_after_restart: bool = False
    attempts: int = 0
    max_attempts: int = 2
    worker_id: str = ""
    locked_at: str = ""
    next_retry_at: str = ""


class AnalysisRunResponse(BaseModel):
    run_id: str
    stock_code: str
    status: str = "queued"
    created_at: str = ""
    updated_at: str = ""
    detail: str = ""
    last_event: str = ""
    error: str = ""
    owner: str = ""
    owner_role: str = ""
    archived: bool = False
    retry_of_run_id: str = ""
    latest_report_url: str = ""
    history_url: str = ""
    exports: list[ExportArtifactDTO] = Field(default_factory=list)
    events: list[RunEventDTO] = Field(default_factory=list)
    audit_events: list[RunAuditEventDTO] = Field(default_factory=list)
    run_metrics: RunMetricsDTO = Field(default_factory=RunMetricsDTO)
    actions: RunActionAvailabilityDTO = Field(default_factory=RunActionAvailabilityDTO)
    observability: RunObservabilityDTO = Field(default_factory=RunObservabilityDTO)


class RunStockGroupDTO(BaseModel):
    stock_code: str
    total: int = 0
    active_count: int = 0
    failed_count: int = 0
    archived_count: int = 0
    latest_run_id: str = ""
    latest_status: str = ""
    latest_updated_at: str = ""


class WorkspaceSnapshotDTO(BaseModel):
    tracked_stocks: list[str] = Field(default_factory=list)
    most_active_stock: str = ""
    latest_completed_stock: str = ""
    failed_stock_count: int = 0
    history_backed_stock_count: int = 0
    recommended_concurrency: int = 3
    active_limit_reached: bool = False
    observability_status: str = "basic"
    collaboration_ready: bool = False
    collaborator_count: int = 0
    audited_action_count: int = 0
    archived_run_count: int = 0
    stale_run_count: int = 0
    recovery_status: str = "normal"
    worker_count: int = 1
    retry_scheduled_count: int = 0
    queue_mode: str = "in_process"
    store_backend: str = "sqlite"
    schema_version: int = 0
    wal_enabled: bool = False
    backup_available: bool = False
    last_backup_path: str = ""
    ops_status: str = "healthy"
    alert_count: int = 0
    failure_rate: float = 0.0
    avg_duration_s: float = 0.0
    p95_duration_s: float = 0.0


class WorkspaceStockDTO(BaseModel):
    code: str
    name: str = ""
    count: int = 0
    latest: str = ""


class WorkspaceStocksResponse(BaseModel):
    items: list[WorkspaceStockDTO] = Field(default_factory=list)


class ReportDiffResponse(BaseModel):
    stock_code: str
    base_timestamp: str = ""
    compare_timestamp: str = ""
    rating_changed: bool = False
    rating_delta: float = 0.0
    upside_delta: float = 0.0
    risk_count_delta: int = 0
    conclusion_changed: bool = False
    summary: str = ""


class AnalysisRunListResponse(BaseModel):
    items: list[AnalysisRunResponse] = Field(default_factory=list)
    total: int = 0
    queued_count: int = 0
    running_count: int = 0
    completed_count: int = 0
    failed_count: int = 0
    stock_groups: list[RunStockGroupDTO] = Field(default_factory=list)
    workspace: WorkspaceSnapshotDTO = Field(default_factory=WorkspaceSnapshotDTO)
