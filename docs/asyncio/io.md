# pyassorted.asyncio.io

The `pyassorted.asyncio.io` module provides asynchronous I/O operations, primarily through the `AsyncIOWrapper` class and the `aio_open` function.

## AsyncIOWrapper

```python
class AsyncIOWrapper:
    def __init__(
        self,
        path: Path,
        mode: "OpenTextMode" = "r",
        encoding: Optional[Text] = None,
        **kwargs
    ):
```

This class wraps file I/O operations to make them asynchronous. It provides methods that mirror the standard file object methods but in an asynchronous context.

### Methods

- `__aenter__()`: Async context manager entry.
- `__aexit__()`: Async context manager exit.
- `__aiter__()`: Makes the object iterable asynchronously.
- `__anext__()`: Async iterator for reading lines.
- `close()`: Close the file.
- `read()`: Async read from the file.
- `readline()`: Async read a single line.
- `readlines()`: Async read all lines.
- `seek()`: Async seek in the file.
- `write()`: Async write to the file.
- `writelines()`: Async write multiple lines to the file.

## aio_open

```python
def aio_open(
    file: Union[Text, Path],
    mode: "OpenTextMode" = "r",
    encoding: Optional[Text] = None,
    **kwargs
) -> AsyncIOWrapper:
```

This function is an asynchronous version of the built-in `open()` function. It returns an `AsyncIOWrapper` object that can be used in async contexts.

### Parameters

- `file`: The path to the file to be opened.
- `mode`: The mode in which the file is opened.
- `encoding`: The encoding used to decode or encode the file.
- `**kwargs`: Additional keyword arguments to be passed to the underlying `open()` function.

### Returns

An `AsyncIOWrapper` object.

### Example

```python
import asyncio
from pyassorted.asyncio.io import aio_open

async def main():
    async with aio_open('example.txt', 'w') as f:
        await f.write('Hello, async world!')

    async with aio_open('example.txt', 'r') as f:
        content = await f.read()
        print(content)

asyncio.run(main())
```

This module allows for efficient asynchronous file I/O operations, which can be particularly useful in applications that deal with many files or large amounts of data.

```

For `pyassorted.asyncio.utils`, create a new file `docs/asyncio/utils.md`:

```markdown
# pyassorted.asyncio.utils

The `pyassorted.asyncio.utils` module provides utility functions for working with asynchronous code. Currently, it includes one main function: `is_coro_func`.

## is_coro_func

```python
def is_coro_func(func: Union[Callable[P, T], Callable[P, Awaitable[T]]]) -> bool:
```

This function checks whether the given function is a coroutine function or not.

### Parameters

- `func`: The function to be checked. It can be either a regular callable or an awaitable callable.

### Returns

- `bool`: True if the function is a coroutine function, False otherwise.

### Raises

- `ValueError`: If the input is not callable.

### Example

```python
import asyncio
from pyassorted.asyncio.utils import is_coro_func

def normal_func():
    return "I'm a normal function"

async def async_func():
    await asyncio.sleep(1)
    return "I'm an async function"

print(is_coro_func(normal_func))  # False
print(is_coro_func(async_func))   # True
```

This function is particularly useful when you need to determine whether a function should be awaited or called directly, especially in scenarios where you're working with mixed synchronous and asynchronous code.

The `is_coro_func` function handles various cases:

1. Regular functions
2. Async functions
3. Methods of classes (both regular and async)
4. Static methods (both regular and async)
5. Class methods (both regular and async)
6. Callable objects with `__call__` method (both regular and async)
7. Partial functions

This comprehensive checking makes it a robust tool for introspecting function types in asynchronous contexts.
