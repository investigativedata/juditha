from juditha.clean import clean_value, normalize


def test_normalize():
    # lowercase
    assert normalize("BAR") == "bar"

    # fingerprints
    assert normalize(" Siemens, Aktiengesellschaft") == "ag siemens"

    # no digits
    assert normalize("Jane 123") == "jane"

    # remove double characters
    assert normalize("Foo bar") == "bar fo"
    assert normalize("Foooofoooo bar") == "bar fofo"

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
    # assert normalize("é") == "e" FIXME
    assert normalize("éé") == "e"
    assert normalize("عبد الحميد دشتي") == "alhmyd bd dshty"
    assert normalize("ヴラジーミル・プーチン") == "puchin vurajimiru"

    # clean value: only clean whitespace
    assert clean_value("Foo  Bar") == "Foo Bar"
    assert clean_value(" Foo,  Bar") == "Foo, Bar"
    value = """
    Foo
    Bar
    """
    assert clean_value(value) == "Foo Bar"
    assert clean_value("Foo, 10. Bar") == "Foo, 10. Bar"
