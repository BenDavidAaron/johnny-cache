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

    def get(self, key: str) -> Any:
        val = self.__get_from_memory(key)
        if val is not None:
            return val
        val = self.__get_from_disk(key)
        return val

    def __get_from_memory(self, key):
        return self.__store__.get(key)

    def __get_from_disk(self, key):
        try:
            val = pickle.load((self.directory / key).open("rb"))
        except FileNotFoundError as exc:
            return None
        return val

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError
        else:
            return val

    def put(self, key: str, val: Any):
        self.__store__[key] = val
        self.__unflushed_objects__.append(("PUT", key))
        if len(self.__unflushed_objects__) > self.flush_size:
            self.flush()

    def __setitem__(self, key, val):
        return self.put(key, val)

    def delete(self, key: str):
        del self.__store__[key]
        self.__unflushed_objects__.append(("DEL", key))

    def __delitem__(self, key):
        return self.delete(key)

    def flush(self):
        for verb, key in self.__unflushed_objects__:
            if verb == "DEL":
                (self.directory / key).unlink()
            elif verb == "PUT":
                pickle.dump(
                    self.__get_from_memory(key),
                    (self.directory / key).open("wb"),
                )

    def invalidate(self):
        self.__store__ = {}
        self.__unflushed_objects__ = []
        for file in self.directory.glob("*"):
            file.unlink()
