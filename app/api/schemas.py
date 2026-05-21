"""对外 API DTO。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class AuthRegisterRequest(BaseModel):
    email: str = Field(min_length=3)
    username: str = ""
    password: str = Field(min_length=8)


class AuthLoginRequest(BaseModel):
    email_or_username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AuthUserDTO(BaseModel):
    id: str
    email: str
    username: str
    role: str = "user"
    is_active: bool = True
    created_at: str = ""
    last_login_at: str = ""


class AuthResponse(BaseModel):
    user: AuthUserDTO


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
    citation_coverage_rate: float = 0.0
    unsupported_claim_count: int = 0
    source_reference_count: int = 0
    retrieval_topk_hit_rate: float = 0.0
    rerank_selected_count: int = 0
    multi_agent_role_count: int = 0
    multi_agent_completed_count: int = 0
    multi_agent_failed_count: int = 0
    citation_audit_coverage_rate: float = 0.0


class MultiAgentRoleTraceDTO(BaseModel):
    role_id: str = ""
    role_name: str = ""
    status: str = "pending"
    summary: str = ""
    tool_call_count: int = 0
    duration_s: float = 0.0
    fallback_used: bool = False
    error: str = ""
    phase: str = "pre_write"
    objective: str = ""
    allowed_tools: list[str] = Field(default_factory=list)
    input_summary: str = ""
    quality_checks: list[str] = Field(default_factory=list)


class MultiAgentTraceDTO(BaseModel):
    mode: str = "autogen_graphflow"
    role_count: int = 0
    completed_role_count: int = 0
    failed_role_count: int = 0
    roles: list[MultiAgentRoleTraceDTO] = Field(default_factory=list)


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


class StockSearchItemDTO(BaseModel):
    code: str
    name: str = ""
    match_text: str = ""


class StockSearchResponse(BaseModel):
    query: str = ""
    items: list[StockSearchItemDTO] = Field(default_factory=list)
    total: int = 0


class MarketDailyBarDTO(BaseModel):
    date: str = ""
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    amount: float = 0.0
    change_pct: float = 0.0
    turnover: float = 0.0


class MarketQuoteDTO(BaseModel):
    stock_code: str = ""
    stock_name: str = ""
    price: float = 0.0
    change: float = 0.0
    change_pct: float = 0.0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    previous_close: float = 0.0
    volume: float = 0.0
    amount: float = 0.0
    turnover: float = 0.0
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    updated_at: str = ""
    source_status: str = "degraded"
    provider: str = ""


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
    duplicate_count: int = 0
    status: str = "new"
    status_updated_at: str = ""
    status_note: str = ""
    status_actor: str = ""


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
    stock_name: str = ""
    event_id: str
    rule_id: str = ""
    rule_name: str = ""
    alert_type: str = "high_impact"
    title: str = ""
    message: str = ""
    severity: str = "medium"
    priority: str = "P2"
    status: str = "open"
    created_at: str = ""
    suggested_action: str = ""
    explanation: str = ""
    handled_at: str = ""
    handled_by: str = ""
    handling_note: str = ""


class AlertRuleDTO(BaseModel):
    rule_id: str
    name: str
    description: str = ""
    alert_type: str = ""
    severity: str = "medium"
    priority: str = "P2"
    enabled: bool = True


class AlertRuleListResponse(BaseModel):
    items: list[AlertRuleDTO] = Field(default_factory=list)
    total: int = 0


class TrackingAlertListResponse(BaseModel):
    items: list[TrackingAlertDTO] = Field(default_factory=list)
    total: int = 0
    high_severity_count: int = 0
    risk_alert_count: int = 0
    source_degraded_count: int = 0
    manual_review_count: int = 0
    severity_counts: dict[str, int] = Field(default_factory=dict)
    alert_type_counts: dict[str, int] = Field(default_factory=dict)
    rule_counts: dict[str, int] = Field(default_factory=dict)


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
    alert_count: int = 0
    risk_score: int = 0
    risk_level: str = "low"
    priority_action: str = ""
    latest_event_at: str = ""


class WatchlistSummaryDTO(BaseModel):
    stock_count: int = 0
    event_count: int = 0
    high_impact_count: int = 0
    alert_count: int = 0
    high_severity_count: int = 0
    source_count: int = 0
    placeholder_count: int = 0
    risk_score: int = 0
    risk_level: str = "low"
    risk_summary: str = ""
    open_alert_count: int = 0
    handled_event_count: int = 0
    converted_event_count: int = 0
    manual_review_count: int = 0
    processing_rate: float = 0.0
    dominant_rules: list[str] = Field(default_factory=list)
    priority_actions: list[str] = Field(default_factory=list)
    last_refreshed_at: str = ""
    impacted_stocks: list[WatchlistImpactStockDTO] = Field(default_factory=list)


class WatchlistMarketSnapshotDTO(BaseModel):
    stock_code: str = ""
    stock_name: str = ""
    quote: MarketQuoteDTO = Field(default_factory=MarketQuoteDTO)
    trend_30d: list[MarketDailyBarDTO] = Field(default_factory=list)
    trend_90d: list[MarketDailyBarDTO] = Field(default_factory=list)
    trend_180d: list[MarketDailyBarDTO] = Field(default_factory=list)
    source_status: str = "degraded"
    fallback_message: str = ""
    suggestion: str = ""


class WatchlistDetailResponse(BaseModel):
    watchlist: WatchlistDTO
    events: MarketEventListResponse = Field(default_factory=MarketEventListResponse)
    alerts: TrackingAlertListResponse = Field(default_factory=TrackingAlertListResponse)
    briefing: DailyBriefingResponse = Field(default_factory=DailyBriefingResponse)
    summary: WatchlistSummaryDTO = Field(default_factory=WatchlistSummaryDTO)
    market_snapshots: list[WatchlistMarketSnapshotDTO] = Field(default_factory=list)
    market_updated_at: str = ""
    market_fallback_message: str = ""


class EventImpactReplayItemDTO(BaseModel):
    event_id: str = ""
    title: str = ""
    published_at: str = ""
    event_type: str = ""
    impact_level: str = ""
    sentiment: str = ""
    status: str = ""
    run_id: str = ""
    run_status: str = ""
    event_commentary_url: str = ""
    review_line: str = ""


class EventImpactReviewResponse(BaseModel):
    stock_code: str = ""
    stock_name: str = ""
    total_events: int = 0
    high_impact_count: int = 0
    converted_count: int = 0
    event_driven_run_count: int = 0
    latest_event_at: str = ""
    dominant_event_types: list[str] = Field(default_factory=list)
    summary: str = ""
    replay_items: list[EventImpactReplayItemDTO] = Field(default_factory=list)


class EventBacktestItemDTO(BaseModel):
    event_id: str = ""
    title: str = ""
    published_at: str = ""
    event_type: str = ""
    impact_level: str = ""
    sentiment: str = ""
    base_date: str = ""
    base_close: float = 0.0
    returns: dict[str, float] = Field(default_factory=dict)
    max_drawdown: float = 0.0
    volume_change_pct: float = 0.0


class EventBacktestGroupDTO(BaseModel):
    key: str = ""
    label: str = ""
    event_count: int = 0
    positive_rate: float = 0.0
    average_returns: dict[str, float] = Field(default_factory=dict)
    average_max_drawdown: float = 0.0


class EventBacktestResponse(BaseModel):
    stock_code: str = ""
    stock_name: str = ""
    windows: list[int] = Field(default_factory=lambda: [1, 3, 5, 10])
    total_events: int = 0
    matched_event_count: int = 0
    fallback_message: str = ""
    groups: list[EventBacktestGroupDTO] = Field(default_factory=list)
    items: list[EventBacktestItemDTO] = Field(default_factory=list)


class WatchlistCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    stock_codes: list[str] = Field(min_length=1)
    description: str = ""


class WatchlistUpdateRequest(BaseModel):
    name: str | None = None
    stock_codes: list[str] | None = None
    description: str | None = None


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


class RunEventContextDTO(BaseModel):
    event_id: str = ""
    stock_code: str = ""
    stock_name: str = ""
    title: str = ""
    summary: str = ""
    source: str = ""
    provider: str = ""
    url: str = ""
    published_at: str = ""
    collected_at: str = ""
    event_type: str = ""
    sentiment: str = ""
    impact_level: str = ""
    impact_scope: str = ""
    confidence: float = 0.0
    reason: str = ""
    channel: str = ""
    retrieval_mode: str = ""
    evidence_type: str = ""
    related_sources: list[dict[str, str]] = Field(default_factory=list)
    status: str = ""
    status_note: str = ""
    note: str = ""


class RunEventReportSummaryDTO(BaseModel):
    trigger_label: str = ""
    thesis: str = ""
    impact_direction: str = ""
    impact_level: str = ""
    impact_scope: str = ""
    priority: str = ""
    review_status: str = ""
    action: str = ""
    report_delta_hint: str = ""
    related_source_count: int = 0
    event_commentary_filename: str = ""
    event_commentary_url: str = ""


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
    stock_name: str = ""
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
    event_context: RunEventContextDTO = Field(default_factory=RunEventContextDTO)
    event_report_summary: RunEventReportSummaryDTO = Field(default_factory=RunEventReportSummaryDTO)
    audit_events: list[RunAuditEventDTO] = Field(default_factory=list)
    run_metrics: RunMetricsDTO = Field(default_factory=RunMetricsDTO)
    multi_agent_trace: MultiAgentTraceDTO = Field(default_factory=MultiAgentTraceDTO)
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


class WorkbenchActionDTO(BaseModel):
    label: str = ""
    href: str = ""
    method: str = "GET"
    action_type: str = ""
    target_id: str = ""
    variant: str = "secondary"


class MarketWorkbenchResponse(BaseModel):
    stock_code: str
    stock_name: str = ""
    range: str = "90d"
    quote: MarketQuoteDTO = Field(default_factory=MarketQuoteDTO)
    daily_bars: list[MarketDailyBarDTO] = Field(default_factory=list)
    fallback_message: str = ""
    actions: list[WorkbenchActionDTO] = Field(default_factory=list)


class DashboardSetupDTO(BaseModel):
    title: str = "创建第一个组合"
    description: str = "添加一组股票后，系统会围绕组合生成风险、事件、预警和研报任务入口。"
    suggested_stock_codes: list[str] = Field(default_factory=list)
    primary_action: WorkbenchActionDTO = Field(default_factory=WorkbenchActionDTO)


class DashboardPortfolioSummaryDTO(BaseModel):
    watchlist_count: int = 0
    stock_count: int = 0
    event_count: int = 0
    alert_count: int = 0
    high_impact_count: int = 0
    manual_review_count: int = 0
    risk_score: int = 0
    risk_level: str = "low"
    risk_summary: str = ""
    processing_rate: float = 0.0
    primary_watchlist_id: str = ""


class DashboardResponse(BaseModel):
    mode: str = "setup"
    setup: DashboardSetupDTO = Field(default_factory=DashboardSetupDTO)
    watchlists: WatchlistListResponse = Field(default_factory=WatchlistListResponse)
    portfolio_summary: DashboardPortfolioSummaryDTO = Field(default_factory=DashboardPortfolioSummaryDTO)
    risk_queue: TrackingAlertListResponse = Field(default_factory=TrackingAlertListResponse)
    today_briefing: DailyBriefingResponse = Field(default_factory=DailyBriefingResponse)
    latest_events: MarketEventListResponse = Field(default_factory=MarketEventListResponse)
    recent_runs: AnalysisRunListResponse = Field(default_factory=AnalysisRunListResponse)
    actions: list[WorkbenchActionDTO] = Field(default_factory=list)


class EventWorkbenchResponse(BaseModel):
    view: str = "events"
    events: MarketEventListResponse = Field(default_factory=MarketEventListResponse)
    alerts: TrackingAlertListResponse = Field(default_factory=TrackingAlertListResponse)
    filters: dict[str, str] = Field(default_factory=dict)
    selected_event: MarketEventDTO | None = None
    actions: list[WorkbenchActionDTO] = Field(default_factory=list)


class StockWorkbenchResponse(BaseModel):
    stock_code: str
    stock_name: str = ""
    active_tab: str = "summary"
    is_tracked: bool = False
    latest_report: LatestReportResponse | None = None
    history: StockHistoryResponse | None = None
    timeline: StockEventTimelineResponse = Field(default_factory=lambda: StockEventTimelineResponse(stock_code=""))
    impact_review: EventImpactReviewResponse = Field(default_factory=EventImpactReviewResponse)
    event_backtest: EventBacktestResponse = Field(default_factory=EventBacktestResponse)
    related_watchlists: list[WatchlistDTO] = Field(default_factory=list)
    related_runs: AnalysisRunListResponse = Field(default_factory=AnalysisRunListResponse)
    exports: list[ExportArtifactDTO] = Field(default_factory=list)
    actions: list[WorkbenchActionDTO] = Field(default_factory=list)


class RunWorkbenchResponse(BaseModel):
    runs: AnalysisRunListResponse = Field(default_factory=AnalysisRunListResponse)
    selected_run: AnalysisRunResponse | None = None
    actions: list[WorkbenchActionDTO] = Field(default_factory=list)


class QualityMetricDTO(BaseModel):
    label: str = ""
    value: str = ""
    hint: str = ""


class QualityWorkbenchResponse(BaseModel):
    generated_at: str = ""
    test_count: int = 0
    tracking_eval: dict[str, object] = Field(default_factory=dict)
    agent_eval: dict[str, object] = Field(default_factory=dict)
    financial_qa_eval: dict[str, object] = Field(default_factory=dict)
    rag_eval: dict[str, object] = Field(default_factory=dict)
    run_metrics: OpsMetricsResponse = Field(default_factory=OpsMetricsResponse)
    smoke_status: str = "待验证"
    metrics: list[QualityMetricDTO] = Field(default_factory=list)
