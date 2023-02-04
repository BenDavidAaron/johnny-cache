import os
import pathlib
from typing import Any

import fastapi

DISK_PREFIX = pathlib.Path(
    os.environ.get("JONNY_CACHE_PREFIX", "~/.johnny_cache")
).expanduser().absolute()

DISK_PREFIX.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_SIZE", "1000"))

app = fastapi.FastAPI()
cache = MemoryFirstCache(DISK_PREFIX, CACHE_SIZE)

@app.get("/")
async def healthcheck():
    return {"status": "Truckin'"}


@app.get("/{key}")
async def get_item(key: str):
    return cache[key]

@app.put("/{key}")
async def put_item(key: str, value: str):
    cache[key] = value
    return

