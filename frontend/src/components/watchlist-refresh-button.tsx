'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { refreshWatchlist } from '../lib/api'

export function WatchlistRefreshButton({ watchlistId }: { watchlistId: string }) {
  const router = useRouter()
  const [pending, setPending] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  async function refresh() {
    setPending(true)
    setMessage('')
    setError('')
    try {
      const detail = await refreshWatchlist(watchlistId)
      setMessage(`已刷新 ${detail.events.total} 条事件`)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '刷新组合事件失败')
    } finally {
      setPending(false)
    }
  }

  return (
    <div>
      <button className="button" onClick={refresh} disabled={pending}>
        {pending ? '刷新中...' : '刷新组合事件'}
      </button>
      {message ? <div className="pendingText">{message}</div> : null}
      {error ? <div className="inlineError">{error}</div> : null}
    </div>
  )
}
