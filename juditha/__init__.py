from juditha.settings import FUZZY
from juditha.store import classify, get_store, lookup


class Juditha:
    def __init__(self, url: str) -> "Juditha":
        self.store = get_store(juditha_url=url)

    def lookup(self, name: str, fuzzy: bool | None = FUZZY) -> str | None:
        return self.store.lookup(name, fuzzy=fuzzy)

    def classify(self, name: str) -> str | None:
        return self.store.classify(name)


__version__ = "0.0.3"
__all__ = ["lookup", "classify"]
