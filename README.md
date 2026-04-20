# 📊 金融研报智能分析系统

> 基于 **ReAct Agent + RAG** 的 A 股深度研报自动生成系统，支持 CLI、Web 工作台、质量评测、消融实验、黄金集回归与质量门禁。

---

## 项目亮点

- **完整分析链路**：输入股票代码后，自动完成数据采集、研究推理、RAG 增强写作与报告生成
- **11 个金融分析工具**：覆盖杜邦分析、DCF + 蒙特卡洛估值、可比公司估值、趋势分析、风险识别等核心环节
- **质量与可信度导向**：内置规则评分、LLM-as-Judge、事实一致性检查、风险证据/传导、估值锚与数据降级披露指标
- **双入口体验**：既可通过 `main.py` 统一 CLI 使用，也可通过 Streamlit Web 工作台进行交互式浏览
- **工程化能力完整**：包含消融实验、固定黄金集回归、质量门禁、最小 GitHub Actions CI 样板
- **测试覆盖完善**：当前包含 **29 个测试文件 / 161 个测试用例**

---

## 这个项目解决什么问题

传统“自动写研报”往往停留在模板拼接或单轮问答。本项目更关注：

1. **分析过程是否像真实研究流程**：先规划，再执行工具研究，再反思补充
2. **结论是否有数据和估值支撑**：不仅输出观点，还输出估值、风险、同行对比和财务拆解
3. **结果是否可评估、可回归、可持续优化**：不是只看一篇研报，而是能看评分、回归、消融和质量门禁

---

## 快速导航

- [快速开始](#快速开始)
- [核心能力](#核心能力)
- [系统概览](#系统概览)
- [仓库结构](#仓库结构)
- [评测与工程化能力](#评测与工程化能力)
- [补充文档](#补充文档)
- [产出物展示](#-产出物展示)

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

最小配置示例：

```env
LLM_PROVIDER=zhipu
ZHIPUAI_API_KEY=your_api_key_here
```

如使用 OpenAI 兼容接口：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://your-compatible-endpoint/v1
```

### 3. 运行项目

```bash
# 默认分析 600519
python main.py 600519

# 显式 analyze 子命令
python main.py analyze 000858 --eval

# 启动 Web 工作台
python main.py web
```

### 4. 常用扩展命令

```bash
# 重建知识库
python main.py analyze 600519 --rebuild-kb

# 消融实验
python main.py ablation

# 黄金集回归
python main.py regression

# 质量门禁
python main.py quality-gate
```

---

## 核心能力

- 🔍 **杜邦分析**：ROE 三因素/五因素分解，定位盈利驱动因子
- 💰 **DCF + 蒙特卡洛估值**：自由现金流折现模型 + 概率分布估值区间
- 📈 **敏感性分析**：关键假设参数的敏感性矩阵
- 🏢 **可比公司估值**：同行 PE / PB / PS 横向对比
- 📊 **趋势与 CAGR 分析**：营收 / 利润 / 现金流趋势拆解
- ⭐ **量化综合评分**：多维度加权打分体系
- ⚠️ **风险识别**：财务风险、经营风险、行业风险自动识别
- 📝 **研报自动评测**：规则型评分 + LLM-as-Judge + 一致性诊断

---

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
| **Web 工作台** | 多级页面浏览、进度反馈、质量仪表板与历史入口 |

### 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.10+** | 核心开发语言 |
| **Streamlit** | Web 交互界面 |
| **智谱 GLM-5.1 / OpenAI Compatible** | 大语言模型推理与生成 |
| **FAISS** | 向量相似度检索 |
| **akshare** | A 股金融数据获取 |
| **NumPy / Pandas** | 数值计算与数据处理 |

---

## 仓库结构

```text
├── main.py                 # 统一 CLI 入口（analyze / web / ablation / regression / quality-gate / human-eval）
├── web_app.py              # Streamlit Web 界面
├── run_ablation.py         # 消融评测兼容脚本
├── run_regression.py       # 黄金集回归兼容脚本
├── run_quality_gate.py     # 一键质量门禁兼容脚本
├── run_human_eval_pack.py  # 人工评审包生成兼容脚本
├── docs/                   # 补充文档（技术说明 / 仓库整理 / 项目展示材料）
├── app/                    # 核心源码
├── data/                   # 知识库、行业映射、评测种子数据等
├── tests/                  # 29 个测试文件 / 161 个测试用例
└── output/                 # 本地产出目录（建议不提交）
```

---

## 评测与工程化能力

### 统一入口

推荐统一通过 `main.py` 使用：

```bash
python main.py analyze 600519 --eval
python main.py web
python main.py ablation
python main.py regression
python main.py quality-gate
python main.py human-eval output/report_xxx.md --stock-code 600519
```

### 工程化支持

- **消融实验**：`baseline / no_reflection / no_rag`
- **固定黄金集回归**：持续检查成功率、平均评分、章节覆盖率、估值锚覆盖率
- **质量门禁**：支持本地与 CI 统一执行
- **最小 CI 样板**：`.github/workflows/quality-gate.yml`

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

## Web 工作台

当前 Web 工作台已整理为更清晰的多级结构：

- `首页概览 / 分析工作台 / 结果浏览` 三层视图分离
- 结果浏览内部再按 `总览 / 分析 / 诊断` 分组组织标签页
- 支持结果总览卡片、质量/可靠性仪表板、最近结果继续入口、历史筛选、历史 master-detail 回看、加载占位与失败分类引导

如仅用于 GitHub 展示，建议在 README 首页保留架构、能力、快速开始和评测流程，把更长的技术细节放到 `docs/` 下。

---

## Docker 运行（轻量部署）

```bash
# 构建镜像
docker build -t fin-report-agent .

# 运行 Web 应用（需提供 .env）
docker run --rm -p 8501:8501 --env-file .env fin-report-agent
```

启动后访问 `http://localhost:8501`。

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
