'use client'

import Link from 'next/link'
import { useCallback, useEffect, useState } from 'react'

import { fetchRecentRuns } from '../lib/api'
import type { AnalysisRunListResponse, AnalysisRunResponse } from '../lib/types'

function runTone(status: AnalysisRunResponse['status']) {
  if (status === 'completed') return 'tagPositive'
  if (status === 'failed') return 'tagNegative'
  return ''
}

export function GlobalRunCenter() {
  const [runs, setRuns] = useState<AnalysisRunResponse[]>([])
  const [workspace, setWorkspace] = useState<AnalysisRunListResponse['workspace']>({ tracked_stocks: [], most_active_stock: '', latest_completed_stock: '', failed_stock_count: 0, history_backed_stock_count: 0, recommended_concurrency: 3, active_limit_reached: false, observability_status: 'enhanced', collaboration_ready: true, collaborator_count: 0, audited_action_count: 0, archived_run_count: 0, stale_run_count: 0, recovery_status: 'normal', worker_count: 2, retry_scheduled_count: 0, queue_mode: 'worker_queue', store_backend: 'sqlite-wal', schema_version: 3, wal_enabled: true, backup_available: false, last_backup_path: '', ops_status: 'healthy', alert_count: 0, failure_rate: 0, avg_duration_s: 0, p95_duration_s: 0 })
  const [stats, setStats] = useState({ total: 0, queued: 0, running: 0, completed: 0, failed: 0 })
  const [syncLabel, setSyncLabel] = useState('正在同步任务状态...')

  const applyPayload = useCallback((payload: AnalysisRunListResponse) => {
    setRuns(payload.items)
    setStats({
      total: payload.total,
      queued: payload.queued_count,
      running: payload.running_count,
      completed: payload.completed_count,
      failed: payload.failed_count,
    })
    setWorkspace(payload.workspace)
    setSyncLabel('刚刚同步')
  }, [])

  useEffect(() => {
    let active = true
    let timer: ReturnType<typeof setTimeout> | null = null

    const load = async () => {
      let nextDelay = 9000
      try {
        const payload = await fetchRecentRuns(6)
        nextDelay = payload.items.some((item) => item.status === 'queued' || item.status === 'running') ? 2500 : 9000
        if (active) applyPayload(payload)
      } catch {
        if (active) {
          setSyncLabel('任务状态暂不可用')
        }
      }
      if (active) {
        timer = setTimeout(() => {
          setSyncLabel('后台同步中...')
          void load()
        }, nextDelay)
      }
    }

    void load()
    return () => {
      active = false
      if (timer) clearTimeout(timer)
    }
  }, [applyPayload])

  if (!runs.length && !stats.total) return null

  const activeRuns = runs.filter((item) => item.status === 'queued' || item.status === 'running')
  const latestRuns = activeRuns.length ? activeRuns : runs.slice(0, 3)

  return (
    <section className="globalRunCenter">
      <div className="globalRunSummary">
        <div>
          <div className="sectionEyebrow">Run Center</div>
          <div className="globalRunTitle">全局运行中心</div>
          <div className="globalRunCenterSync">{syncLabel}</div>
        </div>
        <div className="globalRunStats">
          <div className="globalRunStat"><span>总任务</span><strong>{stats.total}</strong></div>
          <div className="globalRunStat"><span>排队 / 运行</span><strong>{stats.queued + stats.running}</strong></div>
          <div className="globalRunStat"><span>失败</span><strong>{stats.failed}</strong></div>
          <div className="globalRunStat"><span>跟踪股票</span><strong>{workspace.tracked_stocks.length}</strong></div>
        </div>
      </div>
      <div className="globalRunList">
        {latestRuns.map((run) => (
          <Link key={run.run_id} href={`/runs/${run.run_id}`} className="globalRunItem">
            <span className={`tag ${runTone(run.status)}`}>{run.status}</span>
            <span className="globalRunCode">{run.stock_code}</span>
            <span className="inlineMeta">{run.actions.suggested_next_action || run.detail || run.last_event || '暂无状态'}</span>
          </Link>
        ))}
        <Link href="/runs" className="globalRunMore">查看全部任务</Link>
      </div>
    </section>
  )
}
