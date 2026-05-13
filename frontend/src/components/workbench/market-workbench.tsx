import Link from 'next/link'

import type { MarketDailyBar, MarketWorkbenchResponse } from '../../lib/types'

const RANGES = [
  { key: '30d', label: '30日' },
  { key: '90d', label: '90日' },
  { key: '180d', label: '180日' },
] as const

export function MarketWorkbench({ data }: { data: MarketWorkbenchResponse }) {
  const quote = data.quote
  const isUp = quote.change_pct >= 0
  return (
    <div className="wbStack">
      <section className="marketQuotePanel">
        <div className="marketQuoteMain">
          <div className="wbEyebrow">行情快照</div>
          <div className="marketPriceRow">
            <strong>{formatPrice(quote.price)}</strong>
            <span className={isUp ? 'marketPositive' : 'marketNegative'}>
              {formatSigned(quote.change)} / {formatSigned(quote.change_pct)}%
            </span>
          </div>
          <div className="wbMuted">
            {data.stock_name || data.stock_code} · {data.stock_code} · {sourceStatusLabel(quote.source_status)} · {quote.updated_at || '暂无更新时间'}
          </div>
        </div>
        <div className="marketQuoteStats">
          <div><span>成交额</span><strong>{formatAmount(quote.amount)}</strong></div>
          <div><span>换手率</span><strong>{formatPercent(quote.turnover)}</strong></div>
          <div><span>市值</span><strong>{formatAmount(quote.market_cap)}</strong></div>
          <div><span>数据源</span><strong>{quote.provider || '降级'}</strong></div>
        </div>
      </section>

      {data.fallback_message ? <div className="wbEmpty">{data.fallback_message}</div> : null}

      <section className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">日线走势</div>
            <h2>收盘价趋势</h2>
          </div>
          <div className="wbTabs">
            {RANGES.map((item) => (
              <Link className={`wbTab ${data.range === item.key ? 'wbTabActive' : ''}`} href={`/markets/${data.stock_code}?range=${item.key}`} key={item.key}>
                {item.label}
              </Link>
            ))}
          </div>
        </div>
        <MarketLineChart bars={data.daily_bars} />
      </section>

      <section className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">关键交易指标</div>
            <h2>行情指标表</h2>
          </div>
          <Link className="wbTextButton" href={`/stocks/${data.stock_code}`}>返回单股情报中心</Link>
        </div>
        <div className="wbTableWrap">
          <table className="wbTable marketTable">
            <tbody>
              <MetricRow label="开盘" value={formatPrice(quote.open)} secondLabel="最高" secondValue={formatPrice(quote.high)} />
              <MetricRow label="最低" value={formatPrice(quote.low)} secondLabel="昨收" secondValue={formatPrice(quote.previous_close)} />
              <MetricRow label="成交额" value={formatAmount(quote.amount)} secondLabel="成交量" secondValue={formatVolume(quote.volume)} />
              <MetricRow label="换手率" value={formatPercent(quote.turnover)} secondLabel="市值" secondValue={formatAmount(quote.market_cap)} />
              <MetricRow label="PE" value={formatRatio(quote.pe_ratio)} secondLabel="PB" secondValue={formatRatio(quote.pb_ratio)} />
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

function MarketLineChart({ bars }: { bars: MarketDailyBar[] }) {
  const points = bars.filter((bar) => Number.isFinite(bar.close) && bar.close > 0)
  if (!points.length) {
    return <div className="wbEmpty">暂无可展示的日线数据。</div>
  }
  const closes = points.map((bar) => bar.close)
  const min = Math.min(...closes)
  const max = Math.max(...closes)
  const span = Math.max(max - min, 1)
  const width = 720
  const height = 260
  const left = 24
  const right = width - 18
  const top = 24
  const bottom = height - 28
  const chartWidth = right - left
  const chartHeight = bottom - top
  const coords = points.map((bar, index) => {
    const x = left + (index / Math.max(points.length - 1, 1)) * chartWidth
    const y = bottom - ((bar.close - min) / span) * chartHeight
    return { x, y, bar }
  })
  const linePath = coords.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`).join(' ')
  const areaPath = `${linePath} L ${coords[coords.length - 1].x.toFixed(2)} ${bottom} L ${coords[0].x.toFixed(2)} ${bottom} Z`
  const first = points[0]
  const latest = points[points.length - 1]

  return (
    <div className="marketChart">
      <svg className="marketChartSvg" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="股票日线收盘价走势图">
        <line className="marketChartAxis" x1={left} y1={top} x2={left} y2={bottom} />
        <line className="marketChartAxis" x1={left} y1={bottom} x2={right} y2={bottom} />
        <path className="marketChartArea" d={areaPath} />
        <path className="marketChartLine" d={linePath} />
        {coords.map((point, index) => index === coords.length - 1 ? <circle className="marketChartDot" cx={point.x} cy={point.y} r="4" key={point.bar.date} /> : null)}
        <text className="marketChartLabel" x={left} y={top - 8}>{formatPrice(max)}</text>
        <text className="marketChartLabel" x={left} y={bottom + 18}>{formatPrice(min)}</text>
        <text className="marketChartLabel marketChartLabelEnd" x={right} y={bottom + 18}>{latest.date}</text>
      </svg>
      <div className="marketChartFooter">
        <span>{first.date} 至 {latest.date}</span>
        <strong>最新收盘 {formatPrice(latest.close)}</strong>
      </div>
    </div>
  )
}

function MetricRow({ label, value, secondLabel, secondValue }: { label: string; value: string; secondLabel: string; secondValue: string }) {
  return (
    <tr>
      <th>{label}</th>
      <td>{value}</td>
      <th>{secondLabel}</th>
      <td>{secondValue}</td>
    </tr>
  )
}

function formatPrice(value: number) {
  return value > 0 ? value.toFixed(2) : '--'
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

function formatVolume(value: number) {
  if (!value) return '--'
  if (value >= 100000000) return `${(value / 100000000).toFixed(2)}亿手`
  if (value >= 10000) return `${(value / 10000).toFixed(2)}万手`
  return value.toFixed(0)
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
