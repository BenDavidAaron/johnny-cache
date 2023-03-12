import pathlib
import pickle
from typing import Any, Dict, List, Tuple
from app import crud, database


class MemoryFirstCache:
    """Store stuff for fast reading."""

    def __init__(self, flush_size: int = 10000):
        self.flush_size = flush_size
        self.__store__: Dict[Any, Any] = {}
        self.__unflushed_objects__: List[Tuple[str, Any]] = []
        self.db = database.SessionLocal()

    def get(self, key: str) -> Any:
        val = self.__get_from_memory(key)
        if val is not None:
            return val
        val = self.__get_from_disk(key)
        return val

    def __get_from_memory(self, key):
        return self.__store__.get(key)

    def __get_from_disk(self, key):
        return crud.get_record(self.db, key)

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
                crud.delete_record(self.db, key)
            elif verb == "PUT":
                crud.put_record(self.db, key, self.__get_from_memory(key))

    def invalidate(self):
        self.__store__ = {}
        self.__unflushed_objects__ = []
        crud.delete_records(self.db)
