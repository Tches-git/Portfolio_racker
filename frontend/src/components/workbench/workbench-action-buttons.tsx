'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { refreshWatchlist } from '../../lib/api'
import type { WorkbenchAction } from '../../lib/types'

export function WorkbenchActionButtons({ actions }: { actions: WorkbenchAction[] }) {
  const router = useRouter()
  const [pendingAction, setPendingAction] = useState('')
  const [error, setError] = useState('')

  async function runAction(action: WorkbenchAction) {
    if (action.action_type !== 'refresh_watchlist' || !action.target_id) return
    setPendingAction(action.target_id)
    setError('')
    try {
      await refreshWatchlist(action.target_id)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '操作失败，请稍后重试')
    } finally {
      setPendingAction('')
    }
  }

  return (
    <div className="wbActions">
      {actions.map((action) => {
        const key = `${action.label}-${action.href}-${action.target_id}`
        const isPageNavigation = (!action.method || action.method === 'GET') && !action.href.startsWith('/api/')
        const className = `wbButton ${action.variant === 'primary' ? 'wbButtonPrimary' : ''}`
        if (isPageNavigation) {
          return (
            <Link className={className} href={action.href || '#'} key={key}>
              {action.label}
            </Link>
          )
        }
        if (action.action_type === 'refresh_watchlist') {
          const pending = pendingAction === action.target_id
          return (
            <button className={className} disabled={pending} key={key} onClick={() => void runAction(action)}>
              {pending ? '刷新中...' : action.label}
            </button>
          )
        }
        return (
          <span className={`${className} wbButtonMuted`} key={key} title="请在当前页面的操作区执行">
            {action.label}
          </span>
        )
      })}
      {error ? <div className="inlineError wbActionError">{error}</div> : null}
    </div>
  )
}
