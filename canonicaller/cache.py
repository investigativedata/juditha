import logging
from functools import cache

import fakeredis
import redis
from normality import normalize

from canonicaller import settings

log = logging.getLogger(__name__)


class Cache:
    def __init__(self):
        if settings.DEBUG:
            con = fakeredis.FakeStrictRedis()
            con.ping()
            log.info("Redis connected: `fakeredis`")
        else:
            con = redis.from_url(settings.REDIS_URL)
            con.ping()
            log.info(f"Redis connected: `{settings.REDIS_URL}`")
        self.cache = con

    def set(self, value: str) -> str:
        value = value.lower()
        self.cache.set(self.get_key(value), value)
        return value

    def get(self, key: str) -> str | None:
        value = self.cache.get(self.get_key(key))
        if value is not None:
            return value.decode().strip()

    @staticmethod
    def get_key(key: str) -> str:
        return f"{settings.REDIS_PREFIX}:{normalize(key)}"


@cache
def get_cache() -> Cache:
    return Cache()
