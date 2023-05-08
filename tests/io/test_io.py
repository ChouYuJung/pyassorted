import random
import string
import tempfile
from pathlib import Path

import pytest

from pyassorted.io import read_json_recursively


"".join(random.choices(string.ascii_letters + string.digits, k=6))


@pytest.fixture
def temp_dir_with_json_files():
    with tempfile.TemporaryDirectory() as f:
        dir_path = Path(f)
        nested_dirname = "".join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )
        dir_path.joinpath(nested_dirname).mkdir(parents=True, exist_ok=True)
        with open(dir_path.joinpath("a.json"), "w") as f:
            f.write('{"a": 1}')
        with open(dir_path.joinpath(nested_dirname).joinpath("b.json"), "w") as f:
            f.write('{"b": 2}')
        with open(dir_path.joinpath(nested_dirname).joinpath("c.json"), "w") as f:
            f.write('{"c": 3}')
        yield dir_path


def test_read_json_recursively(temp_dir_with_json_files: Path):
    filename_json = list(read_json_recursively(temp_dir_with_json_files))
    assert filename_json
    assert len(filename_json[0]) == 2
