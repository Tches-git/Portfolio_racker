import { CommandCenter } from '../components/command-center'
import { MetricCard } from '../components/metric-card'
import { QuickActions } from '../components/quick-actions'
import { RecentRunsPanel } from '../components/recent-runs-panel'
import { StockCardGrid } from '../components/stock-card-grid'
import { fetchRecentRuns, fetchWorkspaceStocks } from '../lib/api'

export default async function Home() {
  const stockCode = '600519'
  const recentRuns = await fetchRecentRuns(6)
  const workspaceStocks = await fetchWorkspaceStocks()
  const activeRuns = recentRuns.items.filter((item) => item.status === 'queued' || item.status === 'running')
  const latestRun = recentRuns.items[0]

  return (
    <main>
      <CommandCenter initialCode={stockCode} />
      <QuickActions stockCode={latestRun?.stock_code || stockCode} latestRunId={latestRun?.run_id} />

      <div className="dashboardGrid">
        <MetricCard label="跟踪股票" value={workspaceStocks.items.length} hint="沉淀过历史研究的标的" />
        <MetricCard label="最近任务" value={recentRuns.total} hint="全局运行队列记录" />
        <MetricCard label="活跃任务" value={activeRuns.length} hint="排队中 / 运行中" />
        <MetricCard label="默认入口" value={stockCode} hint="可直接替换为任意 A 股代码" />
      </div>

      <div className="grid">
        <StockCardGrid stocks={workspaceStocks.items} />
        <RecentRunsPanel runs={recentRuns.items} />
      </div>
    </main>
  )
}
