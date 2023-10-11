"""
build an inverted token-based redis index for fuzzy lookups
"""

from typing import Set

import Levenshtein
from fingerprints import generate as fp

from juditha import settings
from juditha.util import canonize


def tokenize(value: str) -> set[str]:
    value = fp(value)
    if value:
        return {t for t in value.split() if len(t) > 3}
    return set()


def compare(value1: str, value2: str) -> int:
    return Levenshtein.ratio(canonize(value1), canonize(value2))


def find_best(
    value: str, candidates: Set[str], threshold: int | None = settings.FUZZY_SCORE
) -> str | None:
    if not candidates:
        return
    scores: dict[str, int] = {compare(value, c): c for c in candidates}
    score = max(scores.keys())
    if score > threshold:
        return scores[score]
