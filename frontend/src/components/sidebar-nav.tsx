'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

function stockCodeFromPath(pathname: string) {
  const stockMatch = pathname.match(/^\/stocks\/([^/]+)/)
  if (stockMatch?.[1]) return stockMatch[1]
  return ''
}

export function SidebarNav() {
  const pathname = usePathname()
  const stockCode = stockCodeFromPath(pathname)
  const inRunDetail = /^\/runs\/[^/]+/.test(pathname)
  const navGroups = [
    {
      title: '核心导航',
      items: [
        { label: '首页总览', href: '/', icon: '⌂' },
        { label: '事件追踪', href: '/events', icon: '◇' },
        { label: '预警中心', href: '/alerts', icon: '!' },
        { label: '每日简报', href: '/briefing', icon: '☰' },
        { label: '任务中心', href: '/runs', icon: '▣' },
        ...(stockCode ? [{ label: '股票工作台', href: `/stocks/${stockCode}`, icon: '◉' }] : []),
      ],
    },
    ...(stockCode ? [{
      title: '股票工作台',
      items: [
        { label: '摘要详情', href: `/stocks/${stockCode}/summary`, icon: '≡' },
        { label: '事件时间线', href: `/stocks/${stockCode}/timeline`, icon: '◇' },
        { label: '历史脉络', href: `/stocks/${stockCode}/history`, icon: '↺' },
        { label: '导出中心', href: `/stocks/${stockCode}/exports`, icon: '⇩' },
      ],
    }] : []),
    {
      title: '辅助入口',
      items: [
        { label: '组合跟踪', href: '/watchlist', icon: '◍' },
        ...(inRunDetail ? [{ label: '当前任务详情', href: pathname, icon: '◎' }] : []),
      ],
    },
  ]

  return (
    <nav className="navGroups">
      {navGroups.map((group) => (
        <div key={group.title} className="navGroup">
          <div className="navGroupTitle">{group.title}</div>
          <div className="navList">
            {group.items.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href))
              return (
                <Link
                  key={item.label}
                  href={item.href}
                  className={`navItem${isActive ? ' navItemActive' : ''}`}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <span className="navIcon">{item.icon}</span>
                  <span className="navLabel">{item.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      ))}
    </nav>
  )
}
