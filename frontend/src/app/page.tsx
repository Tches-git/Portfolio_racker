import { DashboardOverview } from '../components/workbench/dashboard-overview'
import { WorkspaceShell } from '../components/workbench/workspace-shell'
import { fetchDashboard } from '../lib/api'
import { serverApiOptions } from '../lib/server-auth'

export default async function Home() {
  const apiOptions = await serverApiOptions()
  const dashboard = await fetchDashboard(apiOptions)

  return (
    <WorkspaceShell
      eyebrow={dashboard.mode === 'setup' ? '初始化' : '风险驾驶舱'}
      title={dashboard.mode === 'setup' ? '初始化研究终端' : '组合风险驾驶舱'}
      description={dashboard.mode === 'setup'
        ? '新账号默认没有任何数据。先创建组合，再手动刷新事件，所有事件、预警和研报都只属于当前账号。'
        : '从组合风险出发，集中处理预警、关键事件、今日主题和多智能体研报任务。'}
      actions={dashboard.mode === 'setup' ? dashboard.actions : []}
      className={dashboard.mode === 'setup' ? '' : 'dashboardCommandPage'}
      compact={dashboard.mode !== 'setup'}
    >
      <DashboardOverview data={dashboard} />
    </WorkspaceShell>
  )
}
