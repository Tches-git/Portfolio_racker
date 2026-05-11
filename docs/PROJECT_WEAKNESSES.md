# 项目未解决短板清单（当前版本）

> 说明：本清单只保留**当前仍未收口、仍需继续推进**的短板。
> 已有明确修复或已有阶段性缓解、暂不再作为当前主清单跟踪的事项，已从本文移除。

---

## 一、架构与可维护性短板

### 1. 编排器仍然过重，核心流程耦合度高
- `app/agent/orchestrator.py` 仍承担预取、记忆注入、研究、写作、图检索、后处理、持久化等大量职责。
- ⚠️ 已继续做小步拆分：此前已把研究结果落盘与写作前准备阶段分别收敛到 `_apply_research_result()`、`_prepare_writer_state()`，降低 `_run_traced()` 的直接编排体积；前几轮又把运行收尾阶段里的过程指标与阶段摘要进一步收口到 `run_payload`，由 `_finalize_run()` 统一写入 `agent_steps`、`rag_hits`、`trace_summary`、`phase_breakdown`、`failed_phases`，保留 `sections` 兼容层；随后把 live-tools 执行流程与文档解析阶段里的汇总、source ref 组装、runtime payload 回写继续下沉到 `app/agent/prefetch_helpers.py` 的共享 helper；上轮清掉 orchestrator 中这批已变成薄转发的 helper wrapper；前几轮再把上传文档 ingest 的执行体、empty-input 分支与真实 parser/extractor 绑定继续下沉到共享 helper；本轮再把 live-sources 路径也切到 helper 默认 fetcher 绑定，进一步把 orchestrator 收口为单一 helper 调用点。
- 但单文件仍集中承载过多主流程责任，边界仍不够清晰，修改影响面依然偏大。
- 后续若继续叠加能力，复杂度仍会持续上升。

### 2. `AnalysisState.sections` 仍承担大量隐式协议
- ⚠️ 已继续小步收口：此前已新增 `analysis_payload`，并把 `research_conclusion`、`research_plan`、`research_reflection`、`data_gaps`、`data_gap_count` 这组分析期字段迁到“优先结构化、缺失时回退 sections”的兼容模式；较前几轮继续补上 `run_payload` / `runtime_input_payload`，在原有 `metrics`、`postprocess.fix_count/fixes`、`agent_steps`、`rag_hits`、`trace_summary`、`phase_breakdown`、`failed_phases` 之外，再把 `postprocess.fix_summary`、`document_parse_summary`、`document_parse_success_rate`、`table_extraction_success_rate`、`document_parse_failure_count`、`live_tool_success_rate`，以及 `live_tools.quote_snapshot`、`live_tools.quote_summary`、`live_tools.errors`、`live_tools.error_count`、`live_tools.error_summary`、`live_tools.broker_report_count` 这组运行期/多模态/在线来源指标纳入“优先结构化、缺失时回退 sections”；前几轮继续把 agent tool 路径的 `fetch_announcements / fetch_exchange_filings / fetch_broker_reports / fetch_live_quotes` 同步接入 `runtime_input_payload.live_tools` 与 `source_refs` 维护，并补齐 `success_count / tool_count / failed_count / success_rate / errors / error_summary` 这组 success/error 汇总，同时把 `success_map` 收回 helper 内部状态，不再作为对外 payload contract 暴露；另外已把 live quote summary、quote source ref、live source refs，以及 document source ref 的构造下沉复用到 `prefetch_helpers.py`，并继续把 prefetch/documents/live-tools runtime payload 的组装逻辑抽到 helper；上轮再把 orchestrator 里对应的薄 wrapper 一并移除；前几轮继续把 uploaded document ingest 的空输入/解析/汇总/回写执行体与默认绑定收口到共享 helper；本轮再让 live-sources helper 默认接管真实 fetcher 绑定，继续压缩 orchestrator 侧的 contract 拼装代码。
- 但仍有不少模块通过 `state.sections["..."] = str(...)` 传递状态、指标和中间结果。
- 即使已有结构化 payload，引导层和兼容层仍长期并存，增加理解和维护成本。
- 这会持续限制状态 contract 清晰化与后续节点化拆分。

