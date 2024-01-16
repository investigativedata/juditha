"""
(fuzzy) match known candidates against pieces of (arbitrary) text
"""

from functools import cache
from typing import Generator, Iterable, Literal

import spacy
from pydantic import BaseModel
from rapidfuzz import fuzz, process
from spaczz.matcher import FuzzyMatcher

from juditha import settings
from juditha.clean import normalize


@cache
def get_nlp():
    return spacy.load(settings.SPACY_NER_MODEL)


@cache
def get_matcher():
    nlp = get_nlp()
    return FuzzyMatcher(nlp.vocab)


class Match(BaseModel):
    original: str
    name: str
    score: float


class Collector:
    def __init__(self) -> None:
        self.matches: list[Match] = []

    def add(self, m: Match) -> None:
        self.matches.append(m)

    def all(self) -> Generator[Match, None, None]:
        yield from self.matches

    def sorted(self) -> Generator[Match, None, None]:
        yield from sorted(self.matches, key=lambda x: x.score, reverse=True)

    def unique(self) -> Generator[Match, None, None]:
        seen = set()
        for m in self.sorted():
            if m.name not in seen:
                yield m
                seen.add(m.name)


Processor = Literal["lower", "normalize"]


def find_best(
    original: str, candidates: Iterable[str], preprocess: Processor | None = None
) -> Match | None:
    """
    Find best name (original) match from within candidates
    """
    candidates = set(candidates)
    if preprocess == "lower":
        original = original.lower()
        candidates = [c.lower() for c in candidates]
    if preprocess == "normalize":
        original = normalize(original)
        candidates = [normalize(c) for c in candidates]
    res = process.extractOne(original, candidates, scorer=fuzz.token_sort_ratio)
    if res is not None:
        name, score = res[:2]
        return Match(original=original, name=name, score=score / 100)


def extract(
    text: str,
    candidates: Iterable[str],
    unique: bool | None = True,
    sorted: bool | None = True,
) -> Generator[Match, None, None]:
    """
    Extract candidates from given text, using spacy with fuzzy phrase matching via spaczz
    """
    candidates = set(candidates)
    nlp = get_nlp()
    matcher = get_matcher()
    doc = nlp(text)
    collector = Collector()
    patterns = list(nlp.tokenizer.pipe(candidates))
    matcher.add("NAME", patterns, kwargs=[{"fuzzy_func": "token_sort"}] * len(patterns))
    for _, start, end, ratio, pattern in matcher(doc):
        collector.add(
            Match(original=str(doc[start:end]), name=pattern, score=ratio / 100)
        )

    if unique:
        yield from collector.unique()
    elif sorted:
        yield from collector.sorted()
    else:
        yield from collector.all()
