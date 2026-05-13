import Link from 'next/link'

export function QuickActions({ stockCode, latestRunId }: { stockCode?: string; latestRunId?: string }) {
  return (
    <section className="quickActions">
      <Link className="quickAction primaryAction" href={stockCode ? `/stocks/${stockCode}` : '/watchlist'}>
        <span>股票工作台</span>
        <strong>{stockCode ? `${stockCode} 工作台` : '先建立组合'}</strong>
      </Link>
      <Link className="quickAction" href="/events">
        <span>实时消息</span>
        <strong>事件追踪</strong>
      </Link>
      <Link className="quickAction" href="/watchlist">
        <span>自选范围</span>
        <strong>组合跟踪</strong>
      </Link>
      <Link className="quickAction" href={latestRunId ? `/runs/${latestRunId}` : '/briefing'}>
        <span>研究动作</span>
        <strong>{latestRunId ? '最近任务' : '每日简报'}</strong>
      </Link>
    </section>
  )
}
