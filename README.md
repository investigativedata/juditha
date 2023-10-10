# canonicaller

A super-fast lookup service for canonical names based on redis.

## populate

    echo "Jane Doe\nAlice" | canonicaller import

### from ftm entities

    cat entities.ftm.json | canonicaller import --from-entities

### from anywhere

    canonicaller import -i s3://my_bucket/names.txt
    canonicaller import -i https://data.ftm.store/eu_authorities/entities.ftm.json --from-entities

## lookup

    canonicaller lookup jane

## in python applications

```python
from canonicaller import lookup

assert lookup("jane") == "Jane"
assert lookup("foo") is None
```

## run as api

    uvicorn --port 8000 canonicaller.api:app --workers 8

## settings

set redis endpoint via environment variable:

    REDIS_URL=redis://localhost:6379
