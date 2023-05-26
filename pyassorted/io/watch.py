import time
from pathlib import Path
from typing import Generator, Text, Union


def watch(
    filepath: Union[Path, Text], frequency: float = 0.1
) -> Generator[Union[Path, Text], None, None]:
    """Watch a file for changes.

    Parameters
    ----------
    filepath : Union[Path, Text]
        Path to file to watch.
    frequency : float, optional
        Frequency to check for changes, by default 0.1

    Yields
    ------
    Union[Path, Text]
        Path to file that has changed.

    Examples
    --------
    >>> from pyassorted.io import watch
    >>> for filepath in watch('file.txt'):
    ...     print(filepath)
    """

    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Path '{filepath}' does not exist.")
    file_mtime = filepath.stat().st_mtime

    while True:
        file_mtime_now = filepath.stat().st_mtime
        if file_mtime_now != file_mtime:
            file_mtime = file_mtime_now
            yield filepath
        else:
            time.sleep(frequency)
