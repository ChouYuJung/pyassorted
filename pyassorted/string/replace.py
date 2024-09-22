import re
import string
from enum import Enum
from typing import Dict, Text


class Bracket(Enum):
    NoBracket = 0
    Parenthesis = 1
    CurlyBrackets = 2
    SquareBrackets = 3


def multiple_replace(
    d: Dict[Text, Text], text: Text, wrapped_by: Bracket = Bracket.NoBracket
) -> Text:
    """Replace 'd' keys with 'd' values in 'text' string.

    Parameters
    ----------
    d : Dict[Text, Text]
        Dictionary with keys to be replaced by values.
    text : Text
        Text to be replaced.
    wrapped_by : Bracket, optional
        If specified, the keys will be wrapped by the specified bracket type.
        If not specified, the keys will be replaced without any wrapping.
        The default is Bracket.NoBracket.

    Returns
    -------
    Text
        Text with replaced keys.

    Raises
    ------
    ValueError
        If 'wrapped_by' is not a valid Bracket type.

    Examples
    --------
    >>> d = {"var1": "Hello", "var2": "World"}
    >>> text = "var1 var2"
    >>> multiple_replace(d, text)
    'Hello World'
    """

    if wrapped_by is Bracket.NoBracket:
        regex = re.compile(r"%s" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.Parenthesis:
        regex = re.compile(r"\(\s*(%s)\s*\)" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.SquareBrackets:
        regex = re.compile(r"\[\s*(%s)\s*\]" % "|".join(map(re.escape, d.keys())))
    elif wrapped_by is Bracket.CurlyBrackets:
        regex = re.compile(r"{\s*(%s)\s*}" % "|".join(map(re.escape, d.keys())))
    else:
        raise ValueError(f"Invalid Bracket type: {wrapped_by}")

    if wrapped_by is Bracket.Parenthesis:
        return regex.sub(lambda mo: d[mo.group().strip("() \t\n\r")], text)
    if wrapped_by is Bracket.SquareBrackets:
        return regex.sub(lambda mo: d[mo.group().strip("[] \t\n\r")], text)
    else:
        return regex.sub(lambda mo: d[mo.group().strip("{} \t\n\r")], text)


def limit_consecutive_newlines(text: Text, max_newlines: int = 2) -> Text:
    """Limit consecutive newlines in a string.

    Parameters
    ----------
    text : Text
        Input text with newlines.
    max_newlines : int, optional
        Maximum number of consecutive newlines allowed. The default is 2.

    Returns
    -------
    Text
        Text with limited consecutive newlines.

    Examples
    --------
    >>> text = "Hello\n\n\n\n\nWorld"
    >>> limit_consecutive_newlines(text)
    'Hello\n\nWorld'
    """

    # Creating a regex pattern to match more than `max_newlines` newlines
    pattern = r"\n{" + str(max_newlines + 1) + ",}"
    # Replace found patterns with `max_newlines` amount of newline characters
    return re.sub(pattern, "\n" * max_newlines, text)


def replace_right(source_str: Text, old: Text, new: Text, occurrence: int = -1) -> Text:
    """Replace the rightmost occurrence of a substring in a string.

    Parameters
    ----------
    source_str : Text
        The original string in which to replace the substring.
    old : Text
        The substring to be replaced.
    new : Text
        The substring to replace with.
    occurrence : int, optional
        The number of occurrences to replace from the right.
        If -1 (default), all occurrences will be replaced.

    Returns
    -------
    Text
        The modified string with the specified replacements.

    Examples
    --------
    >>> replace_right("Hello World, World", "World", "Universe", 1)
    'Hello World, Universe'
    >>> replace_right("Hello World, World", "World", "Universe")
    'Hello Universe, Universe'
    """

    return source_str[::-1].replace(old[::-1], new[::-1], occurrence)[::-1]


def replace_non_alphanumeric(text: Text) -> Text:
    pattern = r"[^a-zA-Z0-9]"
    return re.sub(pattern, "", text.casefold())


def str_strong_casefold(text: Text) -> Text:
    """Convert a string to a case-insensitive format.

    Parameters
    ----------
    text : Text
        The input string to be casefolded.

    Returns
    -------
    Text
        The casefolded string, with certain characters removed.

    Examples
    --------
    >>> str_strong_casefold("Hello-World!")
    'helloworld'
    >>> str_strong_casefold("Python_Programming")
    'pythonprogramming'
    """

    pattern = r"[^a-zA-Z0-9]"
    return re.sub(pattern, "", text.casefold())


def remove_punctuation(input_string: Text, extra_punctuation: Text = "") -> Text:
    """Remove punctuation from a string.

    Parameters
    ----------
    input_string : Text
        The string from which to remove punctuation.
    extra_punctuation : Text, optional
        Additional punctuation characters to remove. The default is an empty string.

    Returns
    -------
    Text
        The string with punctuation removed.

    Examples
    --------
    >>> remove_punctuation("Hello, World!")
    'Hello World'
    >>> remove_punctuation("Python: Programming; is fun!", ":;")
    'Python Programming is fun'
    """

    extended_punctuation = (
        string.punctuation + "，？！（）【】《》“”‘’；：" + extra_punctuation
    )
    translator = str.maketrans("", "", extended_punctuation)
    return input_string.translate(translator)
