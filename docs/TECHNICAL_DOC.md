# 金融研报智能分析系统 — 技术文档

> 基于 Agent + RAG 架构的 A 股深度研报自动生成系统

---

## 一、系统架构

### 1.1 整体架构

系统采用 **多 Agent 编排 + RAG 知识增强** 的双引擎架构，核心流程分为三个阶段：

```
用户输入股票代码 (CLI / Streamlit Web)
        │
        ▼
┌─── AgentOrchestrator（编排器）───────────────────────────┐
│                                                          │
│  阶段 1: RAG 知识库初始化                                 │
│    PDF年报扫描 → 分块 → Embedding → FAISS 索引            │
│    增量构建：仅处理新增/变更文档（MD5 指纹去重）           │
│                                                          │
│  阶段 2: Research Agent（自主研究）                        │
│    Planning  → 制定 5-12 步研究计划                       │
│    Acting    → ReAct 循环调用 11 个金融工具                │
│    Reflection→ LLM 自评 + 缺失项自动补研                  │
│                                                          │
│  阶段 3: Report Agent（RAG 增强写作）                     │
│    5 轮主题检索 → FAISS 召回 → LLM 重排序                 │
│    历史记忆对比 → 同行业交叉引用                          │
│    glm-4-plus 生成 4000+ 字深度研报                       │
│                                                          │
│  后处理: 分析结论反哺知识库 → 保存分析记忆                │
└──────────────────────────────────────────────────────────┘
        │
        ▼
  输出: Markdown 研报 + 推理链日志 + 质量评测报告
```

### 1.2 核心模块职责

| 模块 | 文件 | 职责 | 关键设计 |
|------|------|------|----------|
| **ReAct Agent** | `agent/react_agent.py` | 三阶段推理引擎 | 支持 Function Calling 和文本 ReAct 双模式，失败自动回退 |
| **工具集** | `agent/tools.py` | 11 个金融分析工具 | 内置重试（最多 3 次指数退避）+ 调用缓存（相同参数复用结果） |
| **RAG 知识库** | `rag/knowledge_base.py` | 知识管理与检索 | 增量构建 + MD5 去重 + LLM 重排序 + 分析结论反哺 |
| **向量存储** | `rag/vector_store.py` | FAISS 向量检索 | L2 归一化 + 内积检索（等价余弦相似度），无 FAISS 时自动回退 numpy |
| **LLM 层** | `llm.py` | 统一 LLM 调用 | 3 次重试 + Token 统计 + 双模型策略（flash 推理 / plus 写作） |
| **DCF 估值** | `finance/valuation.py` | 现金流折现模型 | 增长率线性衰减 + 蒙特卡洛 1000 次模拟 + WACC×增长率敏感性矩阵 |
| **评测框架** | `evals/report_eval.py` | 研报质量评分 | 规则型指标 + LLM-as-Judge + 报告/状态事实一致性检查 |
| **记忆系统** | `memory/store.py` | 分析记忆持久化 | JSON 存储历史分析记录，支持跨期对比和同行业交叉参照 |

### 1.3 数据流

```
akshare API ──→ 公司信息/财务/同行/新闻
                    │
                    ▼
             AnalysisState（共享状态对象）
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
  杜邦分析     DCF+蒙特卡洛    风险识别
  趋势CAGR    敏感性分析      量化评分
  可比估值                    RAG检索
      │             │             │
      └─────────────┼─────────────┘
                    ▼
           Report Agent (glm-4-plus)
                    │
                    ▼
            Markdown 深度研报
```

---

## 二、关键技术设计

### 2.1 双模式 Agent 推理

系统实现了两种 Agent 推理模式，运行时动态选择：

| 模式 | 触发条件 | 优势 | 劣势 |
|------|----------|------|------|
| **Function Calling** | 默认优先 | 结构化输入输出，LLM 直接返回工具名和参数 JSON | 依赖模型的 FC 能力，部分模型支持不稳定 |
| **文本 ReAct** | FC 失败时自动回退 | 兼容性强，任何 LLM 均可运行 | 需正则解析 `Thought/Action/Action Input`，偶有格式错误 |

**回退机制**：`_act()` 方法先尝试 Function Calling，捕获异常后调用 `_act_text_mode()`，保证系统鲁棒性。

