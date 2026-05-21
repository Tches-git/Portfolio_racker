import Link from 'next/link'
import type { ReactNode } from 'react'

import { CommandCenterShell } from '../big-screen/command-center'
import { formatEventType, formatImpactLevel, formatRunStatus } from '../../lib/labels'
import type { DashboardResponse, MarketEvent } from '../../lib/types'
import { SetupWizard } from './setup-wizard'

function eventTitle(event: MarketEvent) {
  return event.summary || event.reason || '暂无摘要'
}

type DataEntry = {
  label: string
  value: string | number
  hint: string
  href: string
  tone?: 'neutral' | 'warning' | 'danger' | 'success' | 'agent' | 'info'
}

const TRIGGER_TYPES = [
  { key: 'filing', eventType: 'announcement', label: '公告披露', hint: '公告、交易所披露、公司事项' },
  { key: 'market_move', eventType: 'market_move', label: '行情异动', hint: '价格、成交、资金面异常' },
  { key: 'broker_view', eventType: 'broker_view', label: '研报观点', hint: '机构观点、评级和预期变化' },
  { key: 'regulation', eventType: 'regulation', label: '监管政策', hint: '监管、行业政策和合规信号' },
  { key: 'risk_sentiment', eventType: 'risk_sentiment', label: '风险舆情', hint: '负面舆情、争议和风险暴露' },
  { key: 'earnings', eventType: 'earnings', label: '业绩财务', hint: '业绩、利润、现金流和财务指标' },
] as const

const FALLBACK_STOCK_NAMES: Record<string, string> = {
  '600519': '贵州茅台',
  '000858': '五粮液',
  '300750': '宁德时代',
  '000333': '美的集团',
  '600036': '招商银行',
  '601318': '中国平安',
  '600276': '恒瑞医药',
  '002415': '海康威视',
  '002594': '比亚迪',
  '601012': '隆基绿能',
  '601899': '紫金矿业',
  '000002': '万科A',
  '688225': '亚信安全',
}

function riskLabel(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}

function triggerCount(events: MarketEvent[], key: string) {
  if (key === 'regulation') {
    return events.filter((event) => event.event_type === 'regulation' || event.event_type === 'industry_policy').length
  }
  if (key === 'broker_view') {
    return events.filter((event) => event.event_type === 'broker_view' || event.event_type === 'research_view').length
  }
  if (key === 'filing') {
    return events.filter((event) => event.event_type === 'filing' || event.event_type === 'announcement').length
  }
  return events.filter((event) => event.event_type === key).length
}

function latestForTrigger(events: MarketEvent[], key: string) {
  if (key === 'regulation') {
    return events.find((event) => event.event_type === 'regulation' || event.event_type === 'industry_policy')
  }
  if (key === 'broker_view') {
    return events.find((event) => event.event_type === 'broker_view' || event.event_type === 'research_view')
  }
  if (key === 'filing') {
    return events.find((event) => event.event_type === 'filing' || event.event_type === 'announcement')
  }
  return events.find((event) => event.event_type === key)
}

function eventHref(event: MarketEvent, view = 'events') {
  return `/events?view=${view}&selected_event_id=${event.event_id}&stock_codes=${event.stock_code}`
}

function impactTone(level: string) {
  if (level === 'high') return 'tone-danger'
  if (level === 'medium') return 'tone-warning'
  return 'tone-neutral'
}

function compactTime(value: string) {
  if (!value) return '--'
  return value.replace('T', ' ').slice(0, 16)
}

function shortTime(value: string) {
  const time = compactTime(value)
  return time === '--' ? time : time.slice(5)
}

function stockLabel(stockCode: string, stockName = '') {
  const name = stockName || FALLBACK_STOCK_NAMES[stockCode] || ''
  if (name && stockCode && name !== stockCode) return `${name}（${stockCode}）`
  return name || stockCode || '未知标的'
}

function alertTitle(alert: DashboardResponse['risk_queue']['items'][number]) {
  const label = stockLabel(alert.stock_code, alert.stock_name)
  const rawTitle = (alert.title || alert.rule_name || alert.rule_id || '风险预警').trim()
  if (!rawTitle) return label
  if (rawTitle.includes(label)) return rawTitle
  if (alert.stock_code && rawTitle.startsWith(alert.stock_code)) {
    const suffix = rawTitle.slice(alert.stock_code.length).trim()
    return suffix ? `${label} ${suffix}` : label
  }
  return rawTitle
}

