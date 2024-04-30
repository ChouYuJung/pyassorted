from typing import Any, Dict, Optional, Text, TypedDict

import pytest

from pyassorted.types import is_instance_of_typed_dict


class TypedDictClass(TypedDict, total=False):
    a: int
    b: int
    c: Optional[str]


@pytest.mark.parametrize(
    "obj, typed_dict_class, expected",
    [
        ({"a": 5, "b": 10}, TypedDictClass, True),
        ({"a": 5, "b": 10, "c": "hello"}, TypedDictClass, True),
        ({"a": 5, "b": 10, "c": None}, TypedDictClass, True),
        ({"a": 5, "b": "hello"}, TypedDictClass, False),
    ],
)
def test_is_instance_of_typed_dict(
    obj: Dict[Text, Any], typed_dict_class: TypedDictClass, expected: bool
) -> None:
    assert is_instance_of_typed_dict(obj, typed_dict_class) == expected