### 2.2 RAG 检索管线

```
查询 → 智谱 embedding-3 编码 → FAISS IndexFlatIP 召回 (candidate_k=15)
                                         │
                                         ▼
                              LLM 重排序 (reranker.py)
                              ┌─────────────────────┐
                              │ 对每个候选文档评分    │
                              │ 0-100 分 + 理由      │
                              │ 取 score ≥ 50 的 top_k│
                              └─────────────────────┘
                                         │
                                         ▼
                              返回 top_k=5 个最相关文档
```

**知识库组成**：

| 知识来源 | 条目数 | 说明 |
|----------|--------|------|
| 内置金融理论 | 15 条 | 杜邦分析、DCF、可比估值、风险识别、行业分析等 |
| 内置行业知识 | 6 条 | 白酒、银行、新能源、医药、房地产、半导体、消费 |
| PDF 年报文档 | 动态 | 用户放入 `data/knowledge_base/` 的 PDF 自动解析入库 |
| 实时分析数据 | 动态 | 每次分析的财务数据、新闻、行业信息自动入库 |
| 分析结论反哺 | 动态 | Research Agent 的深度结论、杜邦解读、评级等自动入库 |

**增量构建**：使用 `manifest.json` 记录每个文件/页的 MD5 指纹，仅对新增或变更内容重新 Embedding 和索引，避免重复计算。

### 2.3 蒙特卡洛 DCF 模拟

传统 DCF 给出单点估值，对参数假设高度敏感。本系统引入蒙特卡洛模拟将估值结果从 **确定性数值** 转化为 **概率分布**：

```python
# 核心参数采样
WACC  ~ Normal(μ=10%, σ=1.5%)，截断至 [6%, 16%]
Growth ~ Normal(μ=历史均值, σ=3%)，截断至 [0%, 30%]

# 模拟流程（默认 1000 次）
for each simulation:
    1. 采样 WACC 和 Growth
    2. 5年 FCF 预测（增长率线性衰减至永续增长率）
    3. 计算终值 TV = FCF₆ / (WACC - g)
    4. 企业价值 = Σ PV(FCF) + PV(TV) - 净债务
    5. 每股价值 = 股权价值 / 总股本
```

**输出指标**：P10（悲观）、P50（中位数）、P90（乐观）、高于现价概率、均值、标准差。

### 2.4 反思机制（Reflection）

Research Agent 完成推理后，系统自动进入反思阶段：

```
反思输入 → 研究任务 + 计划 + 推理步骤 + 结论 + 数据采集概览
                                │
                                ▼
                       LLM 输出 JSON 评估
                  {is_complete, missing_items, quality_score, suggestions}
                                │
                    ┌───────────┴───────────┐
                    │                       │
              is_complete=true        is_complete=false
              → 结束研究              → 自动补研 1-2 步
                                      → 更新结论
```

**实际效果**：在贵州茅台（600519）的分析中，反思阶段发现缺失"近期新闻、风险评估"，自动触发补充研究，质量评分从初始 6/10 提升至 8/10。

### 2.5 评测框架

采用 **规则型指标 + LLM-as-Judge** 双轨评估，并额外补充报告正文与 `AnalysisState` 的事实一致性检查：

| 评估维度 | 方法 | 权重 | 说明 |
|----------|------|------|------|
| 章节覆盖率 | 规则：关键词匹配 8 个必备章节 | 30 分 | 投资要点/公司概况/杜邦/财务/估值/行业/风险/建议 |
| 数据表格 | 规则：检测 Markdown 表格语法 | 10 分 | `|` 和 `---` 的存在性 |
| 数据引用 | 规则：正则匹配数值+单位 ≥ 10 处 | 10 分 | `\d+\.?\d*[%亿元倍]` |
| 评级一致性 | 规则：评级方向与 DCF 涨跌一致 | 5 分 | 推荐+DCF上涨 / 谨慎+DCF下跌 |
| 风险证据/传导 | 规则：统计“证据：”与“传导路径：”条目 | 诊断项 | 衡量风险段是否具备可追溯性 |
| 投资建议锚 | 规则：检测目标价/估值锚/估值区间 | 诊断项 | 衡量投资建议是否具备估值抓手 |
| 后处理修补 | 规则：读取 `postprocess_fix_count` | 诊断项 | 记录报告后处理自动补齐/增强次数 |
| 完整性 | LLM 评分 1-5 | 11.25 分 | 报告结构是否完整 |
| 数据支撑 | LLM 评分 1-5 | 11.25 分 | 分析是否有具体数据支撑 |
| 推理质量 | LLM 评分 1-5 | 11.25 分 | 因果关系/对比分析/趋势判断 |
| 可读性 | LLM 评分 1-5 | 11.25 分 | 语言专业流畅/结构清晰 |
| **总分** | | **100 分** | 规则型 55 分 + LLM 评分 45 分 |

