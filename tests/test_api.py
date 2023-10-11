from fastapi.testclient import TestClient

from juditha.api import app
from juditha.io import load_proxies


def test_api(fixtures_path):
    load_proxies(fixtures_path / "eu_authorities.ftm.json")

    client = TestClient(app)

    res = client.head("/European parliament")
    assert res.status_code == 200

    res = client.get("/european Parliament")
    assert res.content.decode() == "european parliament"

    res = client.head("/shdfjkoshfaj")
    assert res.status_code == 404
    res = client.get("/dshjka")
    assert res.status_code == 404

    res = client.get("/European parlament")
    assert res.status_code == 404

    res = client.get("/European parlament?fuzzy=true")
    assert res.status_code == 200

    res = client.get("/_classify/European parliament")
    assert res.status_code == 200
    assert res.content.decode() == "PublicBody"
