from typing import TypedDict


class TextGenerationPayload(TypedDict):
    """Payload for text generation"""

    messages: list[dict[str, str]]
    stream: str
    max_tokens: int


class TextTranslationPayload(TypedDict):
    """Payload for text translation"""

    text: str
    source_lang: str
    target_lang: str


class TextToImagePayload(TypedDict):
    """Payload for text to image"""

    prompt: str
    steps: int
