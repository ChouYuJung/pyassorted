from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Text,
    TypeVar,
    Union,
    cast,
)

from pydantic import BaseModel
from rich import print as rich_print
from rich.table import Table

if TYPE_CHECKING:
    from pyassorted.collections.msg import SimpleMessage

    try:
        from openai.types.beta.threads.message import Message  # type: ignore
        from openai.types.chat import ChatCompletionMessageParam  # type: ignore
    except ImportError:
        pass

T = TypeVar("T")


def display_messages(
    messages: Union[
        Sequence["SimpleMessage"],
        Sequence[Dict[Text, Any]],
        Sequence["ChatCompletionMessageParam"],
        Sequence["Message"],
    ],
    *,
    is_print: bool = True,
    table_title: Text = "Messages",
    table_width: int = 120,
    extra_newline_table_start: bool = True,
    extra_newline_message_end: bool = True,
) -> Text:
    """Display messages in a human-readable format."""

    if not messages:
        raise ValueError("No messages to display.")

    # Convert messages to dictionaries
    _messages = [
        m.model_dump() if isinstance(m, BaseModel) else dict(m) for m in messages
    ]

    # Initialize output
    out = ""
    table: Optional["Table"] = None
    if is_print:
        table = Table(title=table_title, width=table_width)
        table.add_column("Role", justify="right", style="bold cyan")
        table.add_column("Content", justify="left")

    # Read messages
    for m in _messages:
        role = str(m.get("role") or "Unknown").capitalize()
        content = m.get("content") or "n/a"
        if isinstance(content, List):  # OpenAI Threads messages
            _content = ""
            for content_block in content:
                content_block = cast(Dict, content_block)
                if content_block.get("type") == "image_file":
                    _image_file = content_block.get("image_file") or {}
                    _image_id = _image_file.get("file_id") or "n/a"
                    _content += f"<image_file file_id={_image_id}/>"
                elif content_block.get("type") == "image_url":
                    _image_url = content_block.get("image_url") or {}
                    _url = _image_url.get("url") or "n/a"
                    _content += f"<image_url url={_url}/>"
                elif content_block.get("type") == "text":
                    _content_text = content_block.get("text") or {}
                    _content_text_value = _content_text.get("value") or "n/a"
                    _content += str(_content_text_value)
                else:
                    _content += str(content_block)
            content = _content
        else:
            content = str(content)

        content = content.strip()
        if extra_newline_message_end:
            content += "\n"
        if is_print:
            table = cast(Table, table)
            table.add_row(role.rjust(9), content)
        out += f"\n\n{role.capitalize()}:\n{content}"
        out = out.strip()

    if is_print:
        if extra_newline_table_start:
            rich_print("\n")
        rich_print(table)
    return out
