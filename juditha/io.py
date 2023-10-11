import logging

from ftmq.io import smart_read, smart_read_proxies
from ftmq.model.dataset import Catalog, Dataset
from pantomime.types import FTM

from juditha.store import get_store
from juditha.util import names

log = logging.getLogger(__name__)


def _load_dataset(dataset: Dataset) -> int:
    store = get_store()
    ix = 0
    names_seen = False
    for resource in dataset.resources:
        if resource.name == "names.txt":
            names_seen = True
            for name in smart_read(resource.url, stream=True):
                store.add(name)
                ix += 1
                if ix % 10_000 == 0:
                    log.info(f"[{dataset.name}] Loading name %d ..." % ix)
    if not names_seen:
        # use entities
        for resource in dataset.resources:
            if resource.mime_type == FTM:
                for proxy in smart_read_proxies(resource.url):
                    for name in names(proxy):
                        store.add(name)
                        ix += 1
                        if ix % 10_000 == 0:
                            log.info(f"[{dataset.name}] Loading name %d ..." % ix)

    return ix


def load_dataset(uri: str) -> int:
    dataset = Dataset.from_uri(uri)
    log.info(f"[{dataset.name}] Loading ...")
    return _load_dataset(dataset)


def load_catalog(uri: str) -> int:
    catalog = Catalog.from_uri(uri)
    ix = 0
    for dataset in catalog.datasets:
        ix += _load_dataset(dataset)
    return ix


def load_names(uri: str) -> int:
    store = get_store()
    for ix, name in enumerate(smart_read(uri, stream=True), 1):
        store.add(name)
        if ix % 10_000 == 0:
            log.info("Loading name %d ..." % ix)
    return ix


def load_proxies(uri: str) -> int:
    store = get_store()
    ix = 0
    for proxy in smart_read_proxies(uri):
        for name in names(proxy):
            store.add(name)
            ix += 1
            if ix % 10_000 == 0:
                log.info("Loading name %d ..." % ix)
