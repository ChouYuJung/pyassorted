import json
import logging
from typing import Any, Dict, Generator, Iterable, List, Literal, Optional, Text, Union

import httpx
import requests
from pydantic import BaseModel


def requests_stream_lines(
    url: Text,
    data: Optional[Dict[Text, Any]] = None,
    method: Literal["POST", "GET"] = "POST",
    headers: Optional[Dict[Text, Text]] = None,
) -> Generator[Text, None, None]:
    """
    Stream lines from a given URL using synchronous requests.

    Parameters
    ----------
    url : Text
        The URL to send the request to.
    data : Optional[Dict[Text, Any]], optional
        The data to send in the request body (default is None).
    method : Literal["POST", "GET"], optional
        The HTTP method to use (default is "POST").
    headers : Optional[Dict[Text, Text]], optional
        Additional headers to include in the request (default is None).

    Yields
    ------
    Text
        Each line of the response as it is received.
    """
    with requests.request(
        method, url, json=data, headers=headers or None, stream=True
    ) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield line + "\n"


async def requests_stream_lines_async(
    url: Text,
    data: Optional[Dict[Text, Any]] = None,
    method: Literal["POST", "GET"] = "POST",
    headers: Optional[Dict[Text, Text]] = None,
):
    """
    Asynchronously stream lines from a given URL.

    Parameters
    ----------
    url : Text
        The URL to send the request to.
    data : Optional[Dict[Text, Any]], optional
        The data to send in the request body (default is None).
    method : Literal["POST", "GET"], optional
        The HTTP method to use (default is "POST").
    headers : Optional[Dict[Text, Text]], optional
        Additional headers to include in the request (default is None).

    Yields
    ------
    Text
        Each line of the response as it is received.
    """

    async with httpx.AsyncClient(timeout=30) as client:
        async with client.stream(
            method, str(url), json=data, headers=headers or None
        ) as response:
            async for chunk in response.aiter_lines():
                yield chunk + "\n"


def encode_sse(
    data: Union[bytes, Text, BaseModel, Dict, List],
    *,
    encoding: Text = "utf-8",
    logger: Optional["logging.Logger"] = None,
) -> bytes:
    """Simple encoding for Server-Sent Events (SSE).

    Parameters
    ----------
    data : Union[bytes, Text, BaseModel, Dict, List]
        The data to encode.
    encoding : str, optional
        The encoding to use. Defaults to 'utf-8'.

    Returns
    -------
    bytes
        The encoded data.
    """

    if isinstance(data, bytes):
        encoded_data = data
    elif isinstance(data, Text):
        encoded_data = data.encode(encoding)
    elif isinstance(data, BaseModel):
        encoded_data = data.model_dump_json().encode(encoding)
    elif isinstance(data, Dict):
        encoded_data = json.dumps(data, default=str).encode(encoding)
    elif isinstance(data, List):
        encoded_data = json.dumps(data, default=str).encode(encoding)
    else:
        if logger is not None:
            logger.warning(f"Unknown data type to encode SSE: {type(data)}")
        encoded_data = str(data).encode(encoding)
    return b"data: " + encoded_data + b"\n\n"


def generate_sse_encode(
    stream: Union[
        Iterable[Union[Text, Dict, List[Any], BaseModel]],
        Generator[Union[Text, Dict, List[Any], BaseModel], None, None],
    ],
    logger: Optional["logging.Logger"] = None,
) -> Generator[Text, None, None]:
    """Generate Server-Sent Events (SSE) encoded data from a stream.

    Parameters
    ----------
    stream : Union[Iterable[Union[Text, Dict, List[Any], BaseModel]],
                    Generator[Union[Text, Dict, List[Any], BaseModel], None, None]]
        An iterable or generator that yields items to be encoded as SSE.
    logger : Optional[logging.Logger], optional
        A logger instance for logging warnings about unknown types.

    Yields
    ------
    Text
        The SSE encoded data for each item in the stream.
    """

    has_warned = False
    for item in stream:
        if isinstance(item, BaseModel):
            yield f"data: {item.model_dump_json()}\n\n"
        elif isinstance(item, (Dict, List)):
            yield f"data: {json.dumps(item)}\n\n"
        elif isinstance(item, Text):
            yield f"data: {item}\n\n"
        else:
            if has_warned is False:
                if logger is not None:
                    logger.warning(
                        f"Unknown type {type(item)} in stream, using str() to encode."
                    )
                has_warned = True
            yield f"data: {str(item)}\n\n"
    yield "data: [DONE]\n\n"
