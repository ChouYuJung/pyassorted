import asyncio
from functools import partial
from multiprocessing import cpu_count, get_context
from multiprocessing.managers import ValueProxy
from typing import Dict, Optional

import pytest
from pyassorted.lock import FileLock


max_workers = 20 if cpu_count() > 20 else cpu_count()


def add_one(num: "ValueProxy", lock: Optional["FileLock"] = None):
    if lock is not None:
        with lock:
            o = num.get()
            num.set(num.get() + 1)
            print(f"{o} -> {num.get()}")
    else:
        o = num.get()
        num.set(num.get() + 1)
        print(f"{o} -> {num.get()}")


def dict_data_add_one(d: Dict, lock: Optional["FileLock"] = None):
    """Add one in dict data.

    Parameters
    ----------
    d : Dict
        The dict data.
    lock : Optional[FileLock], optional
        The file lock, by default None
    """

    if lock is not None:
        with lock:
            o = d["data"]
            d["data"] += 1
            print(f"{o} -> {d['data']}")
    else:
        d["data"] += 1


async def async_dict_data_add_one(d: Dict, lock: Optional["FileLock"] = None):
    """Add one in dict data.

    Parameters
    ----------
    d : Dict
        The dict data.
    lock : Optional[FileLock], optional
        The file lock, by default None
    """

    if lock is not None:
        async with lock:
            o = d["data"]
            d["data"] += 1
            print(f"{o} -> {d['data']}")
    else:
        d["data"] += 1
    await asyncio.sleep(0.001)


def test_file_lock():
    """Test file lock."""

    total_task_num = 100

    # Failure of multiprocessing in race condition
    with get_context("fork").Manager() as manager:
        num = manager.Value("i", 0)
        with get_context("fork").Pool(processes=max_workers) as pool:
            pool.map(add_one, [num] * total_task_num)
        assert num.get() != total_task_num  # Race condition

    # Success with extra file lock
    lock = FileLock()
    with get_context("fork").Manager() as manager:
        num = manager.Value("i", 0)
        with get_context("fork").Pool(processes=max_workers) as pool:
            pool.map(partial(add_one, lock=lock), [num] * total_task_num)
        assert num.get() == total_task_num


@pytest.mark.asyncio
async def test_async_file_lock():
    """Test async file lock."""

    total_task_num = 100
    d = {"data": 0}

    lock = FileLock()

    tasks = [async_dict_data_add_one(d, lock=lock) for _ in range(total_task_num)]
    await asyncio.gather(*tasks)

    assert d["data"] == total_task_num
