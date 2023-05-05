import os
import random
import string
import tempfile
from pathlib import Path

import pytest

from pyassorted.asyncio.io import aio_open


target_filename = "test_io.txt"
test_filename = "test_aio.txt"


def random_string(row: int = 100, length: int = 100) -> str:
    return "\n".join(
        [
            "".join(random.choices(string.ascii_letters + string.digits, k=length))
            for _ in range(row)
        ]
    )


def random_binary(size: int = 10000000):  # 10 MB
    return bytearray(os.urandom(size))


@pytest.mark.asyncio
async def test_aio_open_text_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_filepath = Path(tmp_dir).joinpath(target_filename)
        test_filepath = Path(tmp_dir).joinpath(test_filename)
        random_text_content = random_string()

        # IO write line
        with open(target_filepath, "w") as f:
            f.writelines(["A", "B", "C"])
        # AIO write ine
        async with aio_open(test_filepath, "w") as f:
            await f.writelines(["A", "B", "C"])
        assert os.stat(target_filepath).st_size == os.stat(test_filepath).st_size

        # IO write
        with open(target_filepath, "w") as f:
            f.write(random_text_content)
        # AIO write
        async with aio_open(test_filepath, "w") as f:
            await f.write(random_text_content)
        assert os.stat(target_filepath).st_size == os.stat(test_filepath).st_size

        # Read
        with open(target_filepath, "r") as f:
            data_1 = f.read()
        async with aio_open(test_filepath, "r") as f:
            data_2 = await f.read()
        assert data_1 == data_2

        # Read with chunk
        with open(target_filepath, "r") as f:
            data_1 = f.read(1024)
        async with aio_open(test_filepath, "r") as f:
            data_2 = await f.read(1024)
        assert data_1 == data_2

        # Read after seek
        with open(target_filepath, "r") as f:
            f.read(5)
            f.seek(0)
            data_1 = f.read()
        async with aio_open(test_filepath, "r") as f:
            await f.read(5)
            await f.seek(0)
            data_2 = await f.read()
        assert data_1 == data_2
