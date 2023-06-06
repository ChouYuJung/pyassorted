from typing import Dict, Text

import pytest

from pyassorted.string import Bracket, multiple_replace


@pytest.mark.parametrize(
    "d, text, wraped_by, expected",
    [
        ({"var1": "Hello", "var2": "World"}, "var1 var2", None, "Hello World"),
        (
            {"var1": "Hello", "var2": "World"},
            "( var1) ( var2  )",
            Bracket.Parenthesis,
            "Hello World",
        ),
        (
            {"var1": "Hello", "var2": "World"},
            "[ var1] [ var2  ]",
            Bracket.SquareBrackets,
            "Hello World",
        ),
        (
            {"var1": "Hello", "var2": "World"},
            "{ var1} { var2  }",
            Bracket.CurlyBrackets,
            "Hello World",
        ),
    ],
)
def test_multiple_replace(
    d: Dict[Text, Text], text: Text, wraped_by: Bracket, expected: Text
):
    kwargs = {}
    if wraped_by is not None:
        kwargs["wraped_by"] = wraped_by
    assert multiple_replace(d, text, **kwargs) == expected
