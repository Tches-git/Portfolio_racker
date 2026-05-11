import type { ReactNode } from 'react'

export function MetricCard({ label, value, hint }: { label: string; value: ReactNode; hint?: string }) {
  return (
    <div className="metricCard">
      <div className="statusLabel">{label}</div>
      <div className="metricCardValue">{value}</div>
      {hint ? <div className="inlineMeta">{hint}</div> : null}
    </div>
  )
}
