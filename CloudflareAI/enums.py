"""
Enums for AI models

View more information here: https://developers.cloudflare.com/workers-ai/models/text-generation/
"""

from enum import Enum


class AiImageClassificationModels(Enum):
    """
    Enum for Image Classification models

    Attributes:
    ----------
    RESNET_50 : str : "@cf/microsoft/resnet-50"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    RESNET_50 = "@cf/microsoft/resnet-50"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class AiTranslationModels(Enum):
    """
    Enum for Translation models

    Attributes:
    ----------
    META_100 : str : "@cf/meta/m2m100-1.2b"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    META_100 = "@cf/meta/m2m100-1.2b"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class AiTextGenerationModels(Enum):
    """
    Enum for Text Generation models

    Attributes:
    ----------
    LLAMA_2_7B : str : "@cf/meta/llama-2-7b-chat-fp16"
    LLAMA_2_7B_INT8 : str : "@cf/meta/llama-2-7b-chat-int8"
    MISTRAL_7B : str : "@cf/mistral/mistral-7b-instruct-v0.1"
    CODE_LLAMA_7B : str : "@hf/thebloke/codellama-7b-instruct-awq"
    CODE_LLAMA_2_13B : str : "@hf/thebloke/llama-2-13b-chat-awq"
    ZEPHYR_7B : str : "@hf/thebloke/zephyr-7b-beta-awq"
    MISTRAL_7B_AWQ : str : "@hf/thebloke/mistral-7b-instruct-v0.1-awq"
    OPENHERMES_MISTRAL_7B : str : "@hf/thebloke/openhermes-2.5-mistral-7b-awq"
    NEURAL_CHAT_7B : str : "@hf/thebloke/neural-chat-7b-v3-1-awq"
    LLAMA_GUARD_7B : str : "@hf/thebloke/llamaguard-7b-awq"
    DEEPSEEK_CODER_6_7_BASE : str : "@hf/thebloke/deepseek-coder-6.7b-base-awq"
    DEEPSEEK_CODER_6_7_INSTRUCT : str : "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"
    DEEPSEEK_CODER_6_7_INSTRUCT_V2 : str : "@hf/thebloke/deepseek-coder-6.7b-instruct-v2-awq"
    DEEPSEEK_MATH_7B_INSTRUCT : str : "@cf/deepseek-ai/deepseek-math-7b-instruct"
    OPENCHAT_3_5 : str : "@cf/openai/openchat-3-5"
    PHI_2 : str : "@cf/phi/phi-2"
    TINYLAMA_1_1B : str : "@cf/tinyllama/tinyllama-1.1b-chat-v1.0"
    DISCOLM_GERMAN_7B : str : "@cf/thebloke/discolm-german-7b-v1-awq"
    QWEN_1_5_0_5B_CHAT : str : "@cf/qwen/qwen-1.5.0.5b-chat"
    QWEN1_5_1_8B_CHAT : str : "@cf/qwen/qwen1.5-1.8b-chat"
    QWEN_1_5_7B_CHAT_AWQ : str : "@cf/qwen/qwen1.5-7b-chat-awq"
    QWEN_1_5_14B_CHAT_AWQ : str : "@cf/qwen/qwen1.5-14b-chat-awq"
    FALCON_7B_INSTRUCT : str : "@cf/falcon/falcon-7b-instruct"
    SQL_CODER_7B_2 : str : "@cf/defog/sqlcoder-7b-2"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    LLAMA_2_7B = "@cf/meta/llama-2-7b-chat-fp16"
    LLAMA_2_7B_INT8 = "@cf/meta/llama-2-7b-chat-int8"
    MISTRAL_7B = "@cf/mistral/mistral-7b-instruct-v0.1"
    CODE_LLAMA_7B = "@hf/thebloke/codellama-7b-instruct-awq"
    CODE_LLAMA_2_13B = "@hf/thebloke/llama-2-13b-chat-awq"
    ZEPHYR_7B = "@hf/thebloke/zephyr-7b-beta-awq"
    MISTRAL_7B_AWQ = "@hf/thebloke/mistral-7b-instruct-v0.1-awq"
    OPENHERMES_MISTRAL_7B = "@hf/thebloke/openhermes-2.5-mistral-7b-awq"
    NEURAL_CHAT_7B = "@hf/thebloke/neural-chat-7b-v3-1-awq"
    LLAMA_GUARD_7B = "@hf/thebloke/llamaguard-7b-awq"
    DEEPSEEK_CODER_6_7_BASE = "@hf/thebloke/deepseek-coder-6.7b-base-awq"
    DEEPSEEK_CODER_6_7_INSTRUCT = "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"
    DEEPSEEK_MATH_7B_INSTRUCT = "@cf/deepseek-ai/deepseek-math-7b-instruct"
    OPENCHAT_3_5 = "@cf/openchat/openchat-3.5-0106"
    PHI_2 = "@cf/microsoft/phi-2"
    TINYLAMA_1_1B = "@cf/tinyllama/tinyllama-1.1b-chat-v1.0"
    DISCOLM_GERMAN_7B = "@cf/thebloke/discolm-german-7b-v1-awq"
    QWEN_1_5_0_5B_CHAT = "@cf/qwen/qwen1.5-0.5b-chat"
    QWEN1_5_1_8B_CHAT = "@cf/qwen/qwen1.5-1.8b-chat"
    QWEN_1_5_7B_CHAT_AWQ = "@cf/qwen/qwen1.5-7b-chat-awq"
    QWEN_1_5_14B_CHAT_AWQ = "@cf/qwen/qwen1.5-14b-chat-awq"
    FALCON_7B_INSTRUCT = "@cf/tiiuae/falcon-7b-instruct"
    SQL_CODER_7B_2 = "@cf/defog/sqlcoder-7b-2"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class ImageToTextModels(Enum):
    """
    Enum for Image to Text models

    Attributes:
    ----------
    UFORM_GEN2_QWEN_500M : str = "@cf/unum/uform-gen2-qwen-500m"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    UFORM_GEN2_QWEN_500M = "@cf/unum/uform-gen2-qwen-500m"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class AiSpeechRecognitionModels(Enum):
    """
    Enum for Speech Recognition models

    Attributes:
    ----------
    WHISPER : str : "@cf/openai/whisper"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    WHISPER = "@cf/openai/whisper"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class AiTextToImageModels(Enum):
    """
    Enum for Text to Image models

    Attributes:
    ----------
    XL_BASE : str : "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    DREAMSHAPER_8_LCM : str : "@cf/lykon/dreamshaper-8-lcm"
    STABLE_DIFFUSION_1_5_INPAINTING : str : "@cf/runwayml/stable-diffusion-v1-5-inpainting"
    STABLE_DIFFUSION_1_5_IMG_2_IMG : str : "@cf/runwayml/stable-diffusion-v1-5-img2img"
    STABLE_DIFFUSION_XL_LIGHTNING : str : "@cf/bytedance/stable-diffusion-xl-lightning"

    methods:
    --------
    models(cls) -> list[str]: return a list of models
    """

    STABLE_DIFFUSION_XL_BASE_1_0 = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    DREAMSHAPER_8_LCM = "@cf/lykon/dreamshaper-8-lcm"
    STABLE_DIFFUSION_1_5_INPAINTING = "@cf/runwayml/stable-diffusion-v1-5-inpainting"
    STABLE_DIFFUSION_1_5_IMG_2_IMG = "@cf/runwayml/stable-diffusion-v1-5-img2img"
    STABLE_DIFFUSION_XL_LIGHTNING = "@cf/bytedance/stable-diffusion-xl-lightning"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class AISummarizationModels(Enum):
    """
    Enum for Summarization models

    Attributes:
    _________
    BART_LARGE_CNN : str : "@cf/facebook/bart-large-cnn"

    methods:
    --------
    models(cls) -> list[str]: return a list of models

    """

    BART_LARGE_CNN = "@cf/facebook/bart-large-cnn"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


class ObjectDetectionModels(Enum):
    """
    Enum for Object Detection models

    Attributes:
    ----------
    DETR_RESNET_50 : str : "@cf/meta/detr-resnet-50"

    methods:
    --------
    models(cls) -> list[str]: return a list of models

    """

    DETR_RESNET_50 = "@cf/meta/detr-resnet-50"

    @classmethod
    def models(cls) -> list[str]:
        return [model.value for model in cls]


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

    methods:
    --------
    languages(cls) -> list[str]: return a list of languages
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

    @classmethod
    def languages(cls) -> list[str]:
        return [lang.value for lang in cls]
