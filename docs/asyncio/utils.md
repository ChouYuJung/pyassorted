# pyassorted.asyncio.utils

## is_coro_func

The `is_coro_func` function is a utility to check if a given function is a coroutine function.

### Function Signature

```python
def is_coro_func(func: Callable) -> bool:
```

### Parameters

- `func` (Callable): The function to be checked.

### Returns

- `bool`: Returns `True` if the function is a coroutine function, `False` otherwise.

### Description

This function determines whether the provided function is a coroutine function. It uses Python's `inspect` module to check if the function is either an async function or a coroutine function.

### Usage Example

```python
import asyncio
from pyassorted.asyncio.utils import is_coro_func

async def async_function():
    await asyncio.sleep(1)

def regular_function():
    return "Hello, World!"

print(is_coro_func(async_function))  # Output: True
print(is_coro_func(regular_function))  # Output: False
```

### Implementation Details

The function likely uses `inspect.iscoroutinefunction(func)` internally to perform the check. This method from the `inspect` module returns `True` for both async def functions and regular functions decorated with `@asyncio.coroutine`.

### Note

This utility is particularly useful when working with mixed synchronous and asynchronous code, allowing you to handle different types of functions appropriately in your application logic.
