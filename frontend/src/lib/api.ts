import type { AlertRuleListResponse, AnalysisRunListResponse, AnalysisRunResponse, AuthLoginRequest, AuthRegisterRequest, AuthResponse, AuthUser, BatchRunCreateResponse, DailyBriefingResponse, DashboardResponse, EventBacktestResponse, EventImpactReviewResponse, EventWorkbenchResponse, LatestReportResponse, MarketEvent, MarketEventListResponse, MarketWorkbenchResponse, QualityWorkbenchResponse, ReportDiffResponse, RunWorkbenchResponse, StockEventTimelineResponse, StockHistoryResponse, StockNewsResponse, StockSearchResponse, StockWorkbenchResponse, TrackingAlertListResponse, WatchlistCreateRequest, WatchlistDetailResponse, WatchlistListResponse, Watchlist, WatchlistUpdateRequest, WorkspaceStocksResponse } from './types'

export const API_BASE = typeof window === 'undefined'
  ? process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'
  : process.env.NEXT_PUBLIC_API_BASE_URL || ''

export type ApiRequestInit = Omit<RequestInit, 'body'> & {
  body?: BodyInit | object | null
  timeoutMs?: number
}

export class ApiError extends Error {
  status: number
  detail: string

  constructor(message: string, status: number, detail = '') {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

export async function apiFetch<T>(path: string, init: ApiRequestInit = {}, fallbackMessage = '请求失败'): Promise<T> {
  const headers = new Headers(init.headers)
  const body = normalizeBody(init.body, headers)
  const timeoutMs = init.timeoutMs ?? 15000
  const controller = !init.signal && timeoutMs > 0 ? new AbortController() : null
  const timeout = controller ? setTimeout(() => controller.abort(), timeoutMs) : null
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...init,
      body,
      headers,
      cache: init.cache ?? 'no-store',
      credentials: init.credentials ?? 'include',
      signal: init.signal ?? controller?.signal,
    })

    if (!res.ok) {
      throw await buildApiError(res, fallbackMessage)
    }

    if (res.status === 204) {
      return undefined as T
    }
    return res.json()
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError(`${fallbackMessage}：请求超时`, 0, '请求超时')
    }
    throw error
  } finally {
    if (timeout) clearTimeout(timeout)
  }
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError
}

export function sameOriginApiUrl(downloadUrl = '') {
  if (!downloadUrl) return ''
  try {
    const url = new URL(downloadUrl)
    return `${url.pathname}${url.search}${url.hash}`
  } catch {
    return downloadUrl.startsWith('/api/') ? downloadUrl : downloadUrl
  }
}

function normalizeBody(body: ApiRequestInit['body'], headers: Headers): BodyInit | null | undefined {
  if (body === undefined || body === null) return body
  if (typeof body === 'string' || body instanceof FormData || body instanceof URLSearchParams || body instanceof Blob || body instanceof ArrayBuffer) {
    return body
  }
  if (!headers.has('content-type')) {
    headers.set('content-type', 'application/json')
  }
  return JSON.stringify(body)
}

async function buildApiError(res: Response, fallbackMessage: string) {
  let detail = ''
  const contentType = res.headers.get('content-type') || ''
  try {
    if (contentType.includes('application/json')) {
      const payload = await res.json()
      detail = typeof payload?.detail === 'string' ? payload.detail : JSON.stringify(payload?.detail || payload)
    } else {
      detail = await res.text()
    }
  } catch {
    detail = ''
  }
  return new ApiError(detail || fallbackMessage, res.status, detail)
}

export async function fetchCurrentUser(options: ApiRequestInit = {}): Promise<AuthUser | null> {
  try {
    return await apiFetch<AuthUser>('/api/v1/me', options, '获取当前用户失败')
  } catch (error) {
    if (isApiError(error) && error.status === 401) return null
    throw error
  }
}

export async function login(payload: AuthLoginRequest): Promise<AuthResponse> {
  return apiFetch<AuthResponse>('/api/v1/auth/login', { method: 'POST', body: payload }, '登录失败')
}

