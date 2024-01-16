import logging
from enum import StrEnum
from functools import cache
from typing import Generator, Set

import fakeredis
import redis
from followthemoney.types import registry
from metaphone import doublemetaphone
from nomenklatura.entity import CE

from juditha import settings
from juditha.clean import clean_value, normalize, text_tokenize
from juditha.match import Match, extract, find_best

log = logging.getLogger(__name__)


class Prefix(StrEnum):
    SCHEMA = "S"
    NORM = "N"
    METAPHONE = "M"


class Cache:
    def __init__(self, url: str | None = None):
        if settings.DEBUG:
            con = fakeredis.FakeStrictRedis()
            con.ping()
            log.info("Redis connected: `fakeredis`")
        else:
            url = url or settings.REDIS_URL
            con = redis.from_url(url)
            con.ping()
            log.info(f"Redis connected: `{url}`")
        self.cache: redis.Redis = con

    def get(self, key: str, prefix: str | None = None) -> str | None:
        value = self.cache.get(self.get_key(key, prefix))
        if value is not None:
            return value.decode()

    def index(self, name: str) -> None:
        """
        Index a name:
        1.) Ensure useful name via keying
        2.) Set exact match for direct lookup via exists
        3.) Add name to normalized lookup SET
        4.) Add metaphones to inverted lookup index
        """
        key = normalize(name)
        if not key:
            return
        self.cache.set(self.get_key(name), 1)
        self.sadd(key.replace(" ", ""), Prefix.NORM, name)
        for token in key.split():
            if len(token) > 3:
                for m in doublemetaphone(token):
                    if m:
                        self.sadd(m, Prefix.METAPHONE, key.replace(" ", ""))

    def index_schema(self, name: str, schema: str) -> None:
        """
        Store schema in SET for given name.
        """
        key = normalize(name)
        if not key:
            return
        self.sadd(key, Prefix.SCHEMA, schema)

    def index_proxy(
        self,
        proxy: CE,
        schema: str | None = "LegalEntity",
        with_schema: bool | None = False,
    ) -> None:
        """
        Index proxy names and optional it's schema (for classification queries)
        """
        if schema is not None and not proxy.schema.is_a(schema):
            return
        for name in proxy.get_type_values(registry.name):
            self.index(name)
            if with_schema:
                self.index_schema(name, proxy.schema.name)

    def lookup(
        self,
        name: str,
        case_sensitive: bool | None = True,
        threshold: float | None = settings.FUZZY_THRESHOLD,
    ) -> Match | None:
        """
        Test a given value against the index.
        1.) Try exact match
        2.) Find best match by normalized lookup
        3.) Find best match by metaphone index lookup
        """
        threshold = threshold or settings.FUZZY_THRESHOLD
        name = clean_value(name)

        # exact lookup
        if self.exists(name):
            if not case_sensitive:
                name = name.lower()
            return Match(name=name, original=name, score=1)

        # normalized lookup
        match = find_best(
            name,
            self.get_normalized_candidates(name),
            preprocess="lower" if not case_sensitive else None,
        )
        if match and match.score > threshold:
            return match

        # metaphone index lookup
        match = find_best(
            name,
            self.get_metaphone_candidates(name),
            preprocess="lower" if not case_sensitive else None,
        )
        if match and match.score > threshold:
            return match

    def extract(
        self,
        text: str,
        case_sensitive: bool | None = True,
        threshold: float | None = settings.FUZZY_THRESHOLD,
    ) -> Generator[Match, None, None]:
        """
        Extract known names from text
        """
        threshold = threshold or settings.FUZZY_THRESHOLD

        if not case_sensitive:
            text = text.lower()

        for match in extract(text, self.get_metaphone_candidates(text)):
            if match.score > threshold:
                yield match

    def get_normalized_candidates(self, name: str) -> Generator[str, None, None]:
        yield from self.smembers(normalize(name), Prefix.NORM)

    def get_metaphone_candidates(self, name: str) -> Generator[str, None, None]:
        for key in text_tokenize(name):
            for cache_key in self.smembers(key, Prefix.METAPHONE):
                yield from self.smembers(cache_key, Prefix.NORM)

    def exists(self, key: str, prefix: str | None = None) -> bool:
        return bool(int(self.cache.exists(self.get_key(key, prefix))))

    def smembers(self, key: str, prefix: str) -> Set[str]:
        key = self.get_key(key, prefix)
        return {v.decode() for v in self.cache.smembers(key)}

    def sadd(self, key: str, prefix: str, *values: str) -> int:
        key = self.get_key(key, prefix)
        return self.cache.sadd(key, *(clean_value(v) for v in values))

    @staticmethod
    def get_key(key: str, prefix: str | None = None) -> bytes:
        if not key:
            raise ValueError(f"Invalid key: `{key}`")
        key = clean_value(key)
        if prefix:
            return f"{settings.REDIS_PREFIX}:{key}:{prefix}".encode()
        return f"{settings.REDIS_PREFIX}:{key}".encode()


@cache
def get_cache(url: str | None = None) -> Cache:
    return Cache(url)
