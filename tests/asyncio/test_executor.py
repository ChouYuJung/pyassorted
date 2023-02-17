import asyncio
import pytest
from typing import Any

from pyassorted.asyncio import run_func


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
