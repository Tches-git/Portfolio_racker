'use client'

import type { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

import { SidebarNav } from './sidebar-nav'

const TOP_LINKS = [
  { label: '总览', href: '/' },
  { label: '事件', href: '/events' },
  { label: '预警', href: '/alerts' },
  { label: '组合', href: '/watchlist' },
  { label: '任务', href: '/runs' },
]

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()

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
          <div className="sidebarCardText">本地单用户模式 · 事件历史、预警处理、研报交付在同一工作台内闭环。</div>
        </div>
      </aside>

      <div className="contentArea">
        <header className="topbar">
          <Link className="topbarProduct" href="/">
            <span className="vercelTriangle" aria-hidden />
            <span>金融消息追踪平台</span>
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
            <Link className="topbarCommand" href="/stocks/600519">打开 600519</Link>
            <span className="topbarMeta"><span className="liveDot" aria-hidden /> 本地接口</span>
          </div>
        </header>
        {children}
      </div>
    </div>
  )
}
