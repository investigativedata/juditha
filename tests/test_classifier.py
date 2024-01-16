from juditha.classify import Schema
from juditha.store import get_store


def test_classifier(eu_authorities):
    assert Schema.resolve({"LegalEntity", "Person"}) == "Person"
    assert Schema.resolve({"LegalEntity"}) == "LegalEntity"
    assert Schema.resolve({"Project"}) is None

    store = get_store()
    store.load_proxies(eu_authorities, with_schema=True)

    proxy = eu_authorities[0]
    assert store.classify(proxy.caption) == proxy.schema.name
