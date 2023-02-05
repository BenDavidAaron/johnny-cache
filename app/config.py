import os
import pathlib

CACHE_PATH = (
    pathlib.Path(os.environ.get("JOHNNY_CACHE_DATA_PATH", "~/.johnny_cache"))
    .expanduser()
    .absolute()
)
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_FLUSH_SIZE", "1000"))
