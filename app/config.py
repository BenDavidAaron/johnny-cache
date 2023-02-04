import os
import pathlib

CACHE_PATH = (
    pathlib.Path(os.environ.get("JONNY_CACHE_PREFIX", "~/.johnny_cache"))
    .expanduser()
    .absolute()
)
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_SIZE", "10000"))
