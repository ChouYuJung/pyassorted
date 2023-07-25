import re
from typing import Text


def is_valid_filename(filename: Text) -> bool:
    """Checks if a filename is valid."""

    if len(filename) > 255:
        return False

    if re.match(r"^[\w\-. ]+$", filename) is None:
        return False

    return True


def sanitize_filename(filename: Text) -> Text:
    """Sanitize the filename by replacing invalid characters and spaces."""

    filename = re.sub(r'[\\/*?:"<>| ]', "_", filename)
    return filename
