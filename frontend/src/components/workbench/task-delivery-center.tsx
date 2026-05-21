import Link from 'next/link'

import { BatchRunLauncher } from '../batch-run-launcher'
import { RunActionControls } from '../run-action-controls'
import { ActionDock, AgentFlowPanel, CommandCenterShell, EvidenceMatrix, HeroRiskBand, KpiRibbon } from '../big-screen/command-center'
import { ChartPanel, DonutChart } from '../big-screen/chart-panel'
import { formatAgentRoleName, formatRunEvent, formatRunStatus } from '../../lib/labels'
import type { AnalysisRunResponse, RunWorkbenchResponse } from '../../lib/types'
import { EmptyState, StatusBadge } from './primitives'

export function TaskDeliveryCenter({ data }: { data: RunWorkbenchResponse }) {
  const selected = data.selected_run || data.runs.items[0] || null
  const activeRuns = data.runs.items.filter((run) => run.status === 'queued' || run.status === 'running')
  const allRuns = data.runs.items
  const taskStateChart = [
    { label: '完成', value: data.runs.completed_count },
    { label: '失败', value: data.runs.failed_count },
    { label: '活跃', value: activeRuns.length },
    { label: '其他', value: Math.max(0, data.runs.total - data.runs.completed_count - data.runs.failed_count - activeRuns.length) },
  ]

  return (
    <CommandCenterShell className="agentMissionDesk agentCommandDashboard">
      <HeroRiskBand
        eyebrow="AGENT MISSION"
        title="多智能体研报任务态势"
        summary="把实时数据采集、角色协作、可信度审计和研报交付放在同一条任务链路里展示。"
        score={data.runs.total}
        level={data.runs.failed_count ? 'high' : activeRuns.length ? 'medium' : 'low'}
        actionHref="/runs"
        actionLabel="查看任务"
      />

      <KpiRibbon items={[
        { label: '总任务', value: data.runs.total, hint: '当前账号', tone: 'agent', href: '/runs' },
        { label: '活跃', value: activeRuns.length, hint: '排队 / 运行', tone: activeRuns.length ? 'info' : 'neutral', href: '/runs' },
        { label: '完成', value: data.runs.completed_count, hint: '可查看交付', tone: 'success', href: '/runs' },
        { label: '失败', value: data.runs.failed_count, hint: '可重试', tone: data.runs.failed_count ? 'danger' : 'neutral', href: '/runs' },
      ]} />

      <section className="agentMissionGrid">
        <main className="agentRunTape">
          <header className="agentSectionHead">
            <div>
              <span>RUN TAPE</span>
              <h2>研报任务队列</h2>
            </div>
            <div className="agentQueueMeta">
              <span>工作区股票 {data.runs.workspace.tracked_stocks.length}</span>
              <span>Worker {data.runs.workspace.worker_count}</span>
              <span>{data.runs.workspace.queue_mode || 'worker_queue'}</span>
            </div>
          </header>
          <RunLedger runs={allRuns} selectedRunId={selected?.run_id || ''} />
        </main>

        <ActionDock title={selected ? currentAgentRole(selected) : '创建第一条研报任务'} eyebrow="AGENT DOCK">
          <ChartPanel eyebrow="TASK STATE" title="任务状态分布">
            <DonutChart data={taskStateChart} emptyLabel="暂无任务" />
          </ChartPanel>
          <section className="agentDockBlock agentCurrentMission">
            <div className="agentDockHead">
              <span>CURRENT MISSION</span>
              {selected ? <Link href={`/runs/${selected.run_id}`}>进入详情</Link> : null}
            </div>
            {selected ? (
              <div className="agentCurrentBody">
                <div className="agentMissionTitle">
                  <StatusBadge tone={statusTone(selected.status)}>{formatRunStatus(selected.status)}</StatusBadge>
                  <strong>{selected.stock_name && selected.stock_name !== selected.stock_code ? `${selected.stock_name}（${selected.stock_code}）` : selected.stock_code}</strong>
                  <p>{compactText(selected.detail || selected.error || '任务状态同步中。', 108)}</p>
                </div>
                <AgentFlowPanel nodes={agentNodes(selected)} />
                <EvidenceMatrix items={[
                  { label: '引用覆盖', value: formatPct(selected.run_metrics.citation_coverage_rate), tone: 'info' },
                  { label: '工具调用', value: selected.run_metrics.tool_calls, tone: 'agent' },
                  { label: '导出物', value: selected.exports.length, tone: selected.exports.length ? 'success' : 'neutral' },
                ]} />
                <RunActionControls run={selected} />
              </div>
            ) : <EmptyState title="暂无任务" description="创建研报任务后，这里会显示当前任务的 Agent 进度和可信度证据。" />}
          </section>

          <section className="agentDockBlock runCreatePanelTarget" id="run-create-panel">
            <div className="agentDockHead">
              <span>CREATE</span>
              <em>实时采集</em>
            </div>
            <BatchRunLauncher initialStocks={data.runs.workspace.tracked_stocks} />
          </section>
        </ActionDock>
      </section>
    </CommandCenterShell>
  )
}

