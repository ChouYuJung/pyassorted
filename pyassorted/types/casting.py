import json
import logging
from numbers import Number
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Text,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from pydantic import BaseModel

T = TypeVar("T")


def should_str_or_none(
    value: Text | Any, *, logger: Optional["logging.Logger"] = None
) -> Optional[Text]:
    """Return the input value if it is a string, otherwise return None.

    Parameters
    ----------
    value : Text | Any
        The value to check.
    logger : Optional[logging.Logger], optional
        Logger to log a warning if the value is not a string.

    Returns
    -------
    Optional[Text]
        The input value if it is a string, None otherwise.
    """

    if isinstance(value, Text):
        return value
    elif value is None:
        return None
    if logger is not None:
        logger.warning(f"Value {value} is not a string, returning None")
    return None


def should_str(value: Text | Any, *, logger: Optional["logging.Logger"] = None) -> Text:
    """Ensure the input value is a string.

    Parameters
    ----------
    value : Text | Any
        The value to check.
    logger : Optional[logging.Logger], optional
        Logger to log a warning if the value is not a string.

    Raises
    ------
    ValueError
        If the value is not a string.

    Returns
    -------
    Text
        The input value if it is a string.
    """

    if should_str_or_none(value, logger=logger) is None:
        raise ValueError(f"Value {value} is not a string")
    return value


def must_list_or_none(
    value: List[T] | Any, return_none_if_empty: bool = False
) -> Optional[List[T]]:
    """Convert the input value to a list or return None.

    Parameters
    ----------
    value : List[T] | Any
        The value to convert.
    return_none_if_empty : bool, optional
        If True, return None for an empty list.

    Returns
    -------
    Optional[List[T]]
        The converted list or None.
    """

    if isinstance(value, List):
        if return_none_if_empty and len(value) == 0:
            return None
        return value
    elif isinstance(value, Tuple):
        if return_none_if_empty and len(value) == 0:
            return None
        return list(value)
    elif value is None:
        return None
    else:
        return [value]


def must_list(value: List[T] | Any) -> List[T]:
    """Ensure the input value is a list.

    Parameters
    ----------
    value : List[T] | Any
        The value to check.

    Raises
    ------
    ValueError
        If the value cannot be converted to a list.

    Returns
    -------
    List[T]
        The input value as a list.
    """

    to_items = must_list_or_none(value)
    if to_items is None:
        raise ValueError(f"Could not convert {value} to a list")
    return to_items


def ensure_list(value: Any) -> List:
    """Ensure the input value is a list.

    Parameters
    ----------
    value : Any
        The value to check.

    Returns
    -------
    List
        The input value as a list, or an empty list if None.
    """

    if isinstance(value, Sequence) and not isinstance(value, Text):
        return list(value)
    if value is None:
        return []
    return [value]


def named_tuples_to_dicts(named_tuples: Sequence[NamedTuple]) -> List[Dict]:
    """Convert a sequence of named tuples to a list of dictionaries.

    Parameters
    ----------
    named_tuples : Sequence[NamedTuple]
        The named tuples to convert.

    Returns
    -------
    List[Dict]
        A list of dictionaries representing the named tuples.
    """

    return [nt._asdict() for nt in named_tuples]


def json_dumps(data: Any, indent: Optional[Union[int, Text]] = None) -> Text:
    """Serialize data to a JSON formatted string.

    Parameters
    ----------
    data : Any
        The data to serialize.
    indent : Optional[Union[int, Text]], optional
        The number of spaces to use for indentation.

    Returns
    -------
    Text
        The JSON formatted string.
    """

    return json.dumps(data, indent=indent, ensure_ascii=False)


@overload
def model_dump(obj: Sequence) -> List[Dict]: ...


@overload
def model_dump(obj: None) -> None: ...


@overload
def model_dump(obj: Any) -> Dict: ...


def model_dump(obj: Any) -> Optional[Union[Dict, List[Dict]]]:
    """Convert a model or data structure to a dictionary or list of dictionaries.

    Parameters
    ----------
    obj : Any
        The object to convert.

    Returns
    -------
    Optional[Union[Dict, List[Dict]]]
        A dictionary or list of dictionaries representing the object, or None if the object is None.
    """

    if obj is None:
        return None
    elif isinstance(obj, Number):
        return {"_number": obj}
    elif isinstance(obj, bool):
        return {"_bool": obj}
    elif isinstance(obj, Text):
        return {"_text": obj}
    elif isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, Sequence) and not isinstance(obj, Text):
        return [model_dump(item) for item in obj]
    return json.loads(json.dumps(obj, default=str))
