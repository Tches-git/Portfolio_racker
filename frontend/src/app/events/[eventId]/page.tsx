import Link from 'next/link'
import { notFound } from 'next/navigation'

import { EventAnalyzeButton } from '../../../components/event-analyze-button'
import { EventStatusControls } from '../../../components/event-status-controls'
import { StatusBadge } from '../../../components/workbench/primitives'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchEventDetail, fetchMarketWorkbench } from '../../../lib/api'
import { formatEventStatus, formatEventType, formatImpactLevel, formatSentiment } from '../../../lib/labels'
import { serverApiOptions } from '../../../lib/server-auth'
import type { MarketEvent, MarketWorkbenchResponse } from '../../../lib/types'

function eventTime(event: MarketEvent) {
  return (event.published_at || event.collected_at || '').replace('T', ' ').slice(0, 16) || '时间待同步'
}

function eventSummary(event: MarketEvent) {
  return event.summary || event.reason || '暂无摘要'
}

function sourceLabel(event: MarketEvent) {
  return event.source || event.provider || '未知来源'
}

function shouldShowMarketSnapshot(event: MarketEvent) {
  return event.event_type === 'market_move' || event.evidence_type === 'quote' || event.provider === 'akshare_profile'
}

function formatNumber(value: number, digits = 2) {
  if (!Number.isFinite(value) || value === 0) return '--'
  return value.toLocaleString('zh-CN', { maximumFractionDigits: digits })
}

