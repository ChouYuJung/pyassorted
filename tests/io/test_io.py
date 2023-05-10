import json
import pprint
import tempfile
from pathlib import Path
from typing import Dict, List, Text, Tuple, Union

import pytest

from pyassorted.io import (
    merge_all_objects,
    merge_json_recursively,
    merge_objects,
    read_json_recursively,
)


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


def test_merge_objects():
    obj_1 = {"a": 1, "b": [2]}
    obj_2 = {"b": [3], "c": 3}
    obj = merge_objects(obj_1, obj_2, inplace=False)
    assert pprint.pformat(obj) == pprint.pformat({"a": 1, "b": [2, 3], "c": 3})
    assert pprint.pformat(obj) != pprint.pformat(obj_1)

    obj_1 = {"a": 1, "b": [2]}
    obj_2 = {"b": [3], "c": 3}
    obj = merge_objects(obj_1, obj_2, inplace=True)
    assert pprint.pformat(obj) == pprint.pformat({"a": 1, "b": [2, 3], "c": 3})
    assert pprint.pformat(obj) == pprint.pformat(obj_1)


def test_merge_all_objects():
    obj_1 = {"a": 1, "b": [2]}
    obj_2 = {"b": [3], "c": {"d": [4]}}
    obj_3 = {"c": {"d": [4], "f": 6}}
    obj = merge_all_objects(obj_1, obj_2, obj_3)
    assert pprint.pformat(obj) == pprint.pformat(
        {"a": 1, "b": [2, 3], "c": {"d": [4, 4], "f": 6}}
    )


def test_read_json_recursively(temp_dir_with_json_files: Path):
    filename_json_list = list(read_json_recursively(temp_dir_with_json_files))
    assert filename_json_list
    assert len(filename_json_list) == len(test_json_file_with_data)


def test_merge_json_recursively(temp_dir_with_json_files: Path):
    obj = merge_json_recursively(temp_dir_with_json_files)
    assert obj
