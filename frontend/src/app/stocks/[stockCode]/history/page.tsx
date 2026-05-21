import { redirect } from 'next/navigation'

export default async function StockHistoryRedirect({ params }: { params: Promise<{ stockCode: string }> }) {
  const { stockCode } = await params
  redirect(`/stocks/${stockCode}?tab=summary`)
}
