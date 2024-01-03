from juditha import io, lookup


def test_io(fixtures_path):
    io.load_dataset(
        "https://data.opensanctions.org/datasets/latest/adb_sanctions/index.json",
        with_schema=True,
    )
    name = "GRUPO MECANICA DEL VUELO SISTEMAS, S.A.U."
    assert lookup(name) == name
    assert lookup(name.lower()) == name

    io.load_catalog(fixtures_path / "catalog.json")
    name = "Education, Youth, Sport and Culture"
    assert lookup(name) == name

    # fingerprinting with lower threshold
    assert lookup(" ".join(sorted(name.split())), threshold=0.9) == name
    assert lookup(" ".join(reversed(name.split())), threshold=0.9) == name
