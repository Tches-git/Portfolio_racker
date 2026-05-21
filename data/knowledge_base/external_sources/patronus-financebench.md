# 外部金融知识源：FinanceBench

## 来源
- 项目/数据源：https://arxiv.org/abs/2311.11944
- 仓库：https://github.com/patronus-ai/financebench
- 引用：Islam et al. FinanceBench: A New Benchmark for Financial Question Answering.

## 关键事实
- 来源 ID：`patronus-financebench`。
- 来源类型：`benchmark`；接入模式：`eval_dataset`。
- 市场范围：`us`；语言：en；许可证/使用口径：research。
- 文档类型：financial_qa, sec_filings, open_book_qa, benchmark。
- 企业级价值：适合评估 RAG 系统能否在真实财务文件中找到证据并回答问题，是金融开放书问答的代表性 benchmark。

## 投研关注点
- RAG top-k 命中率评测
- 引用覆盖率评测
- 答案正确性评测
- SEC 财报证据定位

## RAG 检索关键词
FinanceBench, open-book QA, SEC filings, RAG evaluation, citation coverage

## 使用边界
- 以英文财务文件和美股公司为主
- 用于评测比用于生产知识库更合适
- 接入时需要保留原始 sample_id、evidence 和来源文件信息
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `patronus-financebench`
- `category`: `open_book_financial_qa`
- `market`: `us`
- `ingestion_mode`: `eval_dataset`
- `license`: `research`
