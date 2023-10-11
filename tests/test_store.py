from juditha.store import get_store


def test_store(fixtures_path):
    store = get_store(fixtures_path / "store.yml")
    assert store.lookup("Bayreuther Festspiele") == "bayreuther festspiele"
