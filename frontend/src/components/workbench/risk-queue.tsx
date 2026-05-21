import Link from 'next/link'

import { formatAlertSeverity, formatPriority } from '../../lib/labels'
import type { TrackingAlertListResponse } from '../../lib/types'

export function RiskQueue({ alerts, compact = false }: { alerts: TrackingAlertListResponse; compact?: boolean }) {
  return (
    <section className="wbPanel">
      <div className="wbPanelHead">
        <div>
          <div className="wbEyebrow">风险队列</div>
          <h2>待处理预警</h2>
        </div>
        <Link className="wbTextButton" href="/events?view=alerts">打开处理台</Link>
      </div>
      <div className="wbTableWrap">
        <table className="wbTable">
          <thead>
            <tr>
              <th>优先级</th>
              <th>预警</th>
              <th>股票</th>
              {!compact ? <th>规则</th> : null}
              <th>动作</th>
            </tr>
          </thead>
          <tbody>
            {alerts.items.slice(0, compact ? 5 : 12).map((alert) => (
              <tr key={alert.alert_id}>
                <td><span className={`wbBadge ${alert.severity === 'high' ? 'tone-danger' : alert.severity === 'medium' ? 'tone-warning' : ''}`}>{alert.priority ? formatPriority(alert.priority) : formatAlertSeverity(alert.severity)}</span></td>
                <td>
                  <Link className="wbPrimaryText" href={`/events?view=alerts&selected_event_id=${alert.event_id}`}>{alert.title}</Link>
                  <div className="wbMuted">{alert.message || alert.explanation}</div>
                </td>
                <td>{alert.stock_code}</td>
                {!compact ? <td>{alert.rule_name || alert.rule_id}</td> : null}
                <td><Link className="wbTextButton" href={`/events?view=alerts&selected_event_id=${alert.event_id}`}>处理</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
        {!alerts.items.length ? <div className="wbEmpty">当前没有待处理预警。</div> : null}
      </div>
    </section>
  )
}
