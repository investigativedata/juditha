from typing import TYPE_CHECKING

from alephclient.api import AlephAPI
from ftmq.util import make_proxy
from pydantic import BaseModel

from juditha.util import test_proxy

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

    def lookup(self, value: str) -> str | None:
        for result in self.api.search(value):
            proxy = make_proxy(result)
            name = test_proxy(proxy, value)
            if name is not None:
                return name

    @staticmethod
    def from_source(source: "Source") -> "Aleph":
        return Aleph(**source.config)
