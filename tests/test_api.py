from fastapi.testclient import TestClient

from juditha.api import app


def test_api():
    client = TestClient(app)

    res = client.head("/European parliament")
    assert res.status_code == 200

    res = client.get("/european Parliament")
    assert res.content.decode() == "european parliament"

    res = client.head("/shdfjkoshfaj")
    assert res.status_code == 404
    res = client.get("/dshjka")
    assert res.status_code == 404
