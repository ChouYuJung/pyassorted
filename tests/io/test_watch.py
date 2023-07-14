import asyncio
import concurrent.futures
import math
import signal
import tempfile
import time
from pathlib import Path

import pytest

from pyassorted.asyncio import run_func
from pyassorted.io import async_watch, watch


def write_empty(filepath: Path, wait_start: float, period: float, write_times: int = 1):
    time.sleep(wait_start)
    for _ in range(write_times):
        with open(filepath, "w") as f:
            f.write("")
        time.sleep(period)


def watch_count(
    filepath: Path,
    period: float,
    watch_times: int = 1,
) -> int:
    count = 0
    for _ in watch(filepath, period=period):
        count += 1
        if count >= watch_times:
            break
    return count


async def async_watch_count(filepath: Path, period: float, watch_times: int = 1) -> int:
    count = 0
    async for _ in async_watch(filepath, period=period):
        count += 1
        if count >= watch_times:
            break
    return count


def handle_timeout(sig, frame):
    raise TimeoutError("Timeout!")


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as f:
        dir_path = Path(f)
        yield dir_path


def test_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")
    filepath.touch()

    test_times = 3
    write_wait = 0.1
    write_period = 0.1
    watch_period = 0.01

    signal.signal(signal.SIGALRM, handle_timeout)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(
            watch_count,
            filepath,
            period=watch_period,
            watch_times=test_times,
        )
        executor.submit(
            write_empty,
            filepath,
            wait_start=write_wait,
            period=write_period,
            write_times=test_times,
        )
        timeout = math.ceil(test_times * write_period + write_wait + 1)
        try:
            future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            signal.alarm(1)


@pytest.mark.asyncio
async def test_async_watch(temp_dir: Path):
    assert temp_dir.exists()
    filepath = temp_dir.joinpath("test.txt")
    filepath.touch()

    test_times = 3
    write_wait = 0.1
    write_period = 0.1
    watch_period = 0.01

    watch_task = asyncio.Task(
        async_watch_count(filepath, period=watch_period, watch_times=test_times)
    )
    write_task = asyncio.Task(
        run_func(
            write_empty,
            filepath,
            wait_start=write_wait,
            period=write_period,
            write_times=test_times,
        )
    )
    results = await asyncio.wait_for(
        asyncio.gather(
            *[
                watch_task,
                write_task,
            ]
        ),
        timeout=math.ceil(test_times * write_period + write_wait + 1),
    )
    assert results[0] == test_times
