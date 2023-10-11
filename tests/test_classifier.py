from ftmq.util import make_proxy

from juditha.classify import Schema
from juditha.store import get_store


def test_classifier(eu_authorities):
    tested = False
    for proxy in eu_authorities:
        for name, schema in Schema.from_proxy(proxy):
            assert isinstance(name, str)
            assert schema == proxy.schema.name
            tested = True
    assert tested

    proxy = make_proxy({"id": 1, "schema": "Asset"})
    assert len([x for x in Schema.from_proxy(proxy)]) == 0

    assert Schema.resolve({"LegalEntity", "Person"}) == "Person"
    assert Schema.resolve({"LegalEntity"}) == "LegalEntity"
    assert Schema.resolve({"Project"}) is None

    store = get_store()
    for proxy in eu_authorities:
        store.add_proxy(proxy)

    assert store.classify(proxy.caption) == proxy.schema.name
