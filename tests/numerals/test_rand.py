import pytest

from pyassorted.numerals.rand import rand_port


def test_rand_port():
    # Test that the function returns a value within the specified range
    for _ in range(100):  # Run the test multiple times
        port = rand_port()
        assert 30000 <= port <= 32767

    # Test with custom range
    custom_min = 40000
    custom_max = 50000
    for _ in range(100):
        port = rand_port(custom_min, custom_max)
        assert custom_min <= port <= custom_max
