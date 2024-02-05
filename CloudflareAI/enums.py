from enum import Enum


class AiImageClassificationModels(Enum):
    """
    Enum for Image Classification models

    Attributes:
    ----------
    RESNET_50 : str : "@cf/microsoft/resnet-50"
    """

    RESNET_50 = "@cf/microsoft/resnet-50"


class AiTranslationModels(Enum):
    """
    Enum for Translation models

    Attributes:
    ----------
    META_100 : str : "@cf/meta/m2m100-1.2b"
    """

    META_100 = "@cf/meta/m2m100-1.2b"


class AiTextGenerationModels(Enum):
    """
    Enum for Text Generation models

    Attributes:
    ----------
    LLAMA_2_7B : str : "@cf/meta/llama-2-7b-chat-fp16"
    LLAMA_2_7B_INT8 : str : "@cf/meta/llama-2-7b-chat-int8"
    MISTRAL_7B : str : "@cf/mistral/mistral-7b-instruct-v0.1"
    CODE_LLAMA_7B : str : "@hf/thebloke/codellama-7b-instruct-awq"
    """

    LLAMA_2_7B = "@cf/meta/llama-2-7b-chat-fp16"
    LLAMA_2_7B_INT8 = "@cf/meta/llama-2-7b-chat-int8"
    MISTRAL_7B = "@cf/mistral/mistral-7b-instruct-v0.1"
    CODE_LLAMA_7B = "@hf/thebloke/codellama-7b-instruct-awq"


class AiSpeechRecognitionModels(Enum):
    """
    Enum for Speech Recognition models

    Attributes:
    ----------
    WHISPER : str : "@cf/openai/whisper"
    """

    WHISPER = "@cf/openai/whisper"


class AiTextToImageModels(Enum):
    """
    Enum for Text to Image models

    Attributes:
    ----------
    XL_BASE : str : "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    """

    XL_BASE = "@cf/stabilityai/stable-diffusion-xl-base-1.0"


class TranslationLanguages(Enum):
    """
    Enum for Translation languages

    Attributes:
    ----------
    EN : str : "english"
    CH : str : "chinese"
    FR : str : "french"
    ES : str : "spanish"
    AR : str : "arabic"
    RU : str : "russian"
    DE : str : "german"
    JA : str : "japanese"
    PT : str : "portuguese"
    HI : str : "hindi"
    """

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
