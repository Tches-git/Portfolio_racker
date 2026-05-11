import Link from 'next/link'

export function QuickActions({ stockCode, latestRunId }: { stockCode: string; latestRunId?: string }) {
  return (
    <section className="quickActions">
      <Link className="quickAction primaryAction" href={`/stocks/${stockCode}`}>
        <span>继续研究</span>
        <strong>{stockCode} 工作台</strong>
      </Link>
      <Link className="quickAction" href="/runs">
        <span>查看队列</span>
        <strong>任务中心</strong>
      </Link>
      <Link className="quickAction" href={`/stocks/${stockCode}/history`}>
        <span>复盘变化</span>
        <strong>历史脉络</strong>
      </Link>
      <Link className="quickAction" href={latestRunId ? `/runs/${latestRunId}` : `/stocks/${stockCode}/exports`}>
        <span>交付追踪</span>
        <strong>{latestRunId ? '最近任务' : '导出中心'}</strong>
      </Link>
    </section>
  )
}
