import Link from 'next/link'

import { AgentFlowPanel, EvidenceMatrix } from '../../../components/big-screen/command-center'
import { ChartPanel, DonutChart } from '../../../components/big-screen/chart-panel'
import { RunActionControls } from '../../../components/run-action-controls'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchAnalysisRun, sameOriginApiUrl, stockCodeFromRun } from '../../../lib/api'
import {
  formatAgentRoleName,
  formatAgentRoleStatus,
  formatEventType,
  formatExportKind,
  formatImpactDirection,
  formatImpactLevel,
  formatImpactScope,
  formatPriority,
  formatRecoveryStatus,
  formatReviewStatus,
  formatRunEvent,
  formatRunStatus,
  formatSentiment,
  formatWorkflowMode,
} from '../../../lib/labels'
import { serverApiOptions } from '../../../lib/server-auth'
import type { MultiAgentRoleTrace } from '../../../lib/types'

export default async function RunDetailPage({ params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params
  const apiOptions = await serverApiOptions()
  const run = await fetchAnalysisRun(runId, apiOptions)
  const stockCode = stockCodeFromRun(run)
  const stockName = run.stock_name || run.event_context?.stock_name || ''
  const stockLabel = stockName && stockName !== stockCode ? `${stockName}（${stockCode}）` : stockCode
  const eventContext = run.event_context
  const hasEventContext = Boolean(eventContext?.event_id || eventContext?.title)
  const eventReportSummary = run.event_report_summary
  const hasEventReportSummary = Boolean(eventReportSummary?.trigger_label || eventReportSummary?.thesis)
  const multiAgentRoles = run.multi_agent_trace?.roles || []
  const preWriteRoles = multiAgentRoles.filter((role) => (role.phase || 'pre_write') !== 'post_write')
  const postWriteRoles = multiAgentRoles.filter((role) => (role.phase || 'pre_write') === 'post_write')
  const agentFlowNodes = multiAgentRoles.map((role) => ({
    id: role.role_id,
    label: formatAgentRoleName(role.role_name || role.role_id),
    status: role.fallback_used ? 'degraded' : role.status,
    detail: role.summary || (role.fallback_used ? '已启用降级策略' : '等待输出摘要'),
    metric: `${role.tool_call_count} 工具 / ${role.duration_s.toFixed(1)}s`,
  }))
  const roleStatusChart = [
    { label: '完成', value: run.multi_agent_trace?.completed_role_count || 0 },
    { label: '失败', value: run.multi_agent_trace?.failed_role_count || 0 },
    { label: '待补', value: Math.max(0, (run.multi_agent_trace?.role_count || 0) - (run.multi_agent_trace?.completed_role_count || 0) - (run.multi_agent_trace?.failed_role_count || 0)) },
  ]
  const runFacts = [
    { label: '状态', value: formatRunStatus(run.status) },
    { label: '耗时', value: `${run.run_metrics.duration_s.toFixed(1)}s` },
    { label: '工具调用', value: `${run.run_metrics.tool_calls}` },
    { label: '导出物', value: `${run.exports.length}` },
    { label: '阶段事件', value: `${run.events.length}` },
  ]
  const qualityFacts = [
    { label: '引用覆盖率', value: `${(run.run_metrics.citation_coverage_rate * 100).toFixed(1)}%` },
    { label: '来源数量', value: `${run.run_metrics.source_reference_count}` },
    { label: '无来源观点', value: `${run.run_metrics.unsupported_claim_count}` },
    { label: '检索命中率', value: `${(run.run_metrics.retrieval_topk_hit_rate * 100).toFixed(1)}%` },
    { label: 'Rerank 选中', value: `${run.run_metrics.rerank_selected_count}` },
  ]
  const operationFacts = [
    { label: '负责人', value: run.observability.owner_label },
    { label: '协作角色', value: formatAgentRoleName(run.owner_role) },
    { label: '审计动作', value: `${run.audit_events.length}` },
    { label: '恢复状态', value: formatRecoveryStatus(run.observability.recovery_status) },
    { label: '重试次数', value: `${run.observability.attempts}/${run.observability.max_attempts}` },
  ]

  return (
    <WorkspaceShell
      eyebrow="Agent 执行台"
      title={`${stockLabel} 多智能体研报任务`}
      description="把规划、行情分析、事件分析、风险复核、写作和引用审计串成一条可解释 Trace，证明研报不是黑箱生成。"
      className="runDossierPage"
      compact
      actions={[
        { label: '返回任务中心', href: '/runs', method: 'GET', action_type: 'navigate', target_id: run.run_id, variant: 'secondary' },
        { label: '单股情报中心', href: `/stocks/${stockCode}`, method: 'GET', action_type: 'navigate', target_id: stockCode, variant: 'secondary' },
      ]}
    >
      <section className="runDossierHero">
        <div className="runDossierSignal">
          <span>任务状态</span>
          <strong>{formatRunStatus(run.status)}</strong>
          <em>{run.detail || run.observability.latest_signal || '任务状态同步中'}</em>
        </div>
        <div className="runDossierTicker">
          {runFacts.map((item) => (
            <div key={item.label}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="runCommandVisual">
        <div className="runCommandFlow">
          <div className="runDossierSectionHead">
            <div>
              <span>AGENT FLOW</span>
              <h2>图形化多智能体链路</h2>
            </div>
            <em>完成 {run.multi_agent_trace?.completed_role_count || 0}/{run.multi_agent_trace?.role_count || 0}</em>
          </div>
          <AgentFlowPanel nodes={agentFlowNodes} emptyLabel="该任务尚未写入多智能体 Trace。" />
        </div>
        <ChartPanel eyebrow="ROLE STATE" title="角色状态">
          <DonutChart data={roleStatusChart} emptyLabel="暂无角色状态" />
        </ChartPanel>
        <EvidenceMatrix items={[
          { label: '引用覆盖', value: `${(run.run_metrics.citation_coverage_rate * 100).toFixed(1)}%`, tone: 'info' },
          { label: '来源数量', value: run.run_metrics.source_reference_count, tone: 'success' },
          { label: '无来源观点', value: run.run_metrics.unsupported_claim_count, tone: run.run_metrics.unsupported_claim_count ? 'warning' : 'neutral' },
          { label: '检索命中', value: `${(run.run_metrics.retrieval_topk_hit_rate * 100).toFixed(1)}%`, tone: 'agent' },
        ]} />
      </section>

      <div className="runDossierLayout">
        <main className="runDossierMain">
          <section className="runDossierSection">
            <div className="runDossierSectionHead">
              <div>
                <span>MULTI AGENT TRACE</span>
                <h2>多角色协作证据链</h2>
              </div>
              <em>{formatWorkflowMode(run.multi_agent_trace?.mode || 'autogen_graphflow')} · 完成 {run.multi_agent_trace?.completed_role_count || 0}/{run.multi_agent_trace?.role_count || 0}</em>
            </div>
            {multiAgentRoles.length ? (
              <div className="runAgentPhaseStack">
                <AgentPhaseBlock
                  title="研究前置链路"
                  description="正式写作前完成问题拆解、行情、估值、事件、风险与写作 brief。"
                  roles={preWriteRoles}
                  offset={0}
                  stockLabel={stockLabel}
                  hasEventContext={hasEventContext}
                />
                <AgentPhaseBlock
                  title="报告后置审计"
                  description="RAG 正式生成研报后，再检查引用覆盖、来源数量与无来源观点。"
                  roles={postWriteRoles}
                  offset={preWriteRoles.length}
                  stockLabel={stockLabel}
                  hasEventContext={hasEventContext}
                />
              </div>
            ) : (
              <div className="runDossierEmpty">该任务暂未记录多智能体执行链路，可能是旧版本任务或任务尚未进入研究阶段。</div>
            )}
          </section>

          {hasEventContext ? (
            <section className="runDossierSection">
              <div className="runDossierSectionHead">
                <div>
                  <span>触发事件</span>
                  <h2>事件上下文</h2>
                </div>
                {eventContext.event_id ? <Link className="wbTextButton" href={`/events/${eventContext.event_id}`}>查看事件详情</Link> : null}
              </div>
              <div className="runEventBrief">
                <div className="runEventNarrative">
                  <strong>{eventContext.title || '事件触发研报'}</strong>
                  <em>{eventContext.stock_name || stockLabel} · {eventContext.source || eventContext.provider || '本地事件源'} · {eventContext.published_at || '时间待补齐'}</em>
                  <p>{eventContext.summary || eventContext.reason || '该任务由事件流触发，研报会优先回应事件影响路径。'}</p>
                </div>
                <dl className="runInlineFacts">
                  <div><dt>事件类型</dt><dd>{formatEventType(eventContext.event_type)}</dd></div>
                  <div><dt>影响等级</dt><dd>{formatImpactLevel(eventContext.impact_level)}</dd></div>
                  <div><dt>情绪方向</dt><dd>{formatSentiment(eventContext.sentiment)}</dd></div>
                  <div><dt>影响范围</dt><dd>{formatImpactScope(eventContext.impact_scope)}</dd></div>
                  <div><dt>置信度</dt><dd>{eventContext.confidence ? `${Math.round(eventContext.confidence * 100)}%` : '--'}</dd></div>
                </dl>
              </div>

              {hasEventReportSummary ? (
                <div className="runThesisLine">
                  <div>
                    <span>事件驱动研报摘要</span>
                    <strong>{eventReportSummary.thesis || '事件驱动摘要等待研报完成后回流。'}</strong>
                  </div>
                  <dl>
                    <div><dt>方向</dt><dd>{formatImpactDirection(eventReportSummary.impact_direction)}</dd></div>
                    <div><dt>等级</dt><dd>{formatImpactLevel(eventReportSummary.impact_level)}</dd></div>
                    <div><dt>范围</dt><dd>{formatImpactScope(eventReportSummary.impact_scope)}</dd></div>
                    <div><dt>优先级</dt><dd>{formatPriority(eventReportSummary.priority)}</dd></div>
                    <div><dt>复核</dt><dd>{formatReviewStatus(eventReportSummary.review_status)}</dd></div>
                  </dl>
                  {eventReportSummary.report_delta_hint ? <p>{eventReportSummary.report_delta_hint}</p> : null}
                  {eventReportSummary.event_commentary_url ? <a className="wbTextButton" href={sameOriginApiUrl(eventReportSummary.event_commentary_url)} target="_blank" rel="noreferrer">查看事件点评导出</a> : null}
                </div>
              ) : null}
            </section>
          ) : null}

          <section className="runDossierSection">
            <div className="runDossierSectionHead">
              <div>
                <span>阶段事件</span>
                <h2>运行时间线</h2>
              </div>
              <em>{run.events.length} 条阶段记录</em>
            </div>
            <div className="runEventTimeline">
              {run.events.length ? run.events.map((event, index) => (
                <div className="runTimelineRow" key={`${event.timestamp}-${index}`}>
                  <time>{event.timestamp || '--'}</time>
                  <div>
                    <strong>{formatRunEvent(event.event)}</strong>
                    <span>{formatRunStatus(event.status)}</span>
                    <p>{event.detail || '暂无事件描述'}</p>
                  </div>
                </div>
              )) : <div className="runDossierEmpty">暂无阶段事件。</div>}
            </div>
          </section>

          <section className="runDossierSection">
            <div className="runDossierSectionHead">
              <div>
                <span>审计记录</span>
                <h2>协作审计</h2>
              </div>
              <em>{run.audit_events.length} 条动作</em>
            </div>
            <div className="runAuditList">
              {run.audit_events.length ? run.audit_events.slice().reverse().map((item, index) => (
                <div className="runAuditRow" key={`${item.timestamp}-${index}`}>
                  <strong>{formatRunEvent(item.action)}</strong>
                  <span>{formatAgentRoleName(item.actor)} · {formatAgentRoleName(item.role)} · {item.timestamp}</span>
                  <p>{item.detail}</p>
                </div>
              )) : <div className="runDossierEmpty">暂无审计动作。</div>}
            </div>
          </section>
        </main>

        <aside className="runDossierDock">
          <section className="runDockBlock">
            <span>下一步动作</span>
            <h2>{run.actions.suggested_next_action}</h2>
            <p>{run.observability.has_error ? '当前任务存在异常信号，建议先查看错误或重试。' : '任务状态正常，可继续查看交付、产品页或历史脉络。'}</p>
            <div className="runDockActions">
              <Link className="wbTextButton" href={run.actions.product_route || `/stocks/${stockCode}`}>产品页</Link>
              <Link className="wbTextButton" href={run.actions.history_route || `/stocks/${stockCode}/history`}>历史脉络</Link>
              <Link className="wbTextButton" href={run.actions.exports_route || `/stocks/${stockCode}/exports`}>导出中心</Link>
            </div>
            <RunActionControls run={run} />
          </section>

          <section className="runDockBlock">
            <span>为什么可信</span>
            <h2>引用与审计</h2>
            <p>用来源覆盖、检索命中和无来源观点数量约束生成内容，避免研报只停留在“看起来像”。</p>
            <div className="runDockMetricList">
              {qualityFacts.map((item) => (
                <div key={item.label}>
                  <em>{item.label}</em>
                  <strong>{item.value}</strong>
                </div>
              ))}
            </div>
          </section>

          <section className="runDockBlock">
            <span>运行治理</span>
            <div className="runDockMetricList">
              {operationFacts.map((item) => (
                <div key={item.label}>
                  <em>{item.label}</em>
                  <strong>{item.value}</strong>
                </div>
              ))}
            </div>
            <p>重试链路：{run.observability.retry_lineage || '原始任务'} · 执行器 {run.observability.worker_id || '--'} · 中断 {run.observability.stale_after_restart ? '是' : '否'}</p>
          </section>

          <section className="runDockBlock">
            <span>导出物</span>
            <div className="runExportList">
              {run.exports.length ? run.exports.map((item) => (
                <div className="runExportItem" key={item.filename}>
                  <strong>{formatExportKind(item.kind)}</strong>
                  <em>{item.filename}</em>
                  <span>
                    <a href={sameOriginApiUrl(previewExportUrl(item.download_url))} target="_blank" rel="noreferrer">预览</a>
                    <a href={sameOriginApiUrl(item.download_url)} target="_blank" rel="noreferrer">下载</a>
                  </span>
                </div>
              )) : <p>当前运行尚未产出导出物。</p>}
            </div>
          </section>
        </aside>
      </div>
    </WorkspaceShell>
  )
}

function AgentPhaseBlock({
  title,
  description,
  roles,
  offset,
  stockLabel,
  hasEventContext,
}: {
  title: string
  description: string
  roles: MultiAgentRoleTrace[]
  offset: number
  stockLabel: string
  hasEventContext: boolean
}) {
  if (!roles.length) {
    return (
      <div className="runAgentPhaseBlock">
        <div className="runAgentPhaseHead">
          <div>
            <strong>{title}</strong>
            <span>{description}</span>
          </div>
          <em>暂无记录</em>
        </div>
        <div className="runDossierEmpty">该阶段暂无 Trace，可能是旧任务或任务尚未执行到该阶段。</div>
      </div>
    )
  }
  return (
    <div className="runAgentPhaseBlock">
      <div className="runAgentPhaseHead">
        <div>
          <strong>{title}</strong>
          <span>{description}</span>
        </div>
        <em>{roles.length} 个角色</em>
      </div>
      <ol className="runAgentRail">
        {roles.map((role, index) => (
          <li key={`${role.phase || 'pre_write'}-${role.role_id}`}>
            <div className="runAgentIndex">{String(offset + index + 1).padStart(2, '0')}</div>
            <div>
              <div className="runAgentTitle">
                <strong>{formatAgentRoleName(role.role_name || role.role_id)}</strong>
                <span>{formatAgentRoleStatus(role.status)} · 工具 {role.tool_call_count} 次 · {role.duration_s.toFixed(2)} 秒</span>
              </div>
              <dl className="runAgentEvidence">
                <div><dt>职责目标</dt><dd>{role.objective || roleMission(role.role_id || role.role_name)}</dd></div>
                <div><dt>输入摘要</dt><dd>{role.input_summary || roleInput(role.role_id || role.role_name, stockLabel, hasEventContext)}</dd></div>
                <div><dt>工具边界</dt><dd>{formatToolBoundary(role.allowed_tools)}</dd></div>
                <div><dt>质量检查</dt><dd>{formatQualityChecks(role.quality_checks)}</dd></div>
                <div><dt>输出证据</dt><dd>{role.summary || '该角色暂无输出摘要。'}</dd></div>
              </dl>
              {role.fallback_used ? <small>已启用降级：优先使用已有上下文和结构化数据。</small> : null}
              {role.error ? <small className="tone-danger">异常：{role.error}</small> : null}
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}

function roleMission(value: string) {
  const key = value.toLowerCase().replace(/[\s-]+/g, '_')
  if (key.includes('planner')) return '拆解研究目标，确定研究顺序、关键变量和角色分工。'
  if (key.includes('market')) return '检查行情、交易活跃度和趋势走势，形成市场状态判断。'
  if (key.includes('fundamental') || key.includes('valuation')) return '检查财务质量、估值区间和量化评分，形成基本面证据。'
  if (key.includes('event')) return '阅读公告、新闻和触发事件，判断事件对研究结论的影响。'
  if (key.includes('risk')) return '复核风险、缺失数据、异常信号和降级状态。'
  if (key.includes('writer')) return '整合前序角色输出，形成研报写作 brief 和正文组织。'
  if (key.includes('citation')) return '审计引用覆盖、来源数量和无来源观点。'
  return '参与研报生成链路，输出阶段性研究证据。'
}

function roleInput(value: string, stockLabel: string, hasEventContext: boolean) {
  const key = value.toLowerCase().replace(/[\s-]+/g, '_')
  if (key.includes('planner')) return `${stockLabel} 的研究目标、任务类型和可用数据清单。`
  if (key.includes('market')) return '实时行情、历史走势、交易活跃度和趋势工具结果。'
  if (key.includes('fundamental') || key.includes('valuation')) return '公司画像、财务指标、同行公司、估值模型和评分工具结果。'
  if (key.includes('event')) return hasEventContext ? '触发事件、相关新闻、公告和来源证据。' : '新闻、公告、研报观点和市场消息。'
  if (key.includes('risk')) return '前序分析结论、数据缺口、异常信号和风险条目。'
  if (key.includes('writer')) return '规划、行情分析、事件分析和风险复核输出。'
  if (key.includes('citation')) return '研报正文、RAG 来源列表和引用审计规则。'
  return '当前任务上下文和已有结构化研究结果。'
}

function formatToolBoundary(tools?: string[]) {
  if (!tools?.length) return '不调用工具，仅整合上下文。'
  const toolLabels: Record<string, string> = {
    trend_analysis: '趋势分析',
    dupont_analysis: '杜邦分析',
    dcf_valuation: 'DCF 估值',
    comparable_valuation: '可比估值',
    quantitative_scoring: '量化评分',
    risk_assessment: '风险评估',
  }
  return tools.map((tool) => toolLabels[tool] || tool.replace(/_/g, ' ')).join(' / ')
}

function formatQualityChecks(checks?: string[]) {
  if (!checks?.length) return '按角色职责做一致性与降级检查。'
  return checks.join('；')
}

function previewExportUrl(downloadUrl: string) {
  const normalized = downloadUrl || ''
  return normalized.endsWith('/preview') ? normalized : `${normalized}/preview`
}
