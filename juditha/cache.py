import logging
from enum import StrEnum
from functools import cache
from typing import Set

import fakeredis
import redis
from fingerprints import generate as fp
from normality import normalize

from juditha import settings
from juditha.index import find_best, tokenize
from juditha.util import canonize

log = logging.getLogger(__name__)


class Prefix(StrEnum):
    SCHEMA = "SCHEMA"
    TOKEN = "TOKEN"


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

    def set(self, value: str) -> str | None:
        value = canonize(value)
        if not value:
            return
        self.cache.set(self.get_key(value), value)
        return value

    def get(self, key: str) -> str | None:
        value = self.cache.get(self.get_key(key))
        if value is not None:
            return value.decode().strip()

    def index(self, value: str) -> int:
        value = canonize(value)
        if not value:
            return 0
        # store fingerprint
        fp_value = fp(value)
        if fp_value:
            self.cache.set(self.get_key(fp_value), value)
        # store inverted tokens
        ix = 1
        for token in tokenize(value):
            ix += self.sadd(token, Prefix.TOKEN, value)
        return ix

    def add_schema(self, value: str, schema: str) -> None:
        value = canonize(value)
        self.sadd(value, Prefix.SCHEMA, schema)

    def fuzzy(
        self, value: str, threshold: int | None = settings.FUZZY_SCORE
    ) -> str | None:
        value = canonize(value)
        res = self.get(fp(value))
        if res is not None:
            return res
        for token in tokenize(value):
            match = find_best(
                value, self.smembers(token, Prefix.TOKEN), threshold=threshold
            )
            if match:
                return match

    def smembers(self, key: str, prefix: str) -> Set[str]:
        key = f"{self.get_key(key)}:{prefix}"
        res: Set[bytes] = self.cache.smembers(key)
        return {v.decode() for v in res}

    def sadd(self, key: str, prefix: str, *values: str) -> int:
        key = f"{self.get_key(key)}:{prefix}"
        return self.cache.sadd(key, *values)

    @staticmethod
    def get_key(key: str) -> str:
        return f"{settings.REDIS_PREFIX}:{normalize(key)}"


@cache
def get_cache() -> Cache:
    return Cache()
