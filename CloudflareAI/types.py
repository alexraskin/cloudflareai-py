from typing import TypedDict, List


class Message(TypedDict):
    role: str
    content: str


class TextGenerationPayload(TypedDict):
    messages: List[Message]
    stream: str
    max_tokens: int


class Result(TypedDict):
    response: str


class Response(TypedDict):
    result: Result
    success: bool
    errors: list
    messages: list
