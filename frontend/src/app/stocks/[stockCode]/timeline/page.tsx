import Link from 'next/link'

import { StockWorkspaceNav } from '../../../../components/stock-workspace-nav'
import { fetchStockEvents } from '../../../../lib/api'

function impactTone(level: string) {
  if (level === 'high') return 'tagNegative'
  if (level === 'medium') return 'tagPositive'
  return ''
}

export default async function StockTimelinePage({ params }: { params: Promise<{ stockCode: string }> }) {
  const { stockCode } = await params
  const timeline = await fetchStockEvents(stockCode, 10).catch(() => ({ stock_code: stockCode, stock_name: '', items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode: 'realtime' }))

  return (
    <main>
      <section className="hero stockHero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">股票事件时间线</div>
            <h1>{timeline.stock_name || stockCode} 事件时间线</h1>
            <p>{stockCode} · 聚合公告、披露、行情和研报观点，持续判断事件类型、影响方向和复核优先级。</p>
          </div>
          <Link className="ghostLink" href="/events">全局事件流</Link>
        </div>
      </section>

      <StockWorkspaceNav stockCode={stockCode} current="timeline" />

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">事件总数</div><div className="metricCardValue">{timeline.total}</div><div className="inlineMeta">当前股票</div></div>
        <div className="metricCard"><div className="statusLabel">高影响</div><div className="metricCardValue">{timeline.high_impact_count}</div><div className="inlineMeta">需要优先复核</div></div>
        <div className="metricCard"><div className="statusLabel">来源渠道</div><div className="metricCardValue">{timeline.source_count}</div><div className="inlineMeta">来源覆盖</div></div>
        <div className="metricCard"><div className="statusLabel">合并来源</div><div className="metricCardValue">{timeline.duplicate_count}</div><div className="inlineMeta">重复事件聚合</div></div>
      </div>

      <section className="panel">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">时间线</div>
            <h2>事件明细</h2>
          </div>
        </div>
        <div className="timelineList">
          {timeline.items.map((event) => (
            <div className="timelineCard" key={event.event_id}>
              <div className="timelineDot" />
              <div className="card timelineBody">
                <div className="heroTop">
                  <div>
                    <div className="itemTitle">{event.title}</div>
                    <div className="inlineMeta">{event.published_at || event.collected_at} · {event.provider || event.source} · {event.event_type}</div>
                  </div>
                  <span className={`tag ${impactTone(event.impact_level)}`}>{event.impact_level}</span>
                </div>
                <p className="bodyText">{event.summary || event.reason}</p>
                <div className="detailGrid">
                  <div className="card"><div className="statusLabel">影响方向</div><div className="itemTitle">{event.sentiment}</div><div className="inlineMeta">{event.reason}</div></div>
                  <div className="card"><div className="statusLabel">影响范围</div><div className="itemTitle">{event.impact_scope}</div><div className="inlineMeta">置信度 {(event.confidence * 100).toFixed(0)}%</div></div>
                  <div className="card"><div className="statusLabel">来源数</div><div className="itemTitle">{event.related_sources.length}</div><div className="inlineMeta">{event.retrieval_mode || 'api'}</div></div>
                </div>
                <Link className="downloadLink" href={`/events/${event.event_id}`}>查看事件详情</Link>
              </div>
            </div>
          ))}
          {!timeline.items.length ? <div className="emptyState">当前股票暂无事件。请确认 API 服务可访问，或稍后重新抓取来源。</div> : null}
        </div>
      </section>
    </main>
  )
}
