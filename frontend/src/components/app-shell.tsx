'use client'

import { Suspense, type ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

import type { AuthUser } from '../lib/types'
import { AutoRefreshControl } from './auto-refresh-control'
import { UserMenu } from './user-menu'
import { ContextSidebar } from './workbench/context-sidebar'

export function AppShell({ children, user, runCenter }: { children: ReactNode; user: AuthUser | null; runCenter?: ReactNode }) {
  const pathname = usePathname()
  const isAuthRoute = pathname === '/login' || pathname === '/register'
  const showRunCenter = Boolean(runCenter) && false

  if (isAuthRoute) {
    return <>{children}</>
  }

  return (
    <div className="appFrame">
      <aside className="sidebar">
        <Link className="brandLockup" href="/">
          <div className="brandMark">FT</div>
          <div>
            <div className="brandTitle">金融研究终端</div>
            <div className="brandSub">多智能体金融研究终端</div>
          </div>
        </Link>
        <Suspense fallback={<div className="contextRail" />}>
          <ContextSidebar />
        </Suspense>
      </aside>

      <div className="contentArea">
        <header className="topbar">
          <Link className="topbarProduct" href="/">
            <span className="topbarProductMark" aria-hidden />
            <span>金融研究指挥中心</span>
          </Link>
          <div className="topbarStatusCluster" aria-label="系统状态">
            <span><i className="liveDot" aria-hidden /> 实时采集</span>
            <span>用户隔离</span>
            <span>Agent Trace</span>
            <span>{pathname === '/' ? '驾驶舱' : pathname.startsWith('/runs') ? 'Agent 任务' : pathname.startsWith('/events') ? '事件预警' : pathname.startsWith('/watchlist') ? '组合监控' : '研究工作台'}</span>
          </div>
          <div className="topbarActions">
            <AutoRefreshControl />
            <Link className="topbarCommand" href="/watchlist">新建组合</Link>
            {user ? <UserMenu user={user} /> : (
              <div className="authLinks">
                <Link className="topbarCommand" href="/login">登录</Link>
                <Link className="topbarCommand" href="/register">注册</Link>
              </div>
            )}
          </div>
        </header>
        {showRunCenter ? runCenter : null}
        {children}
      </div>
    </div>
  )
}
