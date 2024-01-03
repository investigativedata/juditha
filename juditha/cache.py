import logging
from enum import StrEnum
from functools import cache
from typing import Set

import fakeredis
import redis
from thefuzz import fuzz

from juditha import settings
from juditha.clean import clean_value, normalize
from juditha.util import find_best

log = logging.getLogger(__name__)


class Prefix(StrEnum):
    SCHEMA = "SCHEMA"
    NORM = "NORM"
    FUZZY = "FUZZY"


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

    def set(self, key: str, value: str, prefix: str | None = None) -> None:
        self.cache.set(self.get_key(key, prefix), clean_value(value))

    def set_name(self, value: str) -> None:
        self.cache.set(self.get_key(value), 1)

    def set_fuzzy(self, value: str, name: str) -> None:
        self.cache.set(self.get_key(value, Prefix.FUZZY), clean_value(name))

    def exists(self, value: str) -> bool:
        return bool(self.cache.exists(self.get_key(value)))

    def get(self, key: str, prefix: str | None = None) -> str | None:
        value = self.cache.get(self.get_key(key, prefix))
        if value is not None:
            return value.decode()

    def index(self, value: str) -> None:
        """
        Index a value name:
        1.) Ensure useful value
        2.) Set exact match for simple key lookup
        3.) Add value to normalized lookup SET
        """
        key = normalize(value)
        if not key:
            return
        self.set_name(value)
        self.sadd(key, Prefix.NORM, value)

    def index_schema(self, value: str, schema: str) -> None:
        """
        Store schema for given name.
        1.) Store direct lookup
        2.) Add to normalized SET
        """
        key = normalize(value)
        if not key:
            return
        self.set(value, schema, prefix=Prefix.SCHEMA)
        self.sadd(key, Prefix.SCHEMA, schema)

    def search(
        self,
        value: str,
        case_sensitive: bool | None = False,
        threshold: float | None = settings.FUZZY_THRESHOLD,
    ) -> str | None:
        """
        Test a given value against the index.
        1.) Try exact match
        2.) Try fuzzy match
        3.) Find best fuzzy match by normalized lookup
        """
        value = clean_value(value)
        if self.exists(value):
            return value
        fuzzy_result = self.get(value, prefix=Prefix.FUZZY)
        if fuzzy_result and fuzz.ratio(fuzzy_result, value) >= threshold * 100:
            return fuzzy_result
        match = find_best(
            value,
            self.smembers(normalize(value), Prefix.NORM),
            case_sensitive=case_sensitive,
            threshold=threshold,
        )
        if match:
            # set shortcut if default threshold:
            if threshold >= settings.FUZZY_THRESHOLD:
                self.set(value, match, Prefix.FUZZY)
            return match

    def smembers(self, key: str, prefix: str) -> Set[str]:
        key = self.get_key(key, prefix) + b"#SET"
        return {v.decode() for v in self.cache.smembers(key)}

    def sadd(self, key: str, prefix: str, *values: str) -> int:
        key = self.get_key(key, prefix) + b"#SET"
        return self.cache.sadd(key, *(clean_value(v) for v in values))

    @staticmethod
    def get_key(key: str, prefix: str | None = None) -> bytes:
        key = clean_value(key)
        if prefix:
            return f"{settings.REDIS_PREFIX}:{key}:{prefix}".encode()
        return f"{settings.REDIS_PREFIX}:{key}".encode()


@cache
def get_cache() -> Cache:
    return Cache()
