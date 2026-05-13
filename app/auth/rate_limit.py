"""Small Redis-first rate limiter with in-process fallback."""
from __future__ import annotations

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.config import REDIS_URL
from app.db.models import RateLimitEventRecord

_memory_events: dict[str, deque[float]] = defaultdict(deque)


class RateLimitExceeded(Exception):
    """Too many attempts."""


def check_rate_limit(db: Session, *, key: str, scope: str, limit: int, window_seconds: int = 3600) -> None:
    if limit <= 0:
        return
    namespaced_key = f"{scope}:{key}"
    if _check_redis(namespaced_key, limit, window_seconds):
        return
    now = time.time()
    queue = _memory_events[namespaced_key]
    while queue and queue[0] < now - window_seconds:
        queue.popleft()
    if len(queue) >= limit:
        raise RateLimitExceeded("请求过于频繁，请稍后再试")
    queue.append(now)
    _record_database_fallback(db, key=key, scope=scope, now=now, window_seconds=window_seconds)


def _check_redis(key: str, limit: int, window_seconds: int) -> bool:
    if not REDIS_URL:
        return False
    try:
        import redis

        client = redis.Redis.from_url(REDIS_URL, socket_connect_timeout=0.2, socket_timeout=0.2)
        count = client.incr(key)
        if count == 1:
            client.expire(key, window_seconds)
        if int(count) > limit:
            raise RateLimitExceeded("请求过于频繁，请稍后再试")
        return True
    except RateLimitExceeded:
        raise
    except Exception:
        return False


def _record_database_fallback(db: Session, *, key: str, scope: str, now: float, window_seconds: int) -> None:
    try:
        cutoff = datetime.utcnow() - timedelta(seconds=window_seconds)
        db.execute(delete(RateLimitEventRecord).where(RateLimitEventRecord.created_at < cutoff))
        db.add(RateLimitEventRecord(key=key, scope=scope))
        db.commit()
    except Exception:
        db.rollback()
