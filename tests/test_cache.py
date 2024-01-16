import pytest

from juditha.cache import Cache, Prefix
from juditha.clean import normalize, tokenize


def test_cache(eu_authorities):
    cache = Cache()
    for proxy in eu_authorities:
        cache.index_proxy(proxy, with_schema=True)

    assert not cache.exists("foo")
    assert cache.exists("European Parliament")
    assert cache.get("European Parliament") == "1"

    # normalized token
    key = normalize("European Parliament").replace(" ", "")
    assert cache.exists(key, Prefix.NORM)

    tested = False
    for token in tokenize("European Parliament"):
        assert cache.exists(token, Prefix.METAPHONE)
        assert key in cache.smembers(token, Prefix.METAPHONE)
        tested = True
    assert tested

    # fuzzy lookup
    assert cache.lookup("European Parliament").name == "European Parliament"
    assert (
        cache.lookup("european parliament", threshold=0.5).name == "European Parliament"
    )
    assert (
        cache.lookup("europen parlament", threshold=0.5).name == "European Parliament"
    )

    # invalid names
    cache.index("-")
    assert not cache.exists("-")
    with pytest.raises(ValueError):
        assert not cache.exists(None)
    with pytest.raises(ValueError):
        assert not cache.exists("")


def test_cache_extract():
    cache = Cache()
    cache.index("Juditha Dommer")
    cache.index("Johann Pachelbel")
    txt = "Ten months later, J. Pachelbel married Judith M. Drommer (Trummert), daughter of a coppersmith."
    res = list(cache.extract(txt, threshold=0.5))
    assert len(res) == 2
    assert res[0].score > res[1].score
    assert res[0].name == "Juditha Dommer"
    assert res[0].original == "Judith M. Drommer"
