import Link from 'next/link'

import { EventAnalyzeButton } from '../event-analyze-button'
import { EventStatusControls } from '../event-status-controls'
import { formatAlertSeverity, formatEventStatus, formatEventType, formatImpactLevel, formatPriority, formatSentiment } from '../../lib/labels'
import type { EventWorkbenchResponse, MarketEvent } from '../../lib/types'
import type { StatusTone } from './primitives'
import { EmptyState, StatusBadge } from './primitives'

type AlertItem = EventWorkbenchResponse['alerts']['items'][number]

const FALLBACK_STOCK_NAMES: Record<string, string> = {
  '600519': '贵州茅台',
  '000858': '五粮液',
  '300750': '宁德时代',
  '000333': '美的集团',
  '600036': '招商银行',
  '601318': '中国平安',
  '600276': '恒瑞医药',
  '002415': '海康威视',
  '002594': '比亚迪',
  '601012': '隆基绿能',
  '601899': '紫金矿业',
  '000002': '万科A',
  '688225': '亚信安全',
}

function eventSummary(event: MarketEvent) {
  return event.summary || event.reason || '暂无摘要'
}

function eventTime(event: MarketEvent) {
  return (event.published_at || event.collected_at || '').replace('T', ' ').slice(0, 16) || '时间待同步'
}

function eventTone(event: MarketEvent): StatusTone {
  if (event.impact_level === 'high') return 'danger'
  if (event.impact_level === 'medium') return 'warning'
  return 'neutral'
}

function eventToneClass(event: MarketEvent) {
  if (event.impact_level === 'high') return 'eventToneDanger'
  if (event.impact_level === 'medium') return 'eventToneWarning'
  return 'eventToneNeutral'
}

export function formatStockIdentity(stockCode: string, stockName?: string) {
  const code = (stockCode || '').trim()
  const name = (stockName || FALLBACK_STOCK_NAMES[code] || '').trim()
  if (name && code && name !== code) return `${name}（${code}）`
  return name || code || '未知标的'
}

export function formatAlertTitle(alert: AlertItem, relatedEvent?: MarketEvent, fallbackStockName = '') {
  const stockName = alert.stock_name || relatedEvent?.stock_name || fallbackStockName
  const stockLabel = formatStockIdentity(alert.stock_code, stockName)
  const rawTitle = (alert.title || alert.rule_name || alert.rule_id || '风险预警').trim()
  const code = (alert.stock_code || '').trim()

  if (!rawTitle) return stockLabel
  if (stockName && rawTitle.includes(stockName) && rawTitle.includes(code)) return rawTitle
  if (stockName && rawTitle.includes(stockName) && !rawTitle.includes(code)) {
    return rawTitle.replace(stockName, stockLabel)
  }
  if (code && rawTitle.startsWith(code)) {
    const suffix = rawTitle.slice(code.length).trim()
    return suffix ? `${stockLabel} ${suffix}` : stockLabel
  }
  if (code && rawTitle.includes(code) && !rawTitle.includes(stockLabel)) {
    return rawTitle.replace(code, stockLabel)
  }
  return rawTitle.includes(stockLabel) ? rawTitle : `${stockLabel} ${rawTitle}`
}

