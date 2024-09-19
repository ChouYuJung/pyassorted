# pyassorted.asyncio.executor

The `pyassorted.asyncio.executor` module provides utility functions to simplify the execution of both synchronous and asynchronous functions in an asynchronous context. It offers two main functions: `run_func` and `run_generator`.

## run_func

```python
async def run_func(
    func: Union[Callable[P, T], Callable[P, Awaitable[T]]],
    *args,
    max_workers=1,
    **kwargs,
) -> T:
```

This function allows you to run either a coroutine function or a regular function in an asynchronous context. If the input is a coroutine function, it will be awaited directly. If it's a regular function, it will be run in a thread pool.

### `run_func` Parameters

- `func`: The function or coroutine function to be executed.
- `*args`: Positional arguments to be passed to the function.
- `max_workers`: The maximum number of workers in the thread pool (default is 1).
- `**kwargs`: Keyword arguments to be passed to the function.

### `run_func` Returns

The return value of the executed function.

### `run_func` Raises

- `ValueError`: If the input is not callable.

### `run_func` Example

```python
import asyncio
from pyassorted.asyncio import run_func

def normal_func() -> bool:
    return True

async def async_func() -> bool:
    await asyncio.sleep(0.1)
    return True

async def main():
    result1 = await run_func(normal_func)
    result2 = await run_func(async_func)
    print(result1, result2)  # True True

asyncio.run(main())
```

## run_generator

```python
async def run_generator(
    generator_func: Union[
        Callable[P, Generator[T, None, None]],
        Callable[P, AsyncGenerator[T, None]],
    ],
    *args,
    max_workers=1,
    **kwargs,
) -> AsyncGenerator[T, None]:
```

This function allows you to run either a generator function or an async generator function and yield its results asynchronously.

### `run_generator` Parameters

- `generator_func`: The generator function or async generator function to be executed.
- `*args`: Positional arguments to be passed to the generator function.
- `max_workers`: The maximum number of workers in the thread pool (default is 1).
- `**kwargs`: Keyword arguments to be passed to the generator function.

### `run_generator` Yields

Items yielded by the generator function.

### `run_generator` Raises

- `ValueError`: If the input is not callable or not a generator function.

### `run_generator` Example

```python
import asyncio
from pyassorted.asyncio import run_generator

def normal_generator(count: int):
    for i in range(count):
        yield i

async def async_generator(count: int):
    for i in range(count):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for item in run_generator(normal_generator, 5):
        print(item)

    async for item in run_generator(async_generator, 5):
        print(item)

asyncio.run(main())
```

These utility functions make it easier to work with both synchronous and asynchronous code in an asynchronous context, providing a unified interface for execution and simplifying the integration of different types of functions in your asyncio-based applications.

## run_generator_thread_pool

```python
async def run_generator_thread_pool(
    generator_func: Callable[P, Generator[T, None, None]],
    *args,
    max_workers=1,
    **kwargs,
) -> AsyncGenerator[T, None]:
```

This function runs a generator function in a thread pool and yields its results asynchronously. It's particularly useful when you need to run a synchronous generator function in an asynchronous context.

### `run_generator_thread_pool` Parameters

- `generator_func`: The generator function to be executed.
- `*args`: Positional arguments to be passed to the generator function.
- `max_workers`: The maximum number of workers in the thread pool (default is 1).
- `**kwargs`: Keyword arguments to be passed to the generator function.

### `run_generator_thread_pool` Yields

Items yielded by the generator function.

### `run_generator_thread_pool` Raises

- `ValueError`: If the input is not callable or not a generator function.

### `run_generator_thread_pool` Example

```python
import asyncio
from pyassorted.asyncio import run_generator_thread_pool

def sync_generator(count: int):
    for i in range(count):
        yield i

async def main():
    async for item in run_generator_thread_pool(sync_generator, 5):
        print(item)

asyncio.run(main())
```

This function is particularly useful when you have a synchronous generator that you want to use in an asynchronous context. It runs the generator in a separate thread, allowing your async code to continue executing while the generator produces values.

The `run_generator_thread_pool` function uses a producer-consumer pattern:

1. The producer runs the generator function in a separate thread.
2. The consumer asynchronously yields the items produced by the generator.

This approach allows for efficient execution of synchronous generators in asynchronous code, preventing blocking of the event loop.
