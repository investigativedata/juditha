from typing import TYPE_CHECKING

import requests
from normality import normalize
from pydantic import BaseModel, HttpUrl

from juditha.settings import FUZZY_THRESHOLD
from juditha.util import find_best

if TYPE_CHECKING:
    from juditha.source import Source


class Wikipedia(BaseModel):
    url: HttpUrl
    api_url: HttpUrl

    def __init__(self, **data):
        if "api_url" not in data:
            data["api_url"] = data["url"] + "/w/api.php"
        super().__init__(**data)

    def lookup(
        self, value: str, threshold: float | None = FUZZY_THRESHOLD
    ) -> str | None:
        value = normalize(value)
        query = {
            "action": "opensearch",
            "format": "json",
            "formatversion": 2,
            "search": value,
            "limit": 10,
        }
        res = requests.get(self.api_url, params=query)
        assert res.ok
        res = res.json()
        candidates = {n for n in res[1]}
        return find_best(value, candidates, threshold=threshold)

    @staticmethod
    def from_source(source: "Source") -> "Wikipedia":
        return Wikipedia(**source.config)
