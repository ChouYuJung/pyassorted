import re
from typing import List, Text


def find_placeholders(
    text: Text, *, open_delim: Text = "{", close_delim: Text = "}"
) -> List[Text]:
    """Find placeholders in a string.

    Parameters
    ----------
    text : Text
        Input string to find placeholders.
    open_delim : Text, optional
        Opening delim for placeholders. The default is "{".
    close_delim : Text, optional
        Closing delim for placeholders. The default is "}".

    Returns
    -------
    List[Text]
        List of placeholder names found in the input string.
    """

    # Escaping delims if necessary for regex usage
    open_delim = re.escape(open_delim)
    close_delim = re.escape(close_delim)

    # Regex pattern to find valid placeholder names
    pattern = rf"{open_delim}([a-zA-Z_][a-zA-Z0-9_-]*){close_delim}"
    return re.findall(pattern, text)