---

## 三、性能数据与消融实验

### 3.1 当前可观测指标

系统已在 `ReportEngine` 和 `Tracer` 层补充运行级指标采集，单次分析可记录：

| 指标类别 | 已采集字段 |
|----------|------------|
| 质量指标 | 综合评分、章节覆盖率、数值引用、LLM 评分 |
| 可信度指标 | `consistency_passed`、`consistency_issue_count`、`consistency_issues` |
| 可靠性指标 | `risk_evidence_count`、`risk_transmission_count`、`investment_anchor_present`、`postprocess_fix_count`、`data_gap_disclosure_count` |
| 效率指标 | `duration_s`、`llm_calls`、`tool_calls`、`total_tokens` |
| 稳定性指标 | `success`、`errors`、`trace_id` |
| 过程指标 | `agent_steps`、`rag_hits`、`report_length`、`news_count`、`risk_count` |

这些指标会写入：
- `state.run_metrics`
- `output/ablation/*/eval_*.json`
- `output/ablation/ablation_summary.json`
- Streamlit Web 的“运行指标”标签页

### 3.2 消融实验脚本

当前推荐通过 `main.py ablation` 统一分发消融评测；`run_ablation.py` 作为兼容脚本继续保留。默认支持：

| 实验组 | 实现方式 | 目的 |
|--------|----------|------|
| `baseline` | 完整系统 | 作为基线 |
| `no_reflection` | monkey patch 跳过 `_reflect()` / `_supplement()` | 验证反思补研收益 |
| `no_rag` | monkey patch 让 `kb.query()` 返回空结果 | 验证写作期 RAG 价值 |

#### 运行方式

```bash
# 默认多股票规则评测
python main.py ablation

# 指定股票/实验组
python main.py ablation --stocks 600519 000858 --experiments baseline no_rag

# 启用 LLM-as-Judge
python main.py ablation --llm-judge
```

兼容方式：`python run_ablation.py ...`

#### 输出结果

- `ablation_summary.md`：Markdown 汇总表（含风险证据、风险传导、估值锚覆盖率、自动修补次数）
- `ablation_summary.json`：聚合指标，便于画图或写简历
- `eval_*.json`：单次实验的质量 + 可靠性 + 性能 + 稳定性指标

### 3.3 黄金集回归脚本

在消融实验之外，项目补充了 `run_regression.py` 用于固定样本回归；当前推荐通过 `main.py regression` 调用，默认仅跑 `baseline`，覆盖 `600519 / 000858 / 300750 / 600036 / 002594` 五只股票，输出统一的 Markdown/JSON 报告，并对以下阈值做自动判定：

- 成功率（默认 `100%`）
- 平均评分（默认 `70`）
- 平均章节覆盖率（默认 `87.5%`）
- 估值锚覆盖率（默认 `100%`）

当任一指标低于阈值时脚本以非零退出码结束，便于本地回归或后续接 CI。

### 3.4 一键质量门禁

项目进一步补充 `run_quality_gate.py`，并由 `main.py quality-gate` 统一分发，把 `pytest` 与 `run_regression.py` 串联为统一门禁入口，支持：

- 默认执行：测试 + 黄金集回归
- 可选跳过：`--skip-tests` / `--skip-regression`
- 阈值透传：成功率、平均评分、章节覆盖率、估值锚覆盖率
- 非零退出：任一步失败即返回非零状态码，适合作为本地检查或 CI job

### 3.5 CI 集成样板

