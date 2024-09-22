from typing import Literal, Text

from pyassorted.string.rand import rand_str


def rand_openai_id(
    type: Literal[
        "chat_completion",
        "chatcmpl",
        "assistant",
        "asst",
        "thread",
        "message",
        "msg",
        "run",
    ]
) -> Text:
    if type in ("chat_completion", "chatcmpl"):
        return rand_chat_completion_id()
    elif type in ("assistant", "asst"):
        return rand_assistant_id()
    elif type == "thread":
        return rand_thread_id()
    elif type in ("message", "msg"):
        return rand_message_id()
    elif type == "run":
        return rand_run_id()
    else:
        raise ValueError(f"Invalid type: {type}")


def rand_chat_completion_id() -> Text:
    return f"chatcmpl-{rand_str(29)}"


def rand_assistant_id() -> Text:
    return f"asst_{rand_str(24)}"


def rand_thread_id() -> Text:
    return f"thread_{rand_str(24)}"


def rand_message_id() -> Text:
    return f"msg_{rand_str(24)}"


def rand_run_id() -> Text:
    return f"run_{rand_str(24)}"
