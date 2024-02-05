"""
Cloudflare AI Python SDK
"""

__title__ = "cloudflareai"
__author__ = "alexraskin"
__license__ = "MIT"
__version__ = "0.1.0"

from .core import CloudflareAI
from .enums import (
  AiImageClassificationModels,
  AiTranslationModels,
  AiTextGenerationModels,
  AiSpeechRecognitionModels,
  AiTextToImageModels,
  TranslationLanguages
)