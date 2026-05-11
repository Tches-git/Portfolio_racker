'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

const POPULAR = [
  ['贵州茅台', '600519'],
  ['宁德时代', '300750'],
  ['招商银行', '600036'],
  ['比亚迪', '002594'],
]

export function SearchShell({ initialCode }: { initialCode: string }) {
  const [code, setCode] = useState(initialCode)
  const router = useRouter()
  const normalized = useMemo(() => code.trim(), [code])

  useEffect(() => {
    setCode(initialCode)
  }, [initialCode])

  return (
    <div className="searchRowWrap">
      <div className="searchRow">
        <input
          className="input"
          value={code}
          onChange={(event) => setCode(event.target.value)}
          placeholder="输入股票代码，如 600519"
        />
        <button
          className="button"
          onClick={() => normalized && router.push(`/stocks/${normalized}`)}
          disabled={!normalized}
        >
          查看产品页
        </button>
      </div>
      <div className="chipRow">
        {POPULAR.map(([name, stockCode]) => (
          <button key={stockCode} className="chip" onClick={() => router.push(`/stocks/${stockCode}`)}>
            {name}
          </button>
        ))}
      </div>
    </div>
  )
}
