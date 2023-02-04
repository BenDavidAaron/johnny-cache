from  app.cache import MemoryFirstCache

def test_cache_put_and_get(tmp_path):
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"

def test_cache_put_get_and_del(tmp_path):
    cash = MemoryFirstCache(tmp_path)
    cash["nevada"] = "Carson City"
    assert cash["nevada"] == "Carson City"
    del cash["nevada"]
    assert cash["nevada"] == None