function AgentProgressMini({ run }: { run: AnalysisRunResponse }) {
  const roles = run.multi_agent_trace?.roles || []
  if (!roles.length) {
    return (
      <div className="agentProgressMini">
        <div className="agentProgressEmpty">该任务尚未写入多智能体 Trace。</div>
      </div>
    )
  }
  return (
    <ol className="agentProgressMini">
      {roles.slice(0, 7).map((role, index) => (
        <li className={`agentMiniRole agentMiniRole-${role.status}`} key={role.role_id}>
          <span>{String(index + 1).padStart(2, '0')}</span>
          <div>
            <strong>{formatAgentRoleName(role.role_name || role.role_id)}</strong>
            <em>{role.fallback_used ? '降级' : role.status === 'completed' ? '完成' : role.status}</em>
          </div>
        </li>
      ))}
    </ol>
  )
}

function statusTone(status: string) {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'danger'
  if (status === 'running' || status === 'queued') return 'info'
  return 'neutral'
}

function compactText(value: string, maxLength = 72) {
  if (!value) return ''
  const normalized = value.replace(/\s+/g, ' ').trim()
  if (normalized.length <= maxLength) return normalized
  return `${normalized.slice(0, maxLength - 1)}…`
}

function RunLedger({ runs, selectedRunId }: { runs: RunWorkbenchResponse['runs']['items']; selectedRunId: string }) {
  return (
    <div className="agentRunTapeRows">
      {runs.map((run) => {
        const activeRole = currentAgentRole(run)
        return (
          <Link className={`agentRunRow ${run.run_id === selectedRunId ? 'agentRunRowActive' : ''}`} href={`/runs/${run.run_id}`} key={run.run_id}>
            <span className={`agentStatusLamp agentStatus-${run.status}`} aria-hidden />
            <div className="agentRunIdentity">
              <strong>{run.stock_name && run.stock_name !== run.stock_code ? `${run.stock_name}（${run.stock_code}）` : run.stock_code}</strong>
              <em>{formatRunStatus(run.status)} · {run.owner || '未分配'} · 尝试 {run.observability.attempts}/{run.observability.max_attempts}</em>
            </div>
            <div className="agentRunSignal">
              <strong>{activeRole}</strong>
              <span>{run.last_event ? formatRunEvent(run.last_event) : compactText(run.detail, 64) || '等待调度'}</span>
              {run.error ? <em>{compactText(run.error, 72)}</em> : null}
            </div>
            <div className="agentRunEvidence">
              <span>角色 {run.multi_agent_trace?.completed_role_count || 0}/{run.multi_agent_trace?.role_count || 0}</span>
              <span>引用 {formatPct(run.run_metrics.citation_coverage_rate)}</span>
              <span>导出 {run.exports.length}</span>
            </div>
            <time>{run.updated_at || run.created_at || '暂无时间'}</time>
          </Link>
        )
      })}
      {!runs.length ? <EmptyState title="暂无任务" description="创建研报任务后，会在这里以 Agent 任务流水展示状态、角色进度和交付物。" /> : null}
    </div>
  )
}

function currentAgentRole(run: AnalysisRunResponse) {
  const roles = run.multi_agent_trace?.roles || []
  const failed = roles.find((role) => role.status === 'failed')
  if (failed) return `${formatAgentRoleName(failed.role_name || failed.role_id)} 异常`
  const active = roles.find((role) => role.status !== 'completed' && role.status !== 'degraded')
  if (active) return `${formatAgentRoleName(active.role_name || active.role_id)} 处理中`
  const last = roles[roles.length - 1]
  if (last) return `${formatAgentRoleName(last.role_name || last.role_id)} 已完成`
  if (run.status === 'queued') return '等待多智能体领取'
  if (run.status === 'running') return '多智能体研究中'
  if (run.status === 'completed') return '研报交付完成'
  if (run.status === 'failed') return '任务失败待处理'
  return '任务状态同步中'
}

function agentNodes(run: AnalysisRunResponse) {
  const roles = run.multi_agent_trace?.roles || []
  return roles.slice(0, 7).map((role) => ({
    id: role.role_id,
    label: formatAgentRoleName(role.role_name || role.role_id),
    status: role.fallback_used ? 'degraded' : role.status,
    detail: role.summary || (role.fallback_used ? '已启用降级策略' : '等待输出摘要'),
    metric: `${role.tool_call_count} 工具 / ${role.duration_s.toFixed(1)}s`,
  }))
}

function formatPct(value: number | undefined) {
  return `${(Number(value || 0) * 100).toFixed(0)}%`
}
