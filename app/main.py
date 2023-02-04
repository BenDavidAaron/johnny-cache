import os
import pathlib
from typing import Any

import fastapi

from app import cache

CACHE_PATH = pathlib.Path(
    os.environ.get("JONNY_CACHE_PREFIX", "~/.johnny_cache")
).expanduser().absolute()
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_SIZE", "10000"))

app = fastapi.FastAPI()
cache = cache.MemoryFirstCache(CACHE_PATH, flush_size=CACHE_SIZE)

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

@app.delete("/{key}")
async def delete_item(key: str):
    del cache[key]
    return
