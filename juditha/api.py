from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException

from juditha import __version__, classify, lookup, settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    contact=settings.CONTACT,
    description=settings.DESCRIPTION,
    version=__version__,
    redoc_url="/",
)


@app.get("/_classify/{q}")
async def api_classify(q: str) -> str:
    schema = classify(q)
    if schema is None:
        return Response("404", status_code=404)
    return Response(schema)


@app.get("/{q}")
async def api_lookup(q: str, threshold: float | None = settings.FUZZY_THRESHOLD) -> str:
    name = lookup(q, threshold=threshold)
    if name is None:
        return Response("404", status_code=404)
    return Response(name)


@app.head("/{q}")
async def api_head(q: str, threshold: float | None = settings.FUZZY_THRESHOLD) -> None:
    name = lookup(q, threshold=threshold)
    if name is None:
        raise HTTPException(404)
    return 200
