from juditha.sources import Aleph, Wikipedia


def test_sources(fixtures_path):
    aleph = Aleph(host="https://aleph.occrp.org")
    assert aleph.lookup("Vladimir Putin") == "VLADIMIR PUTIN"

    wiki = Wikipedia(url="https://de.wikipedia.org")
    assert wiki.lookup("angela merkel") == "Angela Merkel"
