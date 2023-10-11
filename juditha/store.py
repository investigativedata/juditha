from functools import cache, lru_cache

from ftmq.model.mixins import YamlMixin
from pydantic import BaseModel

from juditha.cache import Cache, get_cache
from juditha.settings import JUDITHA_CONFIG
from juditha.source import Source


class Store(BaseModel, YamlMixin):
    sources: list[Source] = []
    cache: Cache | None = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.cache = get_cache()

    def lookup(self, value: str) -> str | None:
        res = self.cache.get(value)
        if res is not None:
            return res
        for source in self.sources:
            res = source.lookup(value)
            if res is not None:
                return self.cache.set(value)


@cache
def get_store(uri: str | None = None) -> Store:
    uri = uri or JUDITHA_CONFIG
    if uri:
        return Store.from_path(uri)
    return Store()


@lru_cache(100_000)
def lookup(value: str) -> str | None:
    store = get_store()
    return store.lookup(value)
