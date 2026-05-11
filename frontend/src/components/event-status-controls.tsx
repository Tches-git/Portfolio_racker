'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { updateEventStatus } from '../lib/api'
import type { MarketEvent } from '../lib/types'

const STATUS_LABELS: Record<MarketEvent['status'], string> = {
  new: '待处理',
  reviewed: '已复核',
  ignored: '已忽略',
  converted_to_report: '已转研报',
}

export function EventStatusBadge({ status }: { status: MarketEvent['status'] }) {
  const tone = status === 'ignored' ? 'tagNegative' : status === 'new' ? '' : 'tagPositive'
  return <span className={`tag ${tone}`}>{STATUS_LABELS[status] || status}</span>
}

export function EventStatusControls({ eventId, status }: { eventId: string; status: MarketEvent['status'] }) {
  const router = useRouter()
  const [pendingStatus, setPendingStatus] = useState<MarketEvent['status'] | ''>('')
  const [error, setError] = useState('')

  async function update(statusValue: MarketEvent['status']) {
    setPendingStatus(statusValue)
    setError('')
    try {
      await updateEventStatus(eventId, statusValue)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '更新事件状态失败')
    } finally {
      setPendingStatus('')
    }
  }

  return (
    <div>
      <div className="chipRow">
        <EventStatusBadge status={status} />
        <button className="ghostButton" onClick={() => void update('reviewed')} disabled={pendingStatus !== '' || status === 'reviewed'}>
          {pendingStatus === 'reviewed' ? '更新中...' : '标记已复核'}
        </button>
        <button className="ghostButton" onClick={() => void update('ignored')} disabled={pendingStatus !== '' || status === 'ignored'}>
          {pendingStatus === 'ignored' ? '更新中...' : '忽略'}
        </button>
      </div>
      {error ? <div className="inlineError">{error}</div> : null}
    </div>
  )
}
