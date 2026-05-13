'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

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
          placeholder="输入 6 位 A 股股票代码"
        />
        <button
          className="button"
          onClick={() => normalized && router.push(`/stocks/${normalized}`)}
          disabled={!normalized}
        >
          查看产品页
        </button>
      </div>
    </div>
  )
}
