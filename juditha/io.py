import logging

from ftmq.io import smart_read, smart_read_proxies
from ftmq.model.dataset import Catalog, Dataset
from pantomime.types import FTM

from juditha.store import get_store

log = logging.getLogger(__name__)


def load_proxies(uri: str, with_schema: bool | None = False) -> int:
    store = get_store()
    ix = 0
    for proxy in smart_read_proxies(uri):
        store.index_proxy(proxy, with_schema=with_schema)
        ix += 1
        if ix % 10_000 == 0:
            log.info("Loading proxy %d ..." % ix)
    return ix


def _load_dataset(dataset: Dataset, with_schema: bool | None = False) -> int:
    store = get_store()
    ix = 0
    names_seen = False
    if not with_schema:
        for resource in dataset.resources:
            if resource.name == "names.txt":
                names_seen = True
                for name in smart_read(resource.url, stream=True, mode="r"):
                    store.index(name)
                    ix += 1
                    if ix % 10_000 == 0:
                        log.info(f"[{dataset.name}] Loading name %d ..." % ix)
    if not names_seen:
        # use entities
        for resource in dataset.resources:
            if resource.mime_type == FTM:
                ix += load_proxies(resource.url, with_schema=with_schema)
    return ix


def load_dataset(uri: str, with_schema: bool | None = False) -> int:
    dataset = Dataset.from_uri(uri)
    log.info(f"[{dataset.name}] Loading ...")
    return _load_dataset(dataset, with_schema=with_schema)


def load_catalog(uri: str, with_schema: bool | None = False) -> int:
    catalog = Catalog.from_uri(uri)
    ix = 0
    for dataset in catalog.datasets:
        ix += _load_dataset(dataset, with_schema=with_schema)
    return ix


def load_names(uri: str) -> int:
    store = get_store()
    for ix, name in enumerate(smart_read(uri, stream=True), 1):
        store.index(name)
        if ix % 10_000 == 0:
            log.info("Loading name %d ..." % ix)
    return ix
