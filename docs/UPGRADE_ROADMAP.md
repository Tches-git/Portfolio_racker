# 项目后续升级方案

> 目标：在不破坏当前单股票分析、研报生成、评测与 FastAPI + Next.js 前端主链路的前提下，把项目逐步升级为更现代的 AI 研究助手系统。

---

## 1. 升级总原则

### 1.1 总体目标

项目后续升级不是为了简单堆功能，而是围绕以下四个目标展开：

1. **输入更丰富**：从“股票代码驱动”扩展到“股票代码 + 文档 + 图片 + 实时数据源驱动”
2. **知识更结构化**：从纯向量检索升级为“向量检索 + 结构化关系检索”
3. **记忆更长期**：从单次分析历史记录升级为个股级长期记忆与跨次分析连续性
4. **系统更工程化**：从单体 orchestrator 升级为更清晰的服务边界与工作流编排

### 1.2 约束条件

升级过程中需要保持以下约束：

- **不破坏当前 CLI / API / Next.js 主路径**
- **所有新能力都应可选开启，而不是强依赖**
- **每一阶段都必须独立可上线、可测试、可回滚**
- **评测、回归、质量门禁需要同步演进**
- **Web 展示层必须跟上，不允许“后端升级了但看不见”**

### 1.3 推荐实施顺序

建议严格按以下顺序推进：

1. **多模态输入 + 在线工具调用**
2. **长期记忆升级**
3. **Graph RAG 混合检索**
4. **MCP / 工作流编排**
5. **横向补齐评测、观测、UI 展示**

原因很简单：

- 第一阶段最容易直接提升分析输入质量
- 第二阶段最容易提升“连续研究”的价值感
- 第三阶段最容易提升关系型问题与风险传导分析质量
- 第四阶段最适合在架构稳定后再做，否则重构成本高

---

## 2. 当前系统升级基线

当前项目已经具备较好的升级基础：

- `app/agent/`：已有 Agent 推理与流程编排骨架
- `app/data_source/`：已有数据获取与清洗入口
- `app/rag/`：已有知识库、嵌入、向量检索、重排序能力
- `app/memory/`：已有历史分析存储能力
- `app/evals/`：已有规则评分、LLM-as-Judge、一致性诊断
- `app/api/` + `frontend/`：已有 API 与 Next.js 工作区，可承接新增能力展示
- `tests/`：已有较完整测试体系，可为升级提供回归保护

换句话说，当前项目不是从零开始设计，而是一个已经具备“Agent + RAG + Eval + UI”闭环的基础版本。

---

## 3. Phase 1：多模态输入与在线工具层

### 3.1 阶段目标

把当前“输入股票代码 → 拉结构化数据”的模式升级为：

- 输入股票代码
- 可选上传 PDF、财报截图、公告图片、表格截图
- 可选接入实时公告 / 新闻 / 行情 / 研报 API
- 把上述内容统一转成可用于 Agent 推理和报告写作的结构化上下文

### 3.2 为什么先做这一阶段

这是最容易形成直观提升的一步，因为它直接决定：

- 数据是不是更全
- 报告里的证据是不是更真实
- Web 页面是不是更像“现代 AI 助手”而不是“单纯的金融分析器”

### 3.3 升级内容

#### 3.3.1 多模态输入处理

建议新增模块：

- `app/data_source/multimodal/ocr.py`
- `app/data_source/multimodal/pdf_layout.py`
- `app/data_source/multimodal/table_extractor.py`
- `app/data_source/multimodal/normalizer.py`

职责：

- OCR：从图片 / 截图中抽文本
- PDF layout：理解 PDF 中的标题、表格、段落块
- table extractor：把表格提取为统一结构
- normalizer：把不同来源的多模态抽取结果归一化

统一输出结构建议：

```python
@dataclass
class SourceDocument:
    source_id: str
    source_type: str   # pdf / image / screenshot / announcement / news / filing
    title: str
    text_blocks: list[str]
    tables: list[dict]
    metadata: dict[str, str]
    extracted_at: str
```

#### 3.3.2 在线工具调用层

建议扩展 `app/data_source/` 和 `app/agent/tools.py`，增加以下工具：

- `fetch_announcements`
- `fetch_live_quotes`
- `fetch_exchange_filings`
- `fetch_broker_reports`
- `extract_document_tables`
- `extract_document_summary`

要求：

- 保持与当前 tools 风格一致
- 支持缓存
- 支持重试
- 返回来源元信息（标题、时间、链接、来源渠道）
- 工具调用 observation 要尽量结构化

#### 3.3.3 状态模型扩展

建议在 `AnalysisState` 中新增：

