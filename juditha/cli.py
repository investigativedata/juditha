import logging
from typing import Annotated

import typer
from rich import print

from juditha import io, settings
from juditha.store import classify, lookup

logging.basicConfig(level=logging.INFO)

cli = typer.Typer(pretty_exceptions_enable=settings.DEBUG)


def success(msg: str) -> None:
    print(f"[green]{msg}")


def error(e: Exception) -> None:
    if not settings.DEBUG:
        return print(f"[red]{e}")
    raise e


@cli.command()
def load(
    uri: Annotated[str, typer.Option("-i", help="Input uri, default stdin")] = "-",
    from_entities: Annotated[
        bool, typer.Option(help="Specify if import data is ftm data (json lines)")
    ] = False,
):
    try:
        if from_entities:
            res = io.load_proxies(uri)
        else:
            res = io.load_names(uri)
        success(f"Imported {res} names.")
    except Exception as e:
        error(e)


@cli.command()
def load_dataset(
    uri: str,
    with_schema: Annotated[
        bool, typer.Option(..., help="Include schemata for classifier")
    ] = False,
) -> int:
    try:
        res = io.load_dataset(uri, with_schema=with_schema)
        success(f"Imported {res} names.")
    except Exception as e:
        error(e)


@cli.command()
def load_catalog(
    uri: str,
    with_schema: Annotated[
        bool, typer.Option(..., help="Include schemata for classifier")
    ] = False,
) -> int:
    try:
        res = io.load_catalog(uri, with_schema=with_schema)
        success(f"Imported {res} names.")
    except Exception as e:
        error(e)


@cli.command("lookup")
def cli_lookup(value: str):
    try:
        result = lookup(value)
        if result is not None:
            print(result)
        else:
            print("[red]not found[/red]")
    except Exception as e:
        error(e)


@cli.command("classify")
def cli_classify(value: str):
    try:
        result = classify(value)
        if result is not None:
            print(result)
        else:
            print("[red]not found[/red]")
    except Exception as e:
        error(e)
