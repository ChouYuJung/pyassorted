import string
from typing import Dict, List, Optional, Text

import pytest

from pyassorted.string import (
    Bracket,
    extract_code_blocks,
    find_placeholders,
    limit_consecutive_newlines,
    multiple_replace,
    rand_str,
)


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


@pytest.mark.parametrize(
    "text, max_newlines, expected_output",
    [
        (
            "Hello\n\n\n\nWorld",
            2,
            "Hello\n\nWorld",
        ),  # More than 2 newlines reduced to 2
        (
            "Line 1\nLine 2\n\n\nLine 3",
            1,
            "Line 1\nLine 2\nLine 3",
        ),  # More than 1 newline reduced to 1
        ("\n\n\n", 1, "\n"),  # Text consisting only of newlines
        ("Single line", 2, "Single line"),  # No newlines to reduce
        (
            "End with newlines\n\n\n",
            2,
            "End with newlines\n\n",
        ),  # Newlines at the end of text
        (
            "\n\nStart with newlines",
            2,
            "\n\nStart with newlines",
        ),  # Newlines at the start of text
        ("", 2, ""),  # Empty input
        (
            "Normal text\n\nNormal text",
            2,
            "Normal text\n\nNormal text",
        ),  # Exactly max_newlines newlines
    ],
)
def test_limit_consecutive_newlines(text, max_newlines, expected_output):
    result = limit_consecutive_newlines(text, max_newlines)
    assert (
        result == expected_output
    ), f"Expected '{expected_output}', but got '{result}'"


@pytest.mark.parametrize(
    "text, language, expected_output",
    [
        ("No code here.", "json", []),
        ('Simple ```json\n{"key": "value"}``` block.', "json", ['{"key": "value"}']),
        (
            'Two blocks ```json\n{"first": 1}``` and ```json\n{"second": 2}```.',
            "json",
            ['{"first": 1}', '{"second": 2}'],
        ),
        ('Nested ```json\n{"key": ```not a block```}``` outer.', "json", ['{"key": ']),
        (
            '```json\n{"key": "value"}\n{"another": "item"}```',
            "json",
            ['{"key": "value"}\n{"another": "item"}'],
        ),
        ('Mismatched ```json{"data": "none"} ```', "json", []),
        ("Check lang ```yml\n- item: value\n```", "yml", ["- item: value\n"]),
        ("Partial match ```go package main``` is not a block.", "go", []),
        ("Correct newline but no content ```go\n```.", "go", [""]),
        (
            "Content with newline after lang ```go\npackage main\nfunc main() {}```",
            "go",
            ["package main\nfunc main() {}"],
        ),
        ("No end marker ```go\npackage main\nfunc main() {}", "go", []),
    ],
)
def test_extract_code_blocks(text, language, expected_output):
    result = extract_code_blocks(text, language)
    assert (
        result == expected_output
    ), f"Expected '{expected_output}', but got '{result}'"
