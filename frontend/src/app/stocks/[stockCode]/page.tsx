import { StockWorkbench } from '../../../components/workbench/stock-workbench'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchStockWorkbench } from '../../../lib/api'
import { serverApiOptions } from '../../../lib/server-auth'
import type { StockWorkbenchResponse } from '../../../lib/types'

const VALID_TABS: StockWorkbenchResponse['active_tab'][] = ['summary', 'timeline', 'history', 'exports']

function normalizeTab(tab?: string): StockWorkbenchResponse['active_tab'] {
  return VALID_TABS.includes(tab as StockWorkbenchResponse['active_tab'])
    ? tab as StockWorkbenchResponse['active_tab']
    : 'summary'
}

export default async function StockPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams?: Promise<{ tab?: string }>
}) {
  const { stockCode } = await params
  const resolvedSearchParams = searchParams ? await searchParams : undefined
  const tab = normalizeTab(resolvedSearchParams?.tab)
  const apiOptions = await serverApiOptions()
  const data = await fetchStockWorkbench(stockCode, tab, apiOptions)

  return (
    <WorkspaceShell
      eyebrow="单股情报中心"
      title={data.stock_name || data.stock_code}
      description={`${data.stock_code} · ${data.is_tracked ? '已加入组合追踪' : '尚未加入组合，历史事件不会隐式沉淀'}。`}
      actions={data.actions}
    >
      <StockWorkbench data={data} />
    </WorkspaceShell>
  )
}
