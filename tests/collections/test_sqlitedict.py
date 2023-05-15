from pyassorted.collections.sqlitedict import SqliteDict


def test_sqlite_dict():
    key = "a"
    cache = SqliteDict()
    assert len(cache) == 0

    # Basic Operations
    cache[key] = 1
    assert len(cache) == 1
    assert cache[key] == 1
    assert cache.get(key) == 1
    assert cache.get("NO_KEY") == None
    assert cache.get("NO_KEY", "DEFAULT") == "DEFAULT"

    cache.set(key, 2.0)
    assert cache.get(key) == 2.0
