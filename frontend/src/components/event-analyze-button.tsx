'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { analyzeEvent } from '../lib/api'

export function EventAnalyzeButton({ eventId, label = '生成事件点评' }: { eventId: string; label?: string }) {
  const router = useRouter()
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')

  async function handleAnalyze() {
    setPending(true)
    setError('')
    try {
      const run = await analyzeEvent(eventId)
      router.push(`/runs/${run.run_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : '事件触发分析失败')
      setPending(false)
    }
  }

  return (
    <div>
      <button className="ghostButton" onClick={handleAnalyze} disabled={pending || !eventId}>
        {pending ? '正在创建任务...' : label}
      </button>
      {error ? <div className="inlineError">{error}</div> : null}
    </div>
  )
}
