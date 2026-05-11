'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

const QUICK_STOCKS = [
  ['贵州茅台', '600519'],
  ['宁德时代', '300750'],
  ['招商银行', '600036'],
  ['比亚迪', '002594'],
]

export function CommandCenter({ initialCode }: { initialCode: string }) {
  const router = useRouter()
  const [code, setCode] = useState(initialCode)
  const normalized = useMemo(() => code.trim(), [code])

  const openStock = () => {
    if (normalized) router.push(`/stocks/${normalized}`)
  }

  return (
    <section className="commandCenter">
      <div className="commandCopy">
        <div className="eyebrow">Command Center</div>
        <h1>从一只股票开始研究</h1>
        <p>输入代码后进入统一股票工作台：最新新闻、浏览器分析、摘要、历史、导出与任务状态都在同一条操作路径里。</p>
      </div>
      <div className="commandBox">
        <div className="commandInputRow">
          <input className="input commandInput" value={code} onChange={(event) => setCode(event.target.value)} placeholder="输入股票代码，如 600519" onKeyDown={(event) => event.key === 'Enter' && openStock()} />
          <button className="button" onClick={openStock} disabled={!normalized}>打开工作台</button>
        </div>
        <div className="chipRow">
          {QUICK_STOCKS.map(([name, stockCode]) => <button className="chip" key={stockCode} onClick={() => router.push(`/stocks/${stockCode}`)}>{name}</button>)}
        </div>
      </div>
    </section>
  )
}
