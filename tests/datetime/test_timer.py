import time

from pyassorted.datetime import Timer


def test_timer():
    sleep_time = 0.1
    timer = Timer()
    assert timer.read() == 0
    assert len(timer.q) == 0

    # Test click
    assert timer.click() == 0
    time.sleep(sleep_time)
    round(timer.click(), 1) == sleep_time
    assert len(timer.q) == 2

    # Test context manager
    with timer:
        time.sleep(sleep_time)
    assert round(timer.read(), 1) == sleep_time
    assert len(timer.q) == 4

    # Test intervals
    assert round(timer.read(intervals=3), 1) == sleep_time * 2

    # Test intervals larger than queue error
    try:
        timer.read(intervals=4)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    # Test reset
    timer.reset()
    assert len(timer.q) == 0
    assert timer.read() == 0
