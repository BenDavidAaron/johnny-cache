import pathlib
import pickle
from typing import Any, Dict, List, Tuple


class MemoryFirstCache:
    """Store stuff for fast reading."""

    def __init__(self, directory: pathlib.Path, flush_size: int = 10000):
        self.flush_size = flush_size
        self.directory = directory
        self.__store__: Dict[Any, Any] = {}
        self.__unflushed_objects__: List[Tuple[str, Any]] = []

    def get_val(self, key: str) -> Any:
        val = self.__get_from_memory__(key)
        if val is None:
            val = self.__get_from_disk__(key)
        return val

    def __get_from_memory__(self, key):
        return self.__store__.get(key)

    def __get_from_disk__(self, key):
        try:
            val = pickle.load((self.directory / key).open("rb"))
        except FileNotFoundError as exc:
            raise KeyError from exc
        return val

    def __getitem__(self, key):
        return self.get_val(key)

    def put_val(self, key: str, val: Any):
        self.__store__[key] = val
        self.__unflushed_objects__.append(("PUT", key))
        if len(self.__unflushed_objects__) > self.flush_size:
            self.flush()

    def __setitem__(self, key, val):
        return self.put_val(key, val)

    def __delitem__(self, key):
        return self.delete_val(key)

    def delete_val(self, key: str):
        del self.__store__[key]
        self.__unflushed_objects__.append(("DEL", key))

    def flush(self):
        for verb, key in self.__unflushed_objects__:
            if verb == "DEL":
                (self.directory / key).unlink()
            elif verb == "PUT":
                pickle.dump(
                    self.__get_from_memory__(key),
                    (self.directory / key).open("wb"),
                )

    def invalidate(self):
        self.__store__ = {}
        self.__unflushed_objects__ = []
        for file in self.directory.glob("*"):
            file.unlink()