- `documents: list[SourceDocument]`
- `source_refs: list[dict]`
- `filings: list[dict]`
- `announcements: list[dict]`

这样后续写作、评测、UI 都可以复用。

### 3.4 Web 与产品层配套

需要同步扩展 Web：

- 首页增加“上传文档 / 图片”入口
- 结果页增加“来源与证据”面板
- 运行过程中显示“多模态解析成功/失败”状态
- 若 OCR / 表格解析失败，要给出明确降级提示

### 3.5 评测与指标

这一阶段建议新增指标：

- `source_reference_count`
- `source_provenance_coverage`
- `document_parse_success_rate`
- `table_extraction_success_rate`
- `live_tool_success_rate`

### 3.6 测试要求

新增测试类型：

- OCR / PDF / 表格解析 adapter 测试
- 工具层 contract 测试
- 多模态失败回退测试
- 新字段写入 `AnalysisState` 的测试
- Web 来源展示的测试

### 3.7 阶段验收标准

- 原有股票代码路径完全不受影响
- 新输入路径可选启用
- 报告可显示来源信息
- UI 可看到解析结果与失败提示
- regression / quality gate 保持可运行

---

## 4. Phase 2：长期记忆与跨次分析积累

### 4.1 阶段目标

把当前 `app/memory/store.py` 的“历史记录快照”升级为真正有研究价值的长期记忆层。

### 4.2 当前问题

当前记忆系统更偏向：

- 保存最近分析结果
- 做简单历史对比
- 为 Web 首页展示最近记录

但还不具备：

- thesis 演变跟踪
- 风险反复出现的模式识别
- 估值区间演化记录
- 个股长期研究档案

### 4.3 目标能力

> 当前进展（2026-04-21）：已开始把历史快照升级为 `StockMemorySnapshot` 长期记忆层，新增 stock memory 持久化、长期记忆摘要/时间线、memory 指标（hit / delta coverage / duplicate rate）以及 Web 历史区的长期研究脉络展示。

建议把记忆分成三层：

1. **Session Memory**：本次运行中的上下文记忆
2. **Stock Memory**：股票级长期记忆
3. **User / Workspace Memory**：未来可选的用户偏好或研究习惯记忆

#### 4.3.1 Stock Memory 结构建议

```python
@dataclass
class StockMemorySnapshot:
    stock_code: str
    timestamp: str
    thesis: str
    rating: str
    target_range: str
    key_risks: list[str]
    catalysts: list[str]
    valuation_summary: str
    confidence_signals: dict[str, float]
```

#### 4.3.2 Memory 检索策略

不是所有记忆都要注入所有阶段，建议：

- **研究阶段**：只注入“最近一次结论差异 + 关键风险演变”
- **写作阶段**：注入“长期 thesis 演化 + 估值变化 + 历史风险复现”
- **UI 展示阶段**：显示“这次 vs 上次”的变化摘要

#### 4.3.3 记忆治理规则

需要增加：

- 时间衰减：老记忆不应始终高权重
- 去重合并：同一结论不要重复注入 prompt
- 冲突标记：若结论前后矛盾，需要显式标出“变化原因”

### 4.4 Web 配套

建议新增：

- “长期研究脉络”面板
- “本次结论 vs 上次结论”对比卡
- 风险演化时间线
- 历史评级 / 估值区间变化小图表

### 4.5 评测与指标

新增指标建议：

- `memory_hit_count`
- `memory_usefulness_score`
- `historical_delta_coverage`
- `duplicate_memory_injection_rate`

### 4.6 测试要求

- save / load / retrieve / merge 测试
- 时间衰减与排序测试
- 冲突记忆检测测试
- UI 历史对比卡测试

### 4.7 阶段验收标准

- 记忆可以明显改善连续分析体验
- Prompt 不因记忆无限膨胀
- Web 能看到长期研究脉络
- regression 保持稳定

---

## 5. Phase 3：Graph RAG 混合检索

### 5.1 阶段目标

在现有向量 RAG 的基础上，增加结构化图检索能力，解决“关系型问题”回答不稳定的问题。

### 5.2 为什么要做 Graph RAG

当前向量 RAG 更适合：

- 找相似语义片段
- 找相关理论说明
- 找近义知识

但对于以下问题，纯向量检索不够理想：

- 某个风险是如何通过业务链条传导到利润的？
- 这家公司和同行之间有哪些结构性差异？
- 某个新闻事件和财务指标之间如何关联？
- 哪些催化剂与估值重估逻辑有关？

这些问题本质上更偏“关系检索”，更适合图结构。

### 5.3 图谱建模建议

建议先做轻量图谱，不要一开始就上复杂图数据库。

实体建议：

