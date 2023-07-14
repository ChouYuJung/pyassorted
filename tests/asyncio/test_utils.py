import asyncio
from typing import Any

import pytest

from pyassorted.asyncio import is_coro_func


def normal_func():
    pass


async def async_func():
    await asyncio.sleep(0.0)


class SampleClass:
    def __call__(self):
        pass

    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        pass

    def normal_method(self):
        pass


class AsyncSampleClass:
    async def __call__(self):
        await asyncio.sleep(0.0)

    @staticmethod
    async def static_method():
        await asyncio.sleep(0.0)

    @classmethod
    async def class_method(cls):
        await asyncio.sleep(0.0)

    async def normal_method(self):
        await asyncio.sleep(0.0)


sample_class = SampleClass()
async_sample_class = AsyncSampleClass()


@pytest.mark.parametrize(
    "func,target",
    [
        (normal_func, False),
        (sample_class, False),
        (sample_class.class_method, False),
        (sample_class.normal_method, False),
        (sample_class.static_method, False),
        (async_func, True),
        (async_sample_class, True),
        (async_sample_class.class_method, True),
        (async_sample_class.normal_method, True),
        (async_sample_class.static_method, True),
    ],
)
def test_is_coro_func(func: Any, target: bool):
    assert is_coro_func(func) is target
