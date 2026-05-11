import Link from 'next/link'

type WorkspaceKey = 'overview' | 'summary' | 'timeline' | 'exports' | 'history' | 'runs'

const ITEMS: Array<{ key: WorkspaceKey; label: string; suffix: string }> = [
  { key: 'overview', label: '总览', suffix: '' },
  { key: 'summary', label: '摘要', suffix: '/summary' },
  { key: 'timeline', label: '事件', suffix: '/timeline' },
  { key: 'history', label: '历史', suffix: '/history' },
  { key: 'exports', label: '导出', suffix: '/exports' },
  { key: 'runs', label: '任务', suffix: '' },
]

export function StockWorkspaceNav({ stockCode, current }: { stockCode: string; current: WorkspaceKey }) {
  return (
    <section className="workspaceNav">
      <div>
        <div className="statusLabel">股票工作区</div>
        <div className="workspaceTitle">{stockCode}</div>
      </div>
      <div className="workspaceTabs">
        {ITEMS.map((item) => {
          const href = item.key === 'runs' ? `/stocks/${stockCode}` : `/stocks/${stockCode}${item.suffix}`
          return (
            <Link
              key={item.key}
              href={href}
              className={`workspaceTab${current === item.key ? ' workspaceTabActive' : ''}`}
              aria-current={current === item.key ? 'page' : undefined}
            >
              {item.label}
            </Link>
          )
        })}
      </div>
    </section>
  )
}
