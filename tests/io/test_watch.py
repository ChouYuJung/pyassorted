import pytest
import tempfile
import time
from pathlib import Path

from pyassorted.io import async_watch, watch


def wait_and_write_empty(filepath: Path):
    with open(filepath, "w") as f:
        f.write("")


def watch_count(filepath: Path, watch_times: int) -> int:
    count = 0
    for _ in watch(filepath, frequency=0.01):
        count += 1
        if count >= watch_times:
            break
    return count


async def async_watch_count(filepath: Path, watch_times: int) -> int:
    count = 0
    async for _ in async_watch(filepath, frequency=0.01):
        count += 1
        if count >= watch_times:
            break
    return count


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as f:
        dir_path = Path(f)
        yield dir_path


def test_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")
    filepath.touch()


@pytest.mark.asyncio
async def test_async_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")
    filepath.touch()
