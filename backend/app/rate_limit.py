"""Simple rate limiting utilities for login attempts."""

from __future__ import annotations

import os
import time

import redis

PREFIX = os.getenv("RATE_LIMIT_TEST_PREFIX", "")
WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))
LIMIT = int(os.getenv("RATE_LIMIT_LOGIN_PER_MIN", "10"))
r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

_MEMORY_STORE: dict[str, list[int]] = {}


def key(user_or_ip: str) -> str:
    return f"{PREFIX}login:{user_or_ip}"


def check_and_inc(user_or_ip: str) -> bool:
    k = key(user_or_ip)
    now = int(time.time())
    try:
        with r.pipeline() as p:
            p.zremrangebyscore(k, 0, now - WINDOW)
            p.zadd(k, {str(now): now})
            p.zcard(k)
            p.expire(k, WINDOW)
            _, _, count, _ = p.execute()
        return int(count) <= LIMIT
    except Exception:
        # Fallback in-memory store if Redis is unavailable
        hits = [ts for ts in _MEMORY_STORE.get(k, []) if ts > now - WINDOW]
        hits.append(now)
        _MEMORY_STORE[k] = hits
        return len(hits) <= LIMIT


def clear_test_keys() -> None:
    if not PREFIX:
        return
    try:
        for k in r.scan_iter(f"{PREFIX}*"):
            r.delete(k)
    except Exception:
        pass
    for k in list(_MEMORY_STORE.keys()):
        if k.startswith(PREFIX):
            del _MEMORY_STORE[k]

