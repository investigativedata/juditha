from fastapi.testclient import TestClient

from juditha.api import app
from juditha.io import load_proxies


def test_api(fixtures_path):
    load_proxies(fixtures_path / "eu_authorities.ftm.json", with_schema=True)

    client = TestClient(app)

    res = client.head("/European parliament")
    assert res.status_code == 200

    res = client.get("/European parliament?threshold=0.8")
    assert res.content.decode() == "European Parliament"

    res = client.head("/shdfjkoshfaj")
    assert res.status_code == 404
    res = client.get("/dshjka")
    assert res.status_code == 404

    res = client.get("/European parlament?threshold=0.8&format=json")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "European Parliament"
    assert data["original"] == "European parlament"
    assert data["score"] < 1

    res = client.get("/_classify/European parliament")
    assert res.status_code == 200
    assert res.content.decode() == "PublicBody"
