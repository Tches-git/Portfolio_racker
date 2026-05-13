import { redirect } from 'next/navigation'

export default async function AlertsRedirect({
  searchParams,
}: {
  searchParams?: Promise<{ stock_codes?: string; status?: string; severity?: string; alert_type?: string; rule_id?: string }>
}) {
  const params = await searchParams
  const query = new URLSearchParams({ view: 'alerts' })
  if (params?.stock_codes) query.set('stock_codes', params.stock_codes)
  if (params?.status) query.set('status', params.status)
  if (params?.severity) query.set('severity', params.severity)
  if (params?.alert_type) query.set('alert_type', params.alert_type)
  if (params?.rule_id) query.set('rule_id', params.rule_id)
  redirect(`/events?${query.toString()}`)
}
