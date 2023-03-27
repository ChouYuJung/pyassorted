from pyassorted.cache import LRU


def test_lru():
    """Test LRU cache."""

    item_count = 999

    # Maxsize is infinite
    lru_cache = LRU(maxsize=-999)
    for i in range(item_count):
        lru_cache.put(i, i)
    assert len(lru_cache) == item_count
    assert lru_cache.full() == False

    assert lru_cache.get(0) == 0
    assert lru_cache.hits == 1
    assert lru_cache.get(-999) == lru_cache.sentinel
    assert lru_cache.misses == 1

    # Maxsize is finite
    lru_cache = LRU(maxsize=20)
    for i in range(item_count):
        lru_cache.put(i, i)
    assert len(lru_cache) != item_count
    assert lru_cache.full() == True

    assert lru_cache.get(0) == lru_cache.sentinel
    assert lru_cache.misses == 1
    assert lru_cache.get(item_count - 1) == item_count - 1
    assert lru_cache.hits == 1

    # Init cache
    lru_cache = LRU(
        init_cache={
            "a": "a",
        }
    )
    lru_cache.get("a") == "a"
    assert lru_cache.hits == 1
    lru_cache.get("b") == lru_cache.sentinel
    assert lru_cache.misses == 1

    # Init cache with LRU
    new_lru_cache = LRU(init_cache=lru_cache)
    new_lru_cache.get("a") == "a"
    assert new_lru_cache.hits == 1
    new_lru_cache.get("b") == new_lru_cache.sentinel
    assert new_lru_cache.misses == 1
