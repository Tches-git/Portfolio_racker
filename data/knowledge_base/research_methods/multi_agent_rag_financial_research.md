# 多 Agent + RAG 金融研究流程知识条目

## 来源
- AutoGen AgentChat 官方文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
- AutoGen GraphFlow 官方文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html
- FinanceBench 金融开放书问答基准：https://arxiv.org/abs/2311.11944

## 关键事实
- 多 Agent 适合将复杂金融研究拆成可审计的角色链路，例如计划、行情分析、基本面估值、事件解读、风险复核、报告写作和引用审计。
- 有向工作流比自由群聊更适合研报生成，因为它能固定角色顺序、约束工具边界、记录失败降级，并让 Trace 更容易复现。
- RAG 在金融场景中应服务于证据定位和来源覆盖，而不仅是给模型补背景；引用审计应在正式报告生成后检查核心观点是否有来源。
- 多 Agent 的价值不是让每个角色都“聊天”，而是通过输入契约、工具白名单、输出格式和质量检查降低幻觉和职责混乱。

## 投研关注点
- PlannerAgent：拆解研究问题，确定数据需求、角色顺序和风险点。
- MarketDataAgent：处理行情、趋势、成交活跃度和技术走势，不负责估值结论。
- FundamentalValuationAgent：处理财务质量、杜邦、DCF、可比估值和量化评分。
- EventAnalysisAgent：处理公告、新闻、政策、舆情和事件影响路径。
- RiskReviewAgent：检查数据缺口、异常值、降级状态、风险传导和反向证据。
- ReportWriterAgent：整合前序角色输出，生成结构化研报 brief。
- CitationAuditAgent：在报告生成后检查引用覆盖、来源数量和无来源观点。

## RAG 检索关键词
AutoGen, AgentChat, GraphFlow, 多智能体, 多 Agent, 金融研报, RAG, 引用审计, 工具白名单, 角色模板, 研究计划, 风险复核, 报告写作, Agent Trace

## 使用边界
- 第一阶段应优先保证有向流程稳定和可复现，不应过早引入自由协商式群聊。
- 每个 Agent 的输出都应进入 Trace，供前端展示和质量评测使用。
- RAG 检索结果只能作为证据候选，最终报告仍需经过风险复核和引用审计。
