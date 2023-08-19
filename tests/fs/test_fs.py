import os

from pyassorted.fs import create_dummy_file


def test_create_dummy_file():
    filepath = create_dummy_file(size_mb=2)
    os.remove(filepath)
