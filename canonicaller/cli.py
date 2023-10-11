import logging
from typing import Annotated

import typer
from rich import print

from canonicaller import io
from canonicaller.store import lookup

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
def load_dataset(uri: str) -> int:
    success(io.load_dataset(uri))


@cli.command()
def load_catalog(uri: str) -> int:
    success(io.load_catalog(uri))


# @cli.callback(invoke_without_command=True)
@cli.command("lookup")
def cli_lookup(value: str):
    result = lookup(value)
    if result is not None:
        print(result)
    else:
        print("[red]not found[/red]")
