"""
Scan fulltext for known names (fuzzy)

Not intended for very long texts

Approach:
    - split text into sentences
    - iterate through every ngram from the sentence, with the longest first
    - normalize the ngrams and lookup as key patterns to get candidate blocks
    - compare actual candidates with real text via `fuzzysearch` and find best match
"""

from typing import Generator, Iterable

from fuzzysearch import find_near_matches
from nltk import sent_tokenize, word_tokenize
from nltk.util import everygrams

from juditha import settings
from juditha.clean import normalize
from juditha.util import find_best


def get_token_keys(txt: str, stream=False) -> Generator[str, None, None]:
    keys = set()
    for sent in sent_tokenize(txt):
        for gram in sorted(everygrams(word_tokenize(sent)), key=len, reverse=True):
            key = normalize("".join(gram))
            if key:
                if stream:
                    yield key
                else:
                    keys.add(key)
    if not stream:
        yield from sorted(keys, key=len, reverse=True)


def search_candidates(
    candidates: Iterable[str],
    txt: str,
    case_sensitive: bool | None = False,
    threshold: float | None = settings.FUZZY_THRESHOLD,
) -> Generator[tuple[str, str], None, None]:
    if not candidates or not txt:
        return
    if not case_sensitive:
        candidates = (c.lower() for c in candidates)
        txt = txt.lower()
    for candidate in candidates:
        matches = {m.matched for m in find_near_matches(candidate, txt, max_l_dist=3)}
        res = find_best(candidate, matches, case_sensitive, threshold)
        if res is not None:
            yield res, candidate
