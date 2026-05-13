export type AuthUser = {
  id: string
  email: string
  username: string
  role: string
  is_active: boolean
  created_at: string
  last_login_at: string
}

export type AuthResponse = {
  user: AuthUser
}

export type AuthLoginRequest = {
  email_or_username: string
  password: string
}

export type AuthRegisterRequest = {
  email: string
  username: string
  password: string
}

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
  status: 'new' | 'reviewed' | 'ignored' | 'converted_to_report'
  status_updated_at: string
  status_note: string
  status_actor: string
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

export type MarketDailyBar = {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
  amount: number
  change_pct: number
  turnover: number
}

export type MarketQuote = {
  stock_code: string
  stock_name: string
  price: number
  change: number
  change_pct: number
  open: number
  high: number
  low: number
  previous_close: number
  volume: number
  amount: number
  turnover: number
  market_cap: number
  pe_ratio: number
  pb_ratio: number
  updated_at: string
  source_status: string
  provider: string
}

export type MarketWorkbenchResponse = {
  stock_code: string
  stock_name: string
  range: '30d' | '90d' | '180d'
  quote: MarketQuote
  daily_bars: MarketDailyBar[]
  fallback_message: string
  actions: WorkbenchAction[]
}

export type TrackingAlert = {
  alert_id: string
  stock_code: string
  event_id: string
  rule_id: string
  rule_name: string
  alert_type: string
  title: string
  message: string
  severity: 'high' | 'medium' | 'low'
  priority: string
  status: string
  created_at: string
  suggested_action: string
  explanation: string
  handled_at: string
  handled_by: string
  handling_note: string
}

export type AlertRule = {
  rule_id: string
  name: string
  description: string
  alert_type: string
  severity: 'high' | 'medium' | 'low'
  priority: string
  enabled: boolean
}

export type AlertRuleListResponse = {
  items: AlertRule[]
  total: number
}

export type TrackingAlertListResponse = {
  items: TrackingAlert[]
  total: number
  high_severity_count: number
  risk_alert_count: number
  source_degraded_count: number
  manual_review_count: number
  severity_counts: Record<string, number>
  alert_type_counts: Record<string, number>
  rule_counts: Record<string, number>
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
  last_refreshed_at: string
}

export type WatchlistListResponse = {
  items: Watchlist[]
  total: number
}

export type WatchlistImpactStock = {
  stock_code: string
  stock_name: string
  event_count: number
  high_impact_count: number
  alert_count: number
  risk_score: number
  risk_level: string
  priority_action: string
  latest_event_at: string
}

export type WatchlistSummary = {
  stock_count: number
  event_count: number
  high_impact_count: number
  alert_count: number
  high_severity_count: number
  source_count: number
  placeholder_count: number
  risk_score: number
  risk_level: string
  risk_summary: string
  open_alert_count: number
  handled_event_count: number
  converted_event_count: number
  manual_review_count: number
  processing_rate: number
  dominant_rules: string[]
  priority_actions: string[]
  last_refreshed_at: string
  impacted_stocks: WatchlistImpactStock[]
}

export type WatchlistDetailResponse = {
  watchlist: Watchlist
  events: MarketEventListResponse
  alerts: TrackingAlertListResponse
  briefing: DailyBriefingResponse
  summary: WatchlistSummary
}

export type EventImpactReviewResponse = {
  stock_code: string
  stock_name: string
  total_events: number
  high_impact_count: number
  converted_count: number
  event_driven_run_count: number
  latest_event_at: string
  dominant_event_types: string[]
  summary: string
  replay_items: Array<{
    event_id: string
    title: string
    published_at: string
    event_type: string
    impact_level: string
    sentiment: string
    status: string
    run_id: string
    run_status: string
    event_commentary_url: string
    review_line: string
  }>
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
  event_context: {
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
    sentiment: string
    impact_level: string
    impact_scope: string
    confidence: number
    reason: string
    channel: string
    retrieval_mode: string
    evidence_type: string
    related_sources: Array<Record<string, string>>
    status: string
    status_note: string
    note: string
  }
  event_report_summary: {
    trigger_label: string
    thesis: string
    impact_direction: string
    impact_level: string
    impact_scope: string
    priority: string
    review_status: string
    action: string
    report_delta_hint: string
    related_source_count: number
    event_commentary_filename: string
    event_commentary_url: string
  }
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

export type WorkbenchAction = {
  label: string
  href: string
  method: string
  action_type: string
  target_id: string
  variant: string
}

export type DashboardSetup = {
  title: string
  description: string
  suggested_stock_codes: string[]
  primary_action: WorkbenchAction
}

export type DashboardPortfolioSummary = {
  watchlist_count: number
  stock_count: number
  event_count: number
  alert_count: number
  high_impact_count: number
  manual_review_count: number
  risk_score: number
  risk_level: string
  risk_summary: string
  processing_rate: number
  primary_watchlist_id: string
}

export type DashboardResponse = {
  mode: 'setup' | 'active'
  setup: DashboardSetup
  watchlists: WatchlistListResponse
  portfolio_summary: DashboardPortfolioSummary
  risk_queue: TrackingAlertListResponse
  today_briefing: DailyBriefingResponse
  latest_events: MarketEventListResponse
  recent_runs: AnalysisRunListResponse
  actions: WorkbenchAction[]
}

export type EventWorkbenchResponse = {
  view: 'events' | 'alerts'
  events: MarketEventListResponse
  alerts: TrackingAlertListResponse
  filters: Record<string, string>
  selected_event: MarketEvent | null
  actions: WorkbenchAction[]
}

export type StockWorkbenchResponse = {
  stock_code: string
  stock_name: string
  active_tab: 'summary' | 'timeline' | 'history' | 'exports'
  is_tracked: boolean
  latest_report: LatestReportResponse | null
  history: StockHistoryResponse | null
  timeline: StockEventTimelineResponse
  impact_review: EventImpactReviewResponse
  related_watchlists: Watchlist[]
  related_runs: AnalysisRunListResponse
  exports: Array<{ kind: string; filename: string; path: string; download_url: string }>
  actions: WorkbenchAction[]
}

export type RunWorkbenchResponse = {
  runs: AnalysisRunListResponse
  selected_run: AnalysisRunResponse | null
  actions: WorkbenchAction[]
}