### 3. 主流程边界不清晰，节点化程度不足
- ⚠️ 已继续小步收敛：上轮把 `_run_traced()` 再拆成 `_prepare_memory_context()`、`_initialize_knowledge_base()`、`_run_research_phase()`、`_run_writer_phase()`，让主流程更接近分阶段 contract；前几轮再把 live-tools 阶段执行体、文档解析阶段里的汇总 / payload 回写以及外层薄转发方法逐步收口到共享 helper；前几轮继续把 uploaded document ingest 执行体、empty-input 分支与默认绑定下沉；本轮再把 live-sources 的真实 fetcher 绑定也收口到 helper 默认行为，让 `_hydrate_live_sources()` 同样更接近纯阶段事件回调层。
- 但当前仍以单体流程推进，缺少更明确的 workflow node / contract 层。
- 数据抓取、检索、研究、写作、评测、持久化之间的边界仍不够硬。
- 当功能继续增长时，流程回归、插拔和可观测性都会继续受限。

### 4. 预取路径与工具调用路径并存，维护成本偏高
- ⚠️ 已继续小步缓解：此前已把预取链路里的核心数据预取与市场上下文预取抽到 `app/agent/prefetch_helpers.py` 的 `prefetch_core_data()`、`prefetch_market_context()`；本轮又把 profile / financials / peers / news 的观察文本格式进一步抽成共享 formatter，并让 `tools.py` 与预取链路复用同一套输出逻辑，降低双路径在文案和字段表现上的漂移风险。
- 但 orchestrator 预取数据写入 `state`，Agent 工具又重复读取或命中缓存，这种“双路径维护”现象本身仍在。
- 这仍容易在字段、格式、时机上出现漂移；一旦工具输出 contract 变化，预取链路也需要同步调整。

### 5. 消融实验仍依赖 monkey patch，演化和测试脆弱
- ⚠️ 已继续小步缓解：前一轮给运行链路补上 `AblationConfig` 显式配置，并让 `run_ablation.py` 通过配置映射驱动 `baseline / no_reflection / no_rag`，由 `ReportEngine` → `AgentOrchestrator` → `ReActAgent` / 写作侧按开关收口行为，先去掉 `no_reflection`、`no_rag` 对 monkey patch 的依赖，同时保持 `main.py ablation` / `run_ablation.py` 兼容入口不变。
- ⚠️ 本轮继续小步收口：把实验组的 `label / banner / config` 再统一到显式 `AblationExperiment` contract，并把 `experiment_banner`、`ablation_config`、`experiment_contracts` 写入评测行结果与汇总 JSON，减少脚本层散落字符串和机器侧隐式约定。
- 但消融实验仍是脚本层兼容能力，尚未形成更完整的阶段指标面板或更细粒度策略对象。
- 若后续实验组继续增加，仍需继续把配置维度、指标口径和评测输出收口到更稳定的显式接口。

---

## 二、数据源与数据质量短板

### 8. 强依赖外部免费数据源，稳定性和一致性天然受限
- 主要依赖 `akshare`、网页接口和第三方公开源。
- 这些来源的字段、频率、可用性和异常值稳定性都不足。
- 这会持续给分析质量与线上稳定性带来上游噪声。

### 12. 财务数据仍缺少更强的数据校验闭环
- 当前虽有 sanitize / clip / fill 等治理逻辑，但还没有形成“异常标记 → 影响传播 → 报告披露”的强约束闭环。
- 当上游数据明显异常时，报告仍可能吸收噪声数据并继续推导。

### 13. 结构化工具返回值仍不够统一
- 很多工具函数内部仍用自然语言字符串表达成功/失败与结果摘要。
- 这不利于程序化判定、失败分类、自动补救和质量统计。
- 当前接口更像“给 LLM 看”的文本层，而不是“给编排层看”的稳定 contract。

---

## 三、多模态能力短板

### 14. OCR 仍是 fallback 骨架，不是真实 OCR 能力
- `app/data_source/multimodal/ocr.py` 目前本质上仍是把图片字节尝试按 UTF-8 解码。
- 对截图、扫描件、图片报告等真实场景几乎不具备可靠可用性。

### 15. PDF 版面理解仍非常基础
- `pdf_layout.py` 目前主要依赖 `pypdf` 抽纯文本。
- 对页眉页脚、双栏、图表、跨页表格、章节层级等复杂版面理解较弱。

