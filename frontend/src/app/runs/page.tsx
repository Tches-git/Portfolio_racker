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
      eyebrow="任务交付中心"
      title="研报与事件点评任务"
      description="集中查看研报任务、事件点评、导出物和失败重试，所有任务按当前账号隔离。"
      actions={data.actions}
    >
      <TaskDeliveryCenter data={data} />
    </WorkspaceShell>
  )
}
