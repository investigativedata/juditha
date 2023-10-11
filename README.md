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

## the name

**Juditha** is Johann Pachelbels, who wrote a *canon*, second wifes name.
