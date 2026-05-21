'use client'

import { useEffect, useMemo, useRef, useState, useTransition } from 'react'
import { usePathname, useRouter } from 'next/navigation'

export function AutoRefreshControl({ intervalSeconds = 60 }: { intervalSeconds?: number }) {
  const router = useRouter()
  const pathname = usePathname()
  const [enabled, setEnabled] = useState(true)
  const [remaining, setRemaining] = useState(intervalSeconds)
  const [lastRefreshedAt, setLastRefreshedAt] = useState('刚刚')
  const [isPending, startTransition] = useTransition()
  const routeKey = useMemo(() => pathname, [pathname])
  const remainingRef = useRef(intervalSeconds)

  useEffect(() => {
    remainingRef.current = intervalSeconds
    setRemaining(intervalSeconds)
  }, [intervalSeconds, routeKey])

  useEffect(() => {
    if (!enabled) return undefined
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'hidden') return
      const shouldRefresh = remainingRef.current <= 1
      const nextRemaining = shouldRefresh ? intervalSeconds : remainingRef.current - 1
      remainingRef.current = nextRemaining
      setRemaining(nextRemaining)
      if (shouldRefresh) {
        refreshPage()
      }
    }, 1000)
    return () => window.clearInterval(timer)
  }, [enabled, intervalSeconds, routeKey])

  function refreshPage() {
    const timestamp = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    setLastRefreshedAt(timestamp)
    startTransition(() => {
      router.refresh()
    })
  }

  function handleManualRefresh() {
    remainingRef.current = intervalSeconds
    setRemaining(intervalSeconds)
    refreshPage()
  }

  return (
    <div className="autoRefreshControl" aria-label="页面刷新控制">
      <button
        className={`autoRefreshToggle${enabled ? ' autoRefreshToggleActive' : ''}`}
        type="button"
        onClick={() => setEnabled((value) => !value)}
        title={enabled ? '关闭页面自动刷新' : '开启页面自动刷新'}
      >
        {enabled ? `自动刷新 ${remaining}s` : '自动刷新 关'}
      </button>
      <button className="autoRefreshButton" type="button" onClick={handleManualRefresh} disabled={isPending}>
        {isPending ? '刷新中' : '立即刷新'}
      </button>
      <span aria-live="polite">上次 {lastRefreshedAt}</span>
    </div>
  )
}
