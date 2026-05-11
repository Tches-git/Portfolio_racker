import Link from 'next/link'

import { fetchMarketEvents } from '../../lib/api'
import { EventAnalyzeButton } from '../../components/event-analyze-button'

function impactTone(level: string) {
  if (level === 'high') return 'tagNegative'
  if (level === 'medium') return 'tagPositive'
  return ''
}

function sentimentText(sentiment: string) {
  if (sentiment === 'positive') return '利好'
  if (sentiment === 'negative') return '利空'
  if (sentiment === 'uncertain') return '不确定'
  return '中性'
}

export default async function EventsPage({ searchParams }: { searchParams?: Promise<{ stock?: string; mode?: string }> }) {
  const params = await searchParams
  const stocks = params?.stock ? [params.stock] : []
  const mode = params?.mode === 'history' ? 'history' : 'realtime'
  const events = await fetchMarketEvents(stocks, 4, mode).catch(() => ({ items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode }))
  const highImpact = events.items.filter((item) => item.impact_level === 'high')

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Market Event Stream</div>
            <h1>金融事件追踪</h1>
            <p>聚合公告、披露、行情与研报来源，把碎片消息整理成可追踪、可解释、可触发研究任务的事件流。</p>
          </div>
          <div className="chipRow">
            <Link className="ghostLink" href="/events?mode=realtime">实时事件</Link>
            <Link className="ghostLink" href="/events?mode=history">历史事件</Link>
            <Link className="ghostLink" href="/runs">任务中心</Link>
          </div>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">事件总数</div><div className="metricCardValue">{events.total}</div><div className="inlineMeta">当前筛选范围</div></div>
        <div className="metricCard"><div className="statusLabel">高影响事件</div><div className="metricCardValue">{events.high_impact_count}</div><div className="inlineMeta">建议优先复核</div></div>
        <div className="metricCard"><div className="statusLabel">来源渠道</div><div className="metricCardValue">{events.source_count}</div><div className="inlineMeta">公告 / 行情 / 研报</div></div>
        <div className="metricCard"><div className="statusLabel">降级来源</div><div className="metricCardValue">{events.placeholder_count}</div><div className="inlineMeta">需人工确认</div></div>
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Events</div>
              <h2>最新事件流</h2>
            </div>
          </div>
          <div className="timelineList">
            {events.items.map((event) => (
              <div className="timelineCard" key={event.event_id}>
                <div className="timelineDot" />
                <div className="card timelineBody">
                  <div className="heroTop">
                    <div>
                      <div className="itemTitle">{event.title}</div>
                      <div className="inlineMeta">{event.stock_code} · {event.event_type} · {event.provider || event.source} · {event.published_at || event.collected_at}</div>
                    </div>
                    <span className={`tag ${impactTone(event.impact_level)}`}>{event.impact_level}</span>
                  </div>
                  <p className="bodyText">{event.summary || event.reason}</p>
                  <div className="chipRow">
                    <span className="tag">{sentimentText(event.sentiment)}</span>
                    <span className="tag">{event.impact_scope}</span>
                    <span className="tag">置信度 {(event.confidence * 100).toFixed(0)}%</span>
                    <Link className="downloadLink" href={`/events/${event.event_id}`}>事件详情</Link>
                    <Link className="downloadLink" href={`/stocks/${event.stock_code}/timeline`}>股票时间线</Link>
                    <EventAnalyzeButton eventId={event.event_id} />
                  </div>
                </div>
              </div>
            ))}
            {!events.items.length ? <div className="emptyState">暂无事件。请确认 API 服务可访问，或先运行一次股票分析沉淀跟踪标的。</div> : null}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Radar</div>
              <h2>高影响雷达</h2>
            </div>
          </div>
          <div className="metricStack">
            {highImpact.slice(0, 6).map((event) => (
              <div className="card" key={event.event_id}>
                <div className="itemTitle">{event.stock_code} · {event.title}</div>
                <p className="bodyText">{event.reason}</p>
                <div className="actionList compactActions">
                  <Link className="downloadLink" href={`/events/${event.event_id}`}>查看事件详情</Link>
                  <Link className="downloadLink" href={`/stocks/${event.stock_code}`}>进入股票工作台</Link>
                </div>
              </div>
            ))}
            {!highImpact.length ? <div className="emptyState">当前没有高影响事件。</div> : null}
          </div>
        </section>
      </div>
    </main>
  )
}
