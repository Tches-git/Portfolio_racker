import Link from 'next/link'
import type { ReactNode } from 'react'

import type { AgentFlowNode, CommandCenterMetric } from '../../lib/types'

export function CommandCenterShell({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`commandCenterShell ${className}`.trim()}>{children}</div>
}

export function HeroRiskBand({
  eyebrow,
  title,
  summary,
  score,
  level,
  actionHref,
  actionLabel,
}: {
  eyebrow: string
  title: string
  summary: string
  score: number | string
  level: string
  actionHref: string
  actionLabel: string
}) {
  return (
    <section className={`heroRiskBand heroRisk-${level}`}>
      <div className="heroRiskCore">
        <span>{eyebrow}</span>
        <strong>{score}</strong>
        <em>{levelText(level)}</em>
      </div>
      <div className="heroRiskCopy">
        <span>COMMAND OBJECTIVE</span>
        <h2>{title}</h2>
        <p>{summary}</p>
      </div>
      <Link className="heroRiskAction" href={actionHref}>{actionLabel}</Link>
    </section>
  )
}

export function KpiRibbon({ items }: { items: CommandCenterMetric[] }) {
  return (
    <section className="kpiRibbon" aria-label="核心指标">
      {items.map((item) => (
        <Link className={`kpiRibbonItem tone-${item.tone || 'neutral'}`} href={item.href || '#'} key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
          {item.hint ? <em>{item.hint}</em> : null}
        </Link>
      ))}
    </section>
  )
}

export function ActionDock({ title, eyebrow = 'NEXT ACTION', children }: { title: string; eyebrow?: string; children: ReactNode }) {
  return (
    <aside className="actionDock">
      <header>
        <span>{eyebrow}</span>
        <h2>{title}</h2>
      </header>
      {children}
    </aside>
  )
}

export function AgentFlowPanel({ nodes, emptyLabel = '暂无多智能体 Trace' }: { nodes: AgentFlowNode[]; emptyLabel?: string }) {
  if (!nodes.length) return <div className="agentFlowEmpty">{emptyLabel}</div>
  return (
    <ol className="agentFlowPanel" aria-label="多智能体执行链路">
      {nodes.map((node, index) => (
        <li className={`agentFlowNode agentFlow-${node.status}`} key={node.id}>
          <span>{String(index + 1).padStart(2, '0')}</span>
          <div>
            <strong>{node.label}</strong>
            <em>{node.detail}</em>
          </div>
          <b>{node.metric}</b>
        </li>
      ))}
    </ol>
  )
}

export function EvidenceMatrix({ items }: { items: CommandCenterMetric[] }) {
  return (
    <div className="evidenceMatrix">
      {items.map((item) => (
        <div className={`evidenceMatrixItem tone-${item.tone || 'neutral'}`} key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
          {item.hint ? <em>{item.hint}</em> : null}
        </div>
      ))}
    </div>
  )
}

function levelText(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  if (level === 'low') return '低风险'
  return level || '待评估'
}
