from typing import Text


def display_object(obj: object) -> Text:
    """Display an object in a human-readable format."""

    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
