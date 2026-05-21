# 外部金融知识源：DISC-FinLLM

## 来源
- 项目/数据源：https://github.com/FudanDISC/DISC-FinLLM
- 仓库：https://github.com/FudanDISC/DISC-FinLLM
- 引用：FudanDISC. DISC-FinLLM: 中文金融大语言模型。

## 关键事实
- 来源 ID：`fudandisc-disc-finllm`。
- 来源类型：`github_project`；接入模式：`catalog_summary`。
- 市场范围：`china`；语言：zh；许可证/使用口径：Apache-2.0。
- 文档类型：instruction_data, retrieval_augmented_instruction, financial_eval, tool_use。
- 企业级价值：提供中文金融咨询、金融 NLP、金融计算和检索增强指令数据的设计参考，适合增强本项目 Agent 任务模板和工具调用评测。

## 投研关注点
- 中文金融 Agent 任务模板扩展
- 检索增强指令样本参考
- 金融计算工具调用设计
- 多专家金融模型任务划分参考

## RAG 检索关键词
DISC-FinLLM, 中文金融, 检索增强指令, 工具调用, 金融计算

## 使用边界
- 完整训练数据并非全部在仓库中直接开放
- 指令数据不等价于事实知识库，不能作为公司公告证据
- 生产研报仍应优先引用公告、财报和公开权威数据源
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `fudandisc-disc-finllm`
- `category`: `chinese_financial_instruction_data`
- `market`: `china`
- `ingestion_mode`: `catalog_summary`
- `license`: `Apache-2.0`
