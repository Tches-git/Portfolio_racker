import { StockWorkbench } from '../../../components/workbench/stock-workbench'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchStockWorkbench } from '../../../lib/api'
import { serverApiOptions } from '../../../lib/server-auth'
import type { StockWorkbenchResponse } from '../../../lib/types'

const VALID_TABS: StockWorkbenchResponse['active_tab'][] = ['summary', 'timeline', 'backtest', 'exports']

function normalizeTab(tab?: string): StockWorkbenchResponse['active_tab'] {
  if (tab === 'history') return 'summary'
  return VALID_TABS.includes(tab as StockWorkbenchResponse['active_tab'])
    ? tab as StockWorkbenchResponse['active_tab']
    : 'summary'
}

export default async function StockPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams?: Promise<{ tab?: string }>
}) {
  const { stockCode } = await params
  const resolvedSearchParams = searchParams ? await searchParams : undefined
  const tab = normalizeTab(resolvedSearchParams?.tab)
  const apiOptions = await serverApiOptions()
  let data: StockWorkbenchResponse
  try {
    data = await fetchStockWorkbench(stockCode, tab, apiOptions)
  } catch {
    data = fallbackStockWorkbench(stockCode, tab)
  }

  return (
    <WorkspaceShell
      eyebrow="Single Stock Intelligence"
      title={`${data.stock_name || data.stock_code} 情报终端`}
      description={`${data.stock_code} · ${data.is_tracked ? '已加入组合追踪' : '尚未加入组合，历史事件不会隐式沉淀'}。`}
      actions={data.actions}
    >
      <StockWorkbench data={data} />
    </WorkspaceShell>
  )
}

function fallbackStockWorkbench(stockCode: string, tab: StockWorkbenchResponse['active_tab']): StockWorkbenchResponse {
  return {
    stock_code: stockCode,
    stock_name: stockCode,
    active_tab: tab,
    is_tracked: false,
    latest_report: null,
    history: null,
    timeline: {
      stock_code: stockCode,
      stock_name: stockCode,
      items: [],
      total: 0,
      high_impact_count: 0,
      placeholder_count: 0,
      duplicate_count: 0,
      source_count: 0,
      mode: 'history',
    },
    impact_review: {
      stock_code: stockCode,
      stock_name: stockCode,
      total_events: 0,
      high_impact_count: 0,
      converted_count: 0,
      event_driven_run_count: 0,
      latest_event_at: '',
      dominant_event_types: [],
      summary: '单股情报服务暂时不可用，页面未写入事件历史或创建追踪状态。',
      replay_items: [],
    },
    event_backtest: {
      stock_code: stockCode,
      stock_name: stockCode,
      windows: [1, 3, 5, 10],
      total_events: 0,
      matched_event_count: 0,
      fallback_message: '事件回测服务暂时不可用，请稍后重试。',
      groups: [],
      items: [],
    },
    related_watchlists: [],
    related_runs: emptyRunList(),
    exports: [],
    actions: [
      { label: '查看行情', href: `/markets/${stockCode}`, method: 'GET', action_type: 'open_market', target_id: stockCode, variant: 'secondary' },
      { label: '返回组合', href: '/watchlist', method: 'GET', action_type: 'open_watchlist', target_id: stockCode, variant: 'secondary' },
    ],
  }
}

function emptyRunList(): StockWorkbenchResponse['related_runs'] {
  return {
    items: [],
    total: 0,
    queued_count: 0,
    running_count: 0,
    completed_count: 0,
    failed_count: 0,
    stock_groups: [],
    workspace: {
      tracked_stocks: [],
      most_active_stock: '',
      latest_completed_stock: '',
      failed_stock_count: 0,
      history_backed_stock_count: 0,
      recommended_concurrency: 1,
      active_limit_reached: false,
      observability_status: 'degraded',
      collaboration_ready: false,
      collaborator_count: 0,
      audited_action_count: 0,
      archived_run_count: 0,
      stale_run_count: 0,
      recovery_status: 'unknown',
      worker_count: 0,
      retry_scheduled_count: 0,
      queue_mode: 'unknown',
      store_backend: 'unknown',
      schema_version: 0,
      wal_enabled: false,
      backup_available: false,
      last_backup_path: '',
      ops_status: 'degraded',
      alert_count: 0,
      failure_rate: 0,
      avg_duration_s: 0,
      p95_duration_s: 0,
    },
  }
}
