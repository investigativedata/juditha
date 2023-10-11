[![juditha on pypi](https://img.shields.io/pypi/v/juditha)](https://pypi.org/project/juditha/) [![Python test and package](https://github.com/investigativedata/juditha/actions/workflows/python.yml/badge.svg)](https://github.com/investigativedata/juditha/actions/workflows/python.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![Coverage Status](https://coveralls.io/repos/github/investigativedata/juditha/badge.svg?branch=main)](https://coveralls.io/github/investigativedata/juditha?branch=main) [![MIT License](https://img.shields.io/pypi/l/juditha)](./LICENSE)

# juditha

A super-fast lookup service for canonical names based on redis and configurable upstream sources (currently [Aleph](https://docs.aleph.occrp.org/) and [Wikipedia](https://www.wikipedia.org/)).

`juditha` wants to solve the noise/garbage problem occurring when working with [Named Entity Recognition](https://en.wikipedia.org/wiki/Named-entity_recognition). Given the availability of huge lists of *known names*, once could canonize `ner`-results against this service to check if they are known.

The implementation uses a pre-populated redis cache which can fallback to other sources.

    pip install juditha

## populate

    echo "Jane Doe\nAlice" | juditha import

## lookup

    juditha lookup Jane
    "jane"

## data import

### from ftm entities

    cat entities.ftm.json | juditha import --from-entities

### from anywhere

    juditha import -i s3://my_bucket/names.txt
    juditha import -i https://data.ftm.store/eu_authorities/entities.ftm.json --from-entities

### a complete dataset or catalog

Following the [`nomenklatura`](https://github.com/opensanctions/nomenklatura) specification, a dataset json config needs `names.txt` or `entities.ftm.json` in its resources.

    juditha load-dataset https://data.ftm.store/eu_authorities/index.json
    juditha load-catalog https://data.ftm.store/investigraph/catalog.json

## use in python applications

```python
from juditha import lookup

assert lookup("jane") == "Jane"
assert lookup("foo") is None
```

## run as api

    uvicorn --port 8000 juditha.api:app --workers 8

### api calls

    curl -I "http://localhost:8000/Berlin"
    HTTP/1.1 200 OK

    curl -I "http://localhost:8000/Bayern"
    HTTP/1.1 404 Not Found

## settings

set redis endpoint via environment variable:

    REDIS_URL=redis://localhost:6379

## sources

Create a `yaml` config:

```yaml
sources:
  - klass: aleph
    config:
      host: https://aleph.investigativedata.org
      # api_key: ...
  - klass: aleph
    config:
      host: https://aleph.occrp.org
      # api_key: ...
  - klass: wikipedia
    config:
      url: https://de.wikipedia.org
```

Store this as a file (e.g. `config.yml`) and use it via env vars:

    JUDITHA_CONFIG=config.yml juditha lookup "Juditha Dommer"

If a lookup is not found in redis, `juditha` would use the fallback sources in the given order to lookup names. The results are stored in redis for the next call.

## use remote juditha

The `juditha` client can use a remote api endpoint of a deployed `juditha`:

    JUDITHA=https://juditha.ftm.store juditha lookup "HIMATIC EXPLOTACIONES SL"

```python
from juditha import Juditha

j = Juditha("https://juditha.ftm.store")
assert j.lookup("HIMATIC EXPLOTACIONES SL") is not None
```

## fuzzy matching

Optionally, search fuzzy. Fuzzyness is controlled by `FUZZY_SCORE` as a threshold (~0.9x) and activated by `FUZZY=true`.

During import, this creates an additional reverted redis index based on value tokens and for lookups compares name candidates via `Levensthein`.

Fuzzy matching is controlled via the api get parameter `fuzzy=true`

    curl -I "http://localhost:8000/Brlin"
    HTTP/1.1 404 Not Found

    curl -I "http://localhost:8000/Brlin?fuzzy=true"
    HTTP/1.1 200 OK

## the name

**Juditha Dommer** was the daughter of a coppersmith and raised seven children, while her husband Johann Pachelbel wrote a *canon*.
