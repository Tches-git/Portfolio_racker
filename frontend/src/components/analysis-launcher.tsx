'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useRef, useState, useTransition } from 'react'

import { createAnalysisRun, fetchAnalysisRun } from '../lib/api'
import type { AnalysisRunResponse } from '../lib/types'

export function AnalysisLauncher({ initialCode, initialRuns = [] }: { initialCode: string; initialRuns?: AnalysisRunResponse[] }) {
  const router = useRouter()
  const [code, setCode] = useState(initialCode)
  const [run, setRun] = useState<AnalysisRunResponse | null>(initialRuns[0] || null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [isRefreshing, startTransition] = useTransition()
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const normalized = useMemo(() => code.trim(), [code])

  useEffect(() => {
    setCode(initialCode)
  }, [initialCode])

  useEffect(() => {
    setRun((current) => current || initialRuns[0] || null)
  }, [initialRuns])

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current)
    }
  }, [])

  const pollRun = async (runId: string) => {
    const next = await fetchAnalysisRun(runId)
    setRun(next)
    setFeedback(next.last_event || next.detail || '任务状态已更新')
    if (next.status === 'completed') {
      setLoading(false)
      setFeedback('分析完成，正在静默同步最新报告...')
      startTransition(() => router.refresh())
      return
    }
    if (next.status === 'failed') {
      setLoading(false)
      setError(next.error || '分析任务失败')
      setFeedback('')
      return
    }
    timerRef.current = setTimeout(() => {
      void pollRun(runId)
    }, 1200)
  }

  const startRun = async () => {
    if (!normalized || loading || isRefreshing) return
    setLoading(true)
    setError('')
    setFeedback('请求已提交，正在创建任务...')
    setRun({
      run_id: 'pending',
      stock_code: normalized,
      status: 'queued',
      created_at: '',
      updated_at: '',
      detail: '正在写入任务队列',
      last_event: 'queued',
      error: '',
      owner: '',
      owner_role: '',
      archived: false,
      retry_of_run_id: '',
      latest_report_url: '',
      history_url: '',
      exports: [],
      events: [],
      event_context: {
        event_id: '',
        stock_code: normalized,
        stock_name: '',
        title: '',
        summary: '',
        source: '',
        provider: '',
        url: '',
        published_at: '',
        collected_at: '',
        event_type: '',
        sentiment: '',
        impact_level: '',
        impact_scope: '',
        confidence: 0,
        reason: '',
        channel: '',
        retrieval_mode: '',
        evidence_type: '',
        related_sources: [],
        status: '',
        status_note: '',
        note: '',
      },
      event_report_summary: {
        trigger_label: '',
        thesis: '',
        impact_direction: '',
        impact_level: '',
        impact_scope: '',
        priority: '',
        review_status: '',
        action: '',
        report_delta_hint: '',
        related_source_count: 0,
        event_commentary_filename: '',
        event_commentary_url: '',
      },
      audit_events: [],
      run_metrics: { duration_s: 0, llm_calls: 0, tool_calls: 0, total_tokens: 0, success: false },
      actions: { can_retry: false, can_cancel: false, can_assign: false, can_archive: false, can_change_owner: false, can_view_audit: false, suggested_next_action: '等待任务进入 worker 队列', product_route: `/stocks/${normalized}`, history_route: `/stocks/${normalized}/history`, exports_route: `/stocks/${normalized}/exports` },
      observability: { event_count: 0, artifact_count: 0, has_error: false, latest_signal: 'queued', owner_label: '未分配', archive_label: '活跃', retry_lineage: '', recovery_status: 'normal', stale_after_restart: false, attempts: 0, max_attempts: 0, worker_id: '', locked_at: '', next_retry_at: '' },
    })
    try {
      const created = await createAnalysisRun(normalized)
      setRun(created)
      setFeedback('任务已入队，页面保持可操作并自动追踪进度。')
      void pollRun(created.run_id)
    } catch (err) {
      setLoading(false)
      setFeedback('')
      setError(err instanceof Error ? err.message : '创建分析任务失败')
    }
  }

  return (
    <section className="panel span-12 actionPanel">
      <div className="sectionHead">
        <div>
          <div className="sectionEyebrow">分析动作</div>
          <h2>浏览器触发分析</h2>
        </div>
      </div>
      <div className="launcherGrid">
        <div className="card">
          <div className="itemTitle">发起新分析</div>
          <p className="bodyText">保持现有 Python 主链路不动，只在兼容 API 层上新增最小写入口，由浏览器发起分析并轮询状态。</p>
          <div className="searchRow launcherRow">
            <input
              className="input"
              value={code}
              onChange={(event) => setCode(event.target.value)}
              placeholder="输入股票代码，如 600519"
            />
            <button className="button" onClick={() => void startRun()} disabled={!normalized || loading || isRefreshing}>
              {loading || isRefreshing ? '分析运行中...' : '开始分析'}
            </button>
          </div>
          {feedback ? <div className="pendingText">{feedback}</div> : null}
          {error ? <div className="inlineError">{error}</div> : null}
        </div>
        <div className="card">
          <div className="itemTitle">任务状态</div>
          {run ? (
            <div className="metricStack">
              <div className="metricRow"><span>任务 ID</span><strong>{run.run_id}</strong></div>
              <div className="metricRow"><span>状态</span><strong>{run.status}</strong></div>
              <div className="metricRow"><span>最新事件</span><strong>{run.last_event || '--'}</strong></div>
              <div className="metricRow"><span>状态说明</span><strong>{run.detail || '--'}</strong></div>
              <div className="metricRow"><span>事件数量</span><strong>{run.events.length}</strong></div>
              <div className="metricRow"><span>运行指标</span><strong>{run.run_metrics.success ? `${run.run_metrics.duration_s.toFixed(1)}s / ${run.run_metrics.total_tokens} tokens` : '--'}</strong></div>
              {run.events.length ? <div className="inlineMeta">最近阶段：{run.events[run.events.length - 1]?.detail || run.detail || '--'}</div> : null}
            </div>
          ) : <p className="bodyText">尚未发起浏览器分析任务。</p>}
        </div>
        <div className="card">
          <div className="itemTitle">完成后动作</div>
          {run ? (
            <div className="actionList">
              <button className="ghostButton" onClick={() => router.push(`/runs/${run.run_id}`)} disabled={run.run_id === 'pending'}>进入任务详情</button>
              <button className="ghostButton" onClick={() => router.push(`/stocks/${run.stock_code}`)}>查看最新产品页</button>
              <button className="ghostButton" onClick={() => void startRun()} disabled={loading || isRefreshing}>再次发起分析</button>
              {run.status === 'completed' ? <button className="ghostButton" onClick={() => router.push(`/stocks/${run.stock_code}/exports`)}>查看导出中心</button> : null}
            </div>
          ) : <p className="bodyText">完成后会自动刷新当前路由，你也可以直接跳到摘要、导出和历史工作区。</p>}
        </div>
      </div>
    </section>
  )
}
