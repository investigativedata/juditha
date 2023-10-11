from juditha.cache import get_cache


def test_index():
    cache = get_cache()
    cache.index("Angela Merkel")
    assert cache.get("Angela Merkel") == "angela merkel"
    assert cache.fuzzy("Angela Mrkel") == "angela merkel"

    cache.index("ETHNIKO KENTRO EREVNAS KAI TECHNOLOGIKIS")
    assert (
        cache.fuzzy("f ETHNIKO KENTRO EREVNAS KAI TECHNOLOGIKIS V")
        == "ethniko kentro erevnas kai technologikis"  # noqa
    )
