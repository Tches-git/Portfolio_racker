# 外部金融知识源：FinQA

## 来源
- 项目/数据源：https://finqasite.github.io/
- 仓库：https://github.com/czyssrs/FinQA
- 引用：Chen et al. FinQA: A Dataset of Numerical Reasoning over Financial Data.

## 关键事实
- 来源 ID：`czyssrs-finqa`。
- 来源类型：`github_dataset`；接入模式：`eval_dataset`。
- 市场范围：`us`；语言：en；许可证/使用口径：research。
- 文档类型：financial_qa, numerical_reasoning, table_text_qa, benchmark。
- 企业级价值：适合测试金融数值推理能力，验证模型能否基于财报表格与文本生成可解释计算步骤。

## 投研关注点
- 财务表格 + 文本混合推理
- 数值计算正确性评测
- Agent 工具调用和计算链路验证
- 公共金融 QA benchmark

## RAG 检索关键词
FinQA, numerical reasoning, financial QA, table QA, benchmark

## 使用边界
- 英文 SEC 财报语境为主，不能直接代表 A 股中文研报场景
- 更适合作为评测集，不应作为事实知识直接召回给研报
- 使用时需要遵循原项目数据协议和引用要求
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `czyssrs-finqa`
- `category`: `financial_numerical_reasoning`
- `market`: `us`
- `ingestion_mode`: `eval_dataset`
- `license`: `research`
