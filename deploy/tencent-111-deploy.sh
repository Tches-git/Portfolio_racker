#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/home/ubuntu/Portfolio_racker}"
PUBLIC_URL="${PUBLIC_URL:-http://portfolio-racker.49.232.61.59.nip.io}"
COMPOSE_FILES=(-f docker-compose.yml -f deploy/docker-compose.tencent-111.yml)

wait_for_url() {
  local name="$1"
  local url="$2"
  local attempts="${3:-30}"
  local delay="${4:-2}"

  for ((i = 1; i <= attempts; i++)); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "OK: ${name}"
      return 0
    fi
    sleep "$delay"
  done

  echo "ERROR: ${name} 健康检查失败：${url}" >&2
  return 1
}

cd "$PROJECT_DIR"

if [[ ! -f .env ]]; then
  echo "ERROR: .env 不存在，请先在服务器上配置生产环境变量。" >&2
  exit 1
fi

if docker ps >/dev/null 2>&1; then
  DOCKER=(docker)
else
  DOCKER=(sudo -n docker)
fi

if [[ "${SKIP_GIT_PULL:-0}" == "1" ]]; then
  echo "==> 跳过 git pull（SKIP_GIT_PULL=1）"
else
  echo "==> 更新代码"
  if ! git pull --ff-only; then
    echo "ERROR: git pull 失败。请确认 tencent-111 的 deploy key 已添加到 GitHub 仓库。" >&2
    exit 1
  fi
fi

echo "==> 构建镜像"
"${DOCKER[@]}" compose "${COMPOSE_FILES[@]}" build api frontend worker

echo "==> 启动服务"
"${DOCKER[@]}" compose "${COMPOSE_FILES[@]}" up -d postgres redis api frontend worker

echo "==> 当前容器"
"${DOCKER[@]}" compose "${COMPOSE_FILES[@]}" ps

echo "==> 健康检查"
wait_for_url "API health" "http://127.0.0.1:3011/api/v1/health"
wait_for_url "前端登录页" "http://127.0.0.1:3011/login"

echo "部署完成：${PUBLIC_URL}/login"
