from enum import Enum


class AiImageClassificationModels(Enum):
    RESNET_50 = "@cf/microsoft/resnet-50"


class AiTranslationModels(Enum):
    META_100 = "@cf/meta/m2m100-1.2b"


class AiTextGenerationModels(Enum):
    LLAMA_2_7B = "@cf/meta/llama-2-7b-chat-fp16"
    LLAMA_2_7B_INT8 = "@cf/meta/llama-2-7b-chat-int8"
    MISTRAL_7B = "@cf/mistral/mistral-7b-instruct-v0.1"
    CODE_LLAMA_7B = "@hf/thebloke/codellama-7b-instruct-awq"


class AiSpeechRecognitionModels(Enum):
    WHISPER = "@cf/openai/whisper"


class AiTextToImageModels(Enum):
    XL_BASE = "@cf/stabilityai/stable-diffusion-xl-base-1.0"


class TranslationLanguages(Enum):
    EN = "english"
    CH = "chinese"
    FR = "french"
    ES = "spanish"
    AR = "arabic"
    RU = "russian"
    DE = "german"
    JA = "japanese"
    PT = "portuguese"
    HI = "hindi"
