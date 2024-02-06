"""
Cloudflare AI Python SDK
"""

__title__ = "cloudflareai"
__author__ = "alexraskin"
__license__ = "Mozilla Public License 2.0"
__version__ = "0.5.0"

from .core import CloudflareAI
from .enums import (
    AiImageClassificationModels,
    AiTranslationModels,
    AiTextGenerationModels,
    AiSpeechRecognitionModels,
    AiTextToImageModels,
    TranslationLanguages,
)
