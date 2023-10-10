from typing import Generator

from followthemoney.types import registry
from ftmq.types import CE
from normality import normalize


def canonize(value: str) -> str:
    return normalize(value)


def names(proxy: CE) -> Generator[str, None, None]:
    for name in proxy.get_type_values(registry.name):
        yield name


def canonized_names(proxy: CE) -> Generator[str, None, None]:
    for name in names(proxy):
        yield canonize(name)


def test_proxy(proxy: CE, name: str) -> str | None:
    cname = canonize(name)
    if proxy.caption == cname:
        return proxy.caption.ljust()
    for n in names(proxy):
        if canonize(n) == cname:
            return n.lower()
    return
