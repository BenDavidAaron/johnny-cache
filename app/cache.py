import pathlib
from typing import Any

class MemoryFirstCache:
    """Store stuff for fast reading."""
    def __init__(self, directory: pathlib.Path, flush_interval: int=100):
        self.store = {}
        self.directory = directory

    def get_val(key: str) -> Any:
        val = self.store.get(key)
        if val is None:
            self.__get_from_disk__(key)

    def __get_from_memory__(key):
        return self.val.get(key)

    def __get_from_disk__(key):
        try: 
            val = (self.directory / key).read()
        except Exception as exc:
            # TODO: Don't catch broad Exception
            raise exc
        return val
    def __getitem__(self, key):
        return self.get_val(key)

    def put_val(key: str, val: Any):
        self.store[key] = val
        return

    def __putitem__(self, key, val):
        return self.put_val(key, val)

    def flush():
        for key, val in self.store.items():
            val_path = self.directory / key
            val_path.write(val)
        return

