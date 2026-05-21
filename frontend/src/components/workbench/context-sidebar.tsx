'use client'

import Link from 'next/link'
import { usePathname, useSearchParams } from 'next/navigation'

import { WorkbenchIcon, type IconName } from './icons'

type ContextLink = {
  label: string
  href: string
  icon: IconName
}

function activeFor(pathname: string, currentUrl: string, href: string) {
  if (href === '/') return pathname === '/'
  if (href.includes('?')) return currentUrl === href
  return pathname === href || (!href.startsWith('/stocks/') && !href.startsWith('/markets/') && pathname.startsWith(href))
}

function stockCodeFromPath(pathname: string) {
  const stockMatch = pathname.match(/^\/(?:stocks|markets)\/([^/?]+)/)
  return stockMatch?.[1] || ''
}

function runIdFromPath(pathname: string) {
  const runMatch = pathname.match(/^\/runs\/([^/?]+)/)
  return runMatch?.[1] || ''
}

function watchlistIdFromPath(pathname: string) {
  const watchlistMatch = pathname.match(/^\/watchlist\/([^/?]+)/)
  return watchlistMatch?.[1] || ''
}

export function ContextSidebar() {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const currentUrl = `${pathname}${searchParams.toString() ? `?${searchParams.toString()}` : ''}`
  const stockCode = stockCodeFromPath(pathname)
  const runId = runIdFromPath(pathname)
  const watchlistId = watchlistIdFromPath(pathname)

  const primary: ContextLink[] = [
    { label: '风险驾驶舱', href: '/', icon: 'dashboard' },
    { label: '组合监控', href: watchlistId ? `/watchlist/${watchlistId}` : '/watchlist', icon: 'portfolio' },
    { label: '事件预警台', href: '/events?view=alerts', icon: 'alerts' },
    { label: 'Agent 任务', href: '/runs', icon: 'runs' },
    { label: '质量指标', href: '/quality', icon: 'quality' },
  ]

  const stockLinks: ContextLink[] = stockCode ? [
    { label: `${stockCode} 情报中心`, href: `/stocks/${stockCode}`, icon: 'stock' },
    { label: '行情快照', href: `/markets/${stockCode}`, icon: 'market' },
    { label: '事件时间线', href: `/stocks/${stockCode}?tab=timeline`, icon: 'events' },
    { label: '影响回测', href: `/stocks/${stockCode}?tab=backtest`, icon: 'trend' },
    { label: '交付物', href: `/stocks/${stockCode}?tab=exports`, icon: 'export' },
  ] : []

  const taskLinks: ContextLink[] = runId ? [
    { label: '当前任务详情', href: `/runs/${runId}`, icon: 'runs' },
    { label: '任务列表', href: '/runs', icon: 'list' },
  ] : []

  return (
    <aside className="contextRail" aria-label="页面上下文">
      <section className="contextBlock">
        <div className="contextTitle">终端菜单</div>
        <nav className="contextList">
          {primary.map((item) => (
            <Link className={`contextItem${activeFor(pathname, currentUrl, item.href) ? ' contextItemActive' : ''}`} href={item.href} key={item.href}>
              <WorkbenchIcon name={item.icon} />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
      </section>

      {stockLinks.length ? (
        <section className="contextBlock">
        <div className="contextTitle">股票上下文</div>
          <nav className="contextList">
            {stockLinks.map((item) => (
              <Link className={`contextItem${activeFor(pathname, currentUrl, item.href) ? ' contextItemActive' : ''}`} href={item.href} key={item.href}>
                <WorkbenchIcon name={item.icon} />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        </section>
      ) : null}

      {taskLinks.length ? (
        <section className="contextBlock">
        <div className="contextTitle">任务上下文</div>
          <nav className="contextList">
            {taskLinks.map((item) => (
              <Link className={`contextItem${activeFor(pathname, currentUrl, item.href) ? ' contextItemActive' : ''}`} href={item.href} key={item.href}>
                <WorkbenchIcon name={item.icon} />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        </section>
      ) : null}

      <section className="contextBlock contextBlockMuted">
        <div className="contextTitle">演示主线</div>
        <div className="contextHint">创建组合 → 实时采集 → Agent 研报 → Trace 证明可信</div>
      </section>
    </aside>
  )
}
