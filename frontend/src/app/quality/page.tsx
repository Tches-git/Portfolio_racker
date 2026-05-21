import Link from 'next/link'

import { EvidenceMatrix } from '../../components/big-screen/command-center'
import { BarPulseChart, ChartPanel, DonutChart } from '../../components/big-screen/chart-panel'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchQualityWorkbench } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

export default async function QualityPage() {
  const apiOptions = await serverApiOptions()
  const data = await fetchQualityWorkbench(apiOptions)
  const agent = data.agent_eval
  const rag = data.rag_eval
  const tracking = data.tracking_eval
  const financialQa = data.financial_qa_eval
  const agentEvidence = [
    { label: '成功率', value: pctValue(agent.task_success_rate) },
    { label: '工具覆盖', value: pctValue(agent.required_tool_coverage) },
    { label: 'Trace', value: pctValue(agent.trace_completeness_rate) },
    { label: '角色覆盖', value: pctValue(agent.multi_agent_role_coverage_rate) },
  ]
  const qaEvidence = [
    { label: '精确匹配', value: pctValue(financialQa.answer_exact_match) },
    { label: '关键命中', value: pctValue(financialQa.answer_key_hit_rate) },
    { label: '词元 F1', value: pctValue(financialQa.answer_token_f1) },
    { label: '引用覆盖', value: pctValue(financialQa.citation_coverage_rate) },
  ]

  const headline = [
    { label: '自动化测试', value: String(data.test_count || 0), hint: '后端与前端构建门禁' },
    { label: 'Agent 样本', value: String(numberOf(agent.sample_count)), hint: '项目内任务评测' },
    { label: '角色覆盖', value: formatScalar(agent.multi_agent_role_coverage_rate), hint: '六角色链路完整性' },
    { label: 'RAG 引用', value: formatScalar(rag.citation_coverage_rate), hint: '来源覆盖约束' },
  ]

  return (
    <WorkspaceShell
      eyebrow="项目质量指标"
      title="Agent 可信度报告"
      description="用可复现评测、任务 Trace、引用审计和运行治理证明：这个项目不是只会生成文本，而是能解释研究过程。"
      className="qualityReportPage"
      compact
    >
      <div className="credibilityReport">
        <section className="credibilityHero">
          <div>
            <span>INTERVIEW EVIDENCE</span>
            <h2>面向大模型 Agent 岗位的项目证据链</h2>
            <p>核心展示顺序：多角色协作是否完整、工具是否覆盖关键步骤、报告是否有来源、异常是否能降级、结果是否可复现。</p>
          </div>
          <div className="credibilityHeroActions">
            <Link href="/runs">查看 Agent 任务</Link>
            <Link href="/events?view=alerts">查看事件预警</Link>
          </div>
        </section>

        <section className="credibilityTicker" aria-label="可信度总览">
          {headline.map((item) => (
            <div key={item.label}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
              <em>{item.hint}</em>
            </div>
          ))}
        </section>

        <section className="credibilityCommandGrid">
          <ChartPanel eyebrow="AGENT SCORE" title="Agent 任务证据">
            <BarPulseChart data={agentEvidence} emptyLabel="暂无 Agent 评测" />
          </ChartPanel>
          <ChartPanel eyebrow="RAG AUDIT" title="引用审计结构">
            <DonutChart data={[
              { label: '有来源', value: Math.round(numberOf(rag.citation_coverage_rate) * 100) },
              { label: '无来源', value: numberOf(rag.unsupported_claim_count) },
              { label: '来源数', value: numberOf(rag.source_reference_count) },
            ]} emptyLabel="暂无 RAG 评测" />
          </ChartPanel>
          <ChartPanel eyebrow="PUBLIC QA" title="公共金融 QA">
            <BarPulseChart data={qaEvidence} emptyLabel="暂无公共 benchmark" />
          </ChartPanel>
          <EvidenceMatrix items={[
            { label: '事件样本', value: numberOf(tracking.sample_count), hint: 'Tracking benchmark', tone: 'info' },
            { label: '测试数量', value: data.test_count || 0, hint: '工程门禁', tone: 'success' },
            { label: '失败率', value: formatScalar(data.run_metrics.failure_rate), hint: '运行治理', tone: data.run_metrics.failure_rate ? 'warning' : 'neutral' },
            { label: '冒烟状态', value: data.smoke_status || '待验证', hint: '本地 / 服务器', tone: 'agent' },
          ]} />
        </section>

        <section className="credibilityBody">
          <main className="credibilityEvidenceTape">
            <EvidenceBlock
              eyebrow="MULTI AGENT"
              title="多角色 Agent 协作"
              summary="验证任务是否被拆解为规划、行情、事件、风险、写作和引用审计，而不是单轮 prompt 直接出报告。"
              facts={[
                ['样本数', String(numberOf(agent.sample_count))],
                ['任务成功率', formatScalar(agent.task_success_rate)],
                ['工具覆盖率', formatScalar(agent.required_tool_coverage)],
                ['Trace 完整率', formatScalar(agent.trace_completeness_rate)],
                ['角色覆盖率', formatScalar(agent.multi_agent_role_coverage_rate)],
                ['降级成功率', formatScalar(agent.fallback_success_rate)],
              ]}
              empty={!numberOf(agent.sample_count)}
              emptyText="尚未生成智能体任务评测。运行 python main.py agent-eval 后会展示最新指标。"
            />

            <EvidenceBlock
              eyebrow="RAG AUDIT"
              title="RAG 引用可信度"
              summary="验证生成报告中的观点是否有来源支撑，降低无来源判断和幻觉式结论。"
              facts={[
                ['引用覆盖率', formatScalar(rag.citation_coverage_rate)],
                ['无来源观点', String(numberOf(rag.unsupported_claim_count))],
                ['来源数量', String(numberOf(rag.source_reference_count))],
                ['检索命中率', formatScalar(rag.retrieval_topk_hit_rate)],
                ['Rerank 选中', String(numberOf(rag.rerank_selected_count))],
              ]}
              empty={!rag.generated_at}
              emptyText="尚未生成 RAG 可信度评测。运行 python main.py rag-eval --stock-code <股票代码> 后会展示。"
            />

            <EvidenceBlock
              eyebrow="EVENT BENCHMARK"
              title="金融事件处理评测"
              summary="验证事件采集后能否完成去重、分类、影响评估和预警命中，是研报前置研究信号的质量门禁。"
              facts={[
                ['样本数', String(numberOf(tracking.sample_count))],
                ['去重 F1', formatMetric(tracking, 'dedupe', 'f1')],
                ['分类 Macro-F1', formatScalar(tracking.event_type_macro_f1)],
                ['高影响识别', formatMetric(tracking, 'high_impact', 'f1')],
                ['预警 F1', formatMetric(tracking, 'alert', 'f1')],
              ]}
              empty={!numberOf(tracking.sample_count)}
              emptyText="尚未生成事件评测结果。运行 python main.py tracking-eval 后会展示。"
            />

            <EvidenceBlock
              eyebrow="PUBLIC BENCHMARK"
              title="公共金融 QA / 检索增强"
              summary="用 FinanceBench、FinQA 或 TAT-QA 本地子集验证检索和答案命中，不把项目指标完全建立在自造样本上。"
              facts={[
                ['样本数', String(numberOf(financialQa.sample_count))],
                ['预测数', String(numberOf(financialQa.prediction_count))],
                ['精确匹配', formatScalar(financialQa.answer_exact_match)],
                ['关键答案命中', formatScalar(financialQa.answer_key_hit_rate)],
                ['词元 F1', formatScalar(financialQa.answer_token_f1)],
                ['上下文命中', formatScalar(financialQa.context_answer_hit_rate)],
                ['引用覆盖', formatScalar(financialQa.citation_coverage_rate)],
              ]}
              empty={!financialQa.generated_at}
              emptyText="尚未生成公共金融基准评测。准备本地子集后运行 python main.py finance-qa-eval --benchmark <路径>。"
            />
          </main>

          <aside className="credibilityDock">
            <section>
              <span>演示状态</span>
              <h2>{data.smoke_status || '待验证'}</h2>
              <p>求职演示时建议先打开本页，再进入 Agent 任务详情页，形成“指标 → Trace → 报告”的讲述闭环。</p>
            </section>
            <section>
              <span>运行治理</span>
              <div className="credibilityDockFacts">
                <div><em>任务总数</em><strong>{data.run_metrics.total_runs}</strong></div>
                <div><em>活跃任务</em><strong>{data.run_metrics.active_runs}</strong></div>
                <div><em>失败率</em><strong>{formatScalar(data.run_metrics.failure_rate)}</strong></div>
                <div><em>平均耗时</em><strong>{formatSeconds(data.run_metrics.avg_duration_s)}</strong></div>
                <div><em>P95 耗时</em><strong>{formatSeconds(data.run_metrics.p95_duration_s)}</strong></div>
                <div><em>运维状态</em><strong>{data.run_metrics.ops_status || '未知'}</strong></div>
              </div>
            </section>
            <section>
              <span>简历口径</span>
              <p>AutoGen 多角色 Agent 工作流 + RAG 可信度评测 + 金融事件 benchmark + 多用户隔离工作台。</p>
            </section>
          </aside>
        </section>
      </div>
    </WorkspaceShell>
  )
}

function EvidenceBlock({
  eyebrow,
  title,
  summary,
  facts,
  empty,
  emptyText,
}: {
  eyebrow: string
  title: string
  summary: string
  facts: Array<[string, string]>
  empty: boolean
  emptyText: string
}) {
  return (
    <article className="evidenceBlock">
      <header>
        <span>{eyebrow}</span>
        <h2>{title}</h2>
        <p>{summary}</p>
      </header>
      <div className="evidenceFactLine">
        {facts.map(([label, value]) => (
          <div key={label}>
            <em>{label}</em>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
      {empty ? <div className="evidenceEmpty">{emptyText}</div> : null}
    </article>
  )
}

function numberOf(value: unknown) {
  return Number(value || 0)
}

function pctValue(value: unknown) {
  return Math.round(Number(value || 0) * 100)
}

function formatScalar(value: unknown) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`
}

function formatMetric(payload: Record<string, unknown>, section: string, key: string) {
  const value = (payload[section] as Record<string, unknown> | undefined)?.[key]
  return formatScalar(value)
}

function formatSeconds(value: unknown) {
  return `${Number(value || 0).toFixed(1)} 秒`
}
