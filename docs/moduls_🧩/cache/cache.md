
# pyassorted.cache.cache

The `pyassorted.cache.cache` module provides caching functionality to enhance performance by reducing expensive or time-consuming function calls and computations. It includes an implementation of the Least Recently Used (LRU) cache policy and a `cached` decorator for easy application of caching to any function or coroutine function.

## LRU Cache

```python
class LRU(CacheObject):
```

The `LRU` class implements a Least Recently Used (LRU) cache using `collections.OrderedDict`. It provides methods for getting and putting items in the cache, as well as tracking cache hits and misses.

### Usage

```python
lru_cache = LRU(maxsize=100)
lru_cache.put("key", "value")
value = lru_cache.get("key")
```

### Parameters

- `maxsize`: Maximum size of the cache (default is 0, which means no limit)
- `init_cache`: Initial cache (can be another LRU instance or a dictionary)
- `sentinel`: Sentinel value for cache misses (default is `EMPTY_CACHE`)

### Methods

- `get(key)`: Retrieve a value from the cache
- `put(key, value)`: Add a value to the cache
- `full()`: Check if the cache is full

## Cached Decorator

```python
def cached(cache: Optional[Union[Type["CacheObject"], Callable]] = None):
```

The `cached` decorator allows you to easily cache the results of functions or coroutine functions. It can be used with or without arguments.

### Usage

```python
@cached()
def expensive_function(x, y):
    # Some expensive computation
    return x + y

@cached
async def async_expensive_function(x, y):
    # Some expensive async computation
    await asyncio.sleep(1)
    return x + y
```

### Parameters

- `cache`: Optional cache object or function to cache. If not provided, a new LRU cache will be used.

## Examples

1. Using LRU cache directly:

```python
lru_cache = LRU()
lru_cache.put("key", "value")
assert lru_cache.get("key") == "value"
assert lru_cache.hits == 1
assert lru_cache.misses == 0
```

2. Using the `cached` decorator with a function:

```python
@cached()
def add(a: int, b: int) -> int:
    return a + b

result = add(1, 2)
assert result == 3
assert add.cache.hits == 0
assert add.cache.misses == 1

result = add(1, 2)
assert result == 3
assert add.cache.hits == 1
assert add.cache.misses == 1
```

3. Using the `cached` decorator with an async function:

```python
import asyncio

@cached
async def async_add(a: int, b: int) -> int:
    await asyncio.sleep(0.1)
    return a + b

async def main():
    result = await async_add(1, 2)
    assert result == 3
    assert async_add.cache.hits == 0
    assert async_add.cache.misses == 1

    result = await async_add(1, 2)
    assert result == 3
    assert async_add.cache.hits == 1
    assert async_add.cache.misses == 1

asyncio.run(main())
```

The `pyassorted.cache.cache` module provides a flexible and efficient caching solution that can be easily integrated into your Python projects to improve performance by reducing redundant computations.
