import json
import tempfile
from pathlib import Path
from typing import Dict, List, Text, Tuple, Union

import pytest

from pyassorted.io import merge_json_recursively, read_json_recursively


test_json_file_with_data: List[Tuple[Text, Union[Dict, List]]] = [
    ("aaa.json", {"a": 1}),
    ("bbb/bbb.json", {"b": [2]}),
    ("bbb/ccc.json", {"c": 3, "b": [3], "d": {"e": [1]}}),
    ("ddd/ddd.json", {"d": {"e": [3]}, "b": [4]}),
]


@pytest.fixture
def temp_dir_with_json_files():
    with tempfile.TemporaryDirectory() as f:
        dir_path = Path(f)
        for _path, _data in test_json_file_with_data:
            filepath = dir_path.joinpath(_path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w") as f:
                json.dump(_data, f)
        yield dir_path


def test_read_json_recursively(temp_dir_with_json_files: Path):
    filename_json_list = list(read_json_recursively(temp_dir_with_json_files))
    assert filename_json_list
    assert len(filename_json_list) == len(test_json_file_with_data)


def test_merge_json_recursively(temp_dir_with_json_files: Path):
    obj = merge_json_recursively(temp_dir_with_json_files)
    assert obj
