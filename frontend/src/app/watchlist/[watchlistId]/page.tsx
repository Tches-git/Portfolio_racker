import Link from 'next/link'

import { EventAnalyzeButton } from '../../../components/event-analyze-button'
import { WatchlistRefreshButton } from '../../../components/watchlist-refresh-button'
import { fetchWatchlistDetail } from '../../../lib/api'

function impactTone(level: string) {
  if (level === 'high') return 'tagNegative'
  if (level === 'medium') return 'tagPositive'
  return ''
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
              <div className="eyebrow">Watchlist Detail</div>
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

  const { watchlist, summary, events, alerts, briefing } = detail
  const stockQuery = watchlist.stock_codes.join(',')
  const highImpactEvents = events.items.filter((event) => event.impact_level === 'high')

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Watchlist Detail</div>
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
        <div className="metricCard"><div className="statusLabel">追踪股票</div><div className="metricCardValue">{summary.stock_count}</div><div className="inlineMeta">当前组合股票池</div></div>
        <div className="metricCard"><div className="statusLabel">历史事件</div><div className="metricCardValue">{summary.event_count}</div><div className="inlineMeta">来源 {summary.source_count} · 降级 {summary.placeholder_count}</div></div>
        <div className="metricCard"><div className="statusLabel">高影响</div><div className="metricCardValue">{summary.high_impact_count}</div><div className="inlineMeta">需要优先复核</div></div>
        <div className="metricCard"><div className="statusLabel">开放预警</div><div className="metricCardValue">{summary.alert_count}</div><div className="inlineMeta">高优先级 {summary.high_severity_count}</div></div>
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Portfolio Events</div>
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
              <div className="sectionEyebrow">Briefing</div>
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
                <div className="inlineMeta">{alert.severity} · {alert.suggested_action}</div>
              </div>
            ))}
            {!alerts.items.length ? <div className="emptyState">当前组合暂无开放预警。</div> : null}
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Stocks</div>
              <h2>受影响股票排序</h2>
            </div>
            <Link className="downloadLink" href={`/alerts?stock_codes=${stockQuery}`}>处理组合预警</Link>
          </div>
          <div className="stockGrid">
            {(summary.impacted_stocks.length ? summary.impacted_stocks : watchlist.stock_codes.map((code) => ({ stock_code: code, stock_name: '', event_count: 0, high_impact_count: 0, latest_event_at: '' }))).map((stock) => (
              <Link className="stockCard" href={`/stocks/${stock.stock_code}`} key={stock.stock_code}>
                <div>
                  <div className="itemTitle">{stock.stock_name || stock.stock_code}</div>
                  <div className="inlineMeta">{stock.stock_code} · 最近事件 {stock.latest_event_at || '待刷新'}</div>
                </div>
                <div className="kpis kpisCompact">
                  <div><div className="kpi-label">事件</div><div className="kpi-value">{stock.event_count}</div></div>
                  <div><div className="kpi-label">高影响</div><div className="kpi-value">{stock.high_impact_count}</div></div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
