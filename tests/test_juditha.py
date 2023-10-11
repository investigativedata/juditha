from juditha import Juditha


def test_juditha():
    j = Juditha("https://juditha.ftm.store")
    assert j.lookup("Angela Merkel") == "angela merkel"
