from typing import List, TypedDict


class Message(TypedDict):
    role: str
    content: str


class TextGenerationPayload(TypedDict):
    messages: List[Message]
    stream: str
    max_tokens: int
