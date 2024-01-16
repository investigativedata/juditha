from functools import cache, lru_cache
from typing import Iterable

from ftmq.types import CE

from juditha import settings
from juditha.cache import Prefix, get_cache
from juditha.classify import Schema
from juditha.clean import normalize
from juditha.match import Match


class Store:
    def __init__(self, redis_url: str | None = None):
        self.cache = get_cache(redis_url)
        self.index = self.cache.index
        self.index_proxy = self.cache.index_proxy
        self.lookup = self.cache.lookup
        self.extract = self.cache.extract

    def classify(self, name: str) -> str | None:
        schemata = self.cache.smembers(normalize(name), Prefix.SCHEMA)
        return Schema.resolve(schemata)

    def load_proxies(
        self,
        proxies: Iterable[CE],
        schema: str | None = "LegalEntity",
        with_schema: bool | None = False,
    ) -> int:
        ix = 0
        for proxy in proxies:
            self.cache.index_proxy(proxy, schema=schema, with_schema=with_schema)
            ix += 1
        return ix

    def load_names(self, names: Iterable[str]) -> int:
        ix = 0
        for name in names:
            self.cache.index(name)
            ix += 1
        return ix


@cache
def get_store(redis_url: str | None = None) -> Store:
    return Store(redis_url)


@lru_cache(100_000)
def lookup(
    value: str,
    threshold: float | None = settings.FUZZY_THRESHOLD,
    case_sensitive: bool | None = True,
) -> Match | None:
    store = get_store()
    return store.lookup(value, threshold=threshold, case_sensitive=case_sensitive)


@lru_cache(100_000)
def classify(value: str) -> str | None:
    store = get_store()
    return store.classify(value)
