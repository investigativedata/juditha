from juditha import scan
from juditha.store import get_store


def test_scan():
    txt = "Ten months later, Pachelbel married Juditha Drommer (Trummert), daughter of a coppersmith."
    ngrams = [x for x in scan.get_token_keys(txt)]
    assert len(ngrams) == 77
    assert "juditha" in ngrams
    assert None not in ngrams

    res = [x for x in scan.search_candidates(["juditha dommer"], txt, threshold=0.5)]
    assert ("juditha drommer", "juditha dommer") in res

    store = get_store()
    store.index("Juditha Dommer")
    res = [x for x in store.scan_text(txt, threshold=0.5)]
    assert ("juditha drommer", "juditha dommer") in res
