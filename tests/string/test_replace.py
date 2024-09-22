import pytest

from pyassorted.string.replace import (
    Bracket,
    limit_consecutive_newlines,
    multiple_replace,
    remove_punctuation,
    replace_right,
    str_strong_casefold,
)


@pytest.mark.parametrize(
    "d, text, wrapped_by, expected",
    [
        (
            {"var1": "Hello", "var2": "World"},
            "var1 var2",
            Bracket.NoBracket,
            "Hello World",
        ),
        (
            {"var1": "Hello", "var2": "World"},
            "(var1) (var2)",
            Bracket.Parenthesis,
            "Hello World",
        ),
        (
            {"var1": "Hello", "var2": "World"},
            "[var1] [var2]",
            Bracket.SquareBrackets,
            "Hello World",
        ),
        (
            {"var1": "Hello", "var2": "World"},
            "{var1} {var2}",
            Bracket.CurlyBrackets,
            "Hello World",
        ),
    ],
)
def test_multiple_replace(d, text, wrapped_by, expected):
    assert multiple_replace(d, text, wrapped_by) == expected


@pytest.mark.parametrize(
    "text, max_newlines, expected",
    [
        ("Hello\n\n\n\n\nWorld", 2, "Hello\n\nWorld"),
        ("Line1\n\nLine2\n\n\n\nLine3", 1, "Line1\nLine2\nLine3"),
        ("No\nNewlines", 3, "No\nNewlines"),
    ],
)
def test_limit_consecutive_newlines(text, max_newlines, expected):
    assert limit_consecutive_newlines(text, max_newlines) == expected


@pytest.mark.parametrize(
    "source_str, old, new, occurrence, expected",
    [
        ("Hello World, World", "World", "Universe", 1, "Hello World, Universe"),
        ("Hello World, World", "World", "Universe", -1, "Hello Universe, Universe"),
        ("One Two Three Two One", "One", "Zero", 1, "One Two Three Two Zero"),
    ],
)
def test_replace_right(source_str, old, new, occurrence, expected):
    assert replace_right(source_str, old, new, occurrence) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello-World!", "helloworld"),
        ("Python_Programming", "pythonprogramming"),
        ("  UPPER lower  ", "upperlower"),
    ],
)
def test_str_strong_casefold(text, expected):
    assert str_strong_casefold(text) == expected


@pytest.mark.parametrize(
    "input_string, extra_punctuation, expected",
    [
        ("Hello, World!", "", "Hello World"),
        ("Python: Programming; is fun!", ":;", "Python Programming is fun"),
        ("Test，？！（）【】《》" "''；：", "", "Test"),
    ],
)
def test_remove_punctuation(input_string, extra_punctuation, expected):
    assert remove_punctuation(input_string, extra_punctuation) == expected
