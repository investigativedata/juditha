from canonicaller.cache import Cache
from canonicaller.util import names


def test_cache(eu_authorities):
    cache = Cache()
    for proxy in eu_authorities:
        for value in names(proxy):
            cache.set(value)

    assert cache.get("european parliament") == cache.get("European Parliament")
    assert cache.get("foo") is None
