from juditha.cache import Cache, Prefix
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

    # cache is populated with fuzzy values after sucessful lookup
    assert not cache.exists("european parliament")
    assert cache.get("european parliament", Prefix.FUZZY) is None
    assert cache.search("european parliament") == "European Parliament"
    # now it is there:
    assert cache.get("european parliament", Prefix.FUZZY) == "European Parliament"
    assert cache.search("european parliament") == "European Parliament"

    # fingerprinting fuzziness threshold
    assert cache.search("parliament european") is None
    assert cache.search("parliament european", threshold=0.5) == "European Parliament"

    # not a real name
    cache.index("-")
    assert not cache.exists("-")
