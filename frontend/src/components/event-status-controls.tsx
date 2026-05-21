'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { updateEventStatus } from '../lib/api'
import { formatEventStatus } from '../lib/labels'
import type { MarketEvent } from '../lib/types'

const STATUS_LABELS: Record<MarketEvent['status'], string> = {
  new: '待处理',
  reviewed: '已复核',
  ignored: '已忽略',
  converted_to_report: '已转研报',
}

export function EventStatusBadge({ status }: { status: MarketEvent['status'] }) {
  const tone = status === 'ignored' ? 'tagNegative' : status === 'new' ? '' : 'tagPositive'
  return <span className={`tag ${tone}`}>{STATUS_LABELS[status] || formatEventStatus(status)}</span>
}

export function EventStatusControls({
  eventId,
  status,
  statusUpdatedAt = '',
  statusActor = '',
  statusNote = '',
}: {
  eventId: string
  status: MarketEvent['status']
  statusUpdatedAt?: string
  statusActor?: string
  statusNote?: string
}) {
  const router = useRouter()
  const [pendingStatus, setPendingStatus] = useState<MarketEvent['status'] | ''>('')
  const [error, setError] = useState('')

  async function update(statusValue: MarketEvent['status'], note: string) {
    setPendingStatus(statusValue)
    setError('')
    try {
      await updateEventStatus(eventId, statusValue, note)
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
        <button className="ghostButton" onClick={() => void update('reviewed', '已在预警处理台完成人工复核')} disabled={pendingStatus !== '' || status === 'reviewed'}>
          {pendingStatus === 'reviewed' ? '更新中...' : '标记已复核'}
        </button>
        <button className="ghostButton" onClick={() => void update('ignored', '已判断无需继续跟踪，预警忽略')} disabled={pendingStatus !== '' || status === 'ignored'}>
          {pendingStatus === 'ignored' ? '更新中...' : '忽略'}
        </button>
      </div>
      {status !== 'new' || statusUpdatedAt || statusNote ? (
        <div className="selectionHint">
          处理闭环：{statusActor || '当前用户'} · {statusUpdatedAt || '时间待同步'}{statusNote ? ` · ${statusNote}` : ''}
        </div>
      ) : null}
      {error ? <div className="inlineError">{error}</div> : null}
    </div>
  )
}
