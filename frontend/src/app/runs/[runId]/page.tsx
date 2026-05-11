import Link from 'next/link'

import { RunActionControls } from '../../../components/run-action-controls'
import { RunStatusBar } from '../../../components/run-status-bar'
import { API_BASE, fetchAnalysisRun, stockCodeFromRun } from '../../../lib/api'

export default async function RunDetailPage({ params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params
  const run = await fetchAnalysisRun(runId)
  const stockCode = stockCodeFromRun(run)
  const hasData = run.status === 'completed'
  const eventContext = run.event_context
  const hasEventContext = Boolean(eventContext?.event_id || eventContext?.title)
  const eventReportSummary = run.event_report_summary
  const hasEventReportSummary = Boolean(eventReportSummary?.trigger_label || eventReportSummary?.thesis)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Run Detail · Task Center</div>
            <h1>{stockCode} 运行任务中心</h1>
            <p>把浏览器触发分析进一步沉淀成独立任务页，统一承接任务状态、阶段事件、导出物与后续跳转入口。</p>
          </div>
          <Link className="ghostLink" href={`/stocks/${stockCode}`}>返回产品页</Link>
        </div>
      </section>

      <RunStatusBar stockCode={stockCode} hasData={hasData} statusHint="任务中心会展示运行事件、导出物和下一步动作。" />

      <div className="grid">
        {hasEventContext ? (
          <section className="panel span-12">
            <div className="sectionHead">
              <div>
                <div className="sectionEyebrow">Trigger Event</div>
                <h2>触发事件上下文</h2>
              </div>
              {eventContext.event_id ? <Link className="ghostLink" href={`/events/${eventContext.event_id}`}>查看事件详情</Link> : null}
            </div>
            <div className="detailGrid">
              <div className="card">
                <div className="itemTitle">{eventContext.title || '事件触发研报'}</div>
                <div className="itemMeta">{eventContext.stock_name || stockCode} · {eventContext.source || eventContext.provider || '本地事件源'} · {eventContext.published_at || '时间待补齐'}</div>
                <p className="bodyText">{eventContext.summary || eventContext.reason || '该任务由事件流触发，研报会优先回应事件影响路径。'}</p>
              </div>
              <div className="card">
                <div className="itemTitle">影响判断</div>
                <div className="metricStack">
                  <div className="metricRow"><span>事件类型</span><strong>{eventContext.event_type || '--'}</strong></div>
                  <div className="metricRow"><span>影响等级</span><strong>{eventContext.impact_level || '--'}</strong></div>
                  <div className="metricRow"><span>情绪方向</span><strong>{eventContext.sentiment || '--'}</strong></div>
                  <div className="metricRow"><span>影响范围</span><strong>{eventContext.impact_scope || '--'}</strong></div>
                  <div className="metricRow"><span>置信度</span><strong>{eventContext.confidence ? `${Math.round(eventContext.confidence * 100)}%` : '--'}</strong></div>
                </div>
              </div>
              <div className="card">
                <div className="itemTitle">研究动作</div>
                <p className="bodyText">{eventContext.note || '研报生成时会带入标题、摘要、来源、影响等级与建议动作，用于更新投资要点、风险传导和后续跟踪指标。'}</p>
                <div className="actionList">
                  {eventContext.url ? <a className="downloadLink" href={eventContext.url} target="_blank" rel="noreferrer">打开原始来源</a> : null}
                  {eventContext.event_id ? <Link className="downloadLink" href={`/events/${eventContext.event_id}`}>回到事件流</Link> : null}
                </div>
              </div>
              {hasEventReportSummary ? (
                <div className="card">
                  <div className="itemTitle">事件驱动研报摘要卡</div>
                  <p className="bodyText">{eventReportSummary.thesis || '事件驱动摘要等待研报完成后回流。'}</p>
                  <div className="metricStack">
                    <div className="metricRow"><span>影响方向</span><strong>{eventReportSummary.impact_direction || '--'}</strong></div>
                    <div className="metricRow"><span>优先级</span><strong>{eventReportSummary.priority || '--'}</strong></div>
                    <div className="metricRow"><span>处理状态</span><strong>{eventReportSummary.review_status || '--'}</strong></div>
                    <div className="metricRow"><span>来源数量</span><strong>{eventReportSummary.related_source_count}</strong></div>
                  </div>
                  {eventReportSummary.report_delta_hint ? <div className="pathText">{eventReportSummary.report_delta_hint}</div> : null}
                  <div className="actionList">
                    {eventReportSummary.event_commentary_url ? <a className="downloadLink" href={`${API_BASE}${eventReportSummary.event_commentary_url}`} target="_blank" rel="noreferrer">查看事件点评导出</a> : null}
                  </div>
                </div>
              ) : null}
            </div>
          </section>
        ) : null}

        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Run Overview</div>
              <h2>任务概览</h2>
            </div>
          </div>
          <div className="detailGrid">
            <div className="card">
              <div className="itemTitle">基础信息</div>
              <div className="metricStack">
                <div className="metricRow"><span>任务 ID</span><strong>{run.run_id}</strong></div>
                <div className="metricRow"><span>股票代码</span><strong>{run.stock_code}</strong></div>
                <div className="metricRow"><span>当前状态</span><strong>{run.status}</strong></div>
                <div className="metricRow"><span>负责人</span><strong>{run.observability.owner_label}</strong></div>
                <div className="metricRow"><span>协作角色</span><strong>{run.owner_role || '--'}</strong></div>
                <div className="metricRow"><span>审计动作</span><strong>{run.audit_events.length}</strong></div>
                <div className="metricRow"><span>最近事件</span><strong>{run.observability.latest_signal || '--'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">运行指标</div>
              <div className="metricStack">
                <div className="metricRow"><span>耗时</span><strong>{run.run_metrics.duration_s.toFixed(1)}s</strong></div>
                <div className="metricRow"><span>LLM 调用</span><strong>{run.run_metrics.llm_calls}</strong></div>
                <div className="metricRow"><span>工具调用</span><strong>{run.run_metrics.tool_calls}</strong></div>
                <div className="metricRow"><span>总 Tokens</span><strong>{run.run_metrics.total_tokens}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">任务路径</div>
              <div className="metricStack">
                <div className="metricRow"><span>时间线条数</span><strong>{run.observability.event_count}</strong></div>
                <div className="metricRow"><span>导出物数量</span><strong>{run.observability.artifact_count}</strong></div>
                <div className="metricRow"><span>结果回流</span><strong>{run.status === 'completed' ? '可进入产品页' : '等待完成'}</strong></div>
                <div className="metricRow"><span>归档状态</span><strong>{run.observability.archive_label}</strong></div>
                <div className="metricRow"><span>运行治理</span><strong>{run.actions.suggested_next_action}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">后续动作</div>
              <div className="actionList">
                <Link className="downloadLink" href={run.actions.product_route || `/stocks/${stockCode}`}>查看产品页</Link>
                <Link className="downloadLink" href={run.actions.history_route || `/stocks/${stockCode}/history`}>查看历史脉络</Link>
                <Link className="downloadLink" href={run.actions.exports_route || `/stocks/${stockCode}/exports`}>查看导出中心</Link>
                <Link className="downloadLink" href="/runs">返回任务中心</Link>
              </div>
              <RunActionControls run={run} />
            </div>
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Artifacts</div>
              <h2>导出物</h2>
            </div>
          </div>
          <div className="statusBar compactStatusBar detailStatusBar">
            <div>
              <div className="statusLabel">动作建议</div>
              <div className="statusValue">{run.actions.suggested_next_action}</div>
            </div>
            <div>
              <div className="statusLabel">异常信号</div>
              <div className="statusValue">{run.observability.has_error ? '需处理' : '正常'}</div>
            </div>
            <div>
              <div className="statusLabel">重试链路</div>
              <div className="statusHint">{run.observability.retry_lineage || '原始任务'} · 尝试 {run.observability.attempts}/{run.observability.max_attempts} · Worker {run.observability.worker_id || '--'} · 恢复状态 {run.observability.recovery_status} · 中断 {run.observability.stale_after_restart ? '是' : '否'}</div>
            </div>
          </div>
          <div className="list">
            {run.exports.length ? run.exports.map((item) => (
              <div className="card" key={item.filename}>
                <div className="itemTitle">{item.kind}</div>
                <div className="itemMeta">{item.filename}</div>
                <div className="inlineMeta">复用统一导出 contract：{item.download_url}</div>
                <a className="downloadLink" href={`${API_BASE}${item.download_url}`} target="_blank" rel="noreferrer">下载 / 查看</a>
              </div>
            )) : <div className="card">当前运行尚未产出导出物。</div>}
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Audit Trail</div>
              <h2>协作审计</h2>
            </div>
          </div>
          <div className="detailGrid">
            {run.audit_events.length ? run.audit_events.slice().reverse().map((item, index) => (
              <div className="card" key={`${item.timestamp}-${index}`}>
                <div className="itemTitle">{item.action}</div>
                <div className="itemMeta">{item.actor} · {item.role} · {item.timestamp}</div>
                <p className="bodyText">{item.detail}</p>
              </div>
            )) : <div className="card">暂无审计动作。</div>}
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Event Timeline</div>
              <h2>阶段事件时间线</h2>
            </div>
          </div>
          {run.events.length ? (
            <div className="timelineSummary">
              <div className="card">
                <div className="itemTitle">起始阶段</div>
                <div className="itemMeta">{run.events[0]?.event || '--'}</div>
                <p className="bodyText">{run.events[0]?.detail || '暂无描述'}</p>
              </div>
              <div className="card">
                <div className="itemTitle">最新阶段</div>
                <div className="itemMeta">{run.events[run.events.length - 1]?.event || '--'}</div>
                <p className="bodyText">{run.events[run.events.length - 1]?.detail || '暂无描述'}</p>
              </div>
            </div>
          ) : null}
          <div className="timelineList">
            {run.events.length ? run.events.map((event, index) => (
              <div className="timelineCard" key={`${event.timestamp}-${index}`}>
                <div className="timelineDot" />
                <div className="card timelineBody">
                  <div className="itemTitle">{event.timestamp || '--'} · {event.event || '--'}</div>
                  <div className="itemMeta">状态：{event.status || '--'}</div>
                  <p>{event.detail || '暂无事件描述'}</p>
                </div>
              </div>
            )) : <div className="card">暂无阶段事件。</div>}
          </div>
        </section>
      </div>
    </main>
  )
}