export async function register(payload: AuthRegisterRequest): Promise<AuthResponse> {
  return apiFetch<AuthResponse>('/api/v1/auth/register', { method: 'POST', body: payload }, '注册失败')
}

export async function logout(): Promise<void> {
  await apiFetch('/api/v1/auth/logout', { method: 'POST' }, '退出登录失败')
}

export async function fetchDashboard(options: ApiRequestInit = {}): Promise<DashboardResponse> {
  return apiFetch<DashboardResponse>('/api/v1/ui/dashboard', options, '获取驾驶舱失败')
}

export async function fetchUiWatchlistDetail(watchlistId: string, options: ApiRequestInit = {}): Promise<WatchlistDetailResponse | null> {
  try {
    return await apiFetch<WatchlistDetailResponse>(`/api/v1/ui/watchlists/${encodeURIComponent(watchlistId)}`, options, '获取组合驾驶舱失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export type EventWorkbenchFilters = {
  view?: 'events' | 'alerts'
  stockCodes?: string[]
  status?: string
  eventType?: string
  impactLevel?: string
  severity?: string
  alertType?: string
  ruleId?: string
  selectedEventId?: string
}

export async function fetchEventWorkbench(filters: EventWorkbenchFilters = {}, options: ApiRequestInit = {}): Promise<EventWorkbenchResponse> {
  const query = new URLSearchParams()
  if (filters.view) query.set('view', filters.view)
  if (filters.stockCodes?.length) query.set('stock_codes', filters.stockCodes.join(','))
  if (filters.status) query.set('status', filters.status)
  if (filters.eventType) query.set('event_type', filters.eventType)
  if (filters.impactLevel) query.set('impact_level', filters.impactLevel)
  if (filters.severity) query.set('severity', filters.severity)
  if (filters.alertType) query.set('alert_type', filters.alertType)
  if (filters.ruleId) query.set('rule_id', filters.ruleId)
  if (filters.selectedEventId) query.set('selected_event_id', filters.selectedEventId)
  const suffix = query.toString()
  return apiFetch<EventWorkbenchResponse>(`/api/v1/ui/events${suffix ? `?${suffix}` : ''}`, options, '获取事件预警工作台失败')
}

export async function fetchStockWorkbench(stockCode: string, tab = 'summary', options: ApiRequestInit = {}): Promise<StockWorkbenchResponse> {
  return apiFetch<StockWorkbenchResponse>(`/api/v1/ui/stocks/${encodeURIComponent(stockCode)}?tab=${encodeURIComponent(tab)}`, options, '获取单股情报中心失败')
}

export async function fetchMarketWorkbench(stockCode: string, range = '90d', options: ApiRequestInit = {}): Promise<MarketWorkbenchResponse> {
  const query = new URLSearchParams()
  query.set('range', range)
  return apiFetch<MarketWorkbenchResponse>(`/api/v1/ui/markets/${encodeURIComponent(stockCode)}?${query.toString()}`, options, '获取行情展示页失败')
}

export async function fetchRunWorkbench(limit = 24, selectedRunId = '', options: ApiRequestInit = {}): Promise<RunWorkbenchResponse> {
  const query = new URLSearchParams()
  query.set('limit', String(limit))
  if (selectedRunId) query.set('selected_run_id', selectedRunId)
  return apiFetch<RunWorkbenchResponse>(`/api/v1/ui/runs?${query.toString()}`, options, '获取任务交付中心失败')
}

export async function fetchQualityWorkbench(options: ApiRequestInit = {}): Promise<QualityWorkbenchResponse> {
  return apiFetch<QualityWorkbenchResponse>('/api/v1/ui/quality', options, '获取质量指标失败')
}

export async function fetchLatestReport(stockCode: string, options: ApiRequestInit = {}): Promise<LatestReportResponse | null> {
  try {
    return await apiFetch<LatestReportResponse>(`/api/v1/reports/latest/${stockCode}`, options, '获取最新研报失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export async function fetchStockHistory(stockCode: string, options: ApiRequestInit = {}): Promise<StockHistoryResponse | null> {
  try {
    return await apiFetch<StockHistoryResponse>(`/api/v1/history/${stockCode}`, options, '获取股票历史失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export async function fetchStockNews(stockCode: string, limit = 8, options: ApiRequestInit = {}): Promise<StockNewsResponse> {
  return apiFetch<StockNewsResponse>(`/api/v1/news/${stockCode}?limit=${limit}`, options, '获取股票新闻失败')
}

export async function fetchStockSearch(query: string, limit = 12, options: ApiRequestInit = {}): Promise<StockSearchResponse> {
  const params = new URLSearchParams()
  params.set('q', query)
  params.set('limit', String(limit))
  return apiFetch<StockSearchResponse>(`/api/v1/stocks/search?${params.toString()}`, options, '搜索股票失败')
}

export async function fetchEventBacktest(stockCode: string, options: ApiRequestInit = {}): Promise<EventBacktestResponse> {
  return apiFetch<EventBacktestResponse>(`/api/v1/stocks/${stockCode}/event-backtest`, options, '获取事件影响回测失败')
}

export async function fetchMarketEvents(stockCodes: string[] = [], limitPerStock = 4, mode = 'realtime', status = '', options: ApiRequestInit = {}): Promise<MarketEventListResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  query.set('mode', mode)
  if (status) query.set('status', status)
  return apiFetch<MarketEventListResponse>(`/api/v1/events?${query.toString()}`, options, '获取事件流失败')
}

export async function fetchEventDetail(eventId: string, options: ApiRequestInit = {}): Promise<MarketEvent | null> {
  try {
    return await apiFetch<MarketEvent>(`/api/v1/events/${eventId}`, options, '获取事件详情失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export async function analyzeEvent(eventId: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/events/${eventId}/analyze`, { method: 'POST' }, '事件触发分析失败')
}

export async function updateEventStatus(eventId: string, status: MarketEvent['status'], note = ''): Promise<MarketEvent> {
  return apiFetch<MarketEvent>(`/api/v1/events/${eventId}/status`, {
    method: 'PATCH',
    headers: { 'X-Actor': 'browser-user', 'X-Role': 'admin' },
    body: { status, note },
  }, '更新事件状态失败')
}

export async function fetchStockEvents(stockCode: string, limit = 6, options: ApiRequestInit = {}): Promise<StockEventTimelineResponse> {
  return apiFetch<StockEventTimelineResponse>(`/api/v1/stocks/${stockCode}/events?limit=${limit}`, options, '获取股票事件时间线失败')
}

export async function fetchEventImpactReview(stockCode: string, limit = 20, options: ApiRequestInit = {}): Promise<EventImpactReviewResponse> {
  return apiFetch<EventImpactReviewResponse>(`/api/v1/stocks/${stockCode}/event-impact-review?limit=${limit}`, options, '获取历史事件影响复盘失败')
}

export type TrackingAlertFilters = {
  mode?: 'realtime' | 'history'
  severity?: string
  alertType?: string
  ruleId?: string
}

export async function fetchTrackingAlerts(stockCodes: string[] = [], limitPerStock = 4, status = 'open', filters: TrackingAlertFilters = {}, options: ApiRequestInit = {}): Promise<TrackingAlertListResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  if (status) query.set('status', status)
  if (filters.mode) query.set('mode', filters.mode)
  if (filters.severity) query.set('severity', filters.severity)
  if (filters.alertType) query.set('alert_type', filters.alertType)
  if (filters.ruleId) query.set('rule_id', filters.ruleId)
  return apiFetch<TrackingAlertListResponse>(`/api/v1/alerts?${query.toString()}`, options, '获取预警中心失败')
}

export async function fetchAlertRules(options: ApiRequestInit = {}): Promise<AlertRuleListResponse> {
  return apiFetch<AlertRuleListResponse>('/api/v1/alerts/rules', options, '获取预警规则失败')
}

export async function fetchDailyBriefing(stockCodes: string[] = [], limitPerStock = 4, options: ApiRequestInit = {}): Promise<DailyBriefingResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  return apiFetch<DailyBriefingResponse>(`/api/v1/briefing/daily?${query.toString()}`, options, '获取每日简报失败')
}

export async function fetchWatchlists(options: ApiRequestInit = {}): Promise<WatchlistListResponse> {
  return apiFetch<WatchlistListResponse>('/api/v1/watchlists', options, '获取组合跟踪失败')
}

export async function fetchWatchlistDetail(watchlistId: string, options: ApiRequestInit = {}): Promise<WatchlistDetailResponse | null> {
  try {
    return await apiFetch<WatchlistDetailResponse>(`/api/v1/watchlists/${encodeURIComponent(watchlistId)}`, options, '获取组合详情失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export async function refreshWatchlist(watchlistId: string): Promise<WatchlistDetailResponse> {
  return apiFetch<WatchlistDetailResponse>(`/api/v1/watchlists/${encodeURIComponent(watchlistId)}/refresh`, { method: 'POST' }, '刷新组合事件失败')
}

export async function createWatchlist(payload: WatchlistCreateRequest): Promise<Watchlist> {
  return apiFetch<Watchlist>('/api/v1/watchlists', {
    method: 'POST',
    body: payload,
  }, '创建组合失败')
}

export async function updateWatchlist(watchlistId: string, payload: WatchlistUpdateRequest): Promise<Watchlist> {
  return apiFetch<Watchlist>(`/api/v1/watchlists/${encodeURIComponent(watchlistId)}`, {
    method: 'PATCH',
    body: payload,
  }, '更新组合失败')
}

export async function deleteWatchlist(watchlistId: string): Promise<void> {
  await apiFetch<void>(`/api/v1/watchlists/${encodeURIComponent(watchlistId)}`, {
    method: 'DELETE',
  }, '删除组合失败')
}

export async function fetchRecentRuns(limit = 10, options: ApiRequestInit = {}): Promise<AnalysisRunListResponse> {
  const payload = await fetchRunWorkbench(limit, '', options)
  return payload.runs
}

export async function fetchWorkspaceStocks(options: ApiRequestInit = {}): Promise<WorkspaceStocksResponse> {
  return apiFetch<WorkspaceStocksResponse>('/api/v1/workspace/stocks', options, '获取工作区股票列表失败')
}

export async function createAnalysisRun(stockCode: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>('/api/v1/runs', {
    method: 'POST',
    body: { stock_code: stockCode },
  }, '创建分析任务失败')
}

export async function createBatchAnalysisRuns(stockCodes: string[]): Promise<BatchRunCreateResponse> {
  return apiFetch<BatchRunCreateResponse>('/api/v1/runs/batch', {
    method: 'POST',
    body: { stock_codes: stockCodes },
  }, '批量创建分析任务失败')
}

export async function fetchReportDiff(stockCode: string, options: ApiRequestInit = {}): Promise<ReportDiffResponse | null> {
  try {
    return await apiFetch<ReportDiffResponse>(`/api/v1/reports/diff/${stockCode}`, options, '获取研报差异失败')
  } catch (error) {
    if (isApiError(error)) return null
    throw error
  }
}

export async function fetchAnalysisRun(runId: string, options: ApiRequestInit = {}): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/runs/${runId}`, options, '获取分析任务状态失败')
}

export async function retryAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/runs/${runId}/retry`, { method: 'POST' }, '重试分析任务失败')
}

export async function cancelAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/runs/${runId}/cancel`, { method: 'POST' }, '取消分析任务失败')
}

export async function assignAnalysisRun(runId: string, owner: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/runs/${runId}/assign`, {
    method: 'POST',
    body: { owner },
  }, '分配任务失败')
}

export async function archiveAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  return apiFetch<AnalysisRunResponse>(`/api/v1/runs/${runId}/archive`, { method: 'POST' }, '归档任务失败')
}

export function stockCodeFromRun(run: AnalysisRunResponse) {
  return run.stock_code
}
