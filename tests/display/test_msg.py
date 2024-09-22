import pytest

from pyassorted.display.msg import display_messages


@pytest.mark.parametrize(
    "messages, is_print",
    [
        ([], True),  # Test with empty messages
        ([{"role": "user", "content": "Hello"}], True),  # Test with a single message
    ],
)
def test_display_messages(messages, is_print):
    if not messages:
        with pytest.raises(ValueError):
            display_messages(messages, is_print=is_print)
    else:
        display_messages(messages, is_print=is_print)
