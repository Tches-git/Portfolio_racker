import Link from 'next/link'

import { fetchAlertRules, fetchTrackingAlerts } from '../../lib/api'
import { EventAnalyzeButton } from '../../components/event-analyze-button'
import { EventStatusControls } from '../../components/event-status-controls'
import type { AlertRuleListResponse, TrackingAlertListResponse } from '../../lib/types'

const EMPTY_ALERTS: TrackingAlertListResponse = {
  items: [],
  total: 0,
  high_severity_count: 0,
  risk_alert_count: 0,
  source_degraded_count: 0,
  manual_review_count: 0,
  severity_counts: {},
  alert_type_counts: {},
  rule_counts: {},
}

const EMPTY_RULES: AlertRuleListResponse = { items: [], total: 0 }

function severityTone(severity: string) {
  if (severity === 'high') return 'tagNegative'
  if (severity === 'medium') return 'tagPositive'
  return ''
}

function alertEventStatus(status: string): 'new' | 'reviewed' | 'ignored' | 'converted_to_report' {
  if (status === 'reviewed' || status === 'ignored' || status === 'converted_to_report') return status
  return 'new'
}

function filterHref(base: Record<string, string>, overrides: Record<string, string>) {
  const next = { ...base, ...overrides }
  const query = new URLSearchParams()
  Object.entries(next).forEach(([key, value]) => {
    if (!value) return
    query.set(key, value)
  })
  const value = query.toString()
  return value ? `/alerts?${value}` : '/alerts'
}

export default async function AlertsPage({ searchParams }: { searchParams?: Promise<{ stock_codes?: string; status?: string; mode?: string; severity?: string; alert_type?: string; rule_id?: string }> }) {
  const params = await searchParams
  const stockCodes = params?.stock_codes ? params.stock_codes.split(',').map((item) => item.trim()).filter(Boolean) : []
  const status = params?.status || 'open'
  const mode = params?.mode === 'history' ? 'history' : 'realtime'
  const severity = params?.severity || ''
  const alertType = params?.alert_type || ''
  const ruleId = params?.rule_id || ''
  const baseQuery = {
    stock_codes: stockCodes.join(','),
    status,
    mode,
    severity,
    alert_type: alertType,
    rule_id: ruleId,
  }
  const [alerts, rules] = await Promise.all([
    fetchTrackingAlerts(stockCodes, 4, status, { mode, severity, alertType, ruleId }).catch(() => EMPTY_ALERTS),
    fetchAlertRules().catch(() => EMPTY_RULES),
  ])
  const activeRule = rules.items.find((rule) => rule.rule_id === ruleId)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">预警中心</div>
            <h1>金融预警中心</h1>
            <p>把高影响事件、风险事件和来源降级集中成待处理事项，帮助研究流程从“看消息”升级到“处理风险”。</p>
          </div>
          <Link className="ghostLink" href="/events">事件追踪</Link>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">预警总数</div><div className="metricCardValue">{alerts.total}</div><div className="inlineMeta">当前追踪范围</div></div>
        <div className="metricCard"><div className="statusLabel">高优先级</div><div className="metricCardValue">{alerts.high_severity_count}</div><div className="inlineMeta">建议立即复核</div></div>
        <div className="metricCard"><div className="statusLabel">人工复核</div><div className="metricCardValue">{alerts.manual_review_count}</div><div className="inlineMeta">低置信高影响</div></div>
        <div className="metricCard"><div className="statusLabel">风险事件</div><div className="metricCardValue">{alerts.risk_alert_count}</div><div className="inlineMeta">监管 / 负面 / 风险暴露</div></div>
        <div className="metricCard"><div className="statusLabel">来源降级</div><div className="metricCardValue">{alerts.source_degraded_count}</div><div className="inlineMeta">需补正式来源</div></div>
      </div>

      <section className="panel">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">规则中心</div>
            <h2>内置预警规则</h2>
          </div>
          <div className="inlineMeta">{mode === 'history' ? '历史事件视角' : '实时事件视角'}</div>
        </div>
        <div className="detailGrid">
          {rules.items.map((rule) => (
            <Link className={`card${rule.rule_id === ruleId ? ' selectedCard' : ''}`} href={filterHref(baseQuery, { rule_id: rule.rule_id })} key={rule.rule_id}>
              <div className="heroTop">
                <div>
                  <div className="itemTitle">{rule.name}</div>
                  <div className="inlineMeta">{rule.priority} · {rule.severity} · 命中 {alerts.rule_counts[rule.rule_id] || 0}</div>
                </div>
                <span className={`tag ${severityTone(rule.severity)}`}>{rule.alert_type}</span>
              </div>
              <p className="bodyText">{rule.description}</p>
            </Link>
          ))}
          {!rules.items.length ? <div className="emptyState">暂未获取到预警规则，请确认 API 服务可用。</div> : null}
        </div>
      </section>

      <section className="panel">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">预警列表</div>
            <h2>{activeRule ? `${activeRule.name} · ` : ''}{status === 'open' ? '待处理预警' : '预警处理记录'}</h2>
          </div>
        </div>
        <div className="filterBar">
          <Link className={`filterChip${mode === 'realtime' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { mode: 'realtime' })}>实时</Link>
          <Link className={`filterChip${mode === 'history' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { mode: 'history' })}>历史</Link>
          <Link className={`filterChip${status === 'open' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { status: 'open' })}>待处理</Link>
          <Link className={`filterChip${status === 'reviewed' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { status: 'reviewed' })}>已复核</Link>
          <Link className={`filterChip${status === 'ignored' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { status: 'ignored' })}>已忽略</Link>
          <Link className={`filterChip${status === 'converted_to_report' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { status: 'converted_to_report' })}>已转研报</Link>
          <Link className={`filterChip${status === 'all' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { status: 'all' })}>全部</Link>
          <Link className={`filterChip${!severity ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { severity: '' })}>全部优先级</Link>
          <Link className={`filterChip${severity === 'high' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { severity: 'high' })}>高优先级</Link>
          <Link className={`filterChip${severity === 'medium' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { severity: 'medium' })}>中优先级</Link>
          <Link className={`filterChip${!alertType ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { alert_type: '' })}>全部类型</Link>
          <Link className={`filterChip${alertType === 'manual_review' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { alert_type: 'manual_review' })}>人工复核</Link>
          <Link className={`filterChip${alertType === 'risk_watch' ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { alert_type: 'risk_watch' })}>风险</Link>
          <Link className={`filterChip${!ruleId ? ' filterChipActive' : ''}`} href={filterHref(baseQuery, { rule_id: '' })}>全部规则</Link>
        </div>
        <div className="detailGrid">
          {alerts.items.map((alert) => (
            <div className="card" key={alert.alert_id}>
              <div className="heroTop">
                <div>
                  <div className="itemTitle">{alert.title}</div>
                  <div className="inlineMeta">{alert.stock_code} · {alert.rule_name || alert.alert_type} · {alert.priority} · {alert.created_at}</div>
                </div>
                <div className="chipRow">
                  <span className={`tag ${severityTone(alert.severity)}`}>{alert.severity}</span>
                  <span className="tag">{alert.status}</span>
                </div>
              </div>
              <p className="bodyText">{alert.message}</p>
              <div className="selectionHint">{alert.explanation}</div>
              <div className="selectionHint">{alert.suggested_action}</div>
              <EventStatusControls
                eventId={alert.event_id}
                status={alertEventStatus(alert.status)}
                statusUpdatedAt={alert.handled_at}
                statusActor={alert.handled_by}
                statusNote={alert.handling_note}
              />
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
