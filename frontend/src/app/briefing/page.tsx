import Link from 'next/link'

import { fetchDailyBriefing } from '../../lib/api'
import { EventAnalyzeButton } from '../../components/event-analyze-button'

export default async function BriefingPage({ searchParams }: { searchParams?: Promise<{ stock_codes?: string }> }) {
  const params = await searchParams
  const stockCodes = params?.stock_codes ? params.stock_codes.split(',').map((item) => item.trim()).filter(Boolean) : []
  const briefing = await fetchDailyBriefing(stockCodes, 4).catch(() => ({ title: '今日金融事件简报', summary: '暂未获取到事件数据。', generated_at: '', total_events: 0, high_impact_count: 0, negative_event_count: 0, source_count: 0, key_events: [], alerts: [], suggested_actions: [], themes: [], review_required_events: [] }))

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">每日简报</div>
            <h1>{briefing.title}</h1>
            <p>{briefing.summary}</p>
          </div>
          <Link className="ghostLink" href="/alerts">预警中心</Link>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">追踪事件</div><div className="metricCardValue">{briefing.total_events}</div><div className="inlineMeta">{briefing.generated_at || '实时生成'}</div></div>
        <div className="metricCard"><div className="statusLabel">高影响</div><div className="metricCardValue">{briefing.high_impact_count}</div><div className="inlineMeta">优先复核</div></div>
        <div className="metricCard"><div className="statusLabel">风险/利空</div><div className="metricCardValue">{briefing.negative_event_count}</div><div className="inlineMeta">进入风险雷达</div></div>
        <div className="metricCard"><div className="statusLabel">来源渠道</div><div className="metricCardValue">{briefing.source_count}</div><div className="inlineMeta">来源覆盖</div></div>
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">关键事件</div>
              <h2>今日关键事件</h2>
            </div>
          </div>
          <div className="timelineList">
            {briefing.key_events.map((event) => (
              <div className="timelineCard" key={event.event_id}>
                <div className="timelineDot" />
                <div className="card timelineBody">
                  <div className="itemTitle">{event.stock_code} · {event.title}</div>
                  <div className="inlineMeta">{event.event_type} · {event.impact_level} · {event.provider || event.source}</div>
                  <p className="bodyText">{event.reason || event.summary}</p>
                  <div className="actionList compactActions">
                    <Link className="downloadLink" href={`/events/${event.event_id}`}>事件详情</Link>
                    <Link className="downloadLink" href={`/stocks/${event.stock_code}/timeline`}>查看时间线</Link>
                    <EventAnalyzeButton eventId={event.event_id} label="更新研报" />
                  </div>
                </div>
              </div>
            ))}
            {!briefing.key_events.length ? <div className="emptyState">暂无关键事件。</div> : null}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">建议动作</div>
              <h2>建议动作</h2>
            </div>
          </div>
          <div className="metricStack">
            {briefing.suggested_actions.map((action) => (
              <div className="card" key={action}>
                <div className="itemTitle">{action}</div>
              </div>
            ))}
            {briefing.themes.map((theme) => (
              <div className="card" key={theme}>
                <div className="itemTitle">今日主题</div>
                <p className="bodyText">{theme}</p>
              </div>
            ))}
            {briefing.review_required_events.map((event) => (
              <div className="card" key={`review-${event.event_id}`}>
                <div className="itemTitle">需人工复核：{event.title}</div>
                <p className="bodyText">{event.reason || event.summary}</p>
                <Link className="downloadLink" href={`/events/${event.event_id}`}>复核事件</Link>
              </div>
            ))}
            {briefing.alerts.slice(0, 4).map((alert) => (
              <div className="card" key={alert.alert_id}>
                <div className="itemTitle">{alert.title}</div>
                <p className="bodyText">{alert.message}</p>
                <Link className="downloadLink" href={`/stocks/${alert.stock_code}/timeline`}>处理预警</Link>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
