import { DashboardOverview } from '../components/workbench/dashboard-overview'
import { WorkspaceShell } from '../components/workbench/workspace-shell'
import { fetchDashboard } from '../lib/api'
import { serverApiOptions } from '../lib/server-auth'

export default async function Home() {
  const apiOptions = await serverApiOptions()
  const dashboard = await fetchDashboard(apiOptions)

  return (
    <WorkspaceShell
      eyebrow="组合风险驾驶舱"
      title={dashboard.mode === 'setup' ? '建立你的追踪范围' : '组合风险驾驶舱'}
      description={dashboard.mode === 'setup'
        ? '新账号默认没有任何数据。先创建组合，再手动刷新事件，所有事件、预警和研报都只属于当前账号。'
        : '从组合风险出发，集中处理预警、关键事件、今日主题和研报任务。'}
      actions={dashboard.actions}
    >
      <DashboardOverview data={dashboard} />
    </WorkspaceShell>
  )
}
