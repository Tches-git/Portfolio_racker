'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import type { MouseEvent } from 'react'

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

  function focusRunCreatePanel(event: MouseEvent<HTMLAnchorElement>, action: WorkbenchAction) {
    if (action.action_type !== 'create_run' && action.action_type !== 'create_batch_run') return
    if (!action.href.startsWith('/runs')) return
    const panel = document.getElementById('run-create-panel')
    if (!panel) return
    event.preventDefault()
    panel.scrollIntoView({ behavior: 'smooth', block: 'center' })
    panel.classList.remove('runCreatePanelPulse')
    void panel.offsetWidth
    panel.classList.add('runCreatePanelPulse')
    window.history.replaceState(null, '', `${window.location.pathname}${window.location.search}#run-create-panel`)
    const input = panel.querySelector<HTMLInputElement>('[data-run-launcher-input="true"]')
    input?.focus()
  }

  return (
    <div className="wbActions">
      {actions.map((action) => {
        const createRunPanelHref =
          (action.action_type === 'create_run' || action.action_type === 'create_batch_run') && action.href.startsWith('/runs')
            ? '/runs#run-create-panel'
            : action.href
        const key = `${action.label}-${createRunPanelHref}-${action.target_id}`
        const isPageNavigation = (!action.method || action.method === 'GET') && !createRunPanelHref.startsWith('/api/')
        const className = `wbButton ${action.variant === 'primary' ? 'wbButtonPrimary' : ''}`
        if (isPageNavigation) {
          return (
            <Link className={className} href={createRunPanelHref || '#'} key={key} onClick={(event) => focusRunCreatePanel(event, action)}>
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
