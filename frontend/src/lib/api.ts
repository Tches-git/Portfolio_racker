import type { AnalysisRunListResponse, AnalysisRunResponse, BatchRunCreateResponse, DailyBriefingResponse, EventImpactReviewResponse, LatestReportResponse, MarketEvent, MarketEventListResponse, ReportDiffResponse, StockEventTimelineResponse, StockHistoryResponse, StockNewsResponse, TrackingAlertListResponse, WatchlistCreateRequest, WatchlistDetailResponse, WatchlistListResponse, Watchlist, WorkspaceStocksResponse } from './types'

export const API_BASE = typeof window === 'undefined'
  ? process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'
  : process.env.NEXT_PUBLIC_API_BASE_URL || ''

export async function fetchLatestReport(stockCode: string): Promise<LatestReportResponse | null> {
  const res = await fetch(`${API_BASE}/api/v1/reports/latest/${stockCode}`, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

export async function fetchStockHistory(stockCode: string): Promise<StockHistoryResponse | null> {
  const res = await fetch(`${API_BASE}/api/v1/history/${stockCode}`, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

export async function fetchStockNews(stockCode: string, limit = 8): Promise<StockNewsResponse> {
  const res = await fetch(`${API_BASE}/api/v1/news/${stockCode}?limit=${limit}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取股票新闻失败')
  }
  return res.json()
}

export async function fetchMarketEvents(stockCodes: string[] = [], limitPerStock = 4, mode = 'realtime', status = ''): Promise<MarketEventListResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  query.set('mode', mode)
  if (status) query.set('status', status)
  const res = await fetch(`${API_BASE}/api/v1/events?${query.toString()}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取事件流失败')
  }
  return res.json()
}

export async function fetchEventDetail(eventId: string): Promise<MarketEvent | null> {
  const res = await fetch(`${API_BASE}/api/v1/events/${eventId}`, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

export async function analyzeEvent(eventId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/events/${eventId}/analyze`, { method: 'POST' })
  if (!res.ok) {
    throw new Error('事件触发分析失败')
  }
  return res.json()
}

export async function updateEventStatus(eventId: string, status: MarketEvent['status'], note = ''): Promise<MarketEvent> {
  const res = await fetch(`${API_BASE}/api/v1/events/${eventId}/status`, {
    method: 'PATCH',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ status, note }),
  })
  if (!res.ok) {
    throw new Error('更新事件状态失败')
  }
  return res.json()
}

export async function fetchStockEvents(stockCode: string, limit = 6): Promise<StockEventTimelineResponse> {
  const res = await fetch(`${API_BASE}/api/v1/stocks/${stockCode}/events?limit=${limit}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取股票事件时间线失败')
  }
  return res.json()
}

export async function fetchEventImpactReview(stockCode: string, limit = 20): Promise<EventImpactReviewResponse> {
  const res = await fetch(`${API_BASE}/api/v1/stocks/${stockCode}/event-impact-review?limit=${limit}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取历史事件影响复盘失败')
  }
  return res.json()
}

export async function fetchTrackingAlerts(stockCodes: string[] = [], limitPerStock = 4, status = 'open'): Promise<TrackingAlertListResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  if (status) query.set('status', status)
  const res = await fetch(`${API_BASE}/api/v1/alerts?${query.toString()}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取预警中心失败')
  }
  return res.json()
}

export async function fetchDailyBriefing(stockCodes: string[] = [], limitPerStock = 4): Promise<DailyBriefingResponse> {
  const query = new URLSearchParams()
  if (stockCodes.length) query.set('stock_codes', stockCodes.join(','))
  query.set('limit_per_stock', String(limitPerStock))
  const res = await fetch(`${API_BASE}/api/v1/briefing/daily?${query.toString()}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取每日简报失败')
  }
  return res.json()
}

export async function fetchWatchlists(): Promise<WatchlistListResponse> {
  const res = await fetch(`${API_BASE}/api/v1/watchlists`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取组合跟踪失败')
  }
  return res.json()
}

export async function fetchWatchlistDetail(watchlistId: string): Promise<WatchlistDetailResponse | null> {
  const res = await fetch(`${API_BASE}/api/v1/watchlists/${encodeURIComponent(watchlistId)}`, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

export async function refreshWatchlist(watchlistId: string): Promise<WatchlistDetailResponse> {
  const res = await fetch(`${API_BASE}/api/v1/watchlists/${encodeURIComponent(watchlistId)}/refresh`, { method: 'POST' })
  if (!res.ok) {
    throw new Error('刷新组合事件失败')
  }
  return res.json()
}

export async function createWatchlist(payload: WatchlistCreateRequest): Promise<Watchlist> {
  const res = await fetch(`${API_BASE}/api/v1/watchlists`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    throw new Error('创建组合失败')
  }
  return res.json()
}

export async function fetchRecentRuns(limit = 10): Promise<AnalysisRunListResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs?limit=${limit}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取最近运行任务失败')
  }
  return res.json()
}

export async function fetchWorkspaceStocks(): Promise<WorkspaceStocksResponse> {
  const res = await fetch(`${API_BASE}/api/v1/workspace/stocks`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取工作区股票列表失败')
  }
  return res.json()
}

export async function createAnalysisRun(stockCode: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ stock_code: stockCode }),
  })
  if (!res.ok) {
    throw new Error('创建分析任务失败')
  }
  return res.json()
}

export async function createBatchAnalysisRuns(stockCodes: string[]): Promise<BatchRunCreateResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/batch`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ stock_codes: stockCodes }),
  })
  if (!res.ok) {
    throw new Error('批量创建分析任务失败')
  }
  return res.json()
}

export async function fetchReportDiff(stockCode: string): Promise<ReportDiffResponse | null> {
  const res = await fetch(`${API_BASE}/api/v1/reports/diff/${stockCode}`, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

export async function fetchAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/${runId}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error('获取分析任务状态失败')
  }
  return res.json()
}

export async function retryAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/${runId}/retry`, { method: 'POST' })
  if (!res.ok) {
    throw new Error('重试分析任务失败')
  }
  return res.json()
}

export async function cancelAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/${runId}/cancel`, { method: 'POST' })
  if (!res.ok) {
    throw new Error('取消分析任务失败')
  }
  return res.json()
}

export async function assignAnalysisRun(runId: string, owner: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/${runId}/assign`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ owner }),
  })
  if (!res.ok) {
    throw new Error('分配任务失败')
  }
  return res.json()
}

export async function archiveAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/runs/${runId}/archive`, { method: 'POST' })
  if (!res.ok) {
    throw new Error('归档任务失败')
  }
  return res.json()
}

export function stockCodeFromRun(run: AnalysisRunResponse) {
  return run.stock_code
}
