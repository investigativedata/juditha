from functools import cache, lru_cache

from ftmq.model.mixins import YamlMixin
from ftmq.types import CE
from pydantic import BaseModel

from juditha.cache import Cache, Prefix, get_cache
from juditha.classify import Schema
from juditha.clean import normalize
from juditha.settings import FUZZY_THRESHOLD, JUDITHA, JUDITHA_CONFIG
from juditha.source import Source
from juditha.util import proxy_names


class Store(BaseModel, YamlMixin):
    sources: list[Source] = []
    cache: Cache | None = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.cache = get_cache()

    def lookup(
        self, value: str, threshold: float | None = FUZZY_THRESHOLD
    ) -> str | None:
        res = self.cache.search(value, threshold=threshold)
        if res is not None:
            return res
        for source in self.sources:
            res = source.lookup(value)
            if res is not None:
                self.cache.set_fuzzy(res, value)
                return res

    def classify(self, name: str) -> str | None:
        schemata = self.cache.smembers(normalize(name), Prefix.SCHEMA)
        return Schema.resolve(schemata)

    def index(self, value: str) -> None:
        self.cache.index(value)

    def index_proxy(self, proxy: CE, with_schema: bool | None = False) -> None:
        if not proxy.schema.is_a("LegalEntity"):
            return
        for name in proxy_names(proxy):
            self.index(name)
        if with_schema:
            for name, schema in Schema.from_proxy(proxy):
                self.cache.index_schema(name, schema)


@cache
def get_store(uri: str | None = None, juditha_url: str | None = None) -> Store:
    uri = uri or JUDITHA_CONFIG
    if uri:
        return Store.from_path(uri)
    url = juditha_url or JUDITHA
    if url:
        return Store(sources=[Source(klass="juditha", config={"url": url})])
    return Store()


@lru_cache(100_000)
def lookup(value: str, threshold: float | None = FUZZY_THRESHOLD) -> str | None:
    store = get_store()
    return store.lookup(value, threshold=threshold)


@lru_cache(100_000)
def classify(value: str) -> str | None:
    store = get_store()
    return store.classify(value)
