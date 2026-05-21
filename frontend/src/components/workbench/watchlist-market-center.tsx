'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useState, useTransition } from 'react'

import { WatchlistRefreshButton } from '../watchlist-refresh-button'
import type { MarketDailyBar, TrackingAlert, WatchlistDetailResponse, WatchlistMarketSnapshot } from '../../lib/types'

type RangeKey = '30d' | '90d' | '180d'

const RANGES: Array<{ key: RangeKey; label: string }> = [
  { key: '30d', label: '30日' },
  { key: '90d', label: '90日' },
  { key: '180d', label: '180日' },
]

export function WatchlistMarketCenter({ detail }: { detail: WatchlistDetailResponse }) {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const snapshots = detail.market_snapshots || []
  const firstCode = snapshots[0]?.stock_code || detail.watchlist.stock_codes[0] || ''
  const [selectedCode, setSelectedCode] = useState(firstCode)
  const [range, setRange] = useState<RangeKey>('90d')

  useEffect(() => {
    if (!snapshots.length) return
    if (!snapshots.some((item) => item.stock_code === selectedCode)) {
      setSelectedCode(snapshots[0].stock_code)
    }
  }, [selectedCode, snapshots])

  useEffect(() => {
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'hidden') return
      startTransition(() => router.refresh())
    }, 60000)
    return () => window.clearInterval(timer)
  }, [router, startTransition])

  const selected = useMemo(
    () => snapshots.find((item) => item.stock_code === selectedCode) || snapshots[0],
    [selectedCode, snapshots],
  )
  const stockQuery = detail.watchlist.stock_codes.join(',')
  const selectedAlerts = selected ? detail.alerts.items.filter((alert) => alert.stock_code === selected.stock_code).slice(0, 4) : []
  const openAlerts = detail.summary.open_alert_count

  function refreshMarket() {
    startTransition(() => router.refresh())
  }

  if (!snapshots.length) {
    return (
      <div className="portfolioMarketCenter">
        <PortfolioMarketHeader detail={detail} isPending={isPending} onRefresh={refreshMarket} />
        <div className="portfolioMarketEmpty">
          <strong>暂无可展示行情</strong>
          <span>{detail.market_fallback_message || '当前组合还没有可用行情数据，请稍后刷新行情或检查股票池。'}</span>
          <Link href="/watchlist">返回组合列表</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="portfolioMarketCenter">
      <PortfolioMarketHeader detail={detail} isPending={isPending} onRefresh={refreshMarket} />

      <section className="portfolioMarketLayout">
        <PortfolioQuoteTable snapshots={snapshots} selectedCode={selected?.stock_code || ''} onSelect={setSelectedCode} />

        <main className="portfolioTrendPanel">
          <div className="portfolioTrendHead">
            <div>
              <span>INTERACTIVE K-LINE</span>
              <h2>{stockTitle(selected)} 日 K 走势</h2>
              <p>{sourceStatusLabel(selected?.source_status || 'degraded')} · 更新时间 {selected?.quote.updated_at || detail.market_updated_at || '--'}</p>
            </div>
            <div className="portfolioRangeTabs" aria-label="走势图区间">
              {RANGES.map((item) => (
                <button className={range === item.key ? 'active' : ''} type="button" onClick={() => setRange(item.key)} key={item.key}>
                  {item.label}
                </button>
              ))}
            </div>
          </div>
          <PortfolioTrendChart bars={trendBars(selected, range)} snapshot={selected} />
          <div className="portfolioMetricTape" aria-label="行情指标">
            <MetricCell label="最新价" value={formatPrice(selected?.quote.price || 0)} tone={(selected?.quote.change_pct || 0) >= 0 ? 'up' : 'down'} />
            <MetricCell label="涨跌幅" value={`${formatSigned(selected?.quote.change_pct || 0)}%`} tone={(selected?.quote.change_pct || 0) >= 0 ? 'up' : 'down'} />
            <MetricCell label="成交额" value={formatAmount(selected?.quote.amount || 0)} />
            <MetricCell label="换手率" value={formatPercent(selected?.quote.turnover || 0)} />
            <MetricCell label="PE / PB" value={`${formatRatio(selected?.quote.pe_ratio || 0)} / ${formatRatio(selected?.quote.pb_ratio || 0)}`} />
            <MetricCell label="数据源" value={selected?.quote.provider || sourceStatusLabel(selected?.source_status || '')} />
          </div>
        </main>

        <MarketSuggestionDock
          snapshot={selected}
          alerts={selectedAlerts}
          openAlerts={openAlerts}
          stockQuery={stockQuery}
          marketFallback={detail.market_fallback_message}
        />
      </section>

      <section className="portfolioSupportStrip">
        <div>
          <span>EVENT RADAR</span>
          <strong>{detail.summary.event_count}</strong>
          <em>当前组合事件</em>
        </div>
        <div>
          <span>HIGH IMPACT</span>
          <strong>{detail.summary.high_impact_count}</strong>
          <em>高影响事件</em>
        </div>
        <div>
          <span>ALERT QUEUE</span>
          <strong>{detail.summary.open_alert_count}</strong>
          <em>开放预警</em>
        </div>
        <div>
          <span>REFRESH MODE</span>
          <strong>60s</strong>
          <em>隐藏标签页暂停</em>
        </div>
      </section>
    </div>
  )
}

