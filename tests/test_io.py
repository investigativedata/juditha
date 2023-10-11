from juditha import io, lookup


def test_io(fixtures_path):
    io.load_dataset(
        "https://data.opensanctions.org/datasets/latest/adb_sanctions/index.json"
    )
    assert lookup("GRUPO MECANICA DEL VUELO SISTEMAS, S.A.U.") is not None

    # io.load_catalog(fixtures_path / "catalog.yml")
    # assert lookup("Alternative for India Development") is not None
