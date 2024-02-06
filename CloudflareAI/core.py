from __future__ import annotations

from typing import Dict, Optional, Union

from .enums import (
    AiImageClassificationModels,
    AiSpeechRecognitionModels,
    AiTextGenerationModels,
    AiTextToImageModels,
    AiTranslationModels,
    TranslationLanguages,
)
from .exceptions import CloudflareException
from .http import Http
from .models import (
    CloudflareAPIResponse,
    CloudflareImageClassificationResponse,
    CloudflareImageResponse,
    CloudflareSpeechRecognitionResponse,
    CloudflareTranslationResponse,
)
from .types import TextGenerationPayload


class CloudflareAI:
    """
    Cloudflare AI API Client

    :param Cloudflare_API_Key: Cloudflare API key.
    :param Cloudflare_Account_Identifier: Cloudflare Account identifier.
    :param retries: Number of retries. Default is 1.
    :param timeout: Timeout in seconds. Default is 60 seconds.

    :raises CloudflareException: If Cloudflare API key or account identifier is not provided.
    """

    def __init__(
        self,
        Cloudflare_API_Key: str,
        Cloudflare_Account_Identifier: str,
        Cloudflare_AI_Gateway_URL: Optional[str] = None,
        Retries: Optional[int] = 1,
        Timeout: Optional[int] = 60,
    ) -> None:
        self.api_key: str = Cloudflare_API_Key
        self.account_identifier: str = Cloudflare_Account_Identifier
        self.gateway_url: str = Cloudflare_AI_Gateway_URL
        self.retries: int = Retries
        self.timeout: int = Timeout
        self._http = Http(api_key=self.api_key, retries=self.retries, timeout=self.timeout)

        if not self.api_key:
            raise CloudflareException("Cloudflare API key is required.")

        if not self.account_identifier:
            raise CloudflareException("Cloudflare account identifier is required.")

    def _build_url(self, model_name: str) -> str:
        """
        Build the AI Model URL.

        :param model_name: Model name.

        :return: str
        """

        if not self.gateway_url:
            return f"https://api.cloudflare.com/client/v4/accounts/{self.account_identifier}/ai/run/{model_name}"

        return f"{self.gateway_url}/{model_name}"

    async def ImageClassification(
        self, image_bytes: bytes, model_name: AiImageClassificationModels
    ) -> Union[CloudflareImageClassificationResponse, CloudflareException]:
        """
        Image classification models take an image input and assigns it labels or classes.

        :param image_path: Path to the image file.
        :param model_name: Model name.

        :return: CloudflareImageClassificationResponse
        """

        if len(image_bytes) > 6 * 1048576:
            raise CloudflareException("Image file size cannot exceed 6MB.")

        url = self._build_url(model_name=model_name.value)
        headers = {"Content-Type": "image/*"}
        response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        return CloudflareImageClassificationResponse(response=response)  # type: ignore

    async def TextGeneration(
        self,
        user_prompt: str,
        system_prompt: str,
        model_name: AiTextGenerationModels,
        stream: Optional[bool] = False,
        max_tokens: Optional[int] = 256,
    ) -> Union[CloudflareAPIResponse, bytes, CloudflareException]:
        """
        Family of generative text models, such as large language models (LLM),
        that can be adapted for a variety of natural language tasks.

        :param user_prompt: User messages are where you actually query the AI by providing a question or a conversation.
        :param system_prompt: System messages define the AI’s personality. You can use them to set rules and how you expect the AI to behave.
        :param model_name: The model to use for text generation.
        :param stream: Stream response or not. Default is False.
        :param max_tokens: Maximum tokens. Default is 256.

        :return: ApiResponse, bytes, CloudflareException
        """

        if len(user_prompt) > 4096:
            raise CloudflareException("Prompt length cannot exceed 4096 characters.")

        if max_tokens > 256:  # type: ignore
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

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        if not stream:
            response = await self._http.fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return CloudflareAPIResponse(response=response)
        else:
            response = await self._http.fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return response

    async def SpeechRecognition(
        self, audio_bytes: bytes, model_name: AiSpeechRecognitionModels
    ) -> Union[CloudflareSpeechRecognitionResponse, CloudflareException]:
        """
        Automatic speech recognition (ASR) models convert a speech signal, typically an audio input, to text.

        :param audio_file: Audio file in bytes.
        :param model_name: Model name.

        :return: CloudflareSpeechRecognitionResponse
        """

        if len(audio_bytes) > 6 * 1048576:
            raise CloudflareException("Audio file size cannot exceed 6MB.")

        url = self._build_url(model_name=model_name.value)
        headers = {"Content-Type": "audio/*"}
        response = await self._http.fetch(
            "POST", url, data=audio_bytes, headers=headers
        )
        return CloudflareSpeechRecognitionResponse(response=response)

    async def Translation(
        self,
        text: str,
        source_lang: TranslationLanguages,
        target_lang: TranslationLanguages,
        model_name: AiTranslationModels,
    ) -> Union[CloudflareTranslationResponse, CloudflareException]:
        """
        Translation models convert a sequence of text from one language to another.

        :param text: Text to translate.
        :param source_lang: Source language.
        :param target_lang: Target language.

        :return: dict or CloudflareException
        """

        if source_lang.value == target_lang.value:
            raise CloudflareException("Source and target languages cannot be the same.")

        url = self._build_url(model_name=model_name.value)

        payload: Dict[str, Union[str, TranslationLanguages]] = {
            "text": text,
            "source_lang": source_lang.value,
            "target_lang": target_lang.value,
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response = await self._http.fetch("POST", url, data=payload, headers=headers)
        return CloudflareTranslationResponse(response)

    async def TextToImage(
        self,
        prompt: str,
        model_name: AiTextToImageModels,
        steps: Optional[int] = 20,
    ) -> Union[CloudflareImageResponse, CloudflareException]:
        """
        Text to image models generate an image from a text input.

        :param prompt: Text to generate image from.
        :param model_name: Model name.

        :return: raw image data or CloudflareException
        """

        if steps > 20:  # type: ignore
            raise CloudflareException("Steps cannot exceed 20.")

        url = self._build_url(model_name=model_name.value)

        payload: Dict[str, str] = {"prompt": prompt, "steps": steps}

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response = await self._http.fetch("POST", url, data=payload, headers=headers)
        return CloudflareImageResponse(response=response)
