# pyassorted.collections.sqlitedict

The `pyassorted.collections.sqlitedict` module provides a dictionary-like interface to SQLite databases. This can be used as a persistent dictionary for Python objects, where keys are restricted to primitive types such as strings and numbers.

## SqliteDict Class

The `SqliteDict` class supports common dictionary operations like getting, setting, and determining the length, with the added feature of enabling these operations asynchronously.

### Example Usage

```python
import asyncio
from pyassorted.collections.sqlitedict import SqliteDict

# Create an in-memory SQLite dictionary
sql_dict = SqliteDict(":memory:")

# Set a value
sql_dict["key"] = "value"
assert sql_dict["key"] == "value"

# Asynchronous usage
async def main():
    await sql_dict.async_set("key", "value")
    assert (await sql_dict.async_get("key")) == "value"

asyncio.run(main())
```

### Key Features

- **Persistent Storage**: Data is stored in a SQLite database, allowing for persistence across program runs.
- **Asynchronous Support**: Methods like `async_set` and `async_get` allow for non-blocking operations, making it suitable for applications with high I/O operations.
- **Common Dictionary Operations**: Supports standard dictionary methods such as `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, and iteration.

### Methods

- `__init__(sqlite_filepath: Text = ":memory:", tablename: Text = "cache", auto_commit: bool = True)`: Initializes the SqliteDict with the specified SQLite file path and table name.
- `__len__()`: Returns the number of items in the dictionary.
- `__getitem__(key: PrimitiveType)`: Retrieves the value associated with the given key.
- `__setitem__(key: PrimitiveType, value: Any)`: Sets the value for the given key.
- `__delitem__(key: PrimitiveType)`: Deletes the specified key and its associated value.
- `get(key: PrimitiveType, default: Any = None)`: Returns the value for the specified key, or a default value if the key does not exist.
- `async_set(key: PrimitiveType, value: Any)`: Asynchronously sets the value for the given key.
- `async_get(key: PrimitiveType)`: Asynchronously retrieves the value associated with the given key.

### Example of Asynchronous Operations

```python
import asyncio
from pyassorted.collections.sqlitedict import SqliteDict

async def example():
    sql_dict = SqliteDict(":memory:")
    await sql_dict.async_set("key", "value")
    value = await sql_dict.async_get("key")
    print(value)  # Output: value

asyncio.run(example())
```

This module is particularly useful for applications that require a lightweight, persistent dictionary with asynchronous capabilities, making it ideal for web applications, data caching, and more.
