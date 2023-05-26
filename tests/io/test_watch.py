import pytest
import tempfile
from pathlib import Path

from pyassorted.io import async_watch, watch


def wait_and_write_empty(filepath: Path):
    with open(filepath, "w") as f:
        f.write("")


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as f:
        dir_path = Path(f)
        yield dir_path


def test_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")


@pytest.mark.asyncio
async def test_async_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")
