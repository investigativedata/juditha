from juditha.store import get_store, lookup


class Juditha:
    def __init__(self, url: str) -> "Juditha":
        self.store = get_store(juditha_url=url)

    def lookup(self, value: str) -> str | None:
        return self.store.lookup(value)


__version__ = "0.0.3"
__all__ = ["lookup"]
