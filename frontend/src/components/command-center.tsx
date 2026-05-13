'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

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
          <input className="input commandInput" value={code} onChange={(event) => setCode(event.target.value)} placeholder="输入 6 位 A 股股票代码" onKeyDown={(event) => event.key === 'Enter' && openStock()} />
          <button className="button" onClick={openStock} disabled={!normalized}>打开工作台</button>
        </div>
        <div className="commandTerminal">
          <div><span>范围</span><strong>{normalized || '待输入'}</strong></div>
          <div><span>流程</span><strong>事件 · 预警 · 简报</strong></div>
        </div>
      </div>
    </section>
  )
}
