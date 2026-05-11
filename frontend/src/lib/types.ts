export type LatestReportResponse = {
  stock: { code: string; name: string; industry: string }
  summary: { rating: string; rating_score: number; conclusion_brief: string }
  valuation: { per_share_value: number; current_price: number; upside: number }
  quality: { source_reference_count: number; placeholder_source_count: number }
  run_metrics: { duration_s: number; llm_calls: number; tool_calls: number; total_tokens: number; success: boolean }
  exports: Array<{ kind: string; filename: string; path: string; download_url: string }>
  delivery: { available_kinds: string[]; previewable_count: number; downloadable_count: number; latest_export_filename: string; contract_path: string }
  generated_at: string
}

export type StockNewsResponse = {
  stock_code: string
  total: number
  items: Array<{ title: string; content: string; time: string; source: string; url: string; channel: string }>
}

export type MarketEvent = {
  event_id: string
  stock_code: string
  stock_name: string
  title: string
  summary: string
  source: string
  provider: string
  url: string
  published_at: string
  collected_at: string
  event_type: string
  sentiment: 'positive' | 'negative' | 'neutral' | 'uncertain'
  impact_level: 'high' | 'medium' | 'low'
  impact_scope: string
  confidence: number
  reason: string
  channel: string
  retrieval_mode: string
  evidence_type: string
  is_placeholder: boolean
  related_sources: Array<{ title: string; source: string; provider: string; url: string; time: string }>
  is_duplicate: boolean
  parent_event_id: string
}

export type MarketEventListResponse = {
  items: MarketEvent[]
  total: number
  high_impact_count: number
  placeholder_count: number
  duplicate_count: number
  source_count: number
  mode: string
}

export type StockEventTimelineResponse = MarketEventListResponse & {
  stock_code: string
  stock_name: string
}

export type TrackingAlert = {
  alert_id: string
  stock_code: string
  event_id: string
  alert_type: string
  title: string
  message: string
  severity: 'high' | 'medium' | 'low'
  status: string
  created_at: string
  suggested_action: string
}

export type TrackingAlertListResponse = {
  items: TrackingAlert[]
  total: number
  high_severity_count: number
  risk_alert_count: number
  source_degraded_count: number
}

export type DailyBriefingResponse = {
  title: string
  summary: string
  generated_at: string
  total_events: number
  high_impact_count: number
  negative_event_count: number
  source_count: number
  key_events: MarketEvent[]
  alerts: TrackingAlert[]
  suggested_actions: string[]
  themes: string[]
  review_required_events: MarketEvent[]
}

export type Watchlist = {
  watchlist_id: string
  name: string
  stock_codes: string[]
  description: string
  created_at: string
  updated_at: string
}

export type WatchlistListResponse = {
  items: Watchlist[]
  total: number
}

export type WatchlistCreateRequest = {
  name: string
  stock_codes: string[]
  description?: string
}

export type StockHistoryResponse = {
  stock: { code: string; name: string; industry: string }
  records: Array<{
    stock_code: string
    stock_name: string
    timestamp: string
    rating: string
    rating_score: number
    conclusion: string
    risk_count: number
    risk_summary: string
    source_reference_count: number
    placeholder_source_count: number
    dcf_per_share: number
    dcf_upside: number
  }>
  memory: Array<{
    timestamp: string
    thesis: string
    rating: string
    target_range: string
    valuation_summary: string
    historical_delta: string
    conflict_flag: boolean
    conflict_reason: string
    key_risks: string[]
    catalysts: string[]
  }>
  insights: {
    conflict_count: number
    latest_conflict_reason: string
    rating_drift_summary: string
    thesis_stability_score: number
    repeated_risk_patterns: string[]
    repeated_catalyst_patterns: string[]
    memory_pattern_summary: string
  }
}

export type AnalysisRunResponse = {
  run_id: string
  stock_code: string
  status: 'queued' | 'running' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  detail: string
  last_event: string
  error: string
  owner: string
  owner_role: string
  archived: boolean
  retry_of_run_id: string
  latest_report_url: string
  history_url: string
  exports: Array<{ kind: string; filename: string; path: string; download_url: string }>
  events: Array<{ timestamp: string; status: string; event: string; detail: string }>
  audit_events: Array<{ timestamp: string; actor: string; role: string; action: string; detail: string }>
  run_metrics: { duration_s: number; llm_calls: number; tool_calls: number; total_tokens: number; success: boolean }
  actions: { can_retry: boolean; can_cancel: boolean; can_assign: boolean; can_archive: boolean; can_change_owner: boolean; can_view_audit: boolean; suggested_next_action: string; product_route: string; history_route: string; exports_route: string }
  observability: { event_count: number; artifact_count: number; has_error: boolean; latest_signal: string; owner_label: string; archive_label: string; retry_lineage: string; recovery_status: string; stale_after_restart: boolean; attempts: number; max_attempts: number; worker_id: string; locked_at: string; next_retry_at: string }
}

export type WorkspaceStocksResponse = {
  items: Array<{ code: string; name: string; count: number; latest: string }>
}

export type BatchRunCreateResponse = {
  items: AnalysisRunResponse[]
  total: number
}

export type ReportDiffResponse = {
  stock_code: string
  base_timestamp: string
  compare_timestamp: string
  rating_changed: boolean
  rating_delta: number
  upside_delta: number
  risk_count_delta: number
  conclusion_changed: boolean
  summary: string
}

export type AnalysisRunListResponse = {
  items: AnalysisRunResponse[]
  total: number
  queued_count: number
  running_count: number
  completed_count: number
  failed_count: number
  stock_groups: Array<{ stock_code: string; total: number; active_count: number; failed_count: number; archived_count: number; latest_run_id: string; latest_status: string; latest_updated_at: string }>
  workspace: { tracked_stocks: string[]; most_active_stock: string; latest_completed_stock: string; failed_stock_count: number; history_backed_stock_count: number; recommended_concurrency: number; active_limit_reached: boolean; observability_status: string; collaboration_ready: boolean; collaborator_count: number; audited_action_count: number; archived_run_count: number; stale_run_count: number; recovery_status: string; worker_count: number; retry_scheduled_count: number; queue_mode: string; store_backend: string; schema_version: number; wal_enabled: boolean; backup_available: boolean; last_backup_path: string; ops_status: string; alert_count: number; failure_rate: number; avg_duration_s: number; p95_duration_s: number }
}
