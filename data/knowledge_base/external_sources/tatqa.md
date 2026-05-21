# 外部金融知识源：TAT-QA

## 来源
- 项目/数据源：https://arxiv.org/abs/2105.07624
- 仓库：https://github.com/NExTplusplus/TAT-QA
- 引用：Zhu et al. TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content in Finance.

## 关键事实
- 来源 ID：`tatqa`。
- 来源类型：`benchmark`；接入模式：`eval_dataset`。
- 市场范围：`us`；语言：en；许可证/使用口径：research。
- 文档类型：table_qa, text_qa, financial_qa, benchmark。
- 企业级价值：适合评估模型是否能同时利用财务表格和文本段落进行问答、计算与证据定位。

## 投研关注点
- 表格 + 文本混合问答
- 财报数字推理
- RAG 上下文组织测试
- 多 Agent 估值/财务角色评测

## RAG 检索关键词
TAT-QA, table QA, financial QA, numerical reasoning, benchmark

## 使用边界
- 主要是英文财务文档评测集
- 接入 A 股场景需要中文表格抽取和会计科目映射
- 适合作为 eval，不适合作为实时知识源
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `tatqa`
- `category`: `table_text_financial_qa`
- `market`: `us`
- `ingestion_mode`: `eval_dataset`
- `license`: `research`