### 16. 表格抽取仍是启发式实现
- `table_extractor.py` 主要识别 markdown-like / 分隔符表格。
- 对图片表格、复杂 PDF 表格、合并单元格、跨页表都缺少稳定支持。
- 这会直接限制多模态资料进入估值与风险链路的质量。

### 17. 多模态失败后的降级解释仍不够细
- 当前更多是“有/无结果”层面的反馈。
- 用户仍难以区分是 OCR 失败、版面理解失败、表格失败，还是源文件本身不可解析。

---

## 四、RAG / Graph RAG 能力短板

### 18. Token / 上下文预算治理仍然偏弱
- 研究结论、历史记忆、RAG 上下文、图摘要、来源材料叠加后，仍可能逼近模型上下文上限。
- 当前主要依赖经验性裁剪和截断，缺少统一预算器。

### 20. Graph RAG 仍偏轻量，不是真正强图检索系统
- `graph_store.py` 仍以关键词命中和轻量关系增强为主。
- 关系评分更多依赖 token 命中与少量 boost，不具备更强的图搜索或图推理能力。

### 21. 图存储缺少持久化和更强治理能力
- `GraphStore` 当前仍是内存对象，生命周期与单次流程绑定。
- 缺少跨会话持久化、增量更新、冲突合并、版本管理等机制。

### 22. 知识库增量去重策略仍偏粗粒度
- `KnowledgeBase` 对文档变更的判断依赖轻量文本片段指纹。
- 这对大文档局部修改、后半部分变化的识别精度有限。
- 长期会影响索引一致性和增量更新准确率。

### 23. RAG 命中是否真正进入最终报告仍不稳定
- 当前系统已具备向量检索、rerank、hybrid context。
- 但“检索到了”不等于“被模型正确吸收并体现在结论中”。
- 最终质量仍明显依赖 embedding、rerank、prompt 表达与模型吸收质量。

---

## 五、评测、测试与质量门禁短板

### 24. 测试总量不错，但完整端到端覆盖仍不够厚
- ⚠️ 已继续小步缓解：前几轮围绕展示层补上 HTML 导出、结果展示面板、风险传导视图、历史对比卡、导出复用等低风险 UI/输出测试；此前已给产品前端 Phase 1 只读 API 补上 server/service/route/download 级测试；前一轮再补 `runs` 写 API / run manager / 前端 Phase 2 路由与状态入口的 focused 测试；上一轮继续补动态 sidebar 与 recent runs 面板相关测试；前一轮再补 run detail 任务页与 run event 时间线相关测试；上一轮继续补全局运行中心、workspace 卡片与导出 master-detail 相关测试；本轮移除旧 Python Web 界面并新增金融事件追踪、预警中心、每日简报后，当前测试集为 **43 个测试文件 / 310 个测试用例**。
- 但完整运行面的覆盖仍然不足。
- 当前测试更强在模块级与局部流程级，不够强在真实主链路、真实外部依赖和命令级运行面。

### 25. 真实外部依赖的集成回归仍然较弱
- 数据源、公告抓取、OpenAI 兼容 provider、多模态解析等能力很多带外部依赖特征。
- 这类能力在单测中通常被 mock，真实环境下的稳定性验证仍不足。
- 上游接口变化往往要到运行时才会暴露。

### 26. 质量门禁产物仍偏轻量
- ⚠️ 已继续小步缓解：此前已补强 `quality_gate_summary.json` 的机器可读产物，新增步骤分类、失败步骤、回归产物路径，以及从 `regression_summary.json` 回填的回归判定 / samples / checks / aggregate 摘要；本轮再补上 `ablation/regression` 的 `history_summary` 与 `artifact_index`，并让 quality-gate 继续透传回归历史摘要和 artifact 索引，降低多脚本产物散落和人工拼接成本。
- 但门禁产物仍缺少更系统的历史归档、趋势对比和跨轮次编目。
- 当前还不足以支撑更长期的质量趋势跟踪和门禁可解释性。

### 27. 自动评测仍缺少强 ground truth
- 目前已有规则评测、LLM-as-Judge、一致性检查、人工 rubric 种子集。
- 但整体仍缺少规模更大的人工标注基准集，难以强验证“高分是否真的等于高质量”。

---

## 六、安全、部署与运行治理短板

### 30. 缺少更系统的运行级保护
- 当前虽有缓存、重试、熔断，但还缺少更完整的配额治理、请求级隔离、用户级限流。
- 对多用户或长时间运行场景准备不足。

