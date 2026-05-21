'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

function stockCodeFromPath(pathname: string) {
  const stockMatch = pathname.match(/^\/(?:stocks|markets)\/([^/]+)/)
  if (stockMatch?.[1]) return stockMatch[1]
  return ''
}

export function SidebarNav() {
  const pathname = usePathname()
  const stockCode = stockCodeFromPath(pathname)
  const inRunDetail = /^\/runs\/[^/]+/.test(pathname)
  const navGroups = [
    {
      title: '工作台',
      items: [
        { label: '组合风险驾驶舱', href: '/', icon: '▦' },
        { label: '组合管理', href: '/watchlist', icon: '◫' },
        { label: '事件预警处理台', href: '/events', icon: '!' },
        { label: '行情展示', href: '/markets', icon: '⌁' },
        { label: '任务交付中心', href: '/runs', icon: '▣' },
        { label: '质量指标', href: '/quality', icon: '✓' },
      ],
    },
    ...(stockCode ? [{
      title: '当前股票',
      items: [
        { label: `${stockCode} 情报中心`, href: `/stocks/${stockCode}`, icon: '◉' },
        { label: '行情', href: `/markets/${stockCode}`, icon: '⌁' },
        { label: '摘要', href: `/stocks/${stockCode}?tab=summary`, icon: '≡' },
        { label: '事件', href: `/stocks/${stockCode}?tab=timeline`, icon: '◇' },
        { label: '复盘', href: `/stocks/${stockCode}?tab=history`, icon: '↺' },
        { label: '影响回测', href: `/stocks/${stockCode}?tab=backtest`, icon: '↗' },
        { label: '交付', href: `/stocks/${stockCode}?tab=exports`, icon: '⇩' },
      ],
    }] : []),
    {
      title: '上下文',
      items: [
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
