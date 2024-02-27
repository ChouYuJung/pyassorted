import asyncio
import concurrent.futures
import functools
from typing import AsyncGenerator, Awaitable, Callable, Generator, Union, cast

from typing_extensions import ParamSpec, TypeVar

from pyassorted.asyncio.utils import is_coro_func

T = TypeVar("T")
P = ParamSpec("P")


async def run_func(
    func: Union[Callable[P, T], Callable[P, Awaitable[T]]],
    *args,
    max_workers=1,
    **kwargs,
) -> T:
    """Run the coroutine function or run function in a thread pool.

    Parameters
    ----------
    func : Union[Callable[P, T], Callable[P, Awaitable[T]]]
        The function or coroutine function.
    max_workers : int, optional
        The worker number of thread pool, by default 1

    Returns
    -------
    Any
        The return value of the function.

    Raises
    ------
    ValueError
        The input is not callable.
    """

    if not callable(func):
        raise ValueError(f"The {func} is not callable.")

    output = None

    if is_coro_func(func):
        partial_func = functools.partial(func, *args, **kwargs)
        partial_func = cast(Callable[[], Awaitable[T]], partial_func)
        output = await partial_func()

    else:
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            partial_func = functools.partial(func, *args, **kwargs)
            output = await loop.run_in_executor(pool, partial_func)

    output = cast(T, output)
    return output


async def run_generator(
    generator_func: Callable[P, Generator[T, None, None]],
    *args,
    max_workers=1,
    **kwargs,
) -> AsyncGenerator[T, None]:
    """Run a generator function in a thread pool and yield its results asynchronously.

    Parameters
    ----------
    generator_func : Callable[P, Generator[T, None, None]]
        The generator function.
    max_workers : int, optional
        The worker number of thread pool, by default 1

    Yields
    ------
    T
        Items yielded by the generator function.

    Raises
    ------
    ValueError
        If the input is not callable.
    """

    if not callable(generator_func):
        raise ValueError(f"The {generator_func} is not callable.")

    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def producer():
        for item in generator_func(*args, **kwargs):
            future = asyncio.run_coroutine_threadsafe(queue.put(item), loop)
            future.result()  # Wait for item to be added to the queue
        future = asyncio.run_coroutine_threadsafe(
            queue.put(None), loop
        )  # Signal completion
        future.result()

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        loop.run_in_executor(pool, producer)
        async for item in consumer():
            yield item
