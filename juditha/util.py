from typing import Generator, Set

from followthemoney.types import registry
from ftmq.types import CE
from thefuzz import process

from juditha import settings


def find_best(
    value: str,
    candidates: Set[str],
    case_sensitive: bool | None = False,
    threshold: float | None = settings.FUZZY_THRESHOLD,
) -> str | None:
    if not candidates:
        return
    if not case_sensitive:
        candidates = {c.lower(): c for c in candidates}
        res = process.extractOne(
            value.lower(), candidates.keys(), score_cutoff=threshold * 100
        )
        if res is not None:
            return candidates[res[0]]
        return
    res = process.extractOne(value, candidates, score_cutoff=threshold * 100)
    if res is not None:
        return res[0]


def proxy_names(proxy: CE) -> Generator[str, None, None]:
    for name in proxy.get_type_values(registry.name):
        yield name
