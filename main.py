import pathlib
import os

import fastapi

from typing import Any

DISK_PREFIX = pathlib.Path(
    os.environ.get("JONNY_CACHE_PREFIX", "~/.johnny_cache")
).expanduser().absolute()

DISK_PREFIX.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_SIZE", "1000"))

app = fastapi.FastAPI()


@app.get("/")
async def healthcheck():
    return {"status": "Truckin'"}


@app.get("/{key}")
async def get_item(key: str):
    return get_from_cache(key)


def get_from_cache(key: str):
    cache_path = DISK_PREFIX / key
    with open(cache_path, "r") as cf:
        return cf.read()


@app.put("/{key}")
async def put_item(key: str, value: str):
    put_in_cache(key, value)
    return


def put_in_cache(key, value):
    cache_path = DISK_PREFIX / key
    with open(cache_path, "w") as cf:
        cf.write(value)
    return

