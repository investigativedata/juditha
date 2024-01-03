import logging
from typing import Annotated

import typer
from rich import print

from juditha import io
from juditha.store import classify, lookup

logging.basicConfig(level=logging.INFO)

cli = typer.Typer()


def success(ix: int) -> None:
    print(f"[green]Imported {ix} names")


@cli.command("import")
def cli_import(
    uri: Annotated[str, typer.Option("-i", help="Input uri, default stdin")] = "-",
    from_entities: Annotated[
        bool, typer.Option(help="Specify if import data is ftm data (json lines)")
    ] = False,
):
    if from_entities:
        success(io.load_proxies(uri))
    else:
        success(io.load_names(uri))


@cli.command()
def load_dataset(
    uri: str,
    with_schema: Annotated[
        bool, typer.Option(..., help="Include schemata for classifier")
    ] = False,
) -> int:
    success(io.load_dataset(uri, with_schema=with_schema))


@cli.command()
def load_catalog(
    uri: str,
    with_schema: Annotated[
        bool, typer.Option(..., help="Include schemata for classifier")
    ] = False,
) -> int:
    success(io.load_catalog(uri, with_schema=with_schema))


@cli.command("lookup")
def cli_lookup(value: str):
    result = lookup(value)
    if result is not None:
        print(result)
    else:
        print("[red]not found[/red]")


@cli.command("classify")
def cli_classify(value: str):
    result = classify(value)
    if result is not None:
        print(result)
    else:
        print("[red]not found[/red]")
