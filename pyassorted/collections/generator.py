from typing import AsyncGenerator, Callable, Generator, Iterable, TypeVar, Union

T = TypeVar("T")


def as_generator(
    generator: Union[
        Generator[T, None, None],
        Iterable[T],
    ],
) -> Callable[[], Generator[T, None, None]]:
    """
    Convert a synchronous generator or iterable into a generator function.

    Parameters
    ----------
    generator : Union[Generator[T, None, None], Iterable[T]]
        A synchronous generator or iterable to be converted.

    Returns
    -------
    Callable[[], Generator[T, None, None]]
        A function that returns a generator yielding items from the input.
    """

    def iterable_generator() -> Generator[T, None, None]:
        for item in generator:
            yield item

    return iterable_generator


def as_async_generator(
    generator: Union[AsyncGenerator[T, None], Generator[T, None, None], Iterable[T]],
) -> Callable[[], AsyncGenerator[T, None]]:
    """
    Convert an asynchronous generator, synchronous generator, or iterable into an async generator function.

    Parameters
    ----------
    generator : Union[AsyncGenerator[T, None], Generator[T, None, None], Iterable[T]]
        An asynchronous generator, synchronous generator, or iterable to be converted.

    Returns
    -------
    Callable[[], AsyncGenerator[T, None]]
        A function that returns an async generator yielding items from the input.
    """

    async def async_item_generator() -> AsyncGenerator[T, None]:
        if isinstance(generator, AsyncGenerator):
            async for item in generator:
                yield item
        else:
            for item in generator:
                yield item

    return async_item_generator
