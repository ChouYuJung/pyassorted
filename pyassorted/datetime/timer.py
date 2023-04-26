import time


class Timer(object):
    def __init__(self):
        self.q = []

    def click(self) -> float:
        self.q.append(time.time())
        return self.read()

    def read(self, intervals: int = 1) -> float:
        if intervals >= 1:
            intervals = int(intervals)
        else:
            raise ValueError(
                "Value intervals must be an integer greater than or equal to 1"
            )
        if not self.q:
            return 0
        elif len(self.q) == 1:
            return 0
        elif len(self.q) - 1 < intervals:
            raise ValueError(f"Value intervals must be less than {len(self.q)}")
        else:
            return self.q[-1] - self.q[-1 - intervals]

    def reset(self):
        self.q = []

    def __enter__(self):
        self.click()
        return self

    def __exit__(self, *args):
        self.click()

    def __str__(self):
        return str(self.elapsed_time)

    def __repr__(self):
        return str(self.elapsed_time)
