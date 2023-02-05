"""Routing code for cache"""
from typing import Any, AnyStr, Dict, List, Union

import fastapi

from app import cache, config

app = fastapi.FastAPI(
    title="JohnnyCache",
    description="He's a ramblin' man",
    version="1.0.0",
    contact={
        "name": "Ben Aaron",
        "url": "https://github.com/BenDavidAaron/johnny-cache",
    },
    licence_info={
        "name": "AGPL_3.0",
        "url": "https://github.com/BenDavidAaron/johnny-cache/blob/717594b035e1db8d40184fad53842153491c8c4a/license",
    },
)
app_cache = cache.MemoryFirstCache(config.CACHE_PATH, flush_size=config.CACHE_SIZE)


@app.get("/")
async def healthcheck():
    """Check if service is alive"""
    return {"status": "Truckin'"}


@app.post("/opt/flush")
async def flush():
    """Flush all in-memory records to disk"""
    app_cache.flush()
    return


@app.delete("/opt/invalidate")
async def invalidate():
    """Clear all records on the cache, completely empty it"""
    app_cache.invalidate()
    return


@app.get("/cache/{key}")
async def get_item(key: str):
    """Get an item from the cache or return a 404"""
    try:
        return app_cache[key]
    except KeyError as exc:
        raise fastapi.HTTPException(404, detail=f"{key} not found") from exc


@app.put("/cache/{key}")
async def put_item(key: str, value: Any = fastapi.Body()):
    """Insert a value into the cache at key"""
    app_cache[key] = value
    return


@app.delete("/cache/{key}")
async def delete_item(key: str):
    """Remove an item from the cache"""
    del app_cache[key]
    return
