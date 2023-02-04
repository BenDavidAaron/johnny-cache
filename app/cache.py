import pathlib
from typing import Any


class MemoryFirstCache:
    """Store stuff for fast reading."""
    def __init__(self, directory: pathlib.Path, flush_interval: int=100):
        self.__store__ = {}
        self.directory = directory

    def get_val(self,key: str) -> Any:
        val = self.__store__.get(key)
        if val is None:
            val = self.__get_from_disk__(key)
        return val

    def __get_from_memory__(self, key):
        return self.val.get(key)

    def __get_from_disk__(self, key):
        try: 
            val = (self.directory / key).read_text()
        except FileNotFoundError:
            raise ValueError
        return val
    def __getitem__(self, key):
        return self.get_val(key)

    def put_val(self, key: str, val: Any):
        self.__store__[key] = val
        return

    def __setitem__(self, key, val):
        return self.put_val(key, val)

    def __delitem__(self, key):
        return self.delete_val(key)

    def delete_val(self, key: str):
        del self.__store__[key]
        try:
            (self.directory / key).unlink()
        except FileNotFoundError:
            # lol never got flushed
            pass
        return

    def flush(self):
        for key, val in self.__store__.items():
            val_path = self.directory / key
            val_path.write_text(val)
        return