function DataCenterHeader({
  name,
  description,
  metrics,
  actionHref,
  actionLabel,
}: {
  name: string
  description: string
  metrics: DataEntry[]
  actionHref: string
  actionLabel: string
}) {
  return (
    <section className="dataCenterHeader">
      <div className="dataCenterIdentity" title={description}>
        <span>PORTFOLIO DATA CENTER</span>
        <h2>{name}</h2>
      </div>
      <div className="dataCenterMetrics">
        {metrics.map((item) => (
          <Link className={`dataCenterMetric tone-${item.tone || 'neutral'}`} href={item.href} key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <em>{item.hint}</em>
          </Link>
        ))}
      </div>
      <div className="dataCenterPrimaryAction">
        <Link href={actionHref}>{actionLabel}</Link>
      </div>
    </section>
  )
}

function DataCategoryGrid({ items }: { items: DataEntry[] }) {
  return (
    <section className="dataCenterPanel dataCategoryPanel">
      <header>
        <span>DATA MAP</span>
        <h2>数据分类矩阵</h2>
      </header>
      <div className="dataCategoryGrid">
        {items.map((item) => (
          <Link className={`dataCategoryItem tone-${item.tone || 'neutral'}`} href={item.href} key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <em>{item.hint}</em>
          </Link>
        ))}
      </div>
    </section>
  )
}

function SnapshotStrip({ items }: { items: DataEntry[] }) {
  return (
    <section className="dataSnapshotStrip" aria-label="数据快照区">
      {items.map((item) => (
        <Link className={`dataSnapshotItem tone-${item.tone || 'neutral'}`} href={item.href} key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
          <em>{item.hint}</em>
        </Link>
      ))}
    </section>
  )
}

function WatchlistEntryPanel({
  total,
  items,
  primaryWatchlistId,
}: {
  total: number
  items: DashboardResponse['watchlists']['items']
  primaryWatchlistId: string
}) {
  return (
    <section className="dataCenterPanel watchlistEntryPanel">
      <header>
        <div>
          <span>MY PORTFOLIOS</span>
          <h2>我的组合</h2>
        </div>
        <strong>{total}</strong>
      </header>
      <div className="watchlistEntryList">
        {items.slice(0, 6).map((watchlist) => (
          <Link
            className={watchlist.watchlist_id === primaryWatchlistId ? 'watchlistEntryItem active' : 'watchlistEntryItem'}
            href={`/watchlist/${watchlist.watchlist_id}`}
            key={watchlist.watchlist_id}
          >
            <strong>{watchlist.name}</strong>
            <span>{watchlist.stock_codes.length} 只股票 · {watchlist.last_refreshed_at ? `刷新 ${shortTime(watchlist.last_refreshed_at)}` : '尚未刷新'}</span>
            <em>进入行情数据中心</em>
          </Link>
        ))}
        {!items.length ? <div className="dataCenterEmpty">暂无组合，请先创建股票池。</div> : null}
      </div>
    </section>
  )
}

function RankPanel({
  eyebrow,
  title,
  href,
  children,
}: {
  eyebrow: string
  title: string
  href: string
  children: ReactNode
}) {
  return (
    <section className="dataCenterPanel">
      <header>
        <div>
          <span>{eyebrow}</span>
          <h2>{title}</h2>
        </div>
        <Link href={href}>查看全部</Link>
      </header>
      {children}
    </section>
  )
}