### 31. 可观测性仍没有真正节点化
- ⚠️ 已继续小步缓解：本轮先把 `Tracer.summary()` 补到阶段级摘要，新增 `phase_total_ms`、`phase_breakdown`、`failed_phases`，让 phase 级失败分类和耗时视图先进入机器可读摘要。
- 但当前仍缺少更稳定的节点级输入/输出摘要、阶段 SLA 历史对比和跨运行聚合视图。
- 当系统继续复杂化后，现有观测手段会逐渐不够。

### 32. Docker 部署材料仍偏最小化
- 当前 Dockerfile 更适合 demo 和展示。
- 仍缺少 healthcheck、非 root 用户、镜像瘦身、启动前自检等更完整的部署治理。

---

## 七、产品与研究能力边界短板

### 33. 当前仍是“单股票深度分析器”，不是完整研究工作台
- ⚠️ 已继续小步缓解：此前已补上独立产品前端演进骨架，新增 `app/api/server.py` 的只读 API 与 `frontend/` 前端壳层；前一轮继续把前端工作区拆到 sidebar 驱动的产品总览 / 摘要详情 / 导出中心 / 历史脉络分路由，并统一复用现有导出下载链路；上一轮再在兼容 API 层补上最小 `runs` 写入口、浏览器触发分析与轮询状态闭环；前一轮继续把 sidebar 改成随当前股票动态切换，并补上 recent runs 面板；前一轮再补 run detail 任务页与事件时间线；上一轮继续补全局运行中心、workspace 卡片与导出 master-detail；前一轮再补独立 runs index 页面与更完整的任务中心导航；上一轮继续把 runs contract 扩到任务统计、首页/全局任务感知、任务详情回流，以及历史/导出页的任务联动；前一轮再把历史/导出工作区推进到可选择的 master-detail 交互；上一轮继续补按股票聚合、组合工作区视角、结构化 history/export insights 与更稳定的前端 contract；前一轮再补运行重试/取消、组合级跟踪入口与轻量运行治理提示；本轮继续补负责人分配、任务归档，并把 API-triggered runs 从 JSON 轻量落盘迁到 SQLite 持久化。
- 现阶段仍主要围绕单次单股票报告生成展开。
- 与真正的研究助手平台相比，还缺少持续研究任务、组合视角、协作视角等更高层能力。

### 34. 长期记忆离“研究档案级记忆”还有距离
- 当前记忆虽已起步，但在冲突治理、时间衰减、事实归因、历史观点可追溯性上仍较早期。
- 对“为什么观点变化了”的解释力仍不足。

### 35. 研究结论仍高度依赖模型生成稳定性
- 系统已经尽量通过工具、RAG、反思、后处理降低波动。
- 但最终结论质量仍明显受模型能力、提示词状态、上下文质量影响。
- 这决定了系统还不是结果强确定的分析引擎。

---

## 八、最值得优先修的未解决短板

1. **继续拆分 orchestrator，降低主流程耦合**
   - 重点继续收敛编排边界、上下文组装边界和状态写入边界。

2. **继续收口 `state.sections` 隐式协议**
   - 持续把关键字段迁到结构化 payload，并保持“优先结构化、缺失时回退 sections”的兼容策略。

3. **补强多模态真实能力**
   - 优先 OCR、PDF 版面理解、表格抽取，而不是继续只保留接口骨架。

4. **补强 token 预算与运行级保护**
   - 优先统一预算器、请求级保护、限流和更清晰的运行时约束。

5. **补足真实外部依赖与端到端回归**
   - 尤其是 CLI 主入口、质量门禁、真实 provider / 数据源联调路径。

6. **补强节点级可观测性与门禁产物**
   - 重点是阶段级摘要、失败分类、历史对比和机器可读产物。

---

## 九、结论

这个项目的优点依然很明显：完整、能跑、工程化意识强、展示价值高。

当前仍需持续解决的核心问题主要集中在：**主流程编排仍偏重、状态协议仍不够收口、真实多模态能力不足、Graph RAG 仍偏轻量、外部依赖治理与运行治理不够厚、完整回归闭环仍不够强。**

如果后续继续沿低风险、可回滚路线推进，最值得优先做的主线仍然是：

**“继续拆 orchestrator / 收口 sections → 再补真实入口与回归 → 再补多模态、预算器与运行治理。”**
