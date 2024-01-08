from itertools import groupby
from string import digits
from typing import Any

from fingerprints import generate as fp

remove_digits = str.maketrans("", "", digits)


def normalize(value: Any, remove_whitespace: bool | None = True) -> str | None:
    """
    Normalize a given name to a cache lookup key in a very hammered way.

    The following normalizations are applied:
    - lowercase
    - fingerprinting via `fingerprints` library:
        - remove all non-ascii
        - strip out common prefixes (Mrs, ...)
        - normalize legal forms (Limited -> ltd)
        - distinct ordered tokens (foo foo bar -> bar foo)
    - remove all digits
    - remove all character double occurrences (foobar -> fobar)
    - optionally remove all whitespace
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

    # remove whitespace
    if remove_whitespace:
        value = value.replace(" ", "")

    return value or None


def clean_value(value: str | bytes) -> str:
    if isinstance(value, bytes):
        value = value.decode()
    return " ".join(value.split())
