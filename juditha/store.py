from functools import cache, lru_cache

from ftmq.model.mixins import YamlMixin
from ftmq.types import CE
from pydantic import BaseModel

from juditha.cache import Cache, Prefix, get_cache
from juditha.classify import Schema
from juditha.settings import FUZZY, JUDITHA, JUDITHA_CONFIG
from juditha.source import Source
from juditha.util import canonized_names


class Store(BaseModel, YamlMixin):
    sources: list[Source] = []
    cache: Cache | None = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.cache = get_cache()

    def lookup(self, value: str, fuzzy: bool | None = FUZZY) -> str | None:
        res = self.cache.get(value)
        if res is not None:
            return res
        for source in self.sources:
            res = source.lookup(value)
            if res is not None:
                return self.cache.set(value)
        if fuzzy:
            return self.cache.fuzzy(value)

    def classify(self, name: str) -> str | None:
        schemata = self.cache.smembers(name, Prefix.SCHEMA)
        return Schema.resolve(schemata)

    def add(self, value: str, fuzzy: bool | None = FUZZY) -> None:
        self.cache.set(value)
        if fuzzy:
            self.cache.index(value)

    def add_proxy(self, proxy: CE, fuzzy: bool | None = FUZZY) -> None:
        for name in canonized_names(proxy):
            self.add(name, fuzzy=fuzzy)
        for name, schema in Schema.from_proxy(proxy):
            self.cache.add_schema(name, schema)


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
def lookup(value: str, fuzzy: bool | None = FUZZY) -> str | None:
    store = get_store()
    return store.lookup(value, fuzzy=fuzzy)


@lru_cache(100_000)
def classify(value: str) -> str | None:
    store = get_store()
    return store.classify(value)
