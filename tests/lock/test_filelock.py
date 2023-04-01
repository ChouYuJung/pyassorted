import asyncio
import platform
import time
from functools import partial
from multiprocessing import cpu_count, get_context
from multiprocessing.managers import ValueProxy
from typing import Dict, Optional

import pytest
from pyassorted.lock import FileLock


max_workers = 20 if cpu_count() > 20 else cpu_count()
mp_ctx_method = "fork" if platform.processor() == "arm" else None


def add_one(num: "ValueProxy", lock: Optional["FileLock"] = None):
    if lock is not None:
        with lock:
            time.sleep(0.001)
            o = num.get()
            n = o + 1
            num.set(n)
            print(f"{o} -> {n}")
    else:
        time.sleep(0.001)
        o = num.get()
        n = o + 1
        num.set(n)
        print(f"{o} -> {n}")


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
            await asyncio.sleep(0.001)
            o = d["data"]
            d["data"] += 1
            print(f"{o} -> {d['data']}")
    else:
        await asyncio.sleep(0.001)
        d["data"] += 1


def test_file_lock():
    """Test file lock."""

    total_task_num = 100

    # Failure of multiprocessing in race condition
    with get_context(mp_ctx_method).Manager() as manager:
        num = manager.Value("i", 0)
        with get_context(mp_ctx_method).Pool(processes=max_workers) as pool:
            pool.map(add_one, [num] * total_task_num)
        assert num.get() != total_task_num  # Race condition

    # Success with extra file lock
    lock = FileLock()
    with get_context(mp_ctx_method).Manager() as manager:
        num = manager.Value("i", 0)
        with get_context(mp_ctx_method).Pool(processes=max_workers) as pool:
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
