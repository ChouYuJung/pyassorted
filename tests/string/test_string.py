import string
from typing import Dict, List, Optional, Text

import pytest

from pyassorted.string import Bracket, find_placeholders, multiple_replace, rand_str


@pytest.mark.parametrize(
    "d, text, wrapped_by, expected",
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
    d: Dict[Text, Text], text: Text, wrapped_by: Bracket, expected: Text
):
    kwargs = {}
    if wrapped_by is not None:
        kwargs["wrapped_by"] = wrapped_by
    assert multiple_replace(d, text, **kwargs) == expected


def test_rand_str():
    chars = string.ascii_letters + string.digits
    random_text = rand_str(length=10, chars=chars)
    assert len(random_text) == 10
    assert all(c in chars for c in random_text)


@pytest.mark.parametrize(
    "text, open_delim, close_delim, expected_output",
    [
        # Test with different delimiter characters
        (
            "Use [placeholder] and [another-one] here.",
            "[",
            "]",
            ["placeholder", "another-one"],
        ),
        # Nested placeholders (expect flat extraction, not nested)
        ("Check {outer{inner}}", "{", "}", ["inner"]),
        # No placeholders present
        ("Plain text without delimiters.", "{", "}", []),
        # Placeholders at the string boundaries
        ("{start} some text {end}", "{", "}", ["start", "end"]),
        # Placeholders with special characters (outside allowed characters)
        ("Special {placeholder*} and {another@}", "{", "}", []),
        # Continuous placeholders without spaces
        ("Here are{first}{second}together", "{", "}", ["first", "second"]),
        # Escaped delimiters within placeholders (not handled by the current regex)
        (
            "Escape example \\{not_a_placeholder\\} and {valid_one}",
            "{",
            "}",
            ["valid_one"],
        ),
        # Completely empty input
        ("", "{", "}", []),
    ],
)
def test_find_placeholders(
    text: Text,
    open_delim: Optional[Text],
    close_delim: Optional[Text],
    expected_output: List[Text],
):
    result = find_placeholders(
        text,
        open_delim=open_delim or "{",
        close_delim=close_delim or "}",
    )
    assert result == expected_output, f"Expected {expected_output}, but got {result}"
