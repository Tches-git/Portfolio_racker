# 多用户 + PostgreSQL + 腾讯云部署改造计划

## 目标

把当前本地单用户金融消息追踪平台改造成可部署在腾讯云 4 核服务器上的多用户版本。第一阶段采用单机 Docker Compose：前端、API、worker、PostgreSQL、Redis、Caddy 运行在同一台服务器上；每个用户拥有独立数据空间；导出文件继续保存在服务器本地 volume。

第一阶段不做工作区/组织、计费、多租户权限矩阵、OAuth、短信登录、Kubernetes，也不立即接腾讯云 COS。

## 架构

- Frontend：Next.js，浏览器通过同源 `/api/v1/*` 访问 API，认证 cookie 由 API 写入。
- API：FastAPI，负责认证、组合、事件、预警、简报、研报任务和导出下载。
- Worker：第一阶段沿用现有 run manager 语义，后续可拆成 Redis 队列消费者。
- PostgreSQL：核心业务主存储，包括用户、组合、事件、预警、任务索引、导出物索引、审计日志和限流兜底记录。
- Redis：注册/登录限流优先使用，后续可扩展任务队列和缓存。
- Caddy：公网只暴露 80/443，自动 HTTPS，反代前端和 API。
- OUTPUT_DIR：保存报告正文、HTML、PDF、日志、sources JSON、事件点评等文件。

## 数据库表

- `users`：邮箱、用户名、密码哈希、角色、启用状态、注册时间、最后登录时间。第一位注册用户自动成为 `admin`，后续用户默认为 `user`。
- `watchlists`：用户组合主表，含名称、描述、刷新时间。
- `watchlist_stocks`：组合股票池，按 `watchlist_id + stock_code` 去重。
- `market_events`：用户历史事件，按 `user_id + event_id` 唯一，`related_sources` 使用 JSON/JSONB。
- `tracking_alerts`：预警处理记录，保留规则、状态、处理人、处理备注。
- `analysis_runs`：研报任务索引，保留现有 run manager 字段，JSON 字段使用 JSON/JSONB。
- `export_artifacts`：导出物索引，用于按用户控制下载权限。
- `audit_logs`：关键操作审计。
- `rate_limit_events`：Redis 不可用时的限流兜底记录。

## 认证与用户隔离

- API 提供 `POST /api/v1/auth/register`、`POST /api/v1/auth/login`、`POST /api/v1/auth/logout`、`GET /api/v1/me`。
- 登录后使用 HttpOnly Cookie 保存访问令牌，前端不直接保存 token。
- `ENABLE_SIGNUP=false` 时关闭开放注册。
- `SIGNUP_RATE_LIMIT_PER_HOUR` 与 `LOGIN_RATE_LIMIT_PER_HOUR` 控制基础限流。
- 生产部署必须设置 `AUTH_REQUIRED=true`，未登录访问核心业务 API 返回 `401`。
- 组合、事件、预警、简报、任务、导出物按当前登录用户过滤。

## 迁移步骤

1. 配置生产环境变量：`DATABASE_URL`、`REDIS_URL`、`AUTH_SECRET`、LLM API key、`AUTH_REQUIRED=true`。
2. 执行 `alembic upgrade head` 创建 PostgreSQL 表。
3. 注册第一个用户，确认角色为 `admin`。
4. 执行一次性迁移脚本，把旧 JSON/SQLite 数据导入指定管理员：
   - `tracking_watchlists.json` -> `watchlists` / `watchlist_stocks`
   - `tracking_events.json` -> `market_events`
   - `api_runs.db` -> `analysis_runs`
   - run exports -> `export_artifacts`
5. 启动 API 和前端，检查组合、事件、预警、任务和导出下载。
6. 稳定后把 `ENABLE_SIGNUP` 按需要关闭或保留。

## Docker Compose 部署

服务组成：

- `postgres`：挂载 `postgres_data`，不开放公网端口。
- `redis`：挂载 `redis_data`，不开放公网端口。
- `api`：运行 FastAPI，挂载 `output_data`。
- `worker`：第一阶段复用 API 镜像，可作为后续队列 worker 入口。
- `frontend`：运行 Next.js。
- `caddy`：公网入口，自动 HTTPS。

公网只开放：

- `80`
- `443`
- `22`

不要开放：

- `5432`
- `6379`

## 腾讯云安全组

- 入站允许 `22` 仅限你的固定 IP 或临时维护 IP。
- 入站允许 `80/443` 面向公网。
- 入站禁止 PostgreSQL、Redis、API 内部端口。
- 出站保持默认放行，保证镜像拉取、证书签发、数据源访问可用。

## 备份策略

- 每日 `pg_dump` 导出 PostgreSQL。
- 每日打包 `OUTPUT_DIR`。
- 备份保留 7 到 14 天。
- 备份文件建议定期拉到本地或后续同步腾讯云 COS。
- 每月至少做一次恢复演练：新目录启动 PostgreSQL，恢复 dump，检查 API 能启动。

## 上线检查清单

- `AUTH_SECRET` 已替换为强随机字符串。
- `AUTH_REQUIRED=true`。
- `ENABLE_SIGNUP` 符合当前开放策略。
- `.env` 没有提交到 Git。
- `alembic upgrade head` 成功。
- 第一个管理员账号可登录。
- 普通用户无法看到管理员的组合、事件、任务和导出物。
- Caddy HTTPS 可访问。
- 重启容器后 PostgreSQL、Redis 和 `OUTPUT_DIR` 数据仍存在。
- `pg_dump` 备份可生成。

## 后续阶段

- 将 run manager 的执行状态完全迁入 PostgreSQL，并把 worker 拆成 Redis 队列消费者。
- 增加管理员用户管理页。
- 增加组织/工作区模型。
- 接入腾讯云 COS 保存导出文件。
- 增加通知推送、后台定时刷新、生产级限流与审计检索。
