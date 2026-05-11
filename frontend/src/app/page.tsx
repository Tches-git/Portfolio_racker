import Link from 'next/link'

import { CommandCenter } from '../components/command-center'
import { MetricCard } from '../components/metric-card'
import { QuickActions } from '../components/quick-actions'
import { RecentRunsPanel } from '../components/recent-runs-panel'
import { StockCardGrid } from '../components/stock-card-grid'
import { fetchDailyBriefing, fetchMarketEvents, fetchRecentRuns, fetchTrackingAlerts, fetchWatchlists, fetchWorkspaceStocks } from '../lib/api'
import type { AnalysisRunListResponse, DailyBriefingResponse, MarketEventListResponse, TrackingAlertListResponse, WatchlistListResponse, WorkspaceStocksResponse } from '../lib/types'

const EMPTY_RUNS: AnalysisRunListResponse = {
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
    observability_status: 'basic',
    collaboration_ready: false,
    collaborator_count: 0,
    audited_action_count: 0,
    archived_run_count: 0,
    stale_run_count: 0,
    recovery_status: 'normal',
    worker_count: 1,
    retry_scheduled_count: 0,
    queue_mode: 'in_process',
    store_backend: 'sqlite',
    schema_version: 0,
    wal_enabled: false,
    backup_available: false,
    last_backup_path: '',
    ops_status: 'healthy',
    alert_count: 0,
    failure_rate: 0,
    avg_duration_s: 0,
    p95_duration_s: 0,
  },
}

const EMPTY_STOCKS: WorkspaceStocksResponse = { items: [] }
const EMPTY_WATCHLISTS: WatchlistListResponse = { items: [], total: 0 }
const EMPTY_EVENTS: MarketEventListResponse = { items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode: 'realtime' }
const EMPTY_ALERTS: TrackingAlertListResponse = { items: [], total: 0, high_severity_count: 0, risk_alert_count: 0, source_degraded_count: 0 }
const EMPTY_BRIEFING: DailyBriefingResponse = {
  title: '今日金融事件简报',
  summary: '暂未获取到事件数据。启动 API 后会自动汇总追踪范围内的关键消息。',
  generated_at: '',
  total_events: 0,
  high_impact_count: 0,
  negative_event_count: 0,
  source_count: 0,
  key_events: [],
  alerts: [],
  suggested_actions: [],
  themes: [],
  review_required_events: [],
}

export default async function Home() {
  const stockCode = '600519'
  const [recentRuns, workspaceStocks, watchlists] = await Promise.all([
    fetchRecentRuns(6).catch(() => EMPTY_RUNS),
    fetchWorkspaceStocks().catch(() => EMPTY_STOCKS),
    fetchWatchlists().catch(() => EMPTY_WATCHLISTS),
  ])
  const focusCodes = watchlists.items[0]?.stock_codes.length
    ? watchlists.items[0].stock_codes
    : workspaceStocks.items.slice(0, 4).map((item) => item.code)
  const trackingCodes = focusCodes.length ? focusCodes : [stockCode]
  const [events, alerts, briefing] = await Promise.all([
    fetchMarketEvents(trackingCodes, 3).catch(() => EMPTY_EVENTS),
    fetchTrackingAlerts(trackingCodes, 3).catch(() => EMPTY_ALERTS),
    fetchDailyBriefing(trackingCodes, 3).catch(() => EMPTY_BRIEFING),
  ])
  const activeRuns = recentRuns.items.filter((item) => item.status === 'queued' || item.status === 'running')
  const latestRun = recentRuns.items[0]

  return (
    <main>
      <CommandCenter initialCode={stockCode} />
      <QuickActions stockCode={latestRun?.stock_code || stockCode} latestRunId={latestRun?.run_id} />

      <div className="dashboardGrid">
        <MetricCard label="追踪事件" value={events.total} hint={`高影响 ${events.high_impact_count} · 来源 ${events.source_count}`} />
        <MetricCard label="开放预警" value={alerts.total} hint={`高优先级 ${alerts.high_severity_count} · 风险 ${alerts.risk_alert_count}`} />
        <MetricCard label="追踪组合" value={watchlists.total || 1} hint={`${trackingCodes.length} 只股票进入工作台`} />
        <MetricCard label="活跃任务" value={activeRuns.length} hint={`最近任务 ${recentRuns.total}`} />
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Market Pulse</div>
              <h2>关键事件雷达</h2>
            </div>
            <Link className="ghostLink" href="/events">进入事件流</Link>
          </div>
          <div className="timelineList">
            {events.items.slice(0, 5).map((event) => (
              <div className="card" key={event.event_id}>
                <div className="heroTop">
                  <div>
                    <div className="itemTitle">{event.stock_code} · {event.title}</div>
                    <div className="inlineMeta">{event.event_type} · {event.provider || event.source || '未知来源'} · {event.published_at || event.collected_at}</div>
                  </div>
                  <span className={`tag ${event.impact_level === 'high' ? 'tagNegative' : event.impact_level === 'medium' ? 'tagPositive' : ''}`}>{event.impact_level}</span>
                </div>
                <p className="bodyText">{event.summary || event.reason}</p>
                <div className="chipRow">
                  <Link className="downloadLink" href={`/events/${event.event_id}`}>事件详情</Link>
                  <Link className="downloadLink" href={`/stocks/${event.stock_code}/timeline`}>股票时间线</Link>
                </div>
              </div>
            ))}
            {!events.items.length ? <div className="emptyState">暂未获取到实时事件。请确认 FastAPI 服务已启动，或先进入组合跟踪维护股票池。</div> : null}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Briefing</div>
              <h2>今日研究简报</h2>
            </div>
            <Link className="ghostLink" href="/briefing">查看简报</Link>
          </div>
          <div className="metricStack">
            <div className="card">
              <div className="itemTitle">{briefing.title}</div>
              <p className="bodyText">{briefing.summary}</p>
              <div className="chipRow">
                {briefing.themes.slice(0, 4).map((theme) => <span className="tag" key={theme}>{theme}</span>)}
              </div>
            </div>
            {alerts.items.slice(0, 3).map((alert) => (
              <div className="card" key={alert.alert_id}>
                <div className="itemTitle">{alert.title}</div>
                <p className="bodyText">{alert.message}</p>
                <Link className="downloadLink" href={`/events/${alert.event_id}`}>处理预警</Link>
              </div>
            ))}
            {briefing.suggested_actions.slice(0, 3).map((action) => (
              <div className="selectionHint" key={action}>{action}</div>
            ))}
          </div>
        </section>

        <StockCardGrid stocks={workspaceStocks.items} />
        <RecentRunsPanel runs={recentRuns.items} />
      </div>
    </main>
  )
}
