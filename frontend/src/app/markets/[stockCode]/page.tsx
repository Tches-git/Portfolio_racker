import { fetchMarketWorkbench } from '../../../lib/api'
import { serverApiOptions } from '../../../lib/server-auth'
import { MarketWorkbench } from '../../../components/workbench/market-workbench'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import type { MarketWorkbenchResponse } from '../../../lib/types'

const VALID_RANGES = ['30d', '90d', '180d'] as const

function normalizeRange(range?: string) {
  return VALID_RANGES.includes(range as typeof VALID_RANGES[number])
    ? range as typeof VALID_RANGES[number]
    : '90d'
}

export default async function MarketPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams: Promise<{ range?: string }>
}) {
  const { stockCode } = await params
  const { range } = await searchParams
  let data: MarketWorkbenchResponse
  try {
    data = await fetchMarketWorkbench(stockCode, normalizeRange(range), await serverApiOptions())
  } catch {
    data = fallbackMarketData(stockCode, normalizeRange(range))
  }
  return (
    <WorkspaceShell
      eyebrow="Market Quote Terminal"
      title={`${data.stock_name || data.stock_code} 行情终端`}
      description="查看选中股票的报价快照、日线趋势和关键交易指标。行情页只读展示，不会创建组合或写入事件历史。"
      actions={data.actions}
    >
      <MarketWorkbench data={data} />
    </WorkspaceShell>
  )
}

function fallbackMarketData(stockCode: string, range: MarketWorkbenchResponse['range']): MarketWorkbenchResponse {
  return {
    stock_code: stockCode,
    stock_name: stockCode,
    range,
    quote: {
      stock_code: stockCode,
      stock_name: stockCode,
      price: 0,
      change: 0,
      change_pct: 0,
      open: 0,
      high: 0,
      low: 0,
      previous_close: 0,
      volume: 0,
      amount: 0,
      turnover: 0,
      market_cap: 0,
      pe_ratio: 0,
      pb_ratio: 0,
      updated_at: '',
      source_status: 'degraded',
      provider: '',
    },
    daily_bars: [],
    fallback_message: '行情服务暂时不可用，请稍后重试。页面没有写入事件历史或创建组合。',
    actions: [
      { label: '返回行情入口', href: '/markets', method: 'GET', action_type: 'open_markets', target_id: '', variant: 'secondary' },
      { label: '返回情报中心', href: `/stocks/${stockCode}`, method: 'GET', action_type: 'open_stock', target_id: stockCode, variant: 'secondary' },
    ],
  }
}
