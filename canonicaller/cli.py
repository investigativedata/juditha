from typing import Annotated

import typer
from followthemoney.types import registry
from ftmq.io import smart_read, smart_read_proxies
from rich import print

from canonicaller.store import get_store, lookup

cli = typer.Typer()


@cli.command("import")
def cli_import(
    in_uri: Annotated[str, typer.Option("-i", help="Input uri, default stdin")] = "-",
    from_entities: Annotated[
        bool, typer.Option(help="Specify if import data is ftm data (json lines)")
    ] = False,
):
    store = get_store()

    if from_entities:
        for proxy in smart_read_proxies(in_uri):
            for value in proxy.get_type_values(registry.name):
                store.set(value)
    else:
        for value in smart_read(in_uri, stream=True):
            store.set(value)


# @cli.callback(invoke_without_command=True)
@cli.command("lookup")
def cli_lookup(value: str):
    result = lookup(value)
    if result is not None:
        print(result)
    else:
        print("[red]not found[/red]")
