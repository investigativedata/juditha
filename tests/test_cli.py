from pathlib import Path

from typer.testing import CliRunner

from juditha.cli import cli

runner = CliRunner()


def test_cli(fixtures_path: Path):
    runner.invoke(cli, ["load", "-i", fixtures_path / "names.txt"])
    res = runner.invoke(cli, ["lookup", "Jane Doe"])
    assert res.exit_code == 0
    assert res.output.strip() == "Jane Doe"

    res = runner.invoke(cli, ["lookup", "doe, jane"])
    assert res.exit_code == 0
    assert "not found" in res.output
    res = runner.invoke(cli, ["lookup", "doe, jane", "--threshold", "0.5"])
    assert res.exit_code == 0
    assert res.output.strip() == "Jane Doe"

    res = runner.invoke(
        cli,
        ["load", "-i", fixtures_path / "eu_authorities.ftm.json", "--from-entities"],
    )
    assert res.exit_code == 0
