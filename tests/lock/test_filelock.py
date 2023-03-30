from functools import partial
from multiprocessing import cpu_count, get_context
from typing import Dict, Optional

from pyassorted.lock import FileLock


max_workers = 20 if cpu_count() > 20 else cpu_count()


def dict_data_add_one(d: Dict, lock: Optional["FileLock"] = None):
    if lock is not None:
        with lock:
            o = d["data"]
            d["data"] += 1
            print(f"{o} -> {d['data']}")
    else:
        d["data"] += 1


def test_file_lock():
    total_task_num = 100

    # Failure of multiprocessing in race condition
    with get_context("fork").Manager() as manager:
        d = manager.dict()
        d["data"] = 0
        with get_context("fork").Pool(processes=max_workers) as pool:
            pool.map(dict_data_add_one, [d] * total_task_num)
        assert d["data"] != total_task_num  # Race condition

    # Success with extra file lock
    lock = FileLock()
    with get_context("fork").Manager() as manager:
        d = manager.dict()
        d["data"] = 0
        with get_context("fork").Pool(processes=max_workers) as pool:
            pool.map(partial(dict_data_add_one, lock=lock), [d] * total_task_num)
        assert d["data"] == total_task_num
