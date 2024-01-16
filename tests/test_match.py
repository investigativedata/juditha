from juditha import match


def test_match():
    candidates = ["Judith Drommer", "Juditha Dommer"]
    name = "Juditha Dommer"
    res = match.find_best(name, candidates)
    assert isinstance(res, match.Match)
    assert res.original == "Juditha Dommer"
    assert res.name == "Juditha Dommer"
    assert res.score == 1

    candidates = ["Johann Pachelbel", "Juditha Dommer"]
    txt = "Ten months later, Pachelbel married Judith Drommer (Trummert), daughter of a coppersmith."
    tested = False
    for res in match.extract(txt, candidates):
        assert isinstance(res, match.Match)
        assert res.original == "Judith Drommer"
        assert res.name == "Juditha Dommer"
        assert res.score < 1
        tested = True
    assert tested

    txt = "Ten months later, J. Pachelbel married Judith Drommer (Trummert), daughter of a coppersmith."
    # sorted by score
    res = [m for m in match.extract(txt, candidates, unique=True)]
    assert res[0].score > res[1].score
    assert res[0].name == "Juditha Dommer"
    assert res[0].original == "Judith Drommer"
    assert res[1].name == "Johann Pachelbel"
    assert res[1].original == "J. Pachelbel"

    txt = "Ten months later, J. Pachelbel married Judith Drommer (Trummert), daughter of a coppersmith."
    # in order of text apperance
    res = [m for m in match.extract(txt, candidates, unique=False, sorted=False)]
    assert res[0].score < res[1].score
    assert res[0].name == "Johann Pachelbel"
    assert res[0].original == "J. Pachelbel"
    assert res[1].name == "Juditha Dommer"
    assert res[1].original == "Judith Drommer"
