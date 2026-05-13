import Link from 'next/link'

import { MarketSearchForm } from '../../components/market-search-form'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchWatchlists } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

function trackedStocks(watchlists: Awaited<ReturnType<typeof fetchWatchlists>>) {
  const seen = new Set<string>()
  const stocks: Array<{ code: string; watchlistName: string }> = []
  for (const watchlist of watchlists.items) {
    for (const code of watchlist.stock_codes) {
      const normalized = String(code || '').trim()
      if (!normalized || seen.has(normalized)) continue
      seen.add(normalized)
      stocks.push({ code: normalized, watchlistName: watchlist.name })
    }
  }
  return stocks
}

export default async function MarketsIndexPage() {
  const watchlists = await safeFetchWatchlists()
  const stocks = trackedStocks(watchlists)

  return (
    <WorkspaceShell
      eyebrow="行情展示"
      title="股票行情"
      description="输入 6 位 A 股代码，查看行情快照、日线趋势和关键交易指标。行情入口只读展示，不写入事件历史。"
      actions={[{ label: '返回驾驶舱', href: '/', method: 'GET', action_type: 'open_dashboard', target_id: '', variant: 'secondary' }]}
    >
      <div className="wbStack">
        <section className="wbTwoColumn">
          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">选择股票</div>
                <h2>打开行情页</h2>
              </div>
            </div>
            <MarketSearchForm />
          </div>

          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">追踪股票</div>
                <h2>从组合进入</h2>
              </div>
              <Link className="wbTextButton" href="/watchlist">管理组合</Link>
            </div>
            <div className="wbList">
              {stocks.slice(0, 12).map((stock) => (
                <Link className="wbListItem" href={`/markets/${stock.code}`} key={stock.code}>
                  <strong>{stock.code}</strong>
                  <span>{stock.watchlistName} · 查看行情快照和日线走势</span>
                </Link>
              ))}
              {!stocks.length ? (
                <div className="wbEmpty">当前账号还没有追踪股票。你可以直接输入代码查看行情，或先创建组合。</div>
              ) : null}
            </div>
          </div>
        </section>
      </div>
    </WorkspaceShell>
  )
}

async function safeFetchWatchlists() {
  try {
    return await fetchWatchlists(await serverApiOptions())
  } catch {
    return { items: [], total: 0 }
  }
}
