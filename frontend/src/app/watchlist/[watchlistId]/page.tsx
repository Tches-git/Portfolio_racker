import Link from 'next/link'

import { EventAnalyzeButton } from '../../../components/event-analyze-button'
import { WatchlistRefreshButton } from '../../../components/watchlist-refresh-button'
import { fetchWatchlistDetail } from '../../../lib/api'
import type { WatchlistSummary } from '../../../lib/types'

function impactTone(level: string) {
  if (level === 'high') return 'tagNegative'
  if (level === 'medium') return 'tagPositive'
  return ''
}

function riskLabel(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中等风险'
  return '低风险'
}

export default async function WatchlistDetailPage({ params }: { params: Promise<{ watchlistId: string }> }) {
  const { watchlistId } = await params
  const detail = await fetchWatchlistDetail(watchlistId).catch(() => null)

  if (!detail) {
    return (
      <main>
        <section className="hero">
          <div className="heroTop">
            <div>
              <div className="eyebrow">组合详情</div>
              <h1>未找到组合</h1>
              <p>该组合可能尚未创建，或 API 服务暂时不可用。</p>
            </div>
            <Link className="ghostLink" href="/watchlist">返回组合跟踪</Link>
          </div>
        </section>
        <div className="emptyState">组合 ID：{watchlistId}</div>
      </main>
    )
  }

  const { watchlist } = detail
  const rawSummary = detail.summary
  const events = { ...detail.events, items: detail.events?.items || [] }
  const alerts = { ...detail.alerts, items: detail.alerts?.items || [] }
  const briefing = { ...detail.briefing, themes: detail.briefing?.themes || [] }
  const summaryDefaults: WatchlistSummary = {
    stock_count: watchlist.stock_codes.length,
    event_count: events.total || events.items.length,
    high_impact_count: events.high_impact_count || 0,
    alert_count: alerts.total || alerts.items.length,
    high_severity_count: alerts.high_severity_count || 0,
    source_count: events.source_count || 0,
    placeholder_count: events.placeholder_count || 0,
    risk_score: 0,
    risk_level: 'low',
    risk_summary: '',
    open_alert_count: alerts.total || 0,
    handled_event_count: 0,
    converted_event_count: 0,
    manual_review_count: alerts.manual_review_count || 0,
    processing_rate: 0,
    dominant_rules: [],
    priority_actions: [],
    last_refreshed_at: watchlist.last_refreshed_at || '',
    impacted_stocks: [],
  }
  const summary: WatchlistSummary = {
    ...summaryDefaults,
    ...rawSummary,
    dominant_rules: rawSummary?.dominant_rules || [],
    priority_actions: rawSummary?.priority_actions || [],
    impacted_stocks: rawSummary?.impacted_stocks || [],
  }
  const stockQuery = watchlist.stock_codes.join(',')
  const highImpactEvents = events.items.filter((event) => event.impact_level === 'high')

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">组合详情</div>
            <h1>{watchlist.name}</h1>
            <p>{watchlist.description || '组合级金融消息追踪工作台。'} · 最近刷新：{summary.last_refreshed_at || '尚未手动刷新'}</p>
          </div>
          <div className="actionList compactActions">
            <WatchlistRefreshButton watchlistId={watchlist.watchlist_id} />
            <Link className="ghostLink" href="/watchlist">组合列表</Link>
          </div>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">组合风险</div><div className="metricCardValue">{summary.risk_score}</div><div className="inlineMeta">{riskLabel(summary.risk_level)} · 处理率 {(summary.processing_rate * 100).toFixed(0)}%</div></div>
        <div className="metricCard"><div className="statusLabel">追踪股票</div><div className="metricCardValue">{summary.stock_count}</div><div className="inlineMeta">当前组合股票池</div></div>
        <div className="metricCard"><div className="statusLabel">历史事件</div><div className="metricCardValue">{summary.event_count}</div><div className="inlineMeta">来源 {summary.source_count} · 降级 {summary.placeholder_count}</div></div>
        <div className="metricCard"><div className="statusLabel">高影响</div><div className="metricCardValue">{summary.high_impact_count}</div><div className="inlineMeta">需要优先复核</div></div>
        <div className="metricCard"><div className="statusLabel">开放预警</div><div className="metricCardValue">{summary.open_alert_count}</div><div className="inlineMeta">高优先级 {summary.high_severity_count} · 已转研报 {summary.converted_event_count}</div></div>
      </div>

      <div className="grid">
        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">风险驾驶舱</div>
              <h2>组合风险驾驶舱</h2>
            </div>
            <Link className="downloadLink" href={`/alerts?stock_codes=${stockQuery}&mode=history`}>进入预警处理台</Link>
          </div>
          <div className="detailGrid">
            <div className="card">
              <div className="itemTitle">风险摘要</div>
              <p className="bodyText">{summary.risk_summary || '暂无风险摘要。'}</p>
              <div className="chipRow">
                <span className={`tag ${impactTone(summary.risk_level)}`}>{riskLabel(summary.risk_level)}</span>
                <span className="tag">处理率 {(summary.processing_rate * 100).toFixed(0)}%</span>
                <span className="tag">人工复核 {summary.manual_review_count}</span>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">优先动作</div>
              <div className="metricStack">
                {summary.priority_actions.map((action) => <div className="selectionHint" key={action}>{action}</div>)}
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">主导规则</div>
              <div className="chipRow">
                {summary.dominant_rules.map((rule) => <span className="tag" key={rule}>{rule}</span>)}
                {!summary.dominant_rules.length ? <span className="tag">暂无规则命中</span> : null}
              </div>
            </div>
          </div>
        </section>

        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">组合事件</div>
              <h2>组合事件雷达</h2>
            </div>
            <Link className="downloadLink" href={`/events?stock_codes=${stockQuery}&mode=history`}>查看历史事件流</Link>
          </div>
          <div className="timelineList">
            {(highImpactEvents.length ? highImpactEvents : events.items).slice(0, 8).map((event) => (
              <div className="timelineCard" key={event.event_id}>
                <div className="timelineDot" />
                <div className="card timelineBody">
                  <div className="heroTop">
                    <div>
                      <div className="itemTitle">{event.stock_code} · {event.title}</div>
                      <div className="inlineMeta">{event.event_type} · {event.provider || event.source || '未知来源'} · {event.published_at || event.collected_at}</div>
                    </div>
                    <span className={`tag ${impactTone(event.impact_level)}`}>{event.impact_level}</span>
                  </div>
                  <p className="bodyText">{event.summary || event.reason}</p>
                  <div className="chipRow">
                    <Link className="downloadLink" href={`/events/${event.event_id}`}>事件详情</Link>
                    <Link className="downloadLink" href={`/stocks/${event.stock_code}`}>股票工作台</Link>
                    <EventAnalyzeButton eventId={event.event_id} label="事件点评" />
                  </div>
                </div>
              </div>
            ))}
            {!events.items.length ? <div className="emptyState">暂无历史事件。点击“刷新组合事件”后会把实时采集结果沉淀到历史库。</div> : null}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">组合简报</div>
              <h2>今日组合摘要</h2>
            </div>
            <Link className="downloadLink" href={`/briefing?stock_codes=${stockQuery}`}>打开简报</Link>
          </div>
          <div className="metricStack">
            <div className="card">
              <div className="itemTitle">{briefing.title}</div>
              <p className="bodyText">{briefing.summary}</p>
              <div className="chipRow">
                {briefing.themes.map((theme) => <span className="tag" key={theme}>{theme}</span>)}
                {!briefing.themes.length ? <span className="tag">暂无主题</span> : null}
              </div>
            </div>
            {alerts.items.slice(0, 4).map((alert) => (
              <div className="card" key={alert.alert_id}>
                <div className="itemTitle">{alert.title}</div>
                <p className="bodyText">{alert.message}</p>
                  <div className="inlineMeta">{alert.priority} · {alert.severity} · {alert.suggested_action}</div>
                  {alert.handled_at ? <div className="selectionHint">处理闭环：{alert.handled_by || 'browser-user'} · {alert.handled_at} · {alert.handling_note || '无备注'}</div> : null}
              </div>
            ))}
            {!alerts.items.length ? <div className="emptyState">当前组合暂无开放预警。</div> : null}
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">股票池</div>
              <h2>受影响股票排序</h2>
            </div>
            <Link className="downloadLink" href={`/alerts?stock_codes=${stockQuery}`}>处理组合预警</Link>
          </div>
          <div className="stockGrid">
            {(summary.impacted_stocks.length ? summary.impacted_stocks : watchlist.stock_codes.map((code) => ({ stock_code: code, stock_name: '', event_count: 0, high_impact_count: 0, alert_count: 0, risk_score: 0, risk_level: 'low', priority_action: '', latest_event_at: '' }))).map((stock) => (
              <Link className="stockCard" href={`/stocks/${stock.stock_code}`} key={stock.stock_code}>
                <div>
                  <div className="itemTitle">{stock.stock_name || stock.stock_code}</div>
                <div className="inlineMeta">{stock.stock_code} · {riskLabel(stock.risk_level)} · 最近事件 {stock.latest_event_at || '待刷新'}</div>
                <div className="selectionHint">{stock.priority_action || '保持观察，等待下一次组合刷新。'}</div>
              </div>
              <div className="kpis kpisCompact">
                <div><div className="kpi-label">事件</div><div className="kpi-value">{stock.event_count}</div></div>
                <div><div className="kpi-label">高影响</div><div className="kpi-value">{stock.high_impact_count}</div></div>
                <div><div className="kpi-label">风险分</div><div className="kpi-value">{stock.risk_score}</div></div>
              </div>
            </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
