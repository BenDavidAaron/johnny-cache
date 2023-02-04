import pytest
import uuid

from app.cache import MemoryFirstCache


def test_cache_put_and_get(tmp_path):
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"
    return

def test_cache_put_get_and_del(tmp_path):
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"
    del cash["nevada"]
    with pytest.raises(ValueError):
        val = cash["nevada"]
    return

def test_cache_flush(tmp_path):
    cash = MemoryFirstCache(tmp_path)
    items_to_insert = {
        str(n): str(uuid.uuid4())
        for n in range(100)
    }
    for key, val in items_to_insert.items():
        cash[key] = val
    cash.flush()
    assert len(items_to_insert) == len([_ for _ in cash.directory.glob('*')])


def test_rehydrate_from_disk(tmp_path):
    (tmp_path / "foo").write_text("bar")
    (tmp_path / "bonk").write_text("bonk")
    cash = MemoryFirstCache(tmp_path)
    assert cash["foo"] == "bar"
    assert cash["bonk"] == "bonk"
