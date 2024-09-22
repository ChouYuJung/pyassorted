import json
from typing import Any, List, Text

from pydantic import BaseModel
from rich import box
from rich import print as rich_print
from rich.style import StyleType
from rich.table import Table
from rich.text import Text as RichText


def debug_print(
    *values: Any,
    title: Text = "Debug Print",
    box: box.Box | None = box.HEAVY_HEAD,
    colors: List[StyleType] = [
        "bright_blue",
        "bright_cyan",
        "bright_green",
        "bright_magenta",
    ],
) -> None:
    if not values:
        return
    tb = Table(title=RichText(title), box=box, show_header=False)
    for idx, value in enumerate(values):
        style = colors[idx % len(colors)]
        if isinstance(value, BaseModel):
            tb.add_row(value.model_dump_json(indent=2), style=style)
        elif isinstance(value, dict):
            tb.add_row(json.dumps(value, indent=2, ensure_ascii=False), style=style)
        else:
            tb.add_row(str(value), style=style)
    rich_print(tb)
