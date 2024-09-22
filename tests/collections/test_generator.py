import pytest

from pyassorted.collections.generator import as_async_generator, as_generator


# Test for as_generator
@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ([1, 2, 3], [1, 2, 3]),
        (iter([4, 5, 6]), [4, 5, 6]),
    ],
)
def test_as_generator(input_data, expected_output):
    gen_func = as_generator(input_data)
    assert list(gen_func()) == expected_output


# Test for as_async_generator


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ([1, 2, 3], [1, 2, 3]),
        (iter([4, 5, 6]), [4, 5, 6]),
    ],
)
@pytest.mark.asyncio
async def test_as_async_generator(input_data, expected_output):
    async_gen_func = as_async_generator(input_data)
    async for item in async_gen_func():
        assert item in expected_output
