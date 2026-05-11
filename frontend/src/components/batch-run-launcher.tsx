'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState, useTransition } from 'react'

import { createBatchAnalysisRuns } from '../lib/api'

export function BatchRunLauncher({ initialStocks }: { initialStocks: string[] }) {
  const router = useRouter()
  const [value, setValue] = useState(initialStocks.join(', '))
  const [message, setMessage] = useState('')
  const [createdRuns, setCreatedRuns] = useState<Array<{ run_id: string; stock_code: string; status: string }>>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isRefreshing, startTransition] = useTransition()
  const loading = isSubmitting || isRefreshing

  const launch = async () => {
    const stockCodes = value.split(/[，,\s]+/).map((item) => item.trim()).filter(Boolean)
    if (!stockCodes.length || loading) return
    setIsSubmitting(true)
    setMessage(`正在把 ${stockCodes.length} 个标的送入队列...`)
    setCreatedRuns(stockCodes.map((stockCode) => ({ run_id: 'pending', stock_code: stockCode, status: 'queued' })))
    try {
      const payload = await createBatchAnalysisRuns(stockCodes)
      setCreatedRuns(payload.items.map((item) => ({ run_id: item.run_id, stock_code: item.stock_code, status: item.status })))
      setMessage(`已创建 ${payload.total} 个批量任务，可立即进入详情。`)
      startTransition(() => router.refresh())
    } catch (err) {
      setCreatedRuns([])
      setMessage(err instanceof Error ? err.message : '批量创建分析任务失败')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="card">
      <div className="itemTitle">批量多股票运行</div>
      <p className="bodyText">输入多个股票代码，用逗号或空格分隔，直接进入统一 worker 队列。</p>
      <div className="searchRow launcherRow">
        <input className="input" value={value} onChange={(event) => setValue(event.target.value)} placeholder="600519, 000858, 300750" />
        <button className="ghostButton" onClick={() => void launch()} disabled={loading}>{loading ? '入队中...' : '批量入队'}</button>
      </div>
      {message ? <div className={loading ? 'pendingText' : 'inlineMeta'}>{message}</div> : null}
      {createdRuns.length ? (
        <div className="pillRow">
          {createdRuns.slice(0, 4).map((item) => item.run_id === 'pending'
            ? <span className="tag" key={item.stock_code}>{item.stock_code} · {item.status}</span>
            : <Link className="tag tagPositive" href={`/runs/${item.run_id}`} key={item.run_id}>{item.stock_code} · {item.status}</Link>)}
        </div>
      ) : null}
    </div>
  )
}
