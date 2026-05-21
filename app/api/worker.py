"""独立研报任务 worker 入口。"""
from __future__ import annotations

import os

# 确保 worker 进程不再额外启动 run_manager 的后台线程。
os.environ.setdefault("RUN_MANAGER_AUTO_START", "false")

from app.api.run_manager import run_manager


def main() -> int:
    worker_id = os.getenv("WORKER_ID", "worker-compose-1")
    poll_interval = float(os.getenv("WORKER_POLL_INTERVAL", "1.0"))
    run_manager.run_external_worker(worker_id=worker_id, poll_interval=poll_interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
