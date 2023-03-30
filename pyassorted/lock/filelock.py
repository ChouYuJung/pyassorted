import tempfile
import time
import uuid
from pathlib import Path
from typing import Optional, Text


class FileLock(object):
    def __init__(
        self,
        file_name: Optional[Text] = None,
        timeout: float = 10,
        delay: float = 0.05,
        lock_expire: int = 60,
    ):
        if file_name is None:
            tmp_dir = tempfile.gettempdir()
            file_name = Path(tmp_dir).joinpath(f"pyassorted-{uuid.uuid4().hex}.lock")
        self.file_name = Path(file_name).resolve()
        self.timeout = timeout
        self.delay = delay
        self.lock_expire = lock_expire

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        start_time = time.time()
        while True:
            current_time = time.time()

            # Timeout
            if current_time - start_time >= self.timeout:
                raise TimeoutError(f"Timeout after {self.timeout} seconds")

            # Expire lock
            if (
                self.file_name.exists() is True
                and current_time - self.file_name.stat().st_mtime > self.lock_expire
            ):
                self.file_name.touch(exist_ok=True)
                return

            # Acquire lock
            try:
                self.file_name.touch(exist_ok=False)
                return
            except FileExistsError:
                try:
                    if current_time - self.file_name.stat().st_mtime > self.lock_expire:
                        self.file_name.touch(exist_ok=True)
                        return
                except FileNotFoundError:
                    pass  # File is deleted by other process, try next loop

            # Delay
            time.sleep(self.delay)

    def release(self):
        self.file_name.unlink(missing_ok=True)

    def __del__(self):
        self.release()
