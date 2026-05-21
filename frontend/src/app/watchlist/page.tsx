import { WatchlistCreateForm } from '../../components/watchlist-create-form'
import { WatchlistManagementPanel } from '../../components/watchlist-management-panel'
import { RiskTicker } from '../../components/workbench/primitives'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchDashboard } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

export default async function WatchlistPage({ searchParams }: { searchParams?: Promise<{ error?: string; notice?: string }> }) {
  const apiOptions = await serverApiOptions()
  const dashboard = await fetchDashboard(apiOptions)
  const params = await searchParams
  const watchlists = dashboard.watchlists.items
  const summary = dashboard.portfolio_summary

  return (
    <WorkspaceShell
      eyebrow="组合管理"
      title="组合监控终端"
      description="以组合为研究范围沉淀事件、预警和研报任务；新账号只显示当前用户创建的数据。"
      actions={dashboard.actions}
      className="watchlistCommandPage"
      compact
    >
      <div className="wbStack">
        {params?.notice ? <div className="inlineNotice">{params.notice}</div> : null}
        {params?.error ? <div className="inlineError">{params.error}</div> : null}

        <RiskTicker items={[
          { label: '组合数', value: dashboard.watchlists.total },
          { label: '追踪股票', value: summary.stock_count },
          { label: '开放预警', value: summary.alert_count, tone: summary.alert_count ? 'warning' : 'neutral' },
          { label: '风险分', value: summary.risk_score, tone: summary.risk_level === 'high' ? 'danger' : summary.risk_level === 'medium' ? 'warning' : 'neutral' },
        ]} />

        <section className="wbSplitPane wbSplitPaneWide terminalMainSplit">
          <div className="wbPanel">
            <WatchlistManagementPanel watchlists={watchlists} />
          </div>

          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">创建范围</div>
                <h2>新建组合</h2>
              </div>
            </div>
            <WatchlistCreateForm />
          </div>
        </section>
      </div>
    </WorkspaceShell>
  )
}
