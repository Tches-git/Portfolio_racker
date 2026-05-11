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
        <div className="eyebrow">全局检索</div>
        <h2>打开股票情报工作台</h2>
        <p>输入股票代码进入单股视图，继续查看事件时间线、所属组合、导出物和事件驱动研报。</p>
        <div className="commandStatusLine">
          <span><span className="liveDot" aria-hidden /> 事件采集</span>
          <span>预警规则</span>
          <span>研报交付</span>
        </div>
      </div>
      <div className="commandBox">
        <div className="commandBoxHeader">
          <span>快速打开</span>
          <span>股票工作台</span>
        </div>
        <div className="commandInputRow">
          <input className="input commandInput" value={code} onChange={(event) => setCode(event.target.value)} placeholder="输入股票代码，如 600519" onKeyDown={(event) => event.key === 'Enter' && openStock()} />
          <button className="button" onClick={openStock} disabled={!normalized}>打开工作台</button>
        </div>
        <div className="commandTerminal">
          <div><span>范围</span><strong>{normalized || '待输入'}</strong></div>
          <div><span>流程</span><strong>事件 · 预警 · 简报</strong></div>
        </div>
        <div className="chipRow">
          {QUICK_STOCKS.map(([name, stockCode]) => <button className="chip" key={stockCode} onClick={() => router.push(`/stocks/${stockCode}`)}>{name}</button>)}
        </div>
      </div>
    </section>
  )
}