项目提供 `.github/workflows/quality-gate.yml` 作为最小 CI 配置：

- `test` job：安装依赖后执行 `python main.py quality-gate --skip-regression`
- `regression` job：依赖 `test` job，且仅在仓库存在 `ZHIPUAI_API_KEY` 或 `OPENAI_API_KEY` secrets 时执行
- 支持通过 `OPENAI_BASE_URL` secrets 与 `LLM_PROVIDER` variables 切换 OpenAI 兼容 provider

这样既能保证默认 PR 检查先覆盖稳定的单元测试，也能在具备密钥时进一步打开真实黄金集回归。

### 3.6 部署与打包基础

项目当前已补充最小部署/打包材料：

- `.env.example`：统一环境变量模板，支持 `zhipu` / `openai` provider 切换
- `Dockerfile`：基于 `python:3.11-slim` 的轻量 Web 部署镜像，默认启动 `streamlit run web_app.py`
- `run_quality_gate.py`：本地/CI 统一质量门禁入口，便于部署前做健康检查

这套材料的目标不是做复杂生产部署，而是保证项目具备“可快速启动、可演示、可迁移”的基本工程化形态。

### 3.7 人工 Rubric 与种子 benchmark

为降低“自动评分提升但人工观感未提升”的风险，项目补充了轻量人工评审工具链，推荐通过 `main.py human-eval` 调用：

- `data/evals/human_benchmark_seed.json`：存放种子 benchmark 条目（股票、行业、关注点、关键风险）
- `app/evals/human_rubric.py`：定义人工 Rubric 维度，并把自动指标包装成评审参考材料
- `run_human_eval_pack.py`：输入一份研报路径与股票代码，输出可直接人工打分的 Markdown 模板

当前 Rubric 包含 5 个维度：结构完整性、证据充分性、推理质量、可靠性、可读性。它的作用不是替代自动评测，而是帮助后续建立小规模人工标注集，校验自动指标是否真正贴近“可用级别”研报。

### 3.7 工程优化措施

| 优化项 | 实现方式 | 效果 |
|--------|----------|------|
| 工具调用缓存 | 相同工具+相同参数 → 复用 observation | 避免重复 API 调用（反思补研时生效） |
| RAG 增量构建 | MD5 指纹比对，仅处理变更文档 | 二次启动无需重建索引 |
| 重排序缓存 | query+候选文档哈希 → 缓存 top_k 结果 | 相同查询不重复调用 LLM |
| 上下文窗口管理 | 文本 ReAct 消息裁剪 + 报告写作上下文压缩 | 降低 prompt 超长风险 |
| 运行指标采集 | Engine 记录耗时/Token/LLM调用/工具调用/错误数 | 支持性能分析和实验对比 |
| 报告后处理 | 标题归一、缺失章节补齐、风险/投资建议段增强 | 提升研报结构稳定性与可读性 |
| 配置校验 | `validate_runtime_config()` + `ensure_runtime_config()` | 运行前尽早发现非法配置 |
| FAISS 回退 | FAISS 未安装时自动切换 numpy 实现 | 降低部署依赖门槛 |
| LLM 重试 | 3 次指数退避重试（1s → 2s → 4s） | 应对 API 限流和瞬时故障 |

---

## 四、技术选型与权衡

| 决策点 | 选择 | 替代方案 | 选择理由 |
|--------|------|----------|----------|
| LLM | 智谱 GLM-4 | OpenAI GPT-4 / 通义千问 | 国产模型，支持中文金融语料，Function Calling 能力完善，价格低 |
| 向量检索 | FAISS (IndexFlatIP) | Milvus / Chroma | 无需外部服务，本地运行，对数据规模（<1万条）够用 |
| 数据源 | akshare | Tushare / Wind | 开源免费，覆盖 A 股全量数据，无需 Token 配额 |
| Agent 框架 | 自研 ReAct | LangChain / AutoGen | 可控性强，减少黑盒依赖，便于调试和定制 Prompt |
| 前端 | Streamlit | Gradio / React | Python 原生，开发效率高，足以展示分析流程 |
| Embedding | 智谱 embedding-3 (2048d) | OpenAI ada / BGE | 与 LLM 同一平台，API 调用统一，中文语义理解好 |

