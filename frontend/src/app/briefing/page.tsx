import { redirect } from 'next/navigation'

export default async function BriefingRedirect({
  searchParams,
}: {
  searchParams?: Promise<{ stock_codes?: string }>
}) {
  const params = searchParams ? await searchParams : undefined
  const query = new URLSearchParams()
  if (params?.stock_codes) query.set('stock_codes', params.stock_codes)
  redirect(query.toString() ? `/events?${query.toString()}` : '/')
}
