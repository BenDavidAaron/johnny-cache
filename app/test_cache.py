"""Tests for Cache"""
import os
import pickle
import uuid

import pytest

from app.cache import MemoryFirstCache


def test_cache_put_and_get(tmp_path):
    """Add and fetch an item"""
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"


def test_cache_put_get_and_del(tmp_path):
    """Delete and fail to fetch an item"""
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"
    del cash["nevada"]
    with pytest.raises(KeyError):
        cash["nevada"]


def test_cache_flush(tmp_path):
    """Test writing to disk"""
    cash = MemoryFirstCache(tmp_path)
    items_to_insert = {str(n): str(uuid.uuid4()) for n in range(100)}
    for key, val in items_to_insert.items():
        cash[key] = val
    cash.flush()
    assert len(items_to_insert) == len(list(cash.directory.glob("*")))


def test_rehydrate_from_disk(tmp_path):
    """Test reinitalizing from disk"""
    (tmp_path / "foo").write_bytes(pickle.dumps("bar"))
    (tmp_path / "bonk").write_bytes(pickle.dumps("bonk"))
    cash = MemoryFirstCache(tmp_path)
    assert cash["foo"] == "bar"
    assert cash["bonk"] == "bonk"


def test_rehdrate_from_disk_large(tmp_path):
    """Test a lot of records on disk"""
    items_to_insert = {str(n): uuid.uuid4() for n in range(1000)}
    for key, val in items_to_insert.items():
        (tmp_path / key).write_bytes(pickle.dumps(val))
    cash = MemoryFirstCache(tmp_path)
    for key, val in items_to_insert.items():
        assert cash[key] == val


def test_put_and_get_binary_object(tmp_path):
    """test binary values"""
    cash = MemoryFirstCache(tmp_path)
    some_bytes = os.urandom(10)
    cash["some_bytes"] = some_bytes
    cash.flush()
    assert cash["some_bytes"] == some_bytes


def test_put_and_get_numbers(tmp_path):
    """test array of ints"""
    cash = MemoryFirstCache(tmp_path)
    nums = [1, 2, 3, 4]
    cash["nums"] = nums
    cash.flush()
    assert cash["nums"] == nums


def test_put_and_get_set(tmp_path):
    """Test for a non json serializable object"""
    cash = MemoryFirstCache(tmp_path)
    nums = set([1, 2, 3, 4])
    cash["nums"] = nums
    cash.flush()
    assert cash["nums"] == nums


def test_invalidation(tmp_path):
    """Test invalidation method"""
    cash = MemoryFirstCache(tmp_path)
    cash["foo"] = "bar"
    cash.flush()
    cash.invalidate()
    with pytest.raises(KeyError):
        cash["foo"]
