from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException

from juditha import __version__, lookup, settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    contact=settings.CONTACT,
    description=settings.DESCRIPTION,
    version=__version__,
    redoc_url="/",
)


@app.get("/{q}")
async def api_lookup(q: str, fuzzy: bool | None = False) -> str:
    value = lookup(q, fuzzy=fuzzy)
    if value is None:
        raise HTTPException(404)
    return Response(value)


@app.head("/{q}")
async def api_head(q: str, fuzzy: bool | None = False) -> None:
    value = lookup(q, fuzzy=fuzzy)
    if value is None:
        raise HTTPException(404)
    return 200