function PortfolioMarketHeader({
  detail,
  isPending,
  onRefresh,
}: {
  detail: WatchlistDetailResponse
  isPending: boolean
  onRefresh: () => void
}) {
  const riskLevel = detail.summary.risk_level
  const stockQuery = detail.watchlist.stock_codes.join(',')
  return (
    <section className={`portfolioMarketHeader marketRisk-${riskLevel}`}>
      <div className="portfolioMarketIdentity">
        <span>PORTFOLIO MARKET CENTER</span>
        <h2>{detail.watchlist.name}</h2>
        <p>{detail.watchlist.description || '组合行情、事件预警和研究建议集中展示。'}</p>
      </div>
      <div className="portfolioMarketMetrics">
        <HeaderMetric label="股票数" value={detail.summary.stock_count || detail.watchlist.stock_codes.length} hint="组合内标的" />
        <HeaderMetric label="风险分" value={detail.summary.risk_score} hint={riskLabel(detail.summary.risk_level)} tone={riskLevel} />
        <HeaderMetric label="开放预警" value={detail.summary.open_alert_count} hint="待处理" tone={detail.summary.open_alert_count ? 'medium' : 'low'} />
        <HeaderMetric label="最近刷新" value={shortTime(detail.summary.last_refreshed_at || detail.watchlist.last_refreshed_at)} hint="事件采集" />
        <HeaderMetric label="行情时间" value={shortTime(detail.market_updated_at)} hint="自动轮询" />
      </div>
      <div className="portfolioMarketActions">
        <button className="portfolioMarketRefresh" type="button" onClick={onRefresh} disabled={isPending}>
          {isPending ? '刷新中' : '刷新行情'}
        </button>
        <WatchlistRefreshButton watchlistId={detail.watchlist.watchlist_id} />
        <Link href={`/events?view=alerts&stock_codes=${stockQuery}`}>处理预警</Link>
      </div>
    </section>
  )
}

function HeaderMetric({ label, value, hint, tone = 'neutral' }: { label: string; value: string | number; hint: string; tone?: string }) {
  return (
    <div className={`portfolioHeaderMetric tone-${tone}`}>
      <span>{label}</span>
      <strong>{value || '--'}</strong>
      <em>{hint}</em>
    </div>
  )
}

