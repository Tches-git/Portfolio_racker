import Link from 'next/link'

import { EventAnalyzeButton } from '../event-analyze-button'
import { EventStatusControls } from '../event-status-controls'
import type { EventWorkbenchResponse, MarketEvent } from '../../lib/types'
import { RiskQueue } from './risk-queue'

function eventSummary(event: MarketEvent) {
  return event.summary || event.reason || '暂无摘要'
}

export function EventWorkbench({ data }: { data: EventWorkbenchResponse }) {
  const selected = data.selected_event || data.events.items[0] || null
  const stockQuery = data.filters.stock_codes ? `&stock_codes=${encodeURIComponent(data.filters.stock_codes)}` : ''

  return (
    <div className="wbStack">
      <div className="wbTabs">
        <Link className={`wbTab ${data.view === 'events' ? 'wbTabActive' : ''}`} href={`/events?view=events${stockQuery}`}>事件列表</Link>
        <Link className={`wbTab ${data.view === 'alerts' ? 'wbTabActive' : ''}`} href={`/events?view=alerts${stockQuery}`}>预警处理</Link>
        <Link className="wbTab" href="/watchlist">组合范围</Link>
      </div>

      <section className="wbMetricGrid">
        <div className="wbMetric"><span>事件总数</span><strong>{data.events.total}</strong><em>当前筛选</em></div>
        <div className="wbMetric"><span>高影响</span><strong>{data.events.high_impact_count}</strong><em>优先复核</em></div>
        <div className="wbMetric"><span>开放预警</span><strong>{data.alerts.total}</strong><em>高优先级 {data.alerts.high_severity_count}</em></div>
        <div className="wbMetric"><span>人工复核</span><strong>{data.alerts.manual_review_count}</strong><em>低置信高影响</em></div>
      </section>

      {data.view === 'alerts' ? (
        <RiskQueue alerts={data.alerts} />
      ) : (
        <section className="wbPanel">
          <div className="wbPanelHead">
            <div>
              <div className="wbEyebrow">事件台</div>
              <h2>事件列表</h2>
            </div>
          </div>
          <div className="wbTableWrap">
            <table className="wbTable">
              <thead>
                <tr>
                  <th>事件</th>
                  <th>股票</th>
                  <th>来源</th>
                  <th>影响</th>
                  <th>状态</th>
                  <th>动作</th>
                </tr>
              </thead>
              <tbody>
                {data.events.items.map((event) => (
                  <tr key={event.event_id}>
                    <td>
                      <Link className="wbPrimaryText" href={`/events?view=events&selected_event_id=${event.event_id}`}>{event.title}</Link>
                      <div className="wbMuted">{eventSummary(event)}</div>
                    </td>
                    <td>{event.stock_code}</td>
                    <td>{event.provider || event.source || '未知'}</td>
                    <td><span className={`wbBadge ${event.impact_level === 'high' ? 'wbBadgeDanger' : ''}`}>{event.impact_level}</span></td>
                    <td>{event.status}</td>
                    <td><Link className="wbTextButton" href={`/stocks/${event.stock_code}`}>股票</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!data.events.items.length ? <div className="wbEmpty">暂无事件。请先创建组合并手动刷新事件。</div> : null}
          </div>
        </section>
      )}

      <section className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">当前事件</div>
            <h2>{selected?.title || '未选择事件'}</h2>
          </div>
          {selected ? <Link className="wbTextButton" href={`/stocks/${selected.stock_code}`}>进入股票</Link> : null}
        </div>
        {selected ? (
          <div className="wbDetailGrid">
            <div>
              <p className="wbLead">{eventSummary(selected)}</p>
              <div className="wbChipRow">
                <span className="wbChip">{selected.stock_code}</span>
                <span className="wbChip">{selected.event_type}</span>
                <span className="wbChip">置信度 {(selected.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
            <div className="wbActionColumn">
              <EventStatusControls eventId={selected.event_id} status={selected.status} statusActor={selected.status_actor} statusNote={selected.status_note} statusUpdatedAt={selected.status_updated_at} />
              <EventAnalyzeButton eventId={selected.event_id} />
            </div>
          </div>
        ) : <div className="wbEmpty">从左侧列表选择事件后，可以复核、忽略或生成事件点评。</div>}
      </section>
    </div>
  )
}
