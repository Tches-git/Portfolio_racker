# 真实用户冒烟检查清单

用于验证“新用户空白工作区 + 多用户隔离 + 首页闭环”。本清单不要求清空旧数据，也不要提交 `.env`、API key 或生产密钥。

## 本地冒烟

1. 启动数据库并执行迁移，确认 API 可访问 `/api/v1/health`。
2. 启动 Next.js，浏览器访问首页时应跳转到 `/login?next=/`。
3. 注册一个全新账号，登录后进入首页。
4. 首页必须显示“创建第一个组合”空态，组合、事件、预警、任务均为 0，不展示旧组合、旧事件或默认股票池。
5. 创建组合，例如名称“冒烟组合”，股票代码使用手动输入；创建成功后应进入 `/watchlist/{watchlist_id}`。
6. 点击刷新组合事件，成功后组合详情、首页、事件预警台只展示当前账号数据。
7. 打开 `/events?view=alerts`，可看到待处理预警或明确的中文空态。
8. 打开 `/markets/{stock_code}`，行情页只读展示，不创建组合、不写入事件历史。
9. 从事件或股票入口生成研报任务，进入 `/runs` 或 `/runs/{run_id}` 后只看到当前账号任务。
10. 退出登录后访问 `/`、`/events`、`/runs`、`/watchlist` 应跳转登录页；直接访问业务 API 应返回 `401 {"detail":"请先登录"}`。

## tencent-111 冒烟

1. 在服务器 `.env` 中设置 `AUTH_REQUIRED=true`、`ENABLE_SIGNUP=true`、强随机 `AUTH_SECRET`、PostgreSQL/Redis 连接、LLM API key。
2. 使用 Docker Compose 启动 `postgres`、`redis`、`api`、`frontend`、`caddy`，确认 `api` 日志中 `alembic upgrade head` 成功。
3. 通过公网入口访问，不直接暴露 `5432` 或 `6379`。
4. 重复“本地冒烟”的注册、空态、创建组合、刷新、事件预警、行情、任务、退出登录流程。
5. 验证同源 `/api/v1/*` 请求携带 HttpOnly cookie；如登录后刷新丢失登录态，检查 Caddy 反代域名、`AUTH_COOKIE_NAME` 和浏览器 cookie 域。

## 失败排查

- 登录页或首页 500：先看 Next.js 日志，再看 API `/api/v1/me` 和 `/api/v1/ui/dashboard`。
- 注册失败：检查 `ENABLE_SIGNUP`、注册限流、数据库连接和唯一邮箱/用户名。
- 空用户出现旧数据：检查对应接口是否按当前 `user_id` 查询，禁止回退到全局 JSON/SQLite。
- 刷新组合失败：检查数据源超时、API 日志、组合是否属于当前用户。
- 导出下载串号：检查 `export_artifacts.user_id` 和下载接口是否按当前用户查 artifact。
