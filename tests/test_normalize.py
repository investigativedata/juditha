from juditha.clean import clean_value, normalize


def test_normalize():
    # lowercase
    assert normalize("BAR") == "bar"

    # fingerprints, no whitespace
    assert normalize(" Siemens, Aktiengesellschaft") == "agsiemens"

    # no digits
    assert normalize("Jane 123") == "jane"

    # remove double characters
    assert normalize("Foo bar") == "barfo"
    assert normalize("Foooofoooo bar") == "barfofo"

    # nothing
    assert normalize("") is None
    assert normalize(" ") is None
    assert normalize("Mrs. -") is None
    assert normalize(None) is None
    assert normalize(False) is None
    assert normalize(1) is None
    assert normalize(0) is None
    assert normalize("123") is None

    # ascii
    assert normalize("éé") == "e"
    assert normalize("عبد الحميد دشتي") == "alhmydbdshty"
    assert normalize("ヴラジーミル・プーチン") == "puchinvurajimiru"

    # clean value: only clean whitespace
    assert clean_value("Foo  Bar") == "Foo Bar"
    assert clean_value(" Foo  Bar") == "Foo Bar"
    value = """
    Foo
    Bar
    """
    assert clean_value(value) == "Foo Bar"
