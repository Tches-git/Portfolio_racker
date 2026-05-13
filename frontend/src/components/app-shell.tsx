'use client'

import type { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

import type { AuthUser } from '../lib/types'
import { SidebarNav } from './sidebar-nav'
import { UserMenu } from './user-menu'

const TOP_LINKS = [
  { label: '驾驶舱', href: '/' },
  { label: '组合', href: '/watchlist' },
  { label: '事件预警', href: '/events' },
  { label: '行情', href: '/markets' },
  { label: '任务交付', href: '/runs' },
]

export function AppShell({ children, user, runCenter }: { children: ReactNode; user: AuthUser | null; runCenter?: ReactNode }) {
  const pathname = usePathname()
  const isAuthRoute = pathname === '/login' || pathname === '/register'

  if (isAuthRoute) {
    return <>{children}</>
  }

  return (
    <div className="appFrame">
      <aside className="sidebar">
        <div>
          <Link className="brandLockup" href="/">
            <div className="brandMark">研</div>
            <div>
              <div className="brandTitle">研究中枢</div>
              <div className="brandSub">金融消息追踪平台</div>
            </div>
          </Link>
        </div>

        <SidebarNav />

        <div className="sidebarCard">
          <div className="sidebarCardTitle">工作区</div>
          <div className="sidebarCardText">多用户工作区 · 当前账号独立数据空间，事件历史、预警处理、研报交付在同一工作台内闭环。</div>
        </div>
      </aside>

      <div className="contentArea">
        <header className="topbar">
          <Link className="topbarProduct" href="/">
            <span className="vercelTriangle" aria-hidden />
            <span>组合风险驾驶舱</span>
          </Link>
          <nav className="topbarNav" aria-label="Global navigation">
            {TOP_LINKS.map((item) => {
              const active = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href))
              return (
                <Link className={`topbarLink${active ? ' topbarLinkActive' : ''}`} href={item.href} key={item.href}>
                  {item.label}
                </Link>
              )
            })}
          </nav>
          <div className="topbarActions">
            <Link className="topbarCommand" href="/watchlist">新建组合</Link>
            <span className="topbarMeta"><span className="liveDot" aria-hidden /> 当前账号独立数据</span>
            {user ? <UserMenu user={user} /> : (
              <div className="authLinks">
                <Link className="topbarCommand" href="/login">登录</Link>
                <Link className="topbarCommand" href="/register">注册</Link>
              </div>
            )}
          </div>
        </header>
        {runCenter}
        {children}
      </div>
    </div>
  )
}
