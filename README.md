# Portfolio Tracker

[![quality-gate](https://github.com/Tches-git/Portfolio_racker/actions/workflows/quality-gate.yml/badge.svg)](https://github.com/Tches-git/Portfolio_racker/actions/workflows/quality-gate.yml)

金融消息追踪与智能研报生成平台。项目把 A 股公告、行情、研报观点和风险舆情归一化为可追踪事件流，并在高影响事件出现时触发研究任务，形成“消息追踪 -> 风险预警 -> 每日简报 -> 研报更新”的闭环。

## 项目亮点

| 能力 | 说明 |
|------|------|
| 金融事件追踪 | 聚合公告、交易所披露、实时行情、券商观点，统一为 `MarketEvent` |
| 组合跟踪 | 维护 Watchlist，自选股票池联动事件流、预警中心和每日简报 |
| 智能研报生成 | 基于 ReAct Agent、RAG、金融工具链生成 A 股深度研究报告 |
| 事件驱动研究 | 单条事件可触发“事件点评 / 更新研报”任务，接入任务中心 |
| 可解释质量体系 | 内置估值锚、风险证据、来源降级、质量门禁、回归测试 |
| 产品化前端 | FastAPI + Next.js，覆盖事件追踪、事件详情、组合、预警、简报和股票工作台 |

## 在线/本地体验

```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env

# 3. 启动 FastAPI
python main.py api

# 4. 启动 Next.js 前端
cd frontend
npm install
npm run dev
```

访问地址：

- 前端工作台：`http://localhost:3000`
- API 健康检查：`http://localhost:8000/api/v1/health`
- 事件追踪：`/events`
- 组合跟踪：`/watchlist`
- 预警中心：`/alerts`
- 每日简报：`/briefing`

## 核心工作流

```text
数据源接入 -> 事件归一化 -> 去重与历史沉淀 -> 影响分类 -> 预警/简报 -> 触发研报更新
```

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端 API | Python, FastAPI, Uvicorn |
| 研究引擎 | ReAct Agent, RAG, FAISS, 金融分析工具链 |
| 数据源 | akshare, CNInfo/交易所披露适配, 本地历史记忆 |
| 前端 | Next.js, React, TypeScript |
| 工程化 | Pytest, GitHub Actions, Docker |

## 快速命令

```bash
# 生成单只股票研报
python main.py analyze 600519 --eval

# 附加 PDF / 图片 / 文本材料
python main.py analyze 600519 --doc docs/sample.txt --doc data/knowledge_base/example.pdf

# 质量门禁
python main.py quality-gate --skip-regression

# 全量测试
pytest -q
```

## 系统概览

### ReAct Agent 三阶段推理

```
Planning（规划） → Acting（执行） → Reflecting（反思）
     ↓                  ↓                  ↓
  制定分析计划      调用金融工具链       质量自检与补充
```

### 核心组件

| 组件 | 说明 |
|------|------|
| **ReAct Agent** | 基于“思考-行动-观察”循环的智能推理引擎 |
| **RAG 知识库** | 基于 FAISS 的行业知识增强模块 |
| **金融工具链** | 11 个专业金融分析工具，覆盖数据获取到估值建模 |
| **评测模块** | 自动化研报质量评分与诊断 |
| **Memory** | 历史分析结果沉淀与回看、对比 |
| **产品前端** | Next.js 工作区、事件追踪、组合跟踪、预警/简报、运行中心与任务详情入口 |

## 仓库结构

```text
├── main.py                 # 统一 CLI 入口（analyze / api / ablation / regression / quality-gate / human-eval）
├── run_ablation.py         # 消融评测兼容脚本
├── run_regression.py       # 黄金集回归兼容脚本
├── run_quality_gate.py     # 一键质量门禁兼容脚本
├── run_human_eval_pack.py  # 人工评审包生成兼容脚本
├── docs/                   # 补充文档（技术说明 / 仓库整理 / 项目展示材料）
├── app/                    # 核心源码
├── frontend/               # Next.js 产品前端
├── data/                   # 知识库、行业映射、评测种子数据等
├── tests/                  # 自动化测试与前端契约测试
└── output/                 # 本地产出目录（建议不提交）
```

---

## 评测与工程化能力

### 统一入口

推荐统一通过 `main.py` 使用：

```bash
python main.py analyze 600519 --eval
python main.py api
python main.py ablation
python main.py regression
python main.py quality-gate
python main.py human-eval output/report_xxx.md --stock-code 600519
```

### 工程化支持

- **消融实验**：`baseline / no_reflection / no_rag`
- **固定黄金集回归**：持续检查成功率、平均评分、章节覆盖率、估值锚覆盖率
- **质量门禁**：支持本地与 CI 统一执行
- **GitHub Actions 流水线**：`.github/workflows/quality-gate.yml` 会运行后端测试、质量门禁和前端类型检查

---

## 补充文档

- [`docs/REPOSITORY_GUIDE.md`](docs/REPOSITORY_GUIDE.md) — GitHub 发布与仓库整理说明
- [`docs/TECHNICAL_DOC.md`](docs/TECHNICAL_DOC.md) — 技术设计细节
- [`docs/IMPROVEMENT_SUGGESTIONS.md`](docs/IMPROVEMENT_SUGGESTIONS.md) — 后续优化清单
- [`docs/RESUME_PROJECT.md`](docs/RESUME_PROJECT.md) — 项目经历 / 简历版材料

---

## GitHub 展示建议

公开仓库时，建议保留源码、测试、示例配置与文档，忽略以下本地产物：

- `.env`
- `output/`
- `data/cache/`
- `data/kb_index/`
- `data/memory/`
- `__pycache__/` / `.pytest_cache/`

如果仓库首页只面向开源读者，建议把更长的技术实现细节放到 `docs/` 下，而把 README 保持为“项目门面”。

---

## 产品前端

旧 Python Web 界面已移除。当前 Web 入口由 FastAPI + Next.js 承接：

- `python main.py api`：启动 FastAPI 兼容接口，提供研报、历史、运行任务、事件追踪、预警、简报与组合跟踪 API
- `frontend/`：独立前端骨架（Next.js），当前消费兼容 API，并已补上动态 sidebar、全局运行中心、独立任务中心、事件追踪 / 事件详情 / 组合跟踪 / 预警中心 / 每日简报 / 股票工作台等页面，以及浏览器触发分析与状态轮询入口
- 事件追踪接口包括 `/api/v1/events`、`/api/v1/events/{event_id}`、`/api/v1/events/{event_id}/analyze`、`/api/v1/watchlists`、`/api/v1/alerts`、`/api/v1/briefing/daily`
- CLI/API 仍支持同时导出 Markdown / HTML 展示版 / 来源索引 JSON；环境已安装 `reportlab` 且可注册中文字体时，会额外生成 PDF 展示版

如仅用于 GitHub 展示，建议在 README 首页保留架构、能力、快速开始和评测流程，把更长的技术细节放到 `docs/` 下。

---

## Docker 运行（轻量部署）

```bash
# 构建镜像
docker build -t fin-report-agent .

# 运行 API 服务（需提供 .env）
docker run --rm -p 8000:8000 --env-file .env fin-report-agent
```

启动后访问 `http://localhost:8000/api/v1/health`。

---

## 📊 产出物展示

### 研报样例（贵州茅台 600519）

系统自动生成 **9000+ 字深度研报**，综合评分 **83.0/100**：

```
# 贵州茅台 深度研究报告

## 一、核心观点
1. 茅台品牌护城河极深，毛利率连续多年保持在91%以上，远超行业平均65%的水平
2. 财务结构持续优化，资产负债率从21.4%降至12.8%，权益乘数保持1.15低水平
3. DCF估值显示每股内在价值555.57元，蒙特卡洛模拟仅0.1%概率高于现价
4. 资产周转率0.44倍，远低于行业均值，但呈上升趋势
5. ROE从31.4%降至24.6%，主要源于净利率下降而非周转率恶化

## 二、公司概况与商业模式 ...
## 三、盈利能力拆解（杜邦分析）... 含多年ROE三因子分解表
## 四、财务深度分析 ............. 含增长质量/利润质量/资产负债表深度分析
## 五、估值分析 ................. 含DCF表/蒙特卡洛分布/敏感性矩阵/可比估值
## 六、行业与竞争格局 ........... 含同行5家公司ROE/PE/毛利率横向对比表
## 七、风险提示 ................. 5条风险，每条含传导路径和影响幅度
## 八、投资建议 ................. 含评级/目标价区间/催化剂/核心跟踪变量
```

> 示例研报会输出到 `output/` 目录；公开仓库时建议不提交运行产物，而是通过 README 截图/节选或单独 release 附件展示样例。

### 自动评测结果

当前评测模块同时支持 **规则评分** 与 **LLM-as-Judge**，并可输出结构化 JSON 指标，便于做基线对比、消融分析和简历量化。

| 维度 | 说明 |
|------|------|
| 章节覆盖率 | 8 个必备章节的规则匹配 |
| 数据表格 | Markdown 表格存在性检测 |
| 数据引用 | 数值+单位引用次数统计 |
| 评级一致性 | 评级方向与 DCF 涨跌是否一致 |
| 事实一致性 | 报告正文是否覆盖评级、DCF 数值、核心风险、新闻、同行信息 |
| 风险可靠性 | 风险证据条目数、风险传导路径条目数 |
| 投资建议可靠性 | 是否包含估值锚 / 目标价区间 |
| 数据降级披露 | 是否显式说明现金流/资产负债/同行/新闻/DCF 等缺口 |
| LLM 评分 | 完整性 / 数据支撑 / 推理质量 / 可读性 |
| 运行指标 | 耗时、LLM调用数、工具调用数、总 Tokens、错误数 |
| 后处理指标 | 自动修补次数、修补项明细 |

---

## 🧪 消融实验与量化评测

系统提供 `run_ablation.py` 统一运行基线/消融评测，可同时输出 **质量、耗时、Token、成功率、工具调用数、Agent 步数、RAG 命中数、风险证据/传导指标、自动修补次数** 等指标。

### 默认实验设计

| 实验组 | 说明 |
|--------|------|
| **baseline** | 完整系统（Agent + RAG + Reflection） |
| **no_reflection** | 移除反思阶段（跳过质量自检和补充研究） |
| **no_rag** | 移除写作阶段 RAG 检索 |

### 运行方式

```bash
# 多股票规则评测（默认 600519 / 000858 / 300750）
python main.py ablation

# 仅跑指定股票与实验组
python main.py ablation --stocks 600519 000858 --experiments baseline no_rag

# 启用 LLM-as-Judge（成本更高）
python main.py ablation --llm-judge
```

> 兼容方式：`python run_ablation.py ...`

### 输出产物

- `output/ablation/ablation_summary.md`：汇总表与相对 Baseline 变化
- `output/ablation/ablation_summary.json`：便于后续画图/做简历量化
- `output/ablation/<stock_code>/report_*.md`：各实验组研报
- `output/ablation/<stock_code>/eval_*.md/.json`：单次评测详情与运行指标

### 黄金集回归

为避免后续优化出现“主观感觉变好、实际指标回退”，项目新增 `run_regression.py` 固定黄金样本回归脚本，默认覆盖 `600519 / 000858 / 300750 / 600036 / 002594` 五只股票，并对成功率、平均评分、章节覆盖率、估值锚覆盖率做阈值判定。

```bash
# 运行固定黄金集回归
python main.py regression

# 自定义阈值
python main.py regression --min-avg-score 75 --min-anchor-coverage 80
```

> 兼容方式：`python run_regression.py ...`

输出产物：
- `output/regression/regression_summary.md`
- `output/regression/regression_summary.json`

### 一键质量门禁

项目新增 `run_quality_gate.py`，用于把 **单元测试 + 黄金集回归** 串成一个本地/CI 都可直接复用的质量门禁入口：

```bash
# 默认执行 pytest + 黄金集回归
python main.py quality-gate

# 仅跑黄金集回归
python main.py quality-gate --skip-tests

# 仅跑测试
python main.py quality-gate --skip-regression

# 调整回归阈值
python main.py quality-gate --min-avg-score 75 --min-anchor-coverage 80
```

> 兼容方式：`python run_quality_gate.py ...`

脚本会在任一步失败时返回非零退出码，便于后续接 GitHub Actions / 本地 pre-push 检查。

### CI 样板

项目已补充最小 GitHub Actions 样板：`.github/workflows/quality-gate.yml`

- `test` job：默认执行 `python main.py quality-gate --skip-regression`
- `regression` job：仅在配置了 `ZHIPUAI_API_KEY` 或 `OPENAI_API_KEY` secrets 时运行黄金集回归

如需启用：
1. 在仓库 Secrets 中配置 `ZHIPUAI_API_KEY` 或 `OPENAI_API_KEY`
2. 如走 OpenAI 兼容接口，可额外配置 `OPENAI_BASE_URL`
3. 可通过仓库 Variables 配置 `LLM_PROVIDER`

### 人工 Rubric 与种子标注集

项目补充了轻量人工评审工具链：

- `data/evals/human_benchmark_seed.json`：小型种子 benchmark（股票/行业/关注点/关键风险）
- `app/evals/human_rubric.py`：人工 Rubric 定义 + 自动指标参考拼装
- `run_human_eval_pack.py`：根据一份已生成研报输出人工评审 Markdown 模板

```bash
python main.py human-eval output/report_600519_xxx.md --stock-code 600519
```

> 兼容方式：`python run_human_eval_pack.py ...`

适合后续逐步沉淀人工 rubric、标注集和自动评测之间的对照关系。

### 当前评测维度

- **质量**：章节覆盖、表格、数值引用、评级一致性、LLM 评分
- **可信度**：`consistency_passed`、`consistency_issue_count`、`consistency_issues`
- **可靠性**：风险证据数、风险传导路径数、估值锚覆盖率、自动修补次数、数据降级披露次数
- **效率**：总耗时、LLM 调用次数、总 Token
- **稳定性**：成功率、错误数、trace_id
- **过程指标**：Agent 步数、工具调用数、RAG 命中数、报告字数、新闻数、风险数

> 完整结果见 [`output/ablation/ablation_summary.md`](output/ablation/ablation_summary.md)

---

## ⚠️ 免责声明

本系统生成的研究报告仅供学习与研究参考，**不构成任何投资建议**。金融市场存在风险，投资决策请以专业持牌机构的研究报告为准。使用本系统所产生的任何投资损失，作者不承担任何责任。
