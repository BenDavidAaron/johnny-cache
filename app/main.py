import os
import pathlib
from typing import Any, AnyStr, Dict, List, Union

import fastapi

from app import cache

CACHE_PATH = (
    pathlib.Path(os.environ.get("JONNY_CACHE_PREFIX", "~/.johnny_cache"))
    .expanduser()
    .absolute()
)
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_SIZE", "10000"))

app = fastapi.FastAPI()
cache = cache.MemoryFirstCache(CACHE_PATH, flush_size=CACHE_SIZE)

json_object = Dict[AnyStr, Any]
json_array = List[Any]
json_struct = Union[json_array, json_object]


@app.get("/")
async def healthcheck():
    return {"status": "Truckin'"}


@app.get("/{key}")
async def get_item(key: str):
    try:
        return cache[key]
    except KeyError:
        raise fastapi.HTTPException(404, detail=f"{key} not found")


@app.put("/{key}")
async def put_item(key: str, value: json_struct = None):
    cache[key] = value
    return


@app.delete("/{key}")
async def delete_item(key: str):
    del cache[key]
    return
