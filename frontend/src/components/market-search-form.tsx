'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'

export function MarketSearchForm({ initialCode = '' }: { initialCode?: string }) {
  const router = useRouter()
  const [stockCode, setStockCode] = useState(initialCode)
  const [error, setError] = useState('')

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const normalized = stockCode.trim()
    if (!/^\d{6}$/.test(normalized)) {
      setError('请输入 6 位 A 股股票代码')
      return
    }
    setError('')
    router.push(`/markets/${normalized}`)
  }

  return (
    <form className="marketSearchForm" onSubmit={submit}>
      <label className="field">
        <span>股票代码</span>
        <input
          className="input"
          inputMode="numeric"
          maxLength={6}
          placeholder="输入 6 位 A 股股票代码"
          value={stockCode}
          onChange={(event) => setStockCode(event.target.value.replace(/\D/g, '').slice(0, 6))}
        />
      </label>
      {error ? <div className="inlineError">{error}</div> : null}
      <button className="button primaryButton" type="submit">查看行情</button>
    </form>
  )
}