export function EventWorkbench({ data, stockNames = {} }: { data: EventWorkbenchResponse; stockNames?: Record<string, string> }) {
  const eventById = new Map(data.events.items.map((event) => [event.event_id, event]))
  const firstAlertEventId = data.alerts.items[0]?.event_id || ''
  const selected = data.selected_event
    || (data.view === 'alerts' && firstAlertEventId
      ? data.events.items.find((event) => event.event_id === firstAlertEventId)
      : null)
    || data.events.items[0]
    || null
  const selectedEventId = selected?.event_id || ''
  const stockQuery = data.filters.stock_codes ? `&stock_codes=${encodeURIComponent(data.filters.stock_codes)}` : ''

  return (
    <div className="eventCommandDesk">
      <section className="eventStatusTape" aria-label="事件风险状态">
        <div><span>事件</span><strong>{data.events.total}</strong><em>当前账号</em></div>
        <div className={data.events.high_impact_count ? 'eventStatusDanger' : ''}><span>高影响</span><strong>{data.events.high_impact_count}</strong><em>优先解读</em></div>
        <div className={data.alerts.total ? 'eventStatusWarning' : ''}><span>开放预警</span><strong>{data.alerts.total}</strong><em>待复核</em></div>
        <div><span>人工复核</span><strong>{data.alerts.manual_review_count}</strong><em>处理闭环</em></div>
      </section>

      <nav className="eventModeBar" aria-label="事件视图切换">
        <Link className={data.view === 'events' ? 'eventModeActive' : ''} href={`/events?view=events${stockQuery}`}>事件流</Link>
        <Link className={data.view === 'alerts' ? 'eventModeActive' : ''} href={`/events?view=alerts${stockQuery}`}>预警处理</Link>
        <Link href="/watchlist">调整组合范围</Link>
      </nav>

      <section className="eventCommandLayout">
        <main className="eventTapeConsole">
          <header className="eventConsoleHead">
            <div>
              <span>{data.view === 'alerts' ? 'ALERT TAPE' : 'EVENT TAPE'}</span>
              <h2>{data.view === 'alerts' ? '待处理风险队列' : '实时事件流'}</h2>
            </div>
            <em>{data.view === 'alerts' ? `${data.alerts.total} 条预警` : `${data.events.total} 条事件`}</em>
          </header>

          {data.view === 'alerts' ? (
            <ol className="eventTapeList alertTapeList">
              {data.alerts.items.map((alert) => {
                const relatedEvent = eventById.get(alert.event_id) || (selected?.event_id === alert.event_id ? selected : undefined)
                const stockName = alert.stock_name || relatedEvent?.stock_name || stockNames[alert.stock_code]
                const stockLabel = formatStockIdentity(alert.stock_code, stockName)
                const alertTitle = formatAlertTitle(alert, relatedEvent, stockName)
                const isSelected = alert.event_id === selectedEventId
                const href = `/events?view=alerts&selected_event_id=${alert.event_id}${stockQuery}`
                return (
                  <li className={`eventTapeRow ${isSelected ? 'eventTapeRowActive' : ''}`} key={alert.alert_id}>
                    <Link href={href}>
                      <span className={`eventSeverityLamp eventSeverity-${alert.severity}`} aria-hidden />
                      <div className="eventTapeTime">
                        <strong>{alert.priority ? formatPriority(alert.priority) : formatAlertSeverity(alert.severity)}</strong>
                        <em>{stockLabel}</em>
                      </div>
                      <div className="eventTapeMain">
                        <span>{alert.rule_name || alert.rule_id}</span>
                        <strong>{alertTitle}</strong>
                        <p>{alert.message || alert.explanation || alert.suggested_action}</p>
                      </div>
                      <div className="eventTapeAction">{isSelected ? '当前处理' : '处理'}</div>
                    </Link>
                  </li>
                )
              })}
            </ol>
          ) : (
            <ol className="eventTapeList">
              {data.events.items.map((event) => {
                const isSelected = event.event_id === selectedEventId
                return (
                  <li className={`eventTapeRow ${eventToneClass(event)} ${isSelected ? 'eventTapeRowActive' : ''}`} key={event.event_id}>
                    <Link href={`/events?view=events&selected_event_id=${event.event_id}${stockQuery}`}>
                      <span className="eventTapeImpact" aria-hidden />
                      <div className="eventTapeTime">
                        <strong>{eventTime(event)}</strong>
                        <em>{event.provider || event.source || '未知来源'}</em>
                      </div>
                      <div className="eventTapeMain">
                        <span>{event.stock_name || event.stock_code} · {formatEventType(event.event_type)} · {formatSentiment(event.sentiment)}</span>
                        <strong>{event.title}</strong>
                        <p>{eventSummary(event)}</p>
                      </div>
                      <div className="eventTapeBadges">
                        <StatusBadge tone={eventTone(event)}>{formatImpactLevel(event.impact_level)}</StatusBadge>
                        <em>{formatEventStatus(event.status)}</em>
                      </div>
                    </Link>
                  </li>
                )
              })}
            </ol>
          )}

          {data.view === 'alerts' && !data.alerts.items.length ? (
            <EmptyState title="暂无待处理预警" description="当高影响、风险暴露或低置信事件出现时，会进入这里等待复核。" action={{ label: '查看事件流', href: '/events?view=events' }} />
          ) : null}
          {data.view === 'events' && !data.events.items.length ? (
            <EmptyState title="暂无事件" description="请先创建组合并手动刷新事件，系统不会为新用户隐式加载旧数据。" action={{ label: '管理组合', href: '/watchlist' }} />
          ) : null}
        </main>

        <aside className="eventDetailDock" id="event-detail">
          <header>
            <span>DETAIL DOCK</span>
            <h2>{selected?.title || '未选择事件'}</h2>
            {selected ? <p>{selected.stock_name || selected.stock_code} · {eventTime(selected)}</p> : null}
          </header>
          {selected ? (
            <div className="eventDetailBody">
              <p className="eventDetailLead">{eventSummary(selected)}</p>
              <dl className="eventFactGrid">
                <div><dt>股票</dt><dd>{selected.stock_name || selected.stock_code}</dd></div>
                <div><dt>类型</dt><dd>{formatEventType(selected.event_type)}</dd></div>
                <div><dt>影响</dt><dd>{formatImpactLevel(selected.impact_level)}</dd></div>
                <div><dt>情绪</dt><dd>{formatSentiment(selected.sentiment)}</dd></div>
                <div><dt>来源</dt><dd>{selected.provider || selected.source || '未知'}</dd></div>
                <div><dt>置信度</dt><dd>{(selected.confidence * 100).toFixed(0)}%</dd></div>
              </dl>

              <section className="eventEvidencePanel">
                <span>来源证据</span>
                {(selected.related_sources.length ? selected.related_sources : [{ title: selected.title, source: selected.source, provider: selected.provider, url: selected.url, time: selected.published_at }]).slice(0, 4).map((source, index) => (
                  source.url ? (
                    <a href={source.url} target="_blank" rel="noreferrer" key={`${source.title}-${index}`}>
                      <strong>{source.title || selected.title}</strong>
                      <em>{source.provider || source.source || '未知来源'} · {(source.time || '').replace('T', ' ').slice(0, 16) || '时间待同步'}</em>
                    </a>
                  ) : (
                    <div key={`${source.title}-${index}`}>
                      <strong>{source.title || selected.title}</strong>
                      <em>{source.provider || source.source || '未知来源'} · {(source.time || '').replace('T', ' ').slice(0, 16) || '时间待同步'}</em>
                    </div>
                  )
                ))}
              </section>

              <section className="eventActionStack">
                <EventStatusControls eventId={selected.event_id} status={selected.status} statusActor={selected.status_actor} statusNote={selected.status_note} statusUpdatedAt={selected.status_updated_at} />
                <EventAnalyzeButton eventId={selected.event_id} />
                <div className="eventDockLinks">
                  <Link href={`/events/${selected.event_id}`}>新闻式详情</Link>
                  <Link href={`/stocks/${selected.stock_code}`}>单股情报</Link>
                  <Link href={`/markets/${selected.stock_code}`}>行情页</Link>
                </div>
              </section>
            </div>
          ) : <EmptyState title="未选择事件" description="从左侧队列选择事件后，可以复核、忽略或生成事件点评。" />}
        </aside>
      </section>
    </div>
  )
}
