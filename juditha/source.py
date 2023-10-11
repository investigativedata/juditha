from typing import Any, Literal, TypeAlias

from pydantic import BaseModel

from juditha.sources.aleph import Aleph
from juditha.sources.wikipedia import Wikipedia

Stores = {
    "aleph": Aleph,
    "wikipedia": Wikipedia,
}
Sources: TypeAlias = Literal[tuple(Stores.keys())]


class Source(BaseModel):
    klass: Sources
    name: str | None = None
    config: dict[str, Any]
    store: Aleph | Wikipedia = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.name = self.name or f"{self.klass}-{hash(repr(self.config))}"
        self.store = Stores[self.klass].from_source(self)

    def lookup(self, value: str) -> str | None:
        return self.store.lookup(value)
