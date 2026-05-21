# 简历指标口径

本文件记录可以写进简历的项目指标来源，避免使用无法复现的数字。

## 可复现命令

- 事件处理评测：`python main.py tracking-eval`
- 真实事件初始样本构建：`python main.py build-tracking-benchmark --stock-codes <股票代码列表> --target-count 150 --live`
- 真实事件评测：`python main.py tracking-eval --benchmark data/benchmarks/tracking_events_real.jsonl --no-expand`
- 扩展压力评测：`python main.py tracking-eval --target-count 1000`
- Agent 任务评测：`python main.py agent-eval`
- Agent 扩展评测：`python main.py agent-eval --target-count 500`
- 公共金融 QA/RAG 子集预测：`python main.py finance-qa-predict --benchmark <本地子集路径> --limit 50 --output output/evals/financebench_50_predictions.jsonl`
- 公共金融 QA/RAG 子集评测：`python main.py finance-qa-eval --benchmark <本地子集路径> --predictions output/evals/financebench_50_predictions.jsonl --limit 50`
- RAG 引用可信度评测：`python main.py rag-eval --stock-code <股票代码>`
- 后端回归测试：`pytest -q`
- 前端类型检查：`cd frontend && npm run typecheck`
- 前端构建：`cd frontend && npm run build`

## 推荐写法

- 基于项目内金融事件种子标注集扩展出可复现评测样本，对事件去重、事件分类、高影响识别和预警规则进行离线评测，输出 Precision / Recall / F1 等指标。
- 从公开公告/新闻等元数据构建真实事件初始样本，并标记需人工复核标签；用真实样本暴露去重合并、影响等级和预警误报等问题。
- 接入公共金融 QA/RAG benchmark 本地子集适配器，支持 FinanceBench、FinQA、TAT-QA 常见格式，统计 Exact Match、Token-F1、关键答案命中率、上下文答案命中率和引用覆盖率。
- 设计事件影响回测模块，统计事件后 T+1 / T+3 / T+5 / T+10 收益、最大回撤和成交量变化，为预警优先级提供量化依据。
- 设计 RAG 引用可信度评测机制，对研报核心观点进行引用覆盖率统计，沉淀 `citation_coverage_rate`、`unsupported_claim_count`、`source_reference_count` 等可信度指标。
- 设计项目内金融研究 Agent 任务评测集，覆盖事件点评、风险复核、组合预警、行情解释、数据源降级和研报更新等任务，统计工具覆盖率、输出完整性、多智能体角色覆盖率、Trace 完整率和降级处理能力。
- 通过 Docker Compose 将 API、前端、PostgreSQL、Redis 和独立 Worker 部署为单机多服务架构，支持长耗时研报任务排队、重试和状态追踪。

## 最近一次实测快照

- 事件处理 Benchmark（2026-05-14）：24 条人工校验种子样本，默认扩展为 500 条可复现评测样本；预警正 / 负样本 420 / 80，高影响识别 F1 94% 左右，预警 F1 97% 左右。
- 事件处理压力评测（2026-05-14）：同一套种子样本扩展为 1000 条可复现评测样本；预警正 / 负样本 836 / 164，用于验证评测脚本和统计链路在更大样本量下可稳定运行。
- 真实事件初始样本（2026-05-14）：从公开来源元数据生成 150 条事件样本，覆盖 13 个股票代码；其中 45 条为低影响/非预警样本，全部标记为需人工复核标签。
- 真实事件评测（2026-05-14）：150 条真实事件初始样本不做扩展，暴露出现有去重规则在公告密集场景下合并过度、高影响识别偏保守等问题；该结果用于定位改进方向，不作为漂亮指标宣传。
- FinanceBench 公开集接入（2026-05-14）：本地已接入 FinanceBench open-source 公开文件 150 条样本；无预测文件时可统计检索上下文是否覆盖标准答案，完整 150 条样本上下文答案命中率为 68.0%。
- FinanceBench 预测子集评测（2026-05-14）：在 FinanceBench open-source 50 条预测子集上，LLM 生成关键答案命中率为 76.0%，相比同一子集的上下文答案命中率 72.0% 提升 4.0 个百分点；严格 Exact Match 为 26.0%，Token-F1 为 39.9%，引用覆盖率为 100.0%。该结果仅代表 50 条本地预测子集，不写成完整 FinanceBench 官方成绩。
- Agent 任务评测（2026-05-14）：88 条项目内金融研究任务种子样本，默认扩展为 300 条可复现任务样本；任务成功率 65.7%、必需工具覆盖率 95.2%、Trace 完整率 90.0%，并接入多角色 Agent 覆盖率指标。
- Agent 扩展评测（2026-05-14）：同一套任务种子扩展为 500 条可复现任务样本；任务成功率 66.8%、必需工具覆盖率 95.2%、Trace 完整率 90.0%，用于验证评测统计链路稳定性。
- 样例研报生成（2026-05-13）：生成 Markdown 研报、HTML 展示版、Trace 和来源索引；规则型研报综合评分 73.2/100，来源覆盖率 100.0%。
- 样例研报 RAG 引用可信度（2026-05-13）：核心观点 28 条、来源引用 10 条、引用覆盖率 35.7%、无来源观点 18 条、检索 Top-K 命中率 100.0%。
- 自动化回归（2026-05-14）：`pytest -q` 为 402 passed；`npm run typecheck` 与 `npm run build` 通过。

## 指标刷新位置

- JSON/Markdown 评测报告默认输出到 `output/evals/`。
- 前端 `/quality` 页面展示最近一次事件评测、Agent 任务评测、公共金融 QA/RAG 评测、RAG 评测、任务运行和冒烟状态。
- 简历中的测试数量以当前 `tests/test_*.py` 文件数量或完整 `pytest -q` 输出为准。
