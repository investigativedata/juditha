from fastapi.testclient import TestClient
from followthemoney.types import registry

from canonicaller import lookup
from canonicaller.api import app
from canonicaller.store import get_store


def test_base(eu_authorities):
    store = get_store()
    for proxy in eu_authorities:
        for value in proxy.get_type_values(registry.name):
            store.set(value)

    assert lookup("european parliament") == lookup("European Parliament")
    assert lookup("foo") is None

    client = TestClient(app)

    res = client.head("/european parliament")
    assert res.status_code == 200

    res = client.get("/european parliament")
    assert res.content.decode() == "European Parliament"

    res = client.head("/foo")
    assert res.status_code == 404
    res = client.get("/foo")
    assert res.status_code == 404
