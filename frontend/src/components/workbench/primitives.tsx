import Link from 'next/link'
import type { ReactNode } from 'react'

import type { WorkbenchAction } from '../../lib/types'
import { WorkbenchActionButtons } from './workbench-action-buttons'

export type StatusTone = 'neutral' | 'success' | 'warning' | 'danger' | 'info'

export type MetricItem = {
  label: string
  value: ReactNode
  hint?: ReactNode
  tone?: StatusTone
}

export type PageAction = {
  label: string
  href: string
  tone?: StatusTone
}

export function PageShell({
  eyebrow,
  title,
  description,
  actions = [],
  className = '',
  compact = false,
  children,
}: {
  eyebrow: string
  title: string
  description?: string
  actions?: WorkbenchAction[]
  className?: string
  compact?: boolean
  children: ReactNode
}) {
  return (
    <main className={`wbPage ${className}`.trim()}>
      <header className={`wbHeader${compact ? ' wbHeaderCompact' : ''}`}>
        <div className="wbHeaderCopy">
          <div className="wbEyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          {description ? <p>{description}</p> : null}
          {!compact ? <div className="terminalStatusLine" aria-label="页面状态">
            <span><i className="liveDot" aria-hidden /> 实时</span>
            <span>用户隔离</span>
            <span>数据库已连接</span>
            <span>多智能体链路</span>
          </div> : null}
        </div>
        {actions.length ? <WorkbenchActionButtons actions={actions} /> : null}
      </header>
      {children}
    </main>
  )
}

export function MetricStrip({ items }: { items: MetricItem[] }) {
  return (
    <section className="wbMetricGrid">
      {items.map((item) => (
        <div className={`wbMetric ${item.tone ? `tone-${item.tone}` : ''}`} key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
          {item.hint ? <em>{item.hint}</em> : null}
        </div>
      ))}
    </section>
  )
}

export function StatusBadge({ tone = 'neutral', children }: { tone?: StatusTone; children: ReactNode }) {
  return <span className={`wbBadge tone-${tone}`}>{children}</span>
}

export function EmptyState({
  title = '暂无数据',
  description,
  action,
}: {
  title?: string
  description?: ReactNode
  action?: PageAction
}) {
  return (
    <div className="wbEmpty">
      <strong>{title}</strong>
      {description ? <span>{description}</span> : null}
      {action ? <Link className="wbTextButton" href={action.href}>{action.label}</Link> : null}
    </div>
  )
}

export function ActionBar({ actions }: { actions: PageAction[] }) {
  if (!actions.length) return null
  return (
    <div className="wbActionBar">
      {actions.map((action) => (
        <Link className={`wbButton ${action.tone === 'danger' ? 'tone-danger' : ''}`} href={action.href} key={`${action.label}-${action.href}`}>
          {action.label}
        </Link>
      ))}
    </div>
  )
}

export function SplitPane({ children }: { children: ReactNode }) {
  return <section className="wbSplitPane">{children}</section>
}

export function DataTable({
  columns,
  children,
  empty,
}: {
  columns: string[]
  children: ReactNode
  empty?: ReactNode
}) {
  return (
    <div className="wbTableWrap">
      <table className="wbTable">
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
      {empty}
    </div>
  )
}

export function TerminalPanel({ title, eyebrow, action, children }: { title: string; eyebrow?: string; action?: ReactNode; children: ReactNode }) {
  return (
    <section className="wbPanel terminalPanel">
      <div className="wbPanelHead">
        <div>
          {eyebrow ? <div className="wbEyebrow">{eyebrow}</div> : null}
          <h2>{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  )
}

export function CommandBar({ children }: { children: ReactNode }) {
  return <div className="terminalCommandBar">{children}</div>
}

export function DetailDock({ children }: { children: ReactNode }) {
  return <aside className="terminalDetailDock">{children}</aside>
}

export function RiskTicker({ items }: { items: Array<{ label: string; value: ReactNode; tone?: StatusTone }> }) {
  return (
    <div className="riskTicker">
      {items.map((item) => (
        <span className={`riskTickerItem ${item.tone ? `tone-${item.tone}` : ''}`} key={item.label}>
          <em>{item.label}</em>
          <strong>{item.value}</strong>
        </span>
      ))}
    </div>
  )
}

export function StatusPill({ tone = 'neutral', children }: { tone?: StatusTone; children: ReactNode }) {
  return <StatusBadge tone={tone}>{children}</StatusBadge>
}
