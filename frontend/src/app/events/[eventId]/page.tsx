import Link from 'next/link'

import { EventAnalyzeButton } from '../../../components/event-analyze-button'
import { fetchEventDetail } from '../../../lib/api'

function sentimentText(sentiment: string) {
  if (sentiment === 'positive') return '利好'
  if (sentiment === 'negative') return '利空'
  if (sentiment === 'uncertain') return '不确定'
  return '中性'
}

export default async function EventDetailPage({ params }: { params: Promise<{ eventId: string }> }) {
  const { eventId } = await params
  const event = await fetchEventDetail(eventId).catch(() => null)

  if (!event) {
    return (
      <main>
        <section className="hero">
          <div className="heroTop">
            <div>
              <div className="eyebrow">Event Detail</div>
              <h1>未找到事件</h1>
              <p>该事件可能尚未进入历史库，或实时来源暂时不可用。</p>
            </div>
            <Link className="ghostLink" href="/events">返回事件追踪</Link>
          </div>
        </section>
        <div className="emptyState">事件 ID：{eventId}</div>
      </main>
    )
  }

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Event Detail</div>
            <h1>{event.title}</h1>
            <p>{event.summary || event.reason}</p>
          </div>
          <div className="actionList compactActions">
            <EventAnalyzeButton eventId={event.event_id} label="更新研报" />
            <Link className="ghostLink" href={`/stocks/${event.stock_code}/timeline`}>股票时间线</Link>
          </div>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">关联股票</div><div className="metricCardValue">{event.stock_code}</div><div className="inlineMeta">{event.stock_name || '待补公司名'}</div></div>
        <div className="metricCard"><div className="statusLabel">事件类型</div><div className="metricCardValue">{event.event_type}</div><div className="inlineMeta">{event.channel || '多源事件'}</div></div>
        <div className="metricCard"><div className="statusLabel">影响等级</div><div className="metricCardValue">{event.impact_level}</div><div className="inlineMeta">{event.impact_scope}</div></div>
        <div className="metricCard"><div className="statusLabel">置信度</div><div className="metricCardValue">{(event.confidence * 100).toFixed(0)}%</div><div className="inlineMeta">{sentimentText(event.sentiment)}</div></div>
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Impact</div>
              <h2>影响判断</h2>
            </div>
          </div>
          <div className="metricStack">
            <div className="card">
              <div className="itemTitle">判断理由</div>
              <p className="bodyText">{event.reason || '暂无自动判断理由。'}</p>
            </div>
            <div className="card">
              <div className="itemTitle">来源</div>
              <p className="bodyText">{event.provider || event.source || '未知来源'} · {event.published_at || event.collected_at}</p>
              {event.url ? <Link className="downloadLink" href={event.url}>打开原文</Link> : null}
            </div>
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Evidence</div>
              <h2>相关来源</h2>
            </div>
          </div>
          <div className="metricStack">
            {event.related_sources.map((source, index) => (
              <div className="card" key={`${source.title}-${index}`}>
                <div className="itemTitle">{source.title || event.title}</div>
                <div className="inlineMeta">{source.provider || source.source || '未知来源'} · {source.time || event.published_at}</div>
                {source.url ? <Link className="downloadLink" href={source.url}>查看来源</Link> : null}
              </div>
            ))}
            {!event.related_sources.length ? <div className="emptyState">暂无相关来源，建议回到事件流刷新实时消息。</div> : null}
          </div>
        </section>
      </div>
    </main>
  )
}
