from typing import AsyncGenerator, Callable, Generator, Iterable, TypeVar, Union

T = TypeVar("T")


def as_generator(
    generator: Union[
        Generator[T, None, None],
        Iterable[T],
    ],
) -> Callable[[], Generator[T, None, None]]:
    def iterable_generator() -> Generator[T, None, None]:
        for item in generator:
            yield item

    return iterable_generator


async def as_async_generator(
    generator: Union[AsyncGenerator[T, None], Generator[T, None, None], Iterable[T]],
) -> Callable[[], AsyncGenerator[T, None]]:
    async def async_item_generator() -> AsyncGenerator[T, None]:
        if isinstance(generator, AsyncGenerator):
            async for item in generator:
                yield item
        else:
            for item in generator:
                yield item

    return async_item_generator