export function DashboardOverview({ data }: { data: DashboardResponse }) {
  if (data.mode === 'setup') {
    return <SetupWizard setup={data.setup} />
  }

  const summary = data.portfolio_summary
  const primaryWatchlist = data.watchlists.items.find((item) => item.watchlist_id === summary.primary_watchlist_id) || data.watchlists.items[0]
  const latestEvents = data.latest_events.items
  const topAlerts = data.risk_queue.items.slice(0, 3)
  const topRuns = data.recent_runs.items.slice(0, 3)
  const highImpactCount = latestEvents.filter((event) => event.impact_level === 'high').length
  const nextStepHref = summary.alert_count ? '/events?view=alerts' : primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist'
  const primaryStock = primaryWatchlist?.stock_codes[0] || ''
  const triggerStats = TRIGGER_TYPES.map((trigger) => {
    const count = triggerCount(latestEvents, trigger.key)
    const latest = latestForTrigger(latestEvents, trigger.key)
    return {
      ...trigger,
      count,
      href: latest ? eventHref(latest) : `/events?view=events&event_type=${trigger.eventType}`,
    }
  })
  const latestRun = topRuns[0]
  const latestUpdatedAt = latestEvents[0]?.published_at || latestEvents[0]?.collected_at || latestRun?.updated_at || primaryWatchlist?.last_refreshed_at || ''
  const citationCoverage = latestRun?.run_metrics?.citation_coverage_rate || latestRun?.run_metrics?.citation_audit_coverage_rate || 0
  const sourceCount = latestRun?.run_metrics?.source_reference_count || 0
  const headerMetrics: DataEntry[] = [
    { label: '风险分', value: summary.risk_score, hint: riskLabel(summary.risk_level), href: nextStepHref, tone: summary.risk_level === 'high' ? 'danger' : summary.risk_level === 'medium' ? 'warning' : 'success' },
    { label: '开放预警', value: summary.alert_count, hint: `人工复核 ${summary.manual_review_count}`, href: '/events?view=alerts', tone: summary.alert_count ? 'warning' : 'neutral' },
    { label: '事件数', value: summary.event_count, hint: `高影响 ${highImpactCount || summary.high_impact_count}`, href: '/events?view=events', tone: (highImpactCount || summary.high_impact_count) ? 'danger' : 'info' },
    { label: '任务交付', value: data.recent_runs.total, hint: `完成 ${data.recent_runs.completed_count}`, href: '/runs', tone: 'agent' },
    { label: '更新时间', value: shortTime(latestUpdatedAt), hint: primaryWatchlist?.last_refreshed_at ? '组合最近刷新' : '等待刷新', href: primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist', tone: 'info' },
  ]
  const categoryItems: DataEntry[] = [
    { label: '组合监控', value: summary.watchlist_count, hint: `${summary.stock_count} 只股票`, href: primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist', tone: 'info' },
    { label: '事件预警', value: summary.alert_count, hint: '待处理风险', href: '/events?view=alerts', tone: summary.alert_count ? 'warning' : 'neutral' },
    ...triggerStats.map((item) => ({ label: item.label, value: item.count, hint: item.hint, href: item.href, tone: item.count ? 'info' as const : 'neutral' as const })),
    { label: '研报任务', value: data.recent_runs.total, hint: 'Agent 任务交付', href: '/runs', tone: 'agent' },
    { label: '质量评测', value: 'QA', hint: '可信度与 Benchmark', href: '/quality', tone: 'success' },
  ]
  const snapshotItems: DataEntry[] = [
    { label: '今日主题', value: data.today_briefing.themes.length || 0, hint: data.today_briefing.title || '暂无简报', href: '/events?view=events', tone: 'info' },
    { label: '预警队列', value: topAlerts.length, hint: topAlerts[0]?.title || '当前无待处理预警', href: '/events?view=alerts', tone: topAlerts.length ? 'warning' : 'neutral' },
    { label: '最近交付', value: topRuns.length, hint: latestRun ? `${stockLabel(latestRun.stock_code, latestRun.stock_name)} · ${formatRunStatus(latestRun.status)}` : '暂无近期任务', href: '/runs', tone: 'agent' },
    { label: '引用可信度', value: citationCoverage ? `${Math.round(citationCoverage * 100)}%` : '--', hint: sourceCount ? `${sourceCount} 个来源` : '等待任务生成', href: latestRun ? `/runs/${latestRun.run_id}` : '/quality', tone: citationCoverage ? 'success' : 'neutral' },
  ]

  return (
    <CommandCenterShell className={`dataCenterDashboard marketRisk-${summary.risk_level}`}>
      <DataCenterHeader
        name={primaryWatchlist?.name || '组合风险监控'}
        description={summary.risk_summary || '刷新组合后，这里会持续聚合风险、事件、预警和任务交付状态。'}
        metrics={headerMetrics}
        actionHref={nextStepHref}
        actionLabel={summary.alert_count ? '处理预警' : '进入组合'}
      />

      <SnapshotStrip items={snapshotItems} />

      <section className="dataCenterLayout">
        <aside className="dataCenterLeftRail">
          <WatchlistEntryPanel total={data.watchlists.total} items={data.watchlists.items} primaryWatchlistId={summary.primary_watchlist_id} />
          <DataCategoryGrid items={categoryItems} />
          <section className="dataCenterPanel triggerSpeedPanel">
            <header>
              <span>TRIGGER MAP</span>
              <h2>触发源速览</h2>
            </header>
            <div className="triggerSpeedList">
              {triggerStats.map((item) => (
                <Link href={item.href} key={item.key}>
                  <span>{item.label}</span>
                  <i style={{ width: `${Math.max(8, item.count * 18)}%` }} />
                  <strong>{item.count}</strong>
                </Link>
              ))}
            </div>
          </section>
        </aside>

        <main className="dataCenterMain">
          <RankPanel eyebrow="RISK RANK" title="风险榜单" href="/events?view=alerts">
            <div className="dataRankWrap">
              <table className="dataRankTable">
                <thead>
                  <tr>
                    <th>优先级</th>
                    <th>预警</th>
                    <th>标的</th>
                    <th>动作</th>
                  </tr>
                </thead>
                <tbody>
                  {data.risk_queue.items.slice(0, 7).map((alert) => (
                    <tr key={alert.alert_id}>
                      <td><b className={`rankPill tone-${alert.severity === 'high' ? 'danger' : alert.severity === 'medium' ? 'warning' : 'neutral'}`}>{alert.priority || alert.severity}</b></td>
                      <td>
                        <Link className="rankPrimary" href={`/events?view=alerts&selected_event_id=${alert.event_id}`}>{alertTitle(alert)}</Link>
                        <span>{alert.rule_name || alert.rule_id || '风险规则'}</span>
                      </td>
                      <td>{stockLabel(alert.stock_code, alert.stock_name)}</td>
                      <td><Link className="rankAction" href={`/events?view=alerts&selected_event_id=${alert.event_id}`}>处理</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!data.risk_queue.items.length ? <div className="dataCenterEmpty">暂无待处理预警。</div> : null}
            </div>
          </RankPanel>

          <RankPanel eyebrow="EVENT RANK" title="最新关键事件" href="/events?view=events">
            <div className="dataRankWrap">
              <table className="dataRankTable eventRankTable">
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>事件</th>
                    <th>来源</th>
                    <th>影响</th>
                  </tr>
                </thead>
                <tbody>
                  {latestEvents.slice(0, 8).map((event) => (
                    <tr key={event.event_id}>
                      <td>{shortTime(event.published_at || event.collected_at)}</td>
                      <td>
                        <Link className="rankPrimary" href={eventHref(event)}>{event.title}</Link>
                        <span>{stockLabel(event.stock_code, event.stock_name)} · {formatEventType(event.event_type)} · {eventTitle(event)}</span>
                      </td>
                      <td>{event.provider || event.source || '未知来源'}</td>
                      <td><b className={`rankPill ${impactTone(event.impact_level)}`}>{formatImpactLevel(event.impact_level)}</b></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!latestEvents.length ? <div className="dataCenterEmpty">暂无历史事件，请进入组合详情手动刷新。</div> : null}
            </div>
          </RankPanel>
        </main>

        <aside className="dataCenterRightRail">
          <RankPanel eyebrow="TASK RANK" title="任务榜单" href="/runs">
            <div className="dataRankWrap">
              <table className="dataRankTable taskRankTable">
                <thead>
                  <tr>
                    <th>状态</th>
                    <th>标的</th>
                    <th>交付</th>
                  </tr>
                </thead>
                <tbody>
                  {topRuns.map((run) => (
                    <tr key={run.run_id}>
                      <td><b className={`rankPill tone-${run.status === 'failed' ? 'danger' : run.status === 'completed' ? 'success' : 'agent'}`}>{formatRunStatus(run.status)}</b></td>
                      <td><Link className="rankPrimary" href={`/runs/${run.run_id}`}>{stockLabel(run.stock_code, run.stock_name)}</Link></td>
                      <td>{shortTime(run.updated_at || run.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!topRuns.length ? <div className="dataCenterEmpty">暂无任务交付。</div> : null}
            </div>
          </RankPanel>

          <section className="dataCenterPanel dataBriefingPanel">
            <header>
              <span>BRIEFING</span>
              <h2>今日主题</h2>
            </header>
            <p>{data.today_briefing.summary || data.today_briefing.title || '暂无简报。刷新组合后，系统会汇总当前账号的事件主题。'}</p>
            <div className="themeTokenList">
              {(data.today_briefing.themes.length ? data.today_briefing.themes : ['暂无主题']).slice(0, 6).map((theme) => (
                <span key={theme}>{theme}</span>
              ))}
            </div>
          </section>

          <section className="dataCenterPanel dataActionPanel">
            <header>
              <span>NEXT STEP</span>
              <h2>下一步动作</h2>
            </header>
            <p>{summary.alert_count ? `当前有 ${summary.alert_count} 条预警等待复核，建议先进入事件预警台。` : latestEvents.length ? '已有事件沉淀，可以从事件流生成点评或更新研报。' : '当前账号暂无新事件，请从组合详情手动刷新。'}</p>
            <div className="dataActionLinks">
              <Link href={nextStepHref}>{summary.alert_count ? '进入预警台' : '进入组合'}</Link>
              <Link href={primaryStock ? `/stocks/${primaryStock}` : '/runs'}>生成研报</Link>
              <Link href="/runs">任务交付</Link>
            </div>
          </section>
        </aside>
      </section>
    </CommandCenterShell>
  )
}
