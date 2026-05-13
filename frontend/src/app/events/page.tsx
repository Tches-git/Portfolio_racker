import { EventWorkbench } from '../../components/workbench/event-workbench'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchEventWorkbench } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

export default async function EventsPage({
  searchParams,
}: {
  searchParams?: Promise<{
    view?: 'events' | 'alerts'
    stock?: string
    stock_codes?: string
    status?: string
    event_type?: string
    impact_level?: string
    severity?: string
    alert_type?: string
    rule_id?: string
    selected_event_id?: string
  }>
}) {
  const params = await searchParams
  const apiOptions = await serverApiOptions()
  const stockCodes = (params?.stock_codes || params?.stock || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
  const data = await fetchEventWorkbench({
    view: params?.view || 'events',
    stockCodes,
    status: params?.status,
    eventType: params?.event_type,
    impactLevel: params?.impact_level,
    severity: params?.severity,
    alertType: params?.alert_type,
    ruleId: params?.rule_id,
    selectedEventId: params?.selected_event_id,
  }, apiOptions)

  return (
    <WorkspaceShell
      eyebrow="事件预警处理台"
      title="事件与预警"
      description="在同一个工作台里筛选事件、处理预警、复核状态，并把高影响事件转成事件点评。"
      actions={data.actions}
    >
      <EventWorkbench data={data} />
    </WorkspaceShell>
  )
}
