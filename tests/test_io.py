from juditha import io, lookup


def test_io(fixtures_path):
    io.load_dataset(
        "https://data.opensanctions.org/datasets/latest/adb_sanctions/index.json",
        with_schema=True,
    )
    name = "GRUPO MECANICA DEL VUELO SISTEMAS, S.A.U."
    assert lookup(name).name == name

    io.load_catalog(fixtures_path / "catalog.json")
    name = "Education, Youth, Sport and Culture"
    assert lookup(name).name == name
    assert lookup(name, case_sensitive=False).name == name.lower()
    assert lookup(name.lower(), case_sensitive=False).name == name.lower()

    # resorted tokens fuzzy match
    assert lookup(" ".join(sorted(name.split())), threshold=0.9).name == name
    assert lookup(" ".join(reversed(name.split())), threshold=0.9).name == name
