import { TaskDeliveryCenter } from '../../components/workbench/task-delivery-center'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchRunWorkbench } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

export default async function RunsIndexPage({
  searchParams,
}: {
  searchParams?: Promise<{ selected?: string }>
}) {
  const params = searchParams ? await searchParams : undefined
  const apiOptions = await serverApiOptions()
  const data = await fetchRunWorkbench(24, params?.selected || '', apiOptions)

  return (
    <WorkspaceShell
      eyebrow="Agent 任务"
      title="多智能体研报任务台"
      description="集中展示实时采集后的多 Agent 研报任务、角色协作 Trace、可信度审计和交付物。"
      actions={data.actions}
      className="runsDeskPage"
      compact
    >
      <TaskDeliveryCenter data={data} />
    </WorkspaceShell>
  )
}
