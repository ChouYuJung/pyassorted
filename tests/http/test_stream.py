import asyncio
import time

import pytest

from pyassorted.http.stream import (
    encode_sse,
    generate_sse_encode,
    requests_stream_lines,
    requests_stream_lines_async,
)


def test_encode_sse():
    assert encode_sse("test") == b"data: test\n\n"
    assert encode_sse({"key": "value"}) == b'data: {"key": "value"}\n\n'


def test_generate_sse_encode():
    stream = ["line1", {"key": "value"}, "line3"]
    expected = [
        "data: line1\n\n",
        'data: {"key": "value"}\n\n',
        "data: line3\n\n",
        "data: [DONE]\n\n",
    ]
    assert list(generate_sse_encode(stream)) == expected


def test_requests_stream_lines():
    MAX_LINES = 2

    # Testing GitHub Events API
    headers = {"Accept": "application/json"}
    url = "https://api.github.com/events"
    count = 0
    for line in requests_stream_lines(url, method="GET", headers=headers):
        assert line
        time.sleep(1)  # Add a small delay to avoid flooding the console
        count += 1
        if count >= MAX_LINES:
            break


@pytest.mark.asyncio
async def test_requests_stream_lines_async():
    MAX_LINES = 2

    # Testing GitHub Events API
    headers = {"Accept": "application/json"}
    url = "https://api.github.com/events"
    count = 0
    async for line in requests_stream_lines_async(url, method="GET", headers=headers):
        assert line
        await asyncio.sleep(1)  # Add a small delay to avoid hitting rate limits
        count += 1
        if count >= MAX_LINES:
            break
