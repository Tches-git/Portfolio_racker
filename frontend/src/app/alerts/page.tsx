import Link from 'next/link'

import { fetchTrackingAlerts } from '../../lib/api'
import { EventAnalyzeButton } from '../../components/event-analyze-button'

function severityTone(severity: string) {
  if (severity === 'high') return 'tagNegative'
  if (severity === 'medium') return 'tagPositive'
  return ''
}

export default async function AlertsPage({ searchParams }: { searchParams?: Promise<{ stock_codes?: string }> }) {
  const params = await searchParams
  const stockCodes = params?.stock_codes ? params.stock_codes.split(',').map((item) => item.trim()).filter(Boolean) : []
  const alerts = await fetchTrackingAlerts(stockCodes, 4).catch(() => ({ items: [], total: 0, high_severity_count: 0, risk_alert_count: 0, source_degraded_count: 0 }))

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Alert Center</div>
            <h1>金融预警中心</h1>
            <p>把高影响事件、风险事件和来源降级集中成待处理事项，帮助研究流程从“看消息”升级到“处理风险”。</p>
          </div>
          <Link className="ghostLink" href="/events">事件追踪</Link>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">预警总数</div><div className="metricCardValue">{alerts.total}</div><div className="inlineMeta">当前追踪范围</div></div>
        <div className="metricCard"><div className="statusLabel">高优先级</div><div className="metricCardValue">{alerts.high_severity_count}</div><div className="inlineMeta">建议立即复核</div></div>
        <div className="metricCard"><div className="statusLabel">风险事件</div><div className="metricCardValue">{alerts.risk_alert_count}</div><div className="inlineMeta">监管 / 负面 / 风险暴露</div></div>
        <div className="metricCard"><div className="statusLabel">来源降级</div><div className="metricCardValue">{alerts.source_degraded_count}</div><div className="inlineMeta">需补正式来源</div></div>
      </div>

      <section className="panel">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">Open Alerts</div>
            <h2>待处理预警</h2>
          </div>
        </div>
        <div className="detailGrid">
          {alerts.items.map((alert) => (
            <div className="card" key={alert.alert_id}>
              <div className="heroTop">
                <div>
                  <div className="itemTitle">{alert.title}</div>
                  <div className="inlineMeta">{alert.stock_code} · {alert.alert_type} · {alert.created_at}</div>
                </div>
                <span className={`tag ${severityTone(alert.severity)}`}>{alert.severity}</span>
              </div>
              <p className="bodyText">{alert.message}</p>
              <div className="selectionHint">{alert.suggested_action}</div>
              <div className="actionList compactActions">
                <Link className="downloadLink" href={`/stocks/${alert.stock_code}/timeline`}>查看事件时间线</Link>
                <Link className="downloadLink" href={`/events/${alert.event_id}`}>查看事件详情</Link>
                <EventAnalyzeButton eventId={alert.event_id} label="生成事件点评" />
                <Link className="downloadLink" href={`/stocks/${alert.stock_code}`}>进入股票工作台</Link>
              </div>
            </div>
          ))}
          {!alerts.items.length ? <div className="emptyState">当前没有预警。可以先进入事件追踪页查看实时消息流。</div> : null}
        </div>
      </section>
    </main>
  )
}
