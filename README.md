# juditha

A super-fast lookup service for canonical names based on redis.

## populate

    echo "Jane Doe\nAlice" | juditha import

### from ftm entities

    cat entities.ftm.json | juditha import --from-entities

### from anywhere

    juditha import -i s3://my_bucket/names.txt
    juditha import -i https://data.ftm.store/eu_authorities/entities.ftm.json --from-entities

## lookup

    juditha lookup jane

## in python applications

```python
from juditha import lookup

assert lookup("jane") == "Jane"
assert lookup("foo") is None
```

## run as api

    uvicorn --port 8000 juditha.api:app --workers 8

## settings

set redis endpoint via environment variable:

    REDIS_URL=redis://localhost:6379
