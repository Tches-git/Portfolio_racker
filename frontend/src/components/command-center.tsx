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
        <div className="eyebrow">Market Tracking Desk</div>
        <h1>今日金融追踪工作台</h1>
        <p>围绕自选组合持续跟踪公告、行情、研报观点和风险事件；高影响消息可直接触发事件点评或研报更新。</p>
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
