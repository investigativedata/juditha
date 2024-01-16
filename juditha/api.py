from typing import Literal, TypeAlias

from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from juditha import __version__, classify, lookup, settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    contact=settings.CONTACT,
    description=settings.DESCRIPTION,
    version=__version__,
    redoc_url="/",
)

Format: TypeAlias = Literal["txt", "json"]


@app.get("/_classify/{q}")
async def api_classify(q: str, format: Format | None = "txt") -> Response:
    schema = classify(q)
    if schema is None:
        return Response("404", status_code=404)
    return Response(schema)


@app.get("/{q}")
async def api_lookup(
    q: str,
    threshold: float | None = settings.FUZZY_THRESHOLD,
    format: Format | None = "txt",
) -> Response:
    res = lookup(q, threshold=threshold)
    if res is None:
        return Response("404", status_code=404)
    if format == "json":
        return JSONResponse(res.model_dump())
    return Response(res.name)


@app.head("/{q}")
async def api_head(q: str, threshold: float | None = settings.FUZZY_THRESHOLD) -> int:
    res = lookup(q, threshold=threshold)
    if res is None:
        raise HTTPException(404)
    return 200
