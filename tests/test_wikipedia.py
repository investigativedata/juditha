from canonicaller.sources import Wikipedia


def test_wikipedia():
    wiki = Wikipedia(url="https://de.wikipedia.org")
    assert wiki.lookup("Angela Merkel") == "angela merkel"
