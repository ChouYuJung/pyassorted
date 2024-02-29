import asyncio
from typing import Any, AsyncGenerator, Awaitable, Callable, Generator, Union

import pytest
from typing_extensions import ParamSpec, TypeVar

from pyassorted.asyncio import run_func, run_generator

T = TypeVar("T")
P = ParamSpec("P")


def normal_func() -> bool:
    return True


async def async_func() -> bool:
    await asyncio.sleep(0.0)
    return True


class SampleClass:
    def __call__(self) -> bool:
        return True

    @staticmethod
    def static_method() -> bool:
        return True

    @classmethod
    def class_method(cls) -> bool:
        return True

    def normal_method(self) -> bool:
        return True


class AsyncSampleClass:
    async def __call__(self) -> bool:
        await asyncio.sleep(0.0)
        return True

    @staticmethod
    async def static_method() -> bool:
        await asyncio.sleep(0.0)
        return True

    @classmethod
    async def class_method(cls) -> bool:
        await asyncio.sleep(0.0)
        return True

    async def normal_method(self) -> bool:
        await asyncio.sleep(0.0)
        return True


sample_class = SampleClass()
async_sample_class = AsyncSampleClass()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,return_value",
    [
        (normal_func, True),
        (sample_class, True),
        (sample_class.class_method, True),
        (sample_class.normal_method, True),
        (sample_class.static_method, True),
        (async_func, True),
        (async_sample_class, True),
        (async_sample_class.class_method, True),
        (async_sample_class.normal_method, True),
        (async_sample_class.static_method, True),
    ],
)
async def test_is_coro_func(func: Any, return_value: Any):
    assert await run_func(func) == return_value


def normal_generator(count: int) -> Generator[int, None, None]:
    for i in range(count):
        yield i


async def async_generator(count: int) -> AsyncGenerator[int, None]:
    for i in range(count):
        await asyncio.sleep(0.0)
        yield i


class SampleGeneratorClass:
    def __call__(self, count: int) -> Generator[int, None, None]:
        for i in range(count):
            yield i

    @staticmethod
    def static_method(count: int) -> Generator[int, None, None]:
        for i in range(count):
            yield i

    @classmethod
    def class_method(cls, count: int) -> Generator[int, None, None]:
        for i in range(count):
            yield i

    def normal_method(self, count: int) -> Generator[int, None, None]:
        for i in range(count):
            yield i


class AsyncSampleGeneratorClass:
    async def __call__(self, count: int) -> AsyncGenerator[int, None]:
        for i in range(count):
            await asyncio.sleep(0.0)
            yield i

    @staticmethod
    async def static_method(count: int) -> AsyncGenerator[int, None]:
        for i in range(count):
            await asyncio.sleep(0.0)
            yield i

    @classmethod
    async def class_method(cls, count: int) -> AsyncGenerator[int, None]:
        for i in range(count):
            await asyncio.sleep(0.0)
            yield i

    async def normal_method(self, count: int) -> AsyncGenerator[int, None]:
        for i in range(count):
            await asyncio.sleep(0.0)
            yield i


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "generator_func,count",
    [
        (normal_generator, 10),
        (async_generator, 10),
        (SampleGeneratorClass(), 10),
        (SampleGeneratorClass.class_method, 10),
        (SampleGeneratorClass().normal_method, 10),
        (SampleGeneratorClass.static_method, 10),
        (AsyncSampleGeneratorClass(), 10),
        (AsyncSampleGeneratorClass.class_method, 10),
        (AsyncSampleGeneratorClass().normal_method, 10),
        (AsyncSampleGeneratorClass.static_method, 10),
    ],
)
async def test_run_generator(
    generator_func: Callable[P, Generator[T, None, None]], count: int
):
    returns = []
    async for i in run_generator(generator_func, count):
        returns.append(i)
    assert returns == list(range(count))
