import { redirect } from 'next/navigation'

export default async function StockExportsRedirect({ params }: { params: Promise<{ stockCode: string }> }) {
  const { stockCode } = await params
  redirect(`/stocks/${stockCode}?tab=exports`)
}
