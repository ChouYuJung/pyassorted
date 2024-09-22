from typing import Text

from pydantic import BaseModel

try:
    from openai.types.beta.threads.message import Message  # type: ignore
except ImportError:
    pass


class SimpleMessage(BaseModel):
    role: Text
    content: Text

    @classmethod
    def from_openai_threads_message(cls, message: "Message"):
        """Builds a Message object from an OpenAI Threads message"""

        message_text = ""
        for message_content in message.content:
            if message_content.type == "text":
                message_text += message_content.text.value
        return cls.model_validate(
            {"role": message.role, "content": message_text.strip()}
        )