- Company
- Industry
- Peer
- Metric
- Event
- Risk
- Catalyst
- Filing
- News

关系建议：

- `belongs_to_industry`
- `compares_with`
- `affects_metric`
- `causes_risk`
- `triggers_catalyst`
- `mentions_company`
- `supports_thesis`

### 5.4 模块建议

新增：

- `app/rag/graph_schema.py`
- `app/rag/graph_builder.py`
- `app/rag/graph_store.py`
- `app/rag/hybrid_retriever.py`

职责：

- `graph_builder`：从新闻、公告、历史报告、行业知识中抽实体关系
- `graph_store`：图谱存储与查询
- `hybrid_retriever`：同时调 vector RAG + graph RAG，并做混合排序

### 5.5 使用方式

建议不是全量替代现有 RAG，而是：

- 普通知识补充 → 仍用 vector RAG
- 同行关系、风险传导、事件链分析 → 增加 graph query
- 写作时按段落主题决定是否调用 graph retrieval

### 5.6 UI 配套

建议增加：

- “关系图摘要”卡片
- 风险传导链展示
- 事件 → 指标 → 评级 的因果链可视化

### 5.7 评测与指标

新增指标：

- `graph_hit_count`
- `hybrid_retrieval_hit_rate`
- `relationship_coverage`
- `risk_path_completeness`

### 5.8 测试要求

- 图谱构建测试
- 关系查询测试
- hybrid retrieval 排序测试
- fallback 到 vector-only 的测试

### 5.9 阶段验收标准

- 同行、风险、事件链类问题明显更稳定
- 不破坏原有向量检索路径
- Web 能展示图谱关系摘要

### 5.10 当前进展（2026-04-21）

- 已完成轻量 graph summary、graph store、hybrid retriever 的 additive 接入，仍保持 vector-only fallback 安全可用
- 当前增量继续沿“summary-first + state-driven”路线推进：hybrid retrieval 开始支持 **query-aware** 排序与图查询焦点标记
- graph query 会根据风险传导 / 催化因素 / 同行对比 / 行业归属 / 指标影响等意图对关系边做轻量加权，而不是替代原有向量上下文
- 在单一 focus 之外，系统现在会额外构建 lightweight **多焦点关系摘要**，用于补充风险 / 催化 / 同行 / 行业 / 指标五类关系覆盖面，但仍保持小步增量与 fallback-safe
- 当前进一步开始支持 **章节定向 graph retrieval**：为风险 / 行业 / 估值等章节分别生成轻量图查询摘要，用于在写作阶段按段落主题补充关系证据
- 最新增量已把这些章节定向 graph context **显式注入到对应 prompt 区块附近**，让风险段、行业段、估值段各自拿到更贴近主题的关系材料，而不是只共享总摘要
- orchestrator 继续作为注入点，把 `graph_query_focus`、`graph_focus_summary`、`section_graph_summary` 与增强后的 `hybrid_graph_context` 注入写作 prompt、运行指标与 Web 展示层
- 当前章节定向 query 已开始根据 state 自动带入个股名、核心风险、同行与估值锚，使风险 / 行业 / 估值 graph 检索更贴当前分析上下文
- 最新增量已开始把 **章节 Graph 吸收诊断反向用于 query refinement**：当风险 / 行业 / 估值章节注入后吸收不足时，会对对应 query 做更收紧的风险传导 / 竞争格局 / 估值锚提示，但仍保持 additive 和 vector fallback-safe
- 当前进一步把这条闭环做成可量化信号：evals / Web 现在会额外暴露 **低吸收章节数、收紧是否触发、收紧覆盖率**，便于判断 refinement 是否真正覆盖了需要修正的章节
- 最新增量进一步补上 **refinement 前后对比**：现在不仅能看是否触发收紧，还能度量章节 Graph refinement 前后命中数变化与改善率，便于判断收紧 query 是否真的带来增量命中
- 当前又进一步把低改善章节分型为 **无命中 / 无增量 / 纯低吸收**，用于区分“检索没拿到”“拿到了但没变好”“命中改善了但正文仍未吸收”三类问题
- 最新增量已开始让 refinement **按分型走不同策略**：无命中偏扩词召回、无增量偏改写提问、纯低吸收偏贴近正文表达，并把策略选择同步暴露到 evals / Web
- evals 与 Web 现已同步暴露章节 feedback / refinement 信号，便于观察“注入→吸收→收紧查询”的闭环是否有效
- evals 已进一步补上 **章节级吸收诊断**：现在不仅能看是否注入了 section graph，还能度量风险 / 行业 / 估值章节是否真的吸收这些关系线索
- 本阶段仍要求每次增量都保持独立可交付、可回退，并与 CLI / Web / eval / regression / quality gate 兼容

