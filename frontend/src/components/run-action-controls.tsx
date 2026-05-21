'use client'

import { useRouter } from 'next/navigation'
import { useState, useTransition } from 'react'

import { archiveAnalysisRun, assignAnalysisRun, cancelAnalysisRun, retryAnalysisRun } from '../lib/api'
import { formatRunStatus } from '../lib/labels'
import type { AnalysisRunResponse } from '../lib/types'

export function RunActionControls({ run }: { run: AnalysisRunResponse }) {
  const router = useRouter()
  const [owner, setOwner] = useState(run.owner || '')
  const [error, setError] = useState('')
  const [pendingAction, setPendingAction] = useState('')
  const [optimisticRun, setOptimisticRun] = useState(run)
  const [isRefreshing, startTransition] = useTransition()
  const loading = Boolean(pendingAction) || isRefreshing

  const finishWith = (next: AnalysisRunResponse, nextMessage: string, navigate = false) => {
    setOptimisticRun(next)
    setPendingAction(nextMessage)
    startTransition(() => {
      if (navigate) router.push(`/runs/${next.run_id}`)
      router.refresh()
      setPendingAction('')
    })
  }

  const retry = async () => {
    setPendingAction('正在创建重试任务...')
    setError('')
    try {
      const next = await retryAnalysisRun(run.run_id)
      finishWith(next, '重试任务已创建，正在打开新任务...', true)
    } catch (err) {
      setError(err instanceof Error ? err.message : '重试分析任务失败')
      setPendingAction('')
    }
  }

  const cancel = async () => {
    setPendingAction('正在取消任务...')
    setError('')
    setOptimisticRun((current) => ({ ...current, status: 'failed', detail: '取消请求已发送，正在同步任务状态。' }))
    try {
      const next = await cancelAnalysisRun(run.run_id)
      finishWith(next, '任务已取消，正在同步最新状态...')
    } catch (err) {
      setError(err instanceof Error ? err.message : '取消分析任务失败')
      setOptimisticRun(run)
      setPendingAction('')
    }
  }

  const assign = async () => {
    if (!owner.trim()) return
    setPendingAction('正在分配负责人...')
    setError('')
    setOptimisticRun((current) => ({ ...current, owner: owner.trim() }))
    try {
      const next = await assignAnalysisRun(run.run_id, owner.trim())
      finishWith(next, '负责人已更新，正在同步最新状态...')
    } catch (err) {
      setError(err instanceof Error ? err.message : '分配任务失败')
      setOptimisticRun(run)
      setPendingAction('')
    }
  }

  const archive = async () => {
    setPendingAction('正在归档任务...')
    setError('')
    setOptimisticRun((current) => ({ ...current, archived: true, detail: '归档请求已发送，正在同步任务状态。' }))
    try {
      const next = await archiveAnalysisRun(run.run_id)
      finishWith(next, '任务已归档，正在同步最新状态...')
    } catch (err) {
      setError(err instanceof Error ? err.message : '归档任务失败')
      setOptimisticRun(run)
      setPendingAction('')
    }
  }

  return (
    <div className="actionList">
      <div className="statusBar compactStatusBar detailStatusBar">
        <div>
          <div className="statusLabel">即时状态</div>
          <div className="statusHint">{optimisticRun.owner || '未分配'} · {optimisticRun.archived ? '已归档' : formatRunStatus(optimisticRun.status)} · {optimisticRun.detail || '等待操作'}</div>
        </div>
      </div>
      <div className="searchRow">
        <input className="input" value={owner} onChange={(event) => setOwner(event.target.value)} placeholder="指定负责人，如 research-owner" />
        <button className="ghostButton" onClick={() => void assign()} disabled={loading || !owner.trim()}>分配任务</button>
      </div>
      {run.actions.can_retry ? <button className="ghostButton" onClick={() => void retry()} disabled={loading}>重试任务</button> : null}
      {run.actions.can_cancel ? <button className="ghostButton" onClick={() => void cancel()} disabled={loading}>取消任务</button> : null}
      {run.actions.can_archive ? <button className="ghostButton" onClick={() => void archive()} disabled={loading}>归档任务</button> : null}
      {pendingAction ? <div className="pendingText">{pendingAction}</div> : null}
      {error ? <div className="inlineError">{error}</div> : null}
    </div>
  )
}