function formatPercent(value: number) {
  if (!Number.isFinite(value) || value === 0) return '--'
  return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`
}

export default async function EventDetailPage({ params }: { params: Promise<{ eventId: string }> }) {
  const { eventId } = await params
  const apiOptions = await serverApiOptions()
  const event = await fetchEventDetail(eventId, apiOptions)

  if (!event) notFound()

  let market: MarketWorkbenchResponse | null = null
  if (shouldShowMarketSnapshot(event)) {
    try {
      market = await fetchMarketWorkbench(event.stock_code, '30d', apiOptions)
    } catch {
      market = null
    }
  }

  const relatedSources = event.related_sources.length
    ? event.related_sources
    : [{
        title: event.title,
        source: sourceLabel(event),
        provider: event.provider,
        url: event.url,
        time: event.published_at,
      }]

  return (
    <WorkspaceShell
      eyebrow="事件详情"
      title={event.title}
      description={eventSummary(event)}
      actions={[
        { label: '返回事件台', href: `/events?view=events&selected_event_id=${event.event_id}&stock_codes=${event.stock_code}`, method: 'GET', action_type: 'navigate', target_id: event.event_id, variant: 'secondary' },
        { label: '进入股票', href: `/stocks/${event.stock_code}`, method: 'GET', action_type: 'navigate', target_id: event.stock_code, variant: 'secondary' },
      ]}
    >
      <article className="eventArticle">
        <header className="eventArticleHeader">
          <div className="eventArticleKicker">
            <span>{event.stock_name || event.stock_code}</span>
            <span>{event.stock_code}</span>
            <span>{eventTime(event)}</span>
            <span>{sourceLabel(event)}</span>
          </div>
          <h2>{event.title}</h2>
          <p className="eventArticleLead">{eventSummary(event)}</p>
          <div className="wbChipRow">
            <span className="wbChip">{formatEventType(event.event_type)}</span>
            <span className="wbChip">{formatSentiment(event.sentiment)}</span>
            <StatusBadge tone={event.impact_level === 'high' ? 'danger' : event.impact_level === 'medium' ? 'warning' : 'neutral'}>{formatImpactLevel(event.impact_level)}</StatusBadge>
            <span className="wbChip">置信度 {(event.confidence * 100).toFixed(0)}%</span>
            <span className="wbChip">{formatEventStatus(event.status)}</span>
          </div>
        </header>

        <section className="eventArticleBody">
          <div className="eventArticleMain">
            <section className="eventArticleSection">
              <div className="wbEyebrow">事件正文</div>
              <div className="eventArticleParagraphs">
                <p>{eventSummary(event)}</p>
                <p>
                  系统在 {eventTime(event)} 从 {sourceLabel(event)} 捕获该事件，并将其归类为
                  {formatEventType(event.event_type)}，情绪判断为{formatSentiment(event.sentiment)}，
                  当前影响等级为{formatImpactLevel(event.impact_level)}。
                </p>
                {event.url ? <p><a className="eventInlineLink" href={event.url} target="_blank" rel="noreferrer">打开原始来源</a></p> : null}
              </div>
            </section>

            {market ? (
              <section className="eventArticleSection">
                <div className="wbEyebrow">行情快照</div>
                <div className="eventQuoteStrip">
                  <div>
                    <span>最新价</span>
                    <strong>{formatNumber(market.quote.price)}</strong>
                  </div>
                  <div className={market.quote.change_pct >= 0 ? 'tone-success' : 'tone-danger'}>
                    <span>涨跌幅</span>
                    <strong>{formatPercent(market.quote.change_pct)}</strong>
                  </div>
                  <div>
                    <span>成交额</span>
                    <strong>{formatNumber(market.quote.amount / 100000000)} 亿</strong>
                  </div>
                  <div>
                    <span>更新时间</span>
                    <strong>{market.quote.updated_at || '待同步'}</strong>
                  </div>
                </div>
                <Link className="eventInlineLink" href={`/markets/${event.stock_code}`}>查看完整行情页</Link>
              </section>
            ) : null}

            <section className="eventArticleSection">
              <div className="wbEyebrow">影响判断</div>
              <p>{event.reason || `该事件被识别为${formatSentiment(event.sentiment)}，当前影响等级为${formatImpactLevel(event.impact_level)}。`}</p>
              <dl className="eventArticleFacts">
                <div><dt>事件类型</dt><dd>{formatEventType(event.event_type)}</dd></div>
                <div><dt>影响范围</dt><dd>{event.impact_scope || '待补充'}</dd></div>
                <div><dt>采集模式</dt><dd>{event.retrieval_mode || '历史沉淀'}</dd></div>
                <div><dt>证据类型</dt><dd>{event.evidence_type || '来源文本'}</dd></div>
              </dl>
            </section>

            <section className="eventArticleSection">
              <div className="wbEyebrow">来源证据</div>
              <div className="eventSourceList">
                {relatedSources.map((source, index) => (
                  source.url || event.url ? (
                    <a
                      className="eventSourceItem"
                      href={source.url || event.url}
                      key={`${source.url || source.title}-${index}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      <strong>{source.title || event.title}</strong>
                      <span>{source.source || source.provider || sourceLabel(event)} · {(source.time || event.published_at || '').replace('T', ' ').slice(0, 16) || '时间待同步'}</span>
                      <em>打开原文</em>
                    </a>
                  ) : (
                    <Link className="eventSourceItem" href={`/markets/${event.stock_code}`} key={`${source.title}-${index}`}>
                      <strong>{source.title || event.title}</strong>
                      <span>{source.source || source.provider || sourceLabel(event)} · {(source.time || event.published_at || '').replace('T', ' ').slice(0, 16) || '时间待同步'}</span>
                      <em>无原文链接，查看行情快照</em>
                    </Link>
                  )
                ))}
              </div>
            </section>
          </div>

          <aside className="eventArticleDock">
            <div className="eventArticleDockBlock">
              <div className="wbEyebrow">处理动作</div>
              <EventStatusControls eventId={event.event_id} status={event.status} statusActor={event.status_actor} statusNote={event.status_note} statusUpdatedAt={event.status_updated_at} />
              <EventAnalyzeButton eventId={event.event_id} />
            </div>
            <div className="eventArticleDockBlock">
              <div className="wbEyebrow">快捷入口</div>
              <Link className="wbTextButton" href={`/events?view=events&selected_event_id=${event.event_id}&stock_codes=${event.stock_code}`}>返回事件队列定位</Link>
              <Link className="wbTextButton" href={`/stocks/${event.stock_code}`}>打开单股情报中心</Link>
              <Link className="wbTextButton" href={`/markets/${event.stock_code}`}>查看行情快照</Link>
            </div>
          </aside>
        </section>
      </article>
    </WorkspaceShell>
  )
}
