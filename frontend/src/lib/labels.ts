type LabelMap = Record<string, string>

function keyOf(value: string) {
  return value.trim().toLowerCase().replace(/[\s-]+/g, '_')
}

function labelOf(value: string | null | undefined, labels: LabelMap, fallback = '--') {
  if (!value) return fallback
  const raw = String(value).trim()
  if (!raw) return fallback
  return labels[keyOf(raw)] || labels[raw] || raw
}

const impactLevelLabels: LabelMap = {
  high: '高',
  medium: '中',
  low: '低',
}

const eventTypeLabels: LabelMap = {
  filing: '公告披露',
  announcement: '公告',
  earnings: '业绩',
  regulation: '监管',
  industry_policy: '行业政策',
  market_move: '市场异动',
  broker_view: '研报观点',
  research_view: '研报观点',
  risk_sentiment: '风险舆情',
  shareholder: '股东变动',
  product_price: '产品价格',
  capacity_order: '产能订单',
  news: '新闻',
  other: '其他',
}

const sentimentLabels: LabelMap = {
  positive: '偏利好',
  negative: '偏利空',
  neutral: '中性',
  uncertain: '不确定',
  mixed: '多空交织',
}

const impactScopeLabels: LabelMap = {
  sentiment: '短期情绪',
  fundamentals: '基本面',
  valuation: '估值预期',
  industry: '行业景气',
  risk: '风险暴露',
  liquidity: '流动性',
  policy: '政策环境',
}

const impactDirectionLabels: LabelMap = {
  positive: '利好',
  negative: '利空',
  neutral: '中性',
  uncertain: '不确定',
  mixed: '多空交织',
  bullish: '利好',
  bearish: '利空',
  upside: '利好',
  downside: '利空',
}

const priorityLabels: LabelMap = {
  urgent: '紧急',
  critical: '最高',
  high: '高',
  medium: '中',
  normal: '普通',
  low: '低',
  p0: 'P0',
  p1: 'P1',
  p2: 'P2',
  p3: 'P3',
}

const reviewStatusLabels: LabelMap = {
  pending: '待复核',
  pending_review: '待复核',
  unreviewed: '待复核',
  reviewing: '复核中',
  reviewed: '已复核',
  completed: '已完成',
  done: '已完成',
  ignored: '已忽略',
  converted_to_report: '已转研报',
  escalated: '已升级处理',
}

const runStatusLabels: LabelMap = {
  pending: '待入队',
  queued: '排队中',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
  canceled: '已取消',
  cancelled: '已取消',
  archived: '已归档',
}

const eventStatusLabels: LabelMap = {
  new: '新事件',
  open: '待处理',
  pending: '待处理',
  reviewed: '已复核',
  ignored: '已忽略',
  converted_to_report: '已转研报',
  resolved: '已处理',
  closed: '已关闭',
}

const agentRoleLabels: LabelMap = {
  admin: '管理员',
  user: '普通用户',
  system: '系统',
  browser_user: '当前用户',
  research_owner: '研究负责人',
  planner: '研究规划智能体',
  planneragent: '研究规划智能体',
  planner_agent: '研究规划智能体',
  market_analyst: '行情智能体',
  marketanalyst: '行情智能体',
  market_data: '行情智能体',
  market_data_agent: '行情智能体',
  marketdataagent: '行情智能体',
  fundamental_valuation: '基本面估值智能体',
  fundamental_valuation_agent: '基本面估值智能体',
  fundamentalvaluationagent: '基本面估值智能体',
  event_analyst: '事件分析智能体',
  eventanalyst: '事件分析智能体',
  event_analysis_agent: '事件分析智能体',
  eventanalysisagent: '事件分析智能体',
  risk_reviewer: '风险复核智能体',
  riskreviewer: '风险复核智能体',
  risk_review_agent: '风险复核智能体',
  riskreviewagent: '风险复核智能体',
  report_writer: '研报写作智能体',
  reportwriter: '研报写作智能体',
  report_writer_agent: '研报写作智能体',
  reportwriteragent: '研报写作智能体',
  citation_auditor: '引用审计智能体',
  citationauditor: '引用审计智能体',
  citation_audit_agent: '引用审计智能体',
  citationauditagent: '引用审计智能体',
}

