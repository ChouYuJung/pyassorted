import concurrent.futures
import threading
from typing import Dict, Text

from pyassorted.lock.key_lock import KeyLock


def test_key_lock():
    key_lock = KeyLock()
    store: Dict[Text, int] = {}
    total_keys = 100
    repeaters = 100

    def thread_task(key: Text):
        with key_lock[key]:
            if key not in store:
                store[key] = 0
            _val = store[key]
            store[key] = _val + 1

    task_keys = [f"key_{i}" for i in range(total_keys)] * repeaters
    task_keys.sort()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(thread_task, task_keys)

    assert len(store) == total_keys
    assert all(store[key] == repeaters for key in store)
