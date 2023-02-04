import os
import pathlib
from typing import Any, AnyStr, Dict, List, Union

import fastapi

from app import cache, config

app = fastapi.FastAPI()
app_cache = cache.MemoryFirstCache(config.CACHE_PATH, flush_size=config.CACHE_SIZE)

json_object = Dict[AnyStr, Any]
json_array = List[Any]
json_struct = Union[json_array, json_object]


@app.get("/")
async def healthcheck():
    return {"status": "Truckin'"}


@app.post("/opt/flush")
async def flush():
    app_cache.flush()
    return


@app.delete("/opt/invalidate")
async def invalidate():
    app_cache.invalidate()
    return


@app.get("/cache/{key}")
async def get_item(key: str):
    try:
        return app_cache[key]
    except KeyError:
        raise fastapi.HTTPException(404, detail=f"{key} not found")


@app.put("/cache/{key}")
async def put_item(key: str, value: json_struct = None):
    app_cache[key] = value
    return


@app.delete("/cache/{key}")
async def delete_item(key: str):
    del app_cache[key]
    return