---

## 6. Phase 4：MCP / 工作流编排

### 6.1 阶段目标

把当前以 `AgentOrchestrator` 为中心的单体流程，逐步拆成更清晰的服务边界或工作流节点。

### 6.2 为什么最后做

因为前面几阶段都还在增加核心能力，如果过早做编排重构，会频繁返工。

### 6.3 目标形态

理想目标不是立刻微服务化，而是先把阶段边界明确：

- data fetch
- multimodal parse
- memory retrieve
- rag retrieve
- research
- write
- postprocess
- eval
- persist

### 6.4 两种实现路径

#### 路径 A：应用内工作流节点

优点：

- 改造成本低
- 便于保留现有代码结构
- 适合先验证阶段边界

建议新增：

- `app/workflow/nodes/*.py`
- `app/workflow/runner.py`
- `app/workflow/contracts.py`

#### 路径 B：MCP / 服务化边界

优点：

- 展示更现代
- 更适合后续扩展多仓库、多服务协同
- 有利于把数据源、检索、评测做成标准服务

但缺点是：

- 开发和调试成本更高
- 对当前项目来说不是最先要解决的价值点

### 6.5 推荐策略

建议先做 **应用内工作流节点化**，等稳定后再考虑 MCP 化。

### 6.6 观测与追踪

这一阶段应同步增强可观测性：

- 每个节点耗时
- 每个节点输入输出摘要
- 节点失败率
- 节点重试次数
- 节点级 trace view

### 6.7 UI 配套

可新增：

- 工作流节点时间线
- 每阶段输入 / 输出摘要
- 失败节点高亮
- 节点级日志面板

### 6.8 测试要求

- 节点级单测
- 节点组合集成测试
- 节点失败回退测试
- 与现有 quality gate 的兼容测试

### 6.9 阶段验收标准

- 主流程不再强耦合在一个 orchestrator 大文件中
- 节点可单测、可替换、可观测
- 现有 analyze/web/regression/quality-gate 行为保持稳定

---

## 7. 横向配套：评测、观测、UI 必须同步升级

### 7.1 为什么横向能力必须同步做

很多项目升级失败，不是因为后端没做出来，而是因为：

- 升级后效果无法量化
- UI 看不到新增能力
- 回归体系跟不上，导致功能越多越不稳定

所以每个阶段都必须同步扩展以下三块：

1. **评测体系**
2. **观测体系**
3. **Web 展示层**

### 7.2 新增指标建议

- 多模态：解析成功率、表格抽取成功率、来源覆盖率
- 长期记忆：记忆命中率、历史差异覆盖率、记忆冗余率
- Graph RAG：graph hit 数、关系覆盖率、风险路径完整度
- 工作流：节点耗时、节点失败率、节点回退成功率

### 7.3 Web 展示建议

未来可在现有 Next.js 工作区上新增这些分区：

- 来源与证据
- 多模态解析结果
- 长期记忆摘要
- 图谱关系摘要
- 工作流节点视图

---

## 8. 推荐实施计划

### 8.1 推荐节奏

#### Sprint 1
- 多模态文档抽取骨架
- 在线工具层骨架
- 来源引用展示
- 当前进展（2026-04-20）：已接入可选上传入口、CLI `--doc` 可选文档输入、`app/data_source/multimodal/*` 解析骨架、`app/data_source/live_tools.py` richer provenance 字段（provider / retrieval_mode / evidence_type / placeholder）与 CNInfo 公告/披露抓取优先策略、AnalysisState 来源字段、报告/评测/UI 的来源展示与指标骨架

#### Sprint 2
- Stock Memory 升级
- 历史脉络 UI
- 记忆评测指标

#### Sprint 3
- Graph schema + builder
- hybrid retriever
- 风险传导关系展示

#### Sprint 4
- workflow nodes
- 节点 trace view
- 节点级回归和门禁适配

### 8.2 每阶段交付要求

每一阶段都至少应交付：

- 一组新增模块
- 一组新增测试
- 一组新增评测指标
- 一组 UI 可见变化
- 一次 regression / quality gate 通过记录

---

## 9. 结论

从当前项目出发，最合理的升级路径不是推翻重做，而是沿着以下主线渐进式扩展：

**多模态输入 → 在线工具调用 → 长期记忆 → Graph RAG → 工作流 / MCP 编排**

这条路线的优势在于：

- 与现有代码结构高度兼容
- 每一步都有明确收益
- 每一步都可以形成可展示、可量化的升级成果
- 最终可以把项目从“金融研报生成系统”升级为“更完整的 AI 研究助手平台”