const workflowModeLabels: LabelMap = {
  autogen_graphflow: 'AutoGen 图式多智能体',
  autogen_graphflow_fallback: 'AutoGen 有向多智能体（本地降级）',
  autogen_agentchat: 'AutoGen 多智能体对话',
  multi_agent: '多智能体工作流',
  legacy_react: '旧版单智能体',
  legacy: '旧版链路',
}

const exportKindLabels: LabelMap = {
  report: '研报正文',
  research_report: '研报正文',
  report_markdown: '研报正文',
  markdown: 'Markdown 文档',
  pdf: 'PDF 文档',
  pdf_report: 'PDF 研报',
  event_commentary: '事件点评',
  presentation: '展示材料',
  slides: '展示材料',
  source_data: '来源数据',
  raw_data: '原始数据',
  run_log: '运行日志',
  logs: '运行日志',
  audit_log: '审计日志',
  json: '结构化数据',
  html: '网页文档',
}

const runEventLabels: LabelMap = {
  queued: '任务入队',
  started: '开始执行',
  running: '执行中',
  completed: '执行完成',
  failed: '执行失败',
  canceled: '任务取消',
  cancelled: '任务取消',
  event_analysis_requested: '事件触发分析',
  run_claimed: '任务已领取',
  run_started: '任务启动',
  run_completed: '任务完成',
  run_failed: '任务失败',
  run_canceled: '任务取消',
  run_retry_scheduled: '已安排重试',
  run_interrupted_after_restart: '重启后中断',
  create_run: '创建任务',
  event_analyze: '事件触发分析',
  assign_owner: '分配负责人',
  archive_run: '归档任务',
  cancel_run: '取消任务',
  retry_run: '重试任务',
  role_done: '角色完成',
  role_failed: '角色失败',
  retrying: '准备重试',
  recovered: '恢复执行',
  saved: '结果保存',
  exported: '导出完成',
}

const recoveryStatusLabels: LabelMap = {
  normal: '正常',
  recovered: '已恢复',
  stale: '疑似中断',
  unknown: '未知',
  failed: '恢复失败',
}

export function formatEventType(value: string | null | undefined) {
  return labelOf(value, eventTypeLabels)
}

export function formatImpactLevel(value: string | null | undefined) {
  return labelOf(value, impactLevelLabels)
}

export function formatAlertSeverity(value: string | null | undefined) {
  return formatImpactLevel(value)
}

export function formatSentiment(value: string | null | undefined) {
  return labelOf(value, sentimentLabels)
}

export function formatImpactScope(value: string | null | undefined) {
  return labelOf(value, impactScopeLabels)
}

export function formatImpactDirection(value: string | null | undefined) {
  return labelOf(value, impactDirectionLabels)
}

export function formatPriority(value: string | null | undefined) {
  return labelOf(value, priorityLabels)
}

export function formatReviewStatus(value: string | null | undefined) {
  return labelOf(value, reviewStatusLabels)
}

export function formatRunStatus(value: string | null | undefined) {
  return labelOf(value, runStatusLabels)
}

export function formatEventStatus(value: string | null | undefined) {
  return labelOf(value, eventStatusLabels)
}

export function formatAgentRoleName(value: string | null | undefined) {
  return labelOf(value, agentRoleLabels)
}

export function formatAgentRoleStatus(value: string | null | undefined) {
  if (value === 'degraded') return '已降级完成'
  if (value === 'skipped') return '已跳过'
  return formatRunStatus(value)
}

export function formatWorkflowMode(value: string | null | undefined) {
  return labelOf(value, workflowModeLabels)
}

export function formatExportKind(value: string | null | undefined) {
  return labelOf(value, exportKindLabels)
}

export function formatRunEvent(value: string | null | undefined) {
  return labelOf(value, runEventLabels)
}

export function formatRecoveryStatus(value: string | null | undefined) {
  return labelOf(value, recoveryStatusLabels)
}
