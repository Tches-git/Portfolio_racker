# 外部金融知识源：FinAgent Benchmark

## 来源
- 项目/数据源：https://huggingface.co/datasets/finagent-benchmark/finagent-benchmark
- 仓库：https://huggingface.co/datasets/finagent-benchmark/finagent-benchmark
- 引用：finagent-benchmark. FinAgent Benchmark dataset.

## 关键事实
- 来源 ID：`finagent-benchmark`。
- 来源类型：`huggingface_dataset`；接入模式：`eval_dataset`。
- 市场范围：`us`；语言：en；许可证/使用口径：research。
- 文档类型：agentic_rag, sec_filings, benchmark, verified_qa。
- 企业级价值：用于评估 vector RAG、agentic RAG 和 multi-agent 系统在 SEC 文件问答上的证据定位和答案质量。

## 投研关注点
- Agentic RAG 评测
- 多 Agent 检索与工具调用比较
- SEC 文件问答
- 人工验证问题集

## RAG 检索关键词
FinAgent, agentic RAG, multi-agent, SEC, benchmark

## 使用边界
- 样本规模适合 smoke / benchmark，不是完整生产知识库
- 英文 SEC 语境需要和 A 股中文数据分层管理
- 生产研报不能把 benchmark 答案当作实时事实
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `finagent-benchmark`
- `category`: `agentic_rag_benchmark`
- `market`: `us`
- `ingestion_mode`: `eval_dataset`
- `license`: `research`
