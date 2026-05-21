# 外部金融知识源：FinQwen

## 来源
- 项目/数据源：https://github.com/Tongyi-EconML/FinQwen
- 仓库：https://github.com/Tongyi-EconML/FinQwen
- 引用：Tongyi-EconML. FinQwen: 金融场景智能问答系统。

## 关键事实
- 来源 ID：`tongyi-fin-qwen`。
- 来源类型：`github_project`；接入模式：`manual_license_review`。
- 市场范围：`china`；语言：zh；许可证/使用口径：research。
- 文档类型：chinese_finance_qa, prospectus, table_qa, benchmark。
- 企业级价值：面向中文金融问答和金融场景智能问答，适合补充中文金融 RAG 任务模板、招股书/表格问答场景和本地 benchmark。

## 投研关注点
- 中文金融问答样本
- 招股书和表格问答
- 中文 RAG 评测题型设计
- A 股场景提示词和答案结构参考

## RAG 检索关键词
FinQwen, 中文金融, 金融问答, 招股书, 表格问答

## 使用边界
- 接入前需要逐项确认数据许可证和可再分发范围
- 不应把竞赛或训练数据直接混入生产知识库
- 更适合进入 eval 数据集或任务模板，而不是直接作为事实证据
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `tongyi-fin-qwen`
- `category`: `chinese_financial_qa`
- `market`: `china`
- `ingestion_mode`: `manual_license_review`
- `license`: `research`
