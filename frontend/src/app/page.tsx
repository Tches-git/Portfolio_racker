import Link from 'next/link'

import { CommandCenter } from '../components/command-center'
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
const EMPTY_ALERTS: TrackingAlertListResponse = {
  items: [],
  total: 0,
  high_severity_count: 0,
  risk_alert_count: 0,
  source_degraded_count: 0,
  manual_review_count: 0,
  severity_counts: {},
  alert_type_counts: {},
  rule_counts: {},
}
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

function impactLabel(level: string) {
  if (level === 'high') return '高影响'
  if (level === 'medium') return '中影响'
  return '低影响'
}

function impactTone(level: string) {
  if (level === 'high') return 'tagNegative'
  if (level === 'medium') return 'tagPositive'
  return ''
}

function runStatusLabel(status: string) {
  if (status === 'completed') return '已完成'
  if (status === 'failed') return '失败'
  if (status === 'running') return '运行中'
  if (status === 'queued') return '排队中'
  return status
}

export default async function Home() {
  const stockCode = '600519'
  const [recentRuns, workspaceStocks, watchlists] = await Promise.all([
    fetchRecentRuns(8).catch(() => EMPTY_RUNS),
    fetchWorkspaceStocks().catch(() => EMPTY_STOCKS),
    fetchWatchlists().catch(() => EMPTY_WATCHLISTS),
  ])
  const primaryWatchlist = watchlists.items[0]
  const focusCodes = primaryWatchlist?.stock_codes.length
    ? primaryWatchlist.stock_codes
    : workspaceStocks.items.slice(0, 6).map((item) => item.code)
  const trackingCodes = focusCodes.length ? focusCodes : [stockCode]
  const [events, alerts, briefing] = await Promise.all([
    fetchMarketEvents(trackingCodes, 5).catch(() => EMPTY_EVENTS),
    fetchTrackingAlerts(trackingCodes, 5).catch(() => EMPTY_ALERTS),
    fetchDailyBriefing(trackingCodes, 5).catch(() => EMPTY_BRIEFING),
  ])
  const activeRuns = recentRuns.items.filter((item) => item.status === 'queued' || item.status === 'running')
  const latestRun = recentRuns.items[0]
  const unresolvedWork = alerts.total + activeRuns.length + briefing.review_required_events.length
  const reportCards = [
    {
      title: '组合追踪报告',
      description: '按股票池聚合事件、预警、简报和风险摘要。',
      href: primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist',
      metric: `${watchlists.total || 0} 个组合`,
      detail: `${trackingCodes.length} 只股票`,
    },
    {
      title: '事件流报告',
      description: '查看实时和历史金融事件，继续下钻到单条事件详情。',
      href: `/events?stock_codes=${trackingCodes.join(',')}&mode=history`,
      metric: `${events.total} 条事件`,
      detail: `高影响 ${events.high_impact_count}`,
    },
    {
      title: '预警处理报告',
      description: '集中处理高影响、风险暴露、来源降级和人工复核事项。',
      href: `/alerts?stock_codes=${trackingCodes.join(',')}&mode=history`,
      metric: `${alerts.total} 条预警`,
      detail: `人工复核 ${alerts.manual_review_count}`,
    },
    {
      title: '每日简报',
      description: '把今日主题、关键事件和建议动作整理成研究入口。',
      href: `/briefing?stock_codes=${trackingCodes.join(',')}`,
      metric: `${briefing.themes.length} 个主题`,
      detail: `关键事件 ${briefing.key_events.length}`,
    },
    {
      title: '研报与导出',
      description: '进入最新股票交付中心，下载研报正文、事件点评和来源数据。',
      href: `/stocks/${latestRun?.stock_code || stockCode}/exports`,
      metric: `${latestRun?.exports.length || 0} 个导出物`,
      detail: latestRun ? runStatusLabel(latestRun.status) : '等待运行',
    },
    {
      title: '运行与审计',
      description: '查看分析任务、失败重试、运行状态和近期研究动作。',
      href: '/runs',
      metric: `${recentRuns.total} 个任务`,
      detail: `运行中 ${activeRuns.length}`,
    },
  ]

  return (
    <main className="reportsHub">
      <section className="reportsHeader">
        <div>
          <div className="breadcrumbLine">金融消息追踪平台 / 报告中心</div>
          <h1>报告中心</h1>
          <p>把组合、事件、预警、简报和研报交付按研究工作流重新组织，先看到需要处理的风险，再进入对应工作台。</p>
        </div>
        <div className="reportsHeaderActions">
          <Link className="button" href={`/briefing?stock_codes=${trackingCodes.join(',')}`}>生成每日简报</Link>
          <Link className="ghostLink" href={primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist'}>打开组合驾驶舱</Link>
        </div>
      </section>

      <section className="reportsToolbar">
        <CommandCenter initialCode={latestRun?.stock_code || stockCode} />
        <div className="dateRangePanel">
          <div className="panelKicker">当前视角</div>
          <div className="dateRangeTitle">自选组合 · 近 5 条信号</div>
          <div className="segmentedControl">
            <span className="segmentActive">今日</span>
            <span>7 日</span>
            <span>历史</span>
          </div>
          <p>时间筛选先作为报告中心视角提示，具体历史查询可进入事件流和组合详情页。</p>
        </div>
      </section>

      <section className="summaryStrip" aria-label="核心指标">
        <div className="summaryMetric">
          <span>待处理事项</span>
          <strong>{unresolvedWork}</strong>
          <em>预警 + 运行中任务 + 复核事件</em>
        </div>
        <div className="summaryMetric">
          <span>追踪事件</span>
          <strong>{events.total}</strong>
          <em>高影响 {events.high_impact_count} · 来源 {events.source_count}</em>
        </div>
        <div className="summaryMetric">
          <span>开放预警</span>
          <strong>{alerts.total}</strong>
          <em>高优先级 {alerts.high_severity_count} · 风险 {alerts.risk_alert_count}</em>
        </div>
        <div className="summaryMetric">
          <span>研究任务</span>
          <strong>{recentRuns.total}</strong>
          <em>完成 {recentRuns.completed_count} · 失败 {recentRuns.failed_count}</em>
        </div>
      </section>

      <QuickActions stockCode={latestRun?.stock_code || stockCode} latestRunId={latestRun?.run_id} />

      <div className="reportsLayout">
        <div className="reportsMain">
          <section className="panel">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">报告入口</div>
                <h2>常用研究报告</h2>
              </div>
              <Link className="ghostLink" href="/watchlist">管理组合</Link>
            </div>
            <div className="reportCardGrid">
              {reportCards.map((card) => (
                <Link className="reportCard" href={card.href} key={card.title}>
                  <div>
                    <div className="reportCardTitle">{card.title}</div>
                    <p>{card.description}</p>
                  </div>
                  <div className="reportCardFooter">
                    <strong>{card.metric}</strong>
                    <span>{card.detail}</span>
                  </div>
                </Link>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">事件明细</div>
                <h2>关键事件列表</h2>
              </div>
              <Link className="ghostLink" href={`/events?stock_codes=${trackingCodes.join(',')}&mode=history`}>查看全部事件</Link>
            </div>
            <div className="stripeTableWrap">
              <table className="stripeTable">
                <thead>
                  <tr>
                    <th>事件</th>
                    <th>股票</th>
                    <th>类型</th>
                    <th>影响</th>
                    <th>来源</th>
                    <th>动作</th>
                  </tr>
                </thead>
                <tbody>
                  {events.items.slice(0, 6).map((event) => (
                    <tr key={event.event_id}>
                      <td>
                        <Link className="tablePrimary" href={`/events/${event.event_id}`}>{event.title}</Link>
                        <div className="inlineMeta">{event.summary || event.reason || '暂无摘要'}</div>
                      </td>
                      <td>{event.stock_code}</td>
                      <td>{event.event_type}</td>
                      <td><span className={`tag ${impactTone(event.impact_level)}`}>{impactLabel(event.impact_level)}</span></td>
                      <td>{event.provider || event.source || '未知来源'}</td>
                      <td><Link className="downloadLink" href={`/stocks/${event.stock_code}`}>进入股票</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!events.items.length ? <div className="emptyState">暂未获取到事件。请确认 API 服务可用，或先到组合跟踪维护股票池。</div> : null}
            </div>
          </section>

          <StockCardGrid stocks={workspaceStocks.items} />
          <RecentRunsPanel runs={recentRuns.items} />
        </div>

        <aside className="reportsAside">
          <section className="panel">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">待办</div>
                <h2>需要关注</h2>
              </div>
            </div>
            <div className="sideList">
              {alerts.items.slice(0, 4).map((alert) => (
                <Link className="sideItem" href={`/events/${alert.event_id}`} key={alert.alert_id}>
                  <span className="tag tagNegative">{alert.severity === 'high' ? '高优先级' : '预警'}</span>
                  <strong>{alert.title}</strong>
                  <em>{alert.message}</em>
                </Link>
              ))}
              {!alerts.items.length ? <div className="emptyState">当前没有待处理预警。</div> : null}
            </div>
          </section>

          <section className="panel">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">简报</div>
                <h2>今日主题</h2>
              </div>
              <Link className="ghostLink" href={`/briefing?stock_codes=${trackingCodes.join(',')}`}>打开</Link>
            </div>
            <p className="bodyText">{briefing.summary}</p>
            <div className="chipRow">
              {briefing.themes.slice(0, 6).map((theme) => <span className="tag" key={theme}>{theme}</span>)}
              {!briefing.themes.length ? <span className="tag">暂无主题</span> : null}
            </div>
          </section>

          <section className="panel">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">运行</div>
                <h2>最近任务</h2>
              </div>
              <Link className="ghostLink" href="/runs">全部</Link>
            </div>
            <div className="sideList">
              {recentRuns.items.slice(0, 5).map((run) => (
                <Link className="sideItem compactSideItem" href={`/runs/${run.run_id}`} key={run.run_id}>
                  <strong>{run.stock_code}</strong>
                  <span>{runStatusLabel(run.status)} · {run.updated_at || run.created_at || '暂无时间'}</span>
                </Link>
              ))}
              {!recentRuns.items.length ? <div className="emptyState">当前还没有运行任务。</div> : null}
            </div>
          </section>
        </aside>
      </div>
    </main>
  )
}