export function PortfolioQuoteTable({
  snapshots,
  selectedCode,
  onSelect,
}: {
  snapshots: WatchlistMarketSnapshot[]
  selectedCode: string
  onSelect: (stockCode: string) => void
}) {
  return (
    <aside className="portfolioQuotePane">
      <header>
        <div>
          <span>QUOTE BOARD</span>
          <h2>组合行情表</h2>
        </div>
        <b>{snapshots.length} 只</b>
      </header>
      <div className="portfolioQuoteWrap">
        <table className="portfolioQuoteTable">
          <thead>
            <tr>
              <th>股票</th>
              <th>最新</th>
              <th>涨跌幅</th>
              <th>成交额</th>
              <th>换手</th>
              <th>PE/PB</th>
            </tr>
          </thead>
          <tbody>
            {snapshots.map((snapshot) => {
              const changeTone = snapshot.quote.change_pct >= 0 ? 'marketUp' : 'marketDown'
              return (
                <tr className={snapshot.stock_code === selectedCode ? 'portfolioQuoteRowActive' : ''} key={snapshot.stock_code}>
                  <td>
                    <button className="portfolioQuoteSelect" type="button" onClick={() => onSelect(snapshot.stock_code)}>
                      <strong>{snapshot.stock_name || snapshot.stock_code}</strong>
                      <span>{snapshot.stock_code}</span>
                    </button>
                  </td>
                  <td>{formatPrice(snapshot.quote.price)}</td>
                  <td className={changeTone}>{formatSigned(snapshot.quote.change_pct)}%</td>
                  <td>{formatAmount(snapshot.quote.amount)}</td>
                  <td>{formatPercent(snapshot.quote.turnover)}</td>
                  <td>{formatRatio(snapshot.quote.pe_ratio)} / {formatRatio(snapshot.quote.pb_ratio)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </aside>
  )
}

export function PortfolioTrendChart({ bars, snapshot }: { bars: MarketDailyBar[]; snapshot?: WatchlistMarketSnapshot }) {
  const points = bars.filter((bar) => Number.isFinite(bar.close) && bar.close > 0 && Number.isFinite(bar.high) && Number.isFinite(bar.low))
  if (!points.length) {
    return (
      <div className="portfolioTrendEmpty">
        <strong>暂无日 K</strong>
        <span>{snapshot?.fallback_message || '当前数据源没有返回日线数据。'}</span>
      </div>
    )
  }
  const lows = points.map((bar) => positiveNumber(bar.low, bar.close))
  const highs = points.map((bar) => positiveNumber(bar.high, bar.close))
  const rawMin = Math.min(...lows)
  const rawMax = Math.max(...highs)
  const padding = Math.max((rawMax - rawMin) * 0.08, rawMax * 0.005, 1)
  const min = Math.max(0, rawMin - padding)
  const max = rawMax + padding
  const span = Math.max(max - min, 1)
  const width = 760
  const height = 336
  const left = 58
  const right = width - 20
  const top = 24
  const bottom = height - 58
  const chartWidth = right - left
  const chartHeight = bottom - top
  const yFor = (value: number) => bottom - ((value - min) / span) * chartHeight
  const coords = points.map((bar, index) => {
    const x = left + (index / Math.max(points.length - 1, 1)) * chartWidth
    return {
      x,
      openY: yFor(positiveNumber(bar.open, bar.close)),
      closeY: yFor(bar.close),
      highY: yFor(positiveNumber(bar.high, bar.close)),
      lowY: yFor(positiveNumber(bar.low, bar.close)),
      bar,
    }
  })
  const priceTicks = buildPriceTicks(min, max, 6)
  const dateTicks = buildDateTicks(coords, points.length > 120 ? 6 : points.length > 60 ? 5 : 4)
  const candleWidth = Math.max(2, Math.min(10, (chartWidth / Math.max(points.length, 1)) * 0.62))
  const first = points[0]
  const latest = points[points.length - 1]
  const isUp = latest.close >= first.close
  const latestUp = latest.close >= positiveNumber(latest.open, latest.close)

  return (
    <div className="portfolioTrendChart">
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="组合股票日 K 走势图">
        <line className="portfolioTrendAxis" x1={left} x2={right} y1={bottom} y2={bottom} />
        <line className="portfolioTrendAxis" x1={left} x2={left} y1={top} y2={bottom} />
        {priceTicks.map((tick) => {
          const y = yFor(tick)
          return (
            <g key={`price-${tick}`}>
              <line className="portfolioTrendGrid" x1={left} x2={right} y1={y} y2={y} />
              <text className="portfolioTrendPriceLabel" x={left - 8} y={y + 4}>{formatPrice(tick)}</text>
            </g>
          )
        })}
        {dateTicks.map((point) => (
          <g key={`date-${point.bar.date}-${point.x}`}>
            <line className="portfolioTrendGridVertical" x1={point.x} x2={point.x} y1={top} y2={bottom} />
            <text className="portfolioTrendDateLabel" x={point.x} y={bottom + 22}>{formatShortDate(point.bar.date)}</text>
          </g>
        ))}
        <g aria-label="日K蜡烛">
          {coords.map((point, index) => {
            const candleUp = point.bar.close >= positiveNumber(point.bar.open, point.bar.close)
            const bodyTop = Math.min(point.openY, point.closeY)
            const bodyHeight = Math.max(Math.abs(point.closeY - point.openY), 1.6)
            return (
              <g className={candleUp ? 'portfolioCandle portfolioCandleUp' : 'portfolioCandle portfolioCandleDown'} key={`${point.bar.date}-${index}`}>
                <line className="portfolioCandleWick" x1={point.x} x2={point.x} y1={point.highY} y2={point.lowY} />
                <rect
                  className="portfolioCandleBody"
                  x={point.x - candleWidth / 2}
                  y={bodyTop}
                  width={candleWidth}
                  height={bodyHeight}
                  rx={0.8}
                />
              </g>
            )
          })}
        </g>
        <text className={latestUp ? 'portfolioTrendLastLabel marketUp' : 'portfolioTrendLastLabel marketDown'} x={right} y={top - 8}>
          最新 {formatPrice(latest.close)}
        </text>
      </svg>
      <footer>
        <span>{first.date} 至 {latest.date}</span>
        <strong>{isUp ? '区间上行' : '区间回落'} · 日 K {points.length} 根 · 最新收盘 {formatPrice(latest.close)}</strong>
      </footer>
    </div>
  )
}

export function MarketSuggestionDock({
  snapshot,
  alerts,
  openAlerts,
  stockQuery,
  marketFallback,
}: {
  snapshot?: WatchlistMarketSnapshot
  alerts: TrackingAlert[]
  openAlerts: number
  stockQuery: string
  marketFallback: string
}) {
  const code = snapshot?.stock_code || ''
  return (
    <aside className="marketSuggestionDock">
      <section>
        <span>RESEARCH ADVICE</span>
        <h2>{snapshot?.suggestion || '等待行情数据'}</h2>
        <p>{marketFallback || snapshot?.fallback_message || '行情轮询只更新快照，不会触发事件采集或写入历史。'}</p>
      </section>
      <section>
        <span>TIME & SOURCE</span>
        <div className="marketSourceRows">
          <div><b>更新时间</b><strong>{snapshot?.quote.updated_at || '--'}</strong></div>
          <div><b>数据状态</b><strong>{sourceStatusLabel(snapshot?.source_status || 'degraded')}</strong></div>
          <div><b>数据源</b><strong>{snapshot?.quote.provider || '公开源降级'}</strong></div>
          <div><b>组合预警</b><strong>{openAlerts}</strong></div>
        </div>
      </section>
      <section>
        <span>ALERTS</span>
        <div className="marketAlertMiniList">
          {alerts.map((alert) => (
            <Link href={`/events?view=alerts&selected_event_id=${alert.event_id}&stock_codes=${stockQuery}`} key={alert.alert_id}>
              <strong>{alert.title || alert.rule_name || '风险预警'}</strong>
              <em>{alert.priority || alert.severity} · {alert.rule_name || alert.rule_id || '规则命中'}</em>
            </Link>
          ))}
          {!alerts.length ? <p>该标的暂无开放预警。</p> : null}
        </div>
      </section>
      <section className="marketDockActions">
        <Link href={code ? `/markets/${code}` : '/markets'}>独立行情页</Link>
        <Link href={code ? `/stocks/${code}` : '/watchlist'}>单股情报</Link>
        <Link href={code ? `/events?stock_codes=${code}` : '/events'}>事件详情</Link>
        <Link href="/runs">研报交付</Link>
      </section>
    </aside>
  )
}

function MetricCell({ label, value, tone = 'neutral' }: { label: string; value: string; tone?: string }) {
  return (
    <div className={`portfolioMetricCell tone-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function trendBars(snapshot: WatchlistMarketSnapshot | undefined, range: RangeKey) {
  if (!snapshot) return []
  if (range === '30d') return snapshot.trend_30d
  if (range === '180d') return snapshot.trend_180d
  return snapshot.trend_90d
}

function stockTitle(snapshot: WatchlistMarketSnapshot | undefined) {
  if (!snapshot) return '组合标的'
  const name = snapshot.stock_name || snapshot.quote.stock_name || ''
  if (name && name !== snapshot.stock_code) return `${name}（${snapshot.stock_code}）`
  return snapshot.stock_code
}

function riskLabel(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}

function shortTime(value: string) {
  if (!value) return '--'
  return value.replace('T', ' ').slice(5, 16)
}

function formatPrice(value: number) {
  return value > 0 ? value.toFixed(2) : '--'
}

function formatShortDate(value: string) {
  if (!value) return '--'
  const parts = value.split('-')
  if (parts.length >= 3) return `${parts[1]}-${parts[2]}`
  return value.slice(5) || value
}

function positiveNumber(value: number, fallback: number) {
  return Number.isFinite(value) && value > 0 ? value : fallback
}

function buildPriceTicks(min: number, max: number, count: number) {
  if (count <= 1) return [max]
  return Array.from({ length: count }, (_, index) => max - (index / (count - 1)) * (max - min))
}

function buildDateTicks<T extends { x: number; bar: MarketDailyBar }>(coords: T[], count: number) {
  if (!coords.length) return []
  const indexes = new Set<number>()
  const maxIndex = coords.length - 1
  for (let tick = 0; tick < count; tick += 1) {
    indexes.add(Math.round((tick / Math.max(count - 1, 1)) * maxIndex))
  }
  indexes.add(0)
  indexes.add(maxIndex)
  return Array.from(indexes).sort((a, b) => a - b).map((index) => coords[index])
}

function formatSigned(value: number) {
  if (!Number.isFinite(value) || value === 0) return '0.00'
  return `${value > 0 ? '+' : ''}${value.toFixed(2)}`
}

function formatPercent(value: number) {
  return value > 0 ? `${value.toFixed(2)}%` : '--'
}

function formatRatio(value: number) {
  return value > 0 ? value.toFixed(2) : '--'
}

function formatAmount(value: number) {
  if (!value) return '--'
  if (value >= 100000000) return `${(value / 100000000).toFixed(2)}亿`
  if (value >= 10000) return `${(value / 10000).toFixed(2)}万`
  return value.toFixed(0)
}

function sourceStatusLabel(status: string) {
  if (status === 'ok') return '数据正常'
  if (status === 'partial') return '部分数据'
  return '数据降级'
}
