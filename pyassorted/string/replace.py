import re
from enum import Enum
from typing import Dict, Text


class Bracket(Enum):
    NoBracket = 0
    Parenthesis = 1
    CurlyBrackets = 2
    SquareBrackets = 3


def multiple_replace(
    d: Dict[Text, Text], text: Text, wraped_by: Bracket = Bracket.NoBracket
) -> Text:
    if wraped_by is Bracket.NoBracket:
        regex = re.compile("%s" % "|".join(map(re.escape, d.keys())))
    elif wraped_by is Bracket.Parenthesis:
        raise NotImplementedError
    elif wraped_by is Bracket.SquareBrackets:
        raise NotImplementedError
    elif wraped_by is Bracket.CurlyBrackets:
        regex = re.compile("{\s*(%s)\s*}" % "|".join(map(re.escape, d.keys())))
    else:
        raise ValueError(f"Invalid Bracket type: {wraped_by}")

    return regex.sub(lambda mo: d[mo.group().strip("{} \t\n\r")], text)
