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

        # IO Write
        with open(target_filepath, "w") as f:
            f.write(random_text_content)

        # AIO Write
        async with aio_open(test_filepath, "w") as f:
            await f.write(random_text_content)

        assert os.stat(target_filepath).st_size == os.stat(test_filepath).st_size
