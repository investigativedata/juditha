from juditha.sources import Aleph


def test_aleph(fixtures_path):
    aleph = Aleph(host="https://aleph.occrp.org")
    res = aleph.lookup("Vladimir Putin")
    assert res == "vladimir putin"
