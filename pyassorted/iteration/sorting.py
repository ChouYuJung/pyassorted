from typing import List


def is_ascending(lst: List) -> bool:
    return all(a <= b for a, b in zip(lst, lst[1:]))


def is_descending(lst: List) -> bool:
    return all(a >= b for a, b in zip(lst, lst[1:]))
