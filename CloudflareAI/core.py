from typing import Optional, Union, Dict, TYPE_CHECKING

import os

from .http import Http
from .enums import (
    AiImageClassificationModels,
    AiSpeechRecognitionModels,
    AiTextGenerationModels,
    AiTextToImageModels,
    AiTranslationModels,
    TranslationLanguages,
    ImageToTextModels,
    AISummarizationModels,
    ImageToTextModels,
    ObjectDetectionModels,
)
from .models import (
    CloudflareAPIResponse,
    CloudflareImageClassificationResponse,
    CloudflareImageResponse,
    CloudflareSpeechRecognitionResponse,
    CloudflareTranslationResponse,
    ImageToTextModelsResponse,
)
from .exceptions import CloudflareException


if TYPE_CHECKING:
    import httpx
    from .types import TextGenerationPayload, TextTranslationPayload, TextToImagePayload


class CloudflareAI:
    """
    Cloudflare AI API Client

    Note:
    -----
    These Models are in beta, subject to change and may error out.
    Cloudflare does not recommend using these models in production.

    Parameters:
    -----------
    :param Cloudflare_API_Key: Cloudflare API key.
    :param Cloudflare_Account_Identifier: Cloudflare Account identifier.
    :param Cloudflare_AI_Gateway_URL: Cloudflare AI Gateway URL. Default is None.
    :param retries: Number of retries. Default is 1.
    :param timeout: Timeout in seconds. Default is 60 seconds.

    Exceptions:
    -----------
    :raises CloudflareException: If Cloudflare API key or account identifier is not provided.

    Example:
    --------
    >>> import asyncio
    >>> from CloudflareAI import CloudflareAI, AiImageClassificationModels
    >>> cf = CloudflareAI(Cloudflare_API_Key="API_KEY", Cloudflare_Account_Identifier="ACCOUNT_IDENTIFIER")
    >>> def main():
    >>>   with open("image.jpg", "rb") as file:
    >>>       image = file.read()
    >>>       result = await cf.ImageClassification(image_bytes=image, model_name=AiImageClassificationModels.RESNET_50)
    >>>       print(result.labels)
    >>> asyncio.run(main())

    Methods:
    --------
    - ImageClassification - Image classification models take an image input and assigns it labels or classes.
    - TextGeneration - Family of generative text models, such as large language models (LLM), that can be adapted for a variety of natural language tasks.
    - SpeechRecognition - Automatic speech recognition (ASR) models convert a speech signal, typically an audio input, to text.
    - Translation - Translation models convert a sequence of text from one language to another.
    - TextToImage - Text to image models generate an image from a text input.
    - ImageToText - Image to text models convert an image to text.
    - Summarization - Summarization models generate a summary of a longer piece of text.
    - ObjectDetection - Object detection models detect and classify objects in an image.

    Reference:
    ----------
    url: https://developers.cloudflare.com/workers-ai/
    """

    def __init__(
        self,
        Cloudflare_API_Key: str | None = None,
        Cloudflare_Account_Identifier: str | None = None,
        Cloudflare_AI_Gateway_URL: Optional[str] = None,
        Retries: Optional[int] = 1,
        Timeout: Optional[int] = 60,
    ) -> None:
        if Cloudflare_API_Key is None:
            self.api_key = os.getenv("CLOUDFLARE_API_KEY")
        self.api_key = Cloudflare_API_Key

        if Cloudflare_Account_Identifier is None:
            self.account_identifier = os.getenv("CLOUDFLARE_ACCOUNT_IDENTIFIER")
        self.account_identifier = Cloudflare_Account_Identifier

        self.gateway_url: Union[str, None] = Cloudflare_AI_Gateway_URL
        self.retries: int = Retries
        self.timeout: int = Timeout
        self._http: Http = Http(
            api_key=self.api_key, retries=self.retries, timeout=self.timeout
        )

    def _build_url(self, model_name: str) -> str:
        """
        Build the AI Model URL.

        Parameters:
        -----------
        :param model_name: Model name.

        Returns:
        --------
        :return: str
        """

        if not self.gateway_url:
            return f"https://api.cloudflare.com/client/v4/accounts/{self.account_identifier}/ai/run/{model_name}"

        return f"{self.gateway_url}/{model_name}"

    async def ImageClassification(
        self, image_bytes: bytes, model_name: AiImageClassificationModels
    ) -> CloudflareImageClassificationResponse:
        """
        Image classification models take an image input and assigns it labels or classes.

        Parameters:
        -----------
        :param image_bytes: Image file in bytes.
        :param model_name: Model name.

        Returns:
        --------
        :return: CloudflareImageClassificationResponse
        """

        if isinstance(image_bytes, bytes) is False:
            raise CloudflareException("Image must be in bytes.")

        url: str = self._build_url(model_name=model_name.value)

        headers: Dict[str, str] = {"Content-Type": "image/*"}
        response: httpx.Response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        return CloudflareImageClassificationResponse(response=response)

    async def TextGeneration(
        self,
        user_prompt: str,
        system_prompt: str,
        model_name: AiTextGenerationModels,
        stream: Optional[bool] = False,
        max_tokens: Optional[int] = 256,
    ) -> Union[CloudflareAPIResponse, bytes]:
        """
        Family of generative text models, such as large language models (LLM),
        that can be adapted for a variety of natural language tasks.

        Parameters:
        -----------
        :param user_prompt: User messages are where you actually query the AI by providing a question or a conversation.
        :param system_prompt: System messages define the AI’s personality. You can use them to set rules and how you expect the AI to behave.
        :param model_name: The model to use for text generation.
        :param stream: Stream response or not. Default is False.
        :param max_tokens: Maximum tokens. Default is 256.

        Returns:
        --------
        :return: CloudflareAPIResponse, bytes
        """

        if len(user_prompt) > 4096:
            raise CloudflareException("Prompt length cannot exceed 4096 characters.")

        if max_tokens > 256:
            raise CloudflareException("Max tokens cannot exceed 256.")

        url = self._build_url(model_name=model_name.value)

        payload: TextGenerationPayload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": stream,
            "max_tokens": max_tokens,
        }

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        response: httpx.Response = await self._http.fetch(
            "POST", url, data=payload, headers=headers, stream=stream
        )
        if not stream:
            return CloudflareAPIResponse(response=response)
        return await self._http.process_stream_response(response)

    async def SpeechRecognition(
        self, audio_bytes: bytes, model_name: AiSpeechRecognitionModels
    ) -> Union[CloudflareSpeechRecognitionResponse, CloudflareException]:
        """
        Automatic speech recognition (ASR) models convert a speech signal, typically an audio input, to text.

        Parameters:
        -----------
        :param audio_bytes: Audio file in bytes.
        :param model_name: Model name.

        Returns:
        --------
        :return: CloudflareSpeechRecognitionResponse

        Exceptions:
        -----------
        :raises CloudflareException: If audio is not in bytes or the API returns a non-200 status code.
        """

        if isinstance(audio_bytes, bytes) is False:
            raise CloudflareException("Audio must be in bytes.")

        url: str = self._build_url(model_name=model_name.value)
        headers: Dict[str, str] = {"Content-Type": "audio/*"}
        response: httpx.Response = await self._http.fetch(
            "POST", url, data=audio_bytes, headers=headers
        )
        return CloudflareSpeechRecognitionResponse(response=response)

    async def Translation(
        self,
        text: str,
        source_lang: TranslationLanguages,
        target_lang: TranslationLanguages,
        model_name: AiTranslationModels,
    ) -> CloudflareTranslationResponse:
        """
        Translation models convert a sequence of text from one language to another.

        Parameters:
        -----------
        :param text: Text to translate.
        :param source_lang: Source language.
        :param target_lang: Target language.

        Returns:
        :return: CloudflareTranslationResponse
        """

        if source_lang.value == target_lang.value:
            raise CloudflareException("Source and target languages cannot be the same.")

        url = self._build_url(model_name=model_name.value)

        payload: TextTranslationPayload = {
            "text": text,
            "source_lang": source_lang.value,
            "target_lang": target_lang.value,
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response: httpx.Response = await self._http.fetch(
            "POST", url, data=payload, headers=headers
        )
        return CloudflareTranslationResponse(response=response)

    async def TextToImage(
        self,
        prompt: str,
        model_name: AiTextToImageModels,
        steps: Optional[int] = 20 | 20,
    ) -> CloudflareImageResponse:
        """
        Text to image models generate an image from a text input.

        Parameters:
        -----------
        :param prompt: Text to generate image from.
        :param model_name: Model name.
        :param steps: Number of steps. Default is 20.

        Returns:
        --------
        :return: CloudflareImageResponse
        """

        if steps > 20:
            raise CloudflareException("Steps cannot exceed 20.")

        url: str = self._build_url(model_name=model_name.value)

        payload: TextToImagePayload = {
            "prompt": prompt,
            "steps": steps,
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response: httpx.Response = await self._http.fetch(
            "POST", url, data=payload, headers=headers
        )
        return CloudflareImageResponse(response=response)

    async def ImageToText(
        self, image_bytes: bytes, model: ImageToTextModels
    ) -> ImageToTextModelsResponse:
        """
        Image to text models convert an image to text.

        Parameters:
        -----------
        :param image_bytes: Image file in bytes.
        :param model: Model name.

        Returns:
        --------
        :return: ImageToTextModelsResponse
        """

        if isinstance(image_bytes, bytes) is False:
            raise CloudflareException("Image must be in bytes.")

        url: str = self._build_url(model_name=model.value)
        headers: dict[str, str] = {"Content-Type": "image/*"}

        response: httpx.Response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        return ImageToTextModelsResponse(response=response)

    async def Summarization(
        self, text: str, model_name: AISummarizationModels
    ) -> CloudflareAPIResponse:
        """
        Summarization models generate a summary of a longer piece of text.

        Parameters:
        -----------
        :param text: Text to summarize.
        :param model_name: Model name.

        Returns:
        --------
        :return: CloudflareAPIResponse
        """

        url: str = self._build_url(model_name=model_name.value)

        payload: Dict[str, str] = {"text": text}

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response: httpx.Response = await self._http.fetch(
            "POST", url, data=payload, headers=headers
        )
        return CloudflareAPIResponse(response=response)

    async def ObjectDetection(
        self, image_bytes: bytes, model_name: ObjectDetectionModels
    ) -> CloudflareAPIResponse:
        """
        Object detection models detect and classify objects in an image.

        Parameters:
        -----------
        :param image_bytes: Image file in bytes.
        :param model_name: Model name.

        Returns:
        --------
        :return: CloudflareAPIResponse
        """

        if isinstance(image_bytes, bytes) is False:
            raise CloudflareException("Image must be in bytes.")

        url: str = self._build_url(model_name=model_name.value)
        headers: dict = {"Content-Type": "image/*"}
        response: httpx.Response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        return CloudflareAPIResponse(response=response)
