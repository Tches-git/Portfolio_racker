# 外部金融知识源：edgartools

## 来源
- 项目/数据源：https://github.com/dgunning/edgartools
- 仓库：https://github.com/dgunning/edgartools
- 引用：edgartools. Read and analyze SEC EDGAR filings in Python.

## 关键事实
- 来源 ID：`dgunning-edgartools`。
- 来源类型：`python_library`；接入模式：`connector_candidate`。
- 市场范围：`us`；语言：en；许可证/使用口径：MIT。
- 文档类型：10-k, 10-q, 8-k, xbrl, 13f, sec_filings。
- 企业级价值：可作为企业级美股 RAG 知识库的数据连接器，抓取 SEC EDGAR filings、XBRL 财务表、10-K、10-Q、8-K 和机构持仓等结构化材料。

## 投研关注点
- 美股公司财报 RAG 入库
- XBRL 财务指标抽取
- SEC 事件和公告检索
- 公共金融 QA benchmark 证据源构建

## RAG 检索关键词
SEC, EDGAR, 10-K, 10-Q, XBRL, filings, RAG 数据源

## 使用边界
- 只覆盖 SEC / 美股披露体系，不覆盖 A 股巨潮和交易所公告
- 大规模抓取需要遵守 SEC 访问频率与 User-Agent 要求
- 中文研报生成需要翻译、术语映射和市场口径转换
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `dgunning-edgartools`
- `category`: `sec_filings_connector`
- `market`: `us`
- `ingestion_mode`: `connector_candidate`
- `license`: `MIT`
