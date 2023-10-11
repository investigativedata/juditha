"""
Use a juditha api endpoint as a source ;)
"""

from typing import TYPE_CHECKING

import requests
from pydantic import BaseModel, HttpUrl

if TYPE_CHECKING:
    from juditha.source import Source


class Juditha(BaseModel):
    url: HttpUrl

    def lookup(self, name: str) -> str | None:
        res = requests.get(f"{self.url}/{name}")
        if res.ok:
            return res.content.decode().strip()
        return None

    def classify(self, name: str) -> str | None:
        res = requests.get(f"{self.url}/_classify/{name}")
        if res.ok:
            return res.content.decode().strip()
        return None

    @staticmethod
    def from_source(source: "Source") -> "Juditha":
        return Juditha(**source.config)
