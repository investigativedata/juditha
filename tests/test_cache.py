from juditha.cache import Cache
from juditha.util import proxy_names


def test_cache(eu_authorities):
    cache = Cache()
    for proxy in eu_authorities:
        for value in proxy_names(proxy):
            cache.index(value)
            cache.index_schema(value, proxy.schema.name)

    assert not cache.exists("foo")
    assert cache.exists("European Parliament")
    assert cache.get("European Parliament") == "1"
    assert not cache.exists("european parliament")
    assert cache.search("european parliament") == "European Parliament"
    assert cache.get("european parliament:FUZZY") == "European Parliament"
    assert cache.search("european parliament") == "European Parliament"

    # fingerprinting fuzziness threshold
    assert cache.search("parliament european") is None
    assert cache.search("parliament european", threshold=0.5) == "European Parliament"

    cache.index("-")
    assert not cache.exists("-")
