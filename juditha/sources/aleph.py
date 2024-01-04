from typing import TYPE_CHECKING

from alephclient.api import AlephAPI
from ftmq.util import make_proxy
from pydantic import BaseModel

from juditha.settings import FUZZY_THRESHOLD
from juditha.util import find_best, proxy_names

if TYPE_CHECKING:
    from juditha.source import Source


class Aleph(BaseModel):
    host: str
    api_key: str | None = None
    api: AlephAPI

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data) -> "Aleph":
        data["api"] = AlephAPI(data.get("host"), data.get("api_key"))
        super().__init__(**data)

    def lookup(
        self, value: str, threshold: float | None = FUZZY_THRESHOLD
    ) -> str | None:
        for result in self.api.search(value):
            proxy = make_proxy(result)
            names = {s for s in proxy_names(proxy)}
            match = find_best(value, names, threshold=threshold)
            if match:
                return match

    @staticmethod
    def from_source(source: "Source") -> "Aleph":
        return Aleph(**source.config)
