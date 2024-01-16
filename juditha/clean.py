import logging
from functools import cache
from itertools import groupby
from string import digits
from types import FunctionType
from typing import Any, Generator

import spacy
from fingerprints import generate as fp
from metaphone import doublemetaphone
from nltk import sent_tokenize

remove_digits = str.maketrans("", "", digits)

log = logging.getLogger(__name__)


@cache
def get_sent_splitter() -> FunctionType:
    try:
        nlp = spacy.load("xx_sent_ud_sm")
        return lambda x: nlp(x).sents
    except OSError:
        log.warn(
            "Spacy model `xx_sent_ud_sm` not found."
            "Please install for better results. Falling back to `nltp.sent_tokenize`"
        )
        return sent_tokenize


def split_sentences(txt: str) -> Generator[str, None, None]:
    sentenizer = get_sent_splitter()
    yield from sentenizer(txt)


def normalize(value: Any) -> str | None:
    """
    Normalize a given name to a cache lookup key in a very aggressive way.

    The following normalizations are applied:
    - lowercase
    - fingerprinting via `fingerprints` library:
        - remove all non-ascii
        - strip out common prefixes (Mrs, ...)
        - normalize legal forms (Limited -> ltd)
        - distinct ordered tokens (foo foo bar -> bar foo)
    - remove all digits
    - remove all character double occurrences (foobar -> fobar)
    """

    if not value:
        return

    # fingerprinting
    value = fp(value)
    if not value:  # no real name
        return

    # remove digits
    value = value.translate(remove_digits)

    # remove double characters
    value = "".join(x for x, _ in groupby(value))

    return value.strip() or None


def clean_value(value: str | bytes) -> str:
    if isinstance(value, bytes):
        value = value.decode()
    return " ".join(value.split())


def tokenize(
    txt: str | None, stream: bool | None = False
) -> Generator[str, None, None]:
    """
    generate metaphone tokens from txt, ordered by their length in descending
    order
    optionally in stream mode, which means no reverse sorting by length and no
    deduping of equal tokens.
    """
    txt = normalize(txt)
    if txt is None:
        return
    tokens = set()
    for token in txt.split():
        keys = [k for k in doublemetaphone(token) if k]
        if stream:
            yield from keys
        else:
            tokens.update(keys)
    if not stream:
        yield from [k for k in sorted(tokens, key=len, reverse=True) if len(k) > 1]


def text_tokenize(
    txt: str | None, stream: bool | None = False
) -> Generator[str, None, None]:
    """
    generate metaphone tokens from longer text input.
    optionally in stream mode, which means no reverse sorting by length and no
    deduping of equal tokens.
    Preprocessing: Split text into sentences via spacy or nltk
    """
    tokens = set()
    if txt is None or not txt.strip():
        return
    for sent in split_sentences(txt):
        if stream:
            yield from tokenize(sent, stream=True)
        else:
            tokens.update(tokenize(sent))
    if not stream:
        yield from sorted(tokens, key=len, reverse=True)
