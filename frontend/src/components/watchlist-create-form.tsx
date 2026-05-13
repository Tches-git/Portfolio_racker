'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { createWatchlist } from '../lib/api'

export function WatchlistCreateForm() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [codes, setCodes] = useState('')
  const [description, setDescription] = useState('')
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')

  async function submit() {
    const stockCodes = codes.split(/[,\s，、]+/).map((item) => item.trim()).filter(Boolean)
    if (!name.trim() || !stockCodes.length) {
      setError('请填写组合名称和至少一只股票代码')
      return
    }
    setPending(true)
    setError('')
    try {
      const created = await createWatchlist({ name, stock_codes: stockCodes, description })
      setName('')
      setCodes('')
      setDescription('')
      router.push(`/watchlist/${created.watchlist_id}`)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '创建组合失败')
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="card">
      <div className="itemTitle">新建追踪组合</div>
      <div className="metricStack">
        <input className="input" value={name} onChange={(event) => setName(event.target.value)} placeholder="组合名称" />
        <input className="input" value={codes} onChange={(event) => setCodes(event.target.value)} placeholder="输入你要追踪的 6 位股票代码，用逗号或空格分隔" />
        <input className="input" value={description} onChange={(event) => setDescription(event.target.value)} placeholder="组合说明，可选" />
        <button className="button" onClick={submit} disabled={pending}>{pending ? '创建中...' : '创建组合'}</button>
        {error ? <div className="inlineError">{error}</div> : null}
      </div>
    </div>
  )
}
