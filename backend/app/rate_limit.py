import time

from redis import Redis
from redis.exceptions import RedisError

from .config import get_settings

_memory_store: dict[str, tuple[int, float]] = {}  # key -> (count, window_start_ts)


def _prefix(key: str) -> str:
    s = get_settings()
    return f"{s.rate_limit_test_prefix}{key}" if s.rate_limit_test_prefix else key


def _redis_client() -> Redis | None:
    s = get_settings()
    if not s.redis_url:
        return None
    try:
        return Redis.from_url(s.redis_url, decode_responses=True)
    except Exception:
        return None


def hit(key: str, limit: int, window_sec: int) -> bool:
    """
    Return True if within limit after this hit, False if blocked.
    """
    key = _prefix(key)
    r = _redis_client()
    now = int(time.time())
    if r:
        try:
            pipe = r.pipeline()
            pipe.incr(key)
            pipe.expire(key, window_sec)
            count, _ = pipe.execute()
            return int(count) <= limit
        except RedisError:
            pass
    # Fallback memory
    count, start = _memory_store.get(key, (0, now))
    if now - start >= window_sec:
        count, start = 0, now
    count += 1
    _memory_store[key] = (count, start)
    return count <= limit


def clear_rate_limit_test_keys() -> None:
    s = get_settings()
    prefix = s.rate_limit_test_prefix
    if not prefix:
        return
    r = _redis_client()
    if r:
        for k in r.scan_iter(f"{prefix}*"):
            r.delete(k)
    for k in list(_memory_store.keys()):
        if k.startswith(prefix):
            del _memory_store[k]

