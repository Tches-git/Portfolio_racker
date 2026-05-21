# 金融 RAG 与 Agent 评测方法知识条目

## 来源
- FinanceBench: A New Benchmark for Financial Question Answering：https://arxiv.org/abs/2311.11944
- TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content in Finance：https://arxiv.org/abs/2105.07624
- FinQA: A Dataset of Numerical Reasoning over Financial Data：https://arxiv.org/abs/2109.00122

## 关键事实
- 金融问答不只是开放域检索，常常需要在公告、财报表格、管理层讨论、脚注和多期数据之间做证据定位与数值推理。
- FinanceBench 关注开放书金融问答，适合评估 RAG 系统能否从真实财务文件中找到证据并回答问题。
- TAT-QA 强调表格和文本混合证据，适合评估模型能否同时处理财务报表中的数值表格和解释性文本。
- FinQA 强调金融数值推理和可解释推理程序，适合评估模型是否能把财务问题拆成可检查的计算步骤。

## 投研关注点
- 检索指标：top-k 命中率、证据覆盖率、引用来源数量、无来源观点数量。
- 答案指标：答案正确性、数值计算正确性、拒答准确性、结论一致性。
- Agent 指标：工具调用覆盖、Trace 完整率、失败降级率、角色完成率和可复现性。
- 审计指标：核心观点是否有来源，风险判断是否有证据，财务数字是否能回溯到公告或工具结果。

## RAG 检索关键词
FinanceBench, FinQA, TAT-QA, 金融问答, RAG 评测, 引用覆盖率, 检索命中率, 数值推理, 表格问答, 证据定位, Agent Trace, 可信度评测

## 使用边界
- 公共 benchmark 多基于英文财报和 SEC 文件，迁移到 A 股中文公告时需要补充中文语料和本地标注集。
- 评测指标只能说明系统在给定样本上的表现，不能直接等价为真实投资收益。
- Agent 生成研报时必须区分“事实证据”“推理判断”和“投资假设”。
