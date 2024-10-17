import itertools
from typing import Iterable


def chunks(items: Iterable, batch_size: int = 100):
    """A helper function to break an iterable into chunks of size batch_size."""

    it = iter(items)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))
