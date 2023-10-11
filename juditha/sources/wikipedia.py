from typing import TYPE_CHECKING

import requests
from pydantic import BaseModel, HttpUrl

from juditha.util import canonize

if TYPE_CHECKING:
    from juditha.source import Source


class Wikipedia(BaseModel):
    url: HttpUrl
    api_url: HttpUrl

    def __init__(self, **data):
        if "api_url" not in data:
            data["api_url"] = data["url"] + "/w/api.php"
        super().__init__(**data)

    def lookup(self, value: str) -> str | None:
        value = canonize(value)
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
        for name in res[1]:
            if canonize(name) == value:
                return name.lower()

    @staticmethod
    def from_source(source: "Source") -> "Wikipedia":
        return Wikipedia(**source.config)
