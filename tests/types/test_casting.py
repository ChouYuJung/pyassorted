import pytest

from pyassorted.types.casting import (
    ensure_list,
    json_dumps,
    model_dump,
    must_list,
    must_list_or_none,
    named_tuples_to_dicts,
    should_str,
    should_str_or_none,
)


def test_should_str_or_none():
    assert should_str_or_none("test") == "test"
    assert should_str_or_none(None) is None
    assert should_str_or_none(123) is None


def test_should_str():
    assert should_str("test") == "test"
    with pytest.raises(ValueError):
        should_str(123)


def test_must_list_or_none():
    assert must_list_or_none([1, 2, 3]) == [1, 2, 3]
    assert must_list_or_none(None) is None
    assert must_list_or_none((1, 2), return_none_if_empty=False) == [1, 2]
    assert must_list_or_none([], return_none_if_empty=True) is None


def test_must_list():
    assert must_list([1, 2, 3]) == [1, 2, 3]
    assert must_list(123) == [123]


def test_ensure_list():
    assert ensure_list(None) == []
    assert ensure_list("test") == ["test"]
    assert ensure_list([1, 2, 3]) == [1, 2, 3]


def test_named_tuples_to_dicts():
    from collections import namedtuple

    NamedTuple = namedtuple("NamedTuple", "a b")
    nt = [NamedTuple(1, 2), NamedTuple(3, 4)]
    assert named_tuples_to_dicts(nt) == [{"a": 1, "b": 2}, {"a": 3, "b": 4}]


def test_json_dumps():
    assert json_dumps({"key": "value"}) == '{"key": "value"}'
    assert json_dumps({"key": "value"}, indent=2) == '{\n  "key": "value"\n}'


def test_model_dump():
    assert model_dump(None) is None
    assert model_dump(123) == {"_number": 123}
    assert model_dump("text") == {"_text": "text"}
