'use client'

import type { ReactNode } from 'react'

import type { ChartDatum, RiskRadarPoint } from '../../lib/types'

type ChartPanelProps = {
  title: string
  eyebrow?: string
  description?: string
  children?: ReactNode
  className?: string
}

export function ChartPanel({ title, eyebrow, description, children, className = '' }: ChartPanelProps) {
  return (
    <section className={`chartPanel ${className}`.trim()}>
      <header className="chartPanelHead">
        <div>
          {eyebrow ? <span>{eyebrow}</span> : null}
          <h2>{title}</h2>
        </div>
        {description ? <p>{description}</p> : null}
      </header>
      <div className="chartPanelBody">{children}</div>
    </section>
  )
}

export function DonutChart({ data, emptyLabel = '暂无数据' }: { data: ChartDatum[]; emptyLabel?: string }) {
  const total = data.reduce((sum, item) => sum + Math.max(0, item.value), 0)
  if (!total) return <div className="chartEmpty">{emptyLabel}</div>

  let offset = 25
  const radius = 34
  const circumference = 2 * Math.PI * radius
  return (
    <div className="donutChart">
      <svg viewBox="0 0 120 120" role="img" aria-label="环形分布图">
        <circle className="donutTrack" cx="60" cy="60" r={radius} />
        {data.map((item, index) => {
          const ratio = Math.max(0, item.value) / total
          const dash = ratio * circumference
          const strokeDasharray = `${dash} ${circumference - dash}`
          const strokeDashoffset = offset
          offset -= dash
          return (
            <circle
              className={`donutSlice donutSlice-${index % 6}`}
              cx="60"
              cy="60"
              r={radius}
              key={item.label}
              strokeDasharray={strokeDasharray}
              strokeDashoffset={strokeDashoffset}
            />
          )
        })}
        <text x="60" y="57">{total}</text>
        <text x="60" y="73">TOTAL</text>
      </svg>
      <div className="chartLegend">
        {data.map((item, index) => (
          <span key={item.label}><i className={`legendDot legendDot-${index % 6}`} />{item.label}<strong>{item.value}</strong></span>
        ))}
      </div>
    </div>
  )
}

export function BarPulseChart({ data, emptyLabel = '暂无事件' }: { data: ChartDatum[]; emptyLabel?: string }) {
  const maxValue = Math.max(1, ...data.map((item) => item.value))
  if (!data.length) return <div className="chartEmpty">{emptyLabel}</div>
  return (
    <div className="barPulseChart" role="img" aria-label="柱状脉冲图">
      {data.map((item, index) => (
        <div className="barPulseItem" key={`${item.label}-${index}`}>
          <span style={{ height: `${Math.max(8, (item.value / maxValue) * 100)}%` }} />
          <em>{item.label}</em>
          <strong>{item.value}</strong>
        </div>
      ))}
    </div>
  )
}

export function RiskRadarChart({ data, emptyLabel = '暂无风险数据' }: { data: RiskRadarPoint[]; emptyLabel?: string }) {
  if (!data.length) return <div className="chartEmpty">{emptyLabel}</div>

  const center = 60
  const maxRadius = 44
  const points = data.map((item, index) => {
    const angle = (-90 + (360 / data.length) * index) * (Math.PI / 180)
    const radius = Math.max(0, Math.min(100, item.value)) / 100 * maxRadius
    return {
      ...item,
      x: center + Math.cos(angle) * radius,
      y: center + Math.sin(angle) * radius,
      lx: center + Math.cos(angle) * 54,
      ly: center + Math.sin(angle) * 54,
    }
  })
  const polygon = points.map((item) => `${item.x},${item.y}`).join(' ')
  const grid = [0.35, 0.65, 1].map((scale) => data.map((_, index) => {
    const angle = (-90 + (360 / data.length) * index) * (Math.PI / 180)
    return `${center + Math.cos(angle) * maxRadius * scale},${center + Math.sin(angle) * maxRadius * scale}`
  }).join(' '))

  return (
    <div className="riskRadarChart">
      <svg viewBox="0 0 120 120" role="img" aria-label="风险雷达图">
        {grid.map((line) => <polygon className="radarGrid" points={line} key={line} />)}
        {points.map((item) => <line className="radarAxis" x1={center} y1={center} x2={item.lx} y2={item.ly} key={`axis-${item.label}`} />)}
        <polygon className="radarShape" points={polygon} />
        {points.map((item) => <circle className="radarPoint" cx={item.x} cy={item.y} r="2.3" key={`point-${item.label}`} />)}
      </svg>
      <div className="radarLabels">
        {data.map((item) => <span key={item.label}><em>{item.label}</em><strong>{item.value}</strong></span>)}
      </div>
    </div>
  )
}
