# Portfolio Tracker

[![quality-gate](https://github.com/Tches-git/Portfolio_racker/actions/workflows/quality-gate.yml/badge.svg)](https://github.com/Tches-git/Portfolio_racker/actions/workflows/quality-gate.yml)

面向 A 股投资组合的金融消息追踪与智能研报生成平台。项目把公告、行情、新闻、券商观点和本地知识库统一为可追踪事件流，在高影响事件出现时触发预警、简报、事件点评和深度研报更新，形成“消息追踪 -> 风险预警 -> 研究任务 -> 交付归档”的闭环。

## 当前状态

这个仓库已经从早期的研报生成脚本升级为可本地运行、可 Docker 部署的产品化工作区：

- **组合工作台**：管理 Watchlist，自选股票联动事件、预警、风险评分和任务交付。
- **事件追踪**：聚合市场消息，进行去重、影响分类、状态处理和历史沉淀。
- **多智能体研报**：基于 Planner、Market Analyst、Event Analyst、Risk Reviewer、Report Writer、Citation Auditor 的固定角色链路生成研报。
- **RAG 知识库**：支持本地公司资料、行业材料、公开 benchmark、缓存语料和外部金融知识源导入。
- **评测与质量页**：内置 tracking eval、agent eval、finance QA/RAG eval、RAG 引用可信度评测和 `/quality` 指标页。
- **前后端分离**：FastAPI 提供业务 API，Next.js 提供中文产品界面，Docker Compose 提供 PostgreSQL、Redis、API、Worker、Frontend、Caddy 一体化部署。

## 功能一览

| 模块 | 能力 |
|------|------|
| 报告中心 | 展示组合、事件、预警、简报、研报交付和运行审计 |
| 组合跟踪 | Watchlist 风险分、处理率、优先动作、受影响股票排序 |
| 事件流 | 公告/行情/新闻/观点归一化为 `MarketEvent`，支持语义去重和多来源证据保留 |
| 预警中心 | 高影响、风险暴露、来源降级、多来源共振、监管风险等规则 |
| 研究任务 | 单股研报、事件点评、研报更新、任务取消/重试、Worker 异步消费 |
| 导出中心 | Markdown、HTML、PDF、来源索引、Trace 和运行日志分类归档 |
| 评测体系 | 回归测试、质量门禁、事件 benchmark、Agent 任务集、RAG 引用评测 |

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端 | Python, FastAPI, Uvicorn, SQLAlchemy, Alembic |
| 任务与存储 | PostgreSQL, Redis, 本地 SQLite 兼容模式 |
| 研究引擎 | AutoGen AgentChat, RAG, FAISS, akshare, 自定义金融分析工具链 |
| 前端 | Next.js 15, React 19, TypeScript |
| 部署 | Docker, Docker Compose, Caddy |
| 质量 | Pytest, GitHub Actions, TypeScript typecheck |

## 快速开始

### 1. 本地开发

```bash
# 后端依赖
pip install -r requirements.txt

# 环境变量
cp .env.example .env

# 启动 API
python main.py api
```

另开终端启动前端：

```bash
cd frontend
npm install
npm run dev
```

访问地址：

- 前端工作区：`http://localhost:3000`
- API 健康检查：`http://localhost:8000/api/v1/health`
- 质量指标页：`http://localhost:3000/quality`

### 2. Docker Compose 部署

```bash
cp .env.example .env
docker compose up --build
```

默认会启动：

- `postgres`：业务数据库
- `redis`：任务队列与缓存
- `api`：FastAPI 服务
- `worker`：研报任务消费者
- `frontend`：Next.js 前端
- `caddy`：反向代理与 HTTPS 入口

部署前建议修改 `.env` 中的 `POSTGRES_PASSWORD`、`AUTH_SECRET`、`APP_DOMAIN` 和 LLM API Key。

## 常用命令

```bash
# 生成单只股票研报
python main.py analyze 600519 --eval

# 附加 PDF / 图片 / 文本材料
python main.py analyze 600519 --doc docs/sample.txt --doc data/knowledge_base/example.pdf

# 启动 API
python main.py api

# 质量门禁
python main.py quality-gate --skip-regression

# 全量测试
pytest -q

# 前端类型检查
cd frontend && npm run typecheck
```

## 评测与知识库

```bash
# 金融事件去重 / 分类 / 预警规则评测
python main.py tracking-eval

# 构建真实事件 benchmark 初始样本
python main.py build-tracking-benchmark --stock-codes 600519,300750,002594 --target-count 150 --live

# 项目内金融研究 Agent 任务评测
python main.py agent-eval

# 公共金融 QA/RAG benchmark 本地子集
python main.py finance-qa-predict --benchmark <benchmark-path> --limit 5
python main.py finance-qa-eval --benchmark <benchmark-path> --predictions <predictions-path>

# 外部金融知识源目录与 RAG 摘要导入
python main.py kb-sources list
python main.py kb-sources import --market china --rebuild-kb

# 将本地公开缓存沉淀为 A 股公司知识库
python main.py kb-cache import --rebuild-kb

# 大规模本地公开语料扩容
python main.py kb-bulk import --rebuild-kb

# 研报 RAG 引用可信度评测
python main.py rag-eval --stock-code 600519
```

更多评测口径见 [docs/BENCHMARKS.md](docs/BENCHMARKS.md) 和 [docs/RESUME_METRICS.md](docs/RESUME_METRICS.md)。

## 产品页面

| 页面 | 路径 |
|------|------|
| 报告中心 | `/` |
| 事件追踪 | `/events` |
| 组合跟踪 | `/watchlist` |
| 运行中心 | `/runs` |
| 股票工作台 | `/stocks/{stockCode}` |
| 市场详情 | `/markets/{stockCode}` |
| 质量指标 | `/quality` |

主要 API 包括：

- `/api/v1/events`
- `/api/v1/events/{event_id}`
- `/api/v1/events/{event_id}/analyze`
- `/api/v1/watchlists`
- `/api/v1/alerts`
- `/api/v1/alerts/rules`
- `/api/v1/briefing/daily`
- `/api/v1/runs`

## 系统概览

```text
数据源接入
  -> 事件归一化
  -> 去重与历史沉淀
  -> 影响分类与预警
  -> 简报 / 事件点评 / 研报更新
  -> 导出归档 / Trace / 质量评测
```

多智能体研报链路：

```text
Planner -> Market Analyst -> Event Analyst -> Risk Reviewer -> Report Writer -> Citation Auditor
   |              |                |                |               |                 |
研究规划       财务估值          事件分析         风险复核        研报写作          引用审计
```

## 仓库结构

```text
├── main.py                 # 统一 CLI 入口
├── app/                    # 后端 API、Agent、RAG、追踪、评测、数据库模块
├── frontend/               # Next.js 产品前端
├── alembic/                # 数据库迁移
├── data/                   # benchmark、知识库、外部知识源目录和导入 manifest
├── docs/                   # 技术文档、部署说明、演示材料和评测口径
├── deploy/                 # Caddy 与云部署脚本
├── scripts/                # 质量门禁、回归、消融、人工评审辅助脚本
├── tests/                  # 后端、API、前端契约与评测测试
└── output/                 # 本地产出目录，建议不提交
```

## 文档

- [docs/TECHNICAL_DOC.md](docs/TECHNICAL_DOC.md)：技术设计细节
- [docs/BENCHMARKS.md](docs/BENCHMARKS.md)：评测集与指标口径
- [docs/RESUME_PROJECT.md](docs/RESUME_PROJECT.md)：项目经历材料
- [docs/RESUME_METRICS.md](docs/RESUME_METRICS.md)：简历指标说明
- [docs/平台使用说明.md](docs/平台使用说明.md)：中文使用说明
- [docs/求职演示手册.md](docs/求职演示手册.md)：演示脚本与讲解路径

## 仓库展示建议

公开展示时建议保留源码、测试、示例配置和文档，同时避免提交以下本地产物：

- `.env`
- `output/`
- `data/cache/`
- `data/kb_index/`
- `data/memory/`
- `__pycache__/`
- `.pytest_cache/`

## 免责声明

本项目生成的研究报告和风险提示仅供学习、研究与工程展示参考，不构成任何投资建议。金融市场存在风险，真实投资决策请以专业持牌机构意见和个人风险承受能力为准。
