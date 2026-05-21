import { EventWorkbench } from '../../components/workbench/event-workbench'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchEventWorkbench, fetchStockSearch } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

async function fetchStockNameMap(stockCodes: string[], apiOptions: Awaited<ReturnType<typeof serverApiOptions>>) {
  const uniqueCodes = Array.from(new Set(stockCodes.filter(Boolean))).slice(0, 30)
  const entries = await Promise.all(uniqueCodes.map(async (code) => {
    try {
      const payload = await fetchStockSearch(code, 8, apiOptions)
      const exact = payload.items.find((item) => item.code === code)
      return exact?.name ? [code, exact.name] as const : null
    } catch {
      return null
    }
  }))
  return Object.fromEntries(entries.filter((entry): entry is readonly [string, string] => Boolean(entry)))
}

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
  const stockNameMap = await fetchStockNameMap([
    ...stockCodes,
    ...data.events.items.map((event) => event.stock_code),
    ...data.alerts.items.map((alert) => alert.stock_code),
  ], apiOptions)

  return (
    <WorkspaceShell
      eyebrow="事件风险台"
      title="事件预警处理台"
      description="以队列方式筛选事件、处理预警、复核状态，并把高影响事件转成多智能体事件点评。"
      actions={data.actions}
      className="eventsCommandPage"
      compact
    >
      <EventWorkbench data={data} stockNames={stockNameMap} />
    </WorkspaceShell>
  )
}