---

## 五、已知局限与改进方向

| 局限 | 影响 | 改进方向 |
|------|------|----------|
| akshare 数据无强校验 | 脏数据可能导致分析偏差（如异常 YoY 值） | 增加数据清洗层：异常值检测 + 缺失值插补 |
| FAISS IndexFlatIP 暴力搜索 | 知识库 >10 万条时检索变慢 | 切换 IndexIVFFlat 或 HNSW 索引 |
| 报告质量仍依赖 LLM 输出稳定性 | 不同模型/时间段可能出现结构波动 | 引入更强的结构约束与模板后处理 |
| 单一主供应商依赖 | 默认仍主要依赖智谱 API 可用性 | 扩展 OpenAI 兼容 provider 的实测切换与回归测试 |
| 评测缺少 ground truth | LLM-as-Judge 存在偏好偏差 | 引入人工标注基准集，计算与 LLM 评分的一致性 |
| DCF 净债务估算粗糙 | 用经营现金流近似现金余额 | 接入资产负债表详细数据，精确计算现金及等价物 |

---

## 附录：项目文件清单

```
├── main.py                     # 统一 CLI 入口（analyze / web / ablation / regression / quality-gate / human-eval）
├── web_app.py                  # Streamlit Web 界面（435行）
├── run_ablation.py             # 多股票基线/消融评测兼容脚本
├── run_regression.py           # 固定黄金集回归兼容脚本
├── run_quality_gate.py         # 本地 / CI 质量门禁兼容脚本
├── run_human_eval_pack.py      # 人工评审包兼容脚本
├── app/
│   ├── config.py               # 全局配置 + 运行时配置校验
│   ├── engine.py               # ReportEngine，引入运行指标采集
│   ├── llm.py                  # LLM 统一调用层（chat/chat_json/chat_with_tools）
│   ├── models.py               # 数据模型（含 run_metrics）
│   ├── agent/
│   │   ├── orchestrator.py     # 多 Agent 编排器（627行）
│   │   ├── react_agent.py      # ReAct 三阶段推理（473行）
│   │   └── tools.py            # 11 个金融工具 + 执行器
│   ├── data_source/
│   │   └── akshare_client.py   # A 股数据 API 封装与数据清洗治理
│   ├── finance/
│   │   ├── dupont.py           # 杜邦分析（ROE 三因子分解）
│   │   ├── valuation.py        # DCF + 蒙特卡洛 + 敏感性分析
│   │   ├── trend.py            # 趋势分析 + CAGR 计算
│   │   ├── risk_model.py       # 量化风险识别
│   │   └── metrics.py          # 多维量化评分
│   ├── rag/
│   │   ├── knowledge_base.py   # 知识库管理
│   │   ├── vector_store.py     # FAISS 向量存储
│   │   ├── embeddings.py       # Embedding 调用
│   │   ├── reranker.py         # LLM 重排序器
│   │   ├── pdf_loader.py       # PDF / TXT 解析
│   │   └── document.py         # 文档分块
│   ├── evals/
│   │   ├── report_eval.py      # 自动评测（规则+LLM-as-Judge+一致性诊断）
│   │   └── human_rubric.py     # 人工 Rubric 与 benchmark 评审包
│   ├── memory/
│   │   ├── store.py            # 分析记忆持久化
│   │   └── comparator.py       # 历史对比分析
│   ├── llm_providers/
│   │   ├── zhipu_provider.py   # 智谱 Provider
│   │   └── openai_provider.py  # OpenAI 兼容 Provider
│   └── utils/
│       ├── tables.py           # Markdown 表格生成
│       ├── tracer.py           # 层次化 Span 追踪
│       └── circuit_breaker.py  # 外部接口熔断器
├── tests/                      # 29 个测试文件 / 161 个测试用例
├── data/
│   ├── knowledge_base/         # PDF / TXT 知识文档目录
│   ├── kb_index/               # FAISS 索引持久化
│   ├── cache/                  # 数据缓存
│   ├── evals/                  # benchmark / 评测产物
│   ├── memory/                 # 分析记忆（history.json）
│   └── industry_map.json       # 行业分类映射
└── output/                     # 研报、trace、消融/回归/人工评审结果
```
