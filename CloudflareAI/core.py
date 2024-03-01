from typing import Optional, Union, Dict

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


class CloudflareAI:
    """
    Cloudflare AI API Client

    :param Cloudflare_API_Key: Cloudflare API key.
    :param Cloudflare_Account_Identifier: Cloudflare Account identifier.
    :param Cloudflare_AI_Gateway_URL: Cloudflare AI Gateway URL. Default is None.
    :param retries: Number of retries. Default is 1.
    :param timeout: Timeout in seconds. Default is 60 seconds.

    :raises CloudflareException: If Cloudflare API key or account identifier is not provided.

    url: https://developers.cloudflare.com/workers-ai/
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
        self.gateway_url: Union[str, None] = Cloudflare_AI_Gateway_URL
        self.retries: int = Retries if Retries is not None else 1
        self.timeout: int = Timeout if Timeout is not None else 60
        self._http = Http(
            api_key=self.api_key, retries=self.retries, timeout=self.timeout
        )

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
        if response.status_code != 200:
            return CloudflareException(
                f"The request failed with status code {response.status_code}."
            )
        return CloudflareImageClassificationResponse(response=response)

    async def TextGeneration(
        self,
        user_prompt: str,
        system_prompt: str,
        model_name: AiTextGenerationModels,
        stream=False,
        max_tokens=256,
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

        if max_tokens > 256:
            raise CloudflareException("Max tokens cannot exceed 256.")

        url = self._build_url(model_name=model_name.value)

        payload: dict = {
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

        response = await self._http.fetch(
            "POST", url, data=payload, headers=headers, stream=stream
        )
        if response.status_code != 200:
            return CloudflareException(
                f"The request failed with status code {response.status_code}."
            )
        if not stream:
            return CloudflareAPIResponse(response=response)
        return await self._http.process_stream_response(response)

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
        if response.status_code != 200:
            return CloudflareException(
                f"The request failed with status code {response.status_code}."
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
        if response.status_code != 200:
            return CloudflareException(
                f"The API returned a non 200 statusCode: {response.status_code}."
            )
        return CloudflareTranslationResponse(response=response)

    async def TextToImage(
        self,
        prompt: str,
        model_name: AiTextToImageModels,
        steps=20,
    ) -> Union[CloudflareImageResponse, CloudflareException]:
        """
        Text to image models generate an image from a text input.

        :param prompt: Text to generate image from.
        :param model_name: Model name.

        :return: raw image data or CloudflareException
        """

        if steps > 20:
            raise CloudflareException("Steps cannot exceed 20.")

        url = self._build_url(model_name=model_name.value)

        payload: Dict[
            str,
            Union[str, int],
        ] = {
            "prompt": prompt,
            "steps": steps,
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response = await self._http.fetch("POST", url, data=payload, headers=headers)
        if response.status_code != 200:
            return CloudflareException(
                f"The API returned a non 200 statusCode: {response.status_code}."
            )
        return CloudflareImageResponse(response=response)

    async def ImageToText(
        self, image_bytes: bytes, model: ImageToTextModels
    ) -> Union[ImageToTextModelsResponse, CloudflareException]:
        """
        Image to text models convert an image to text.

        :param image_bytes: Image file in bytes.

        :return: str or CloudflareException
        """

        if len(image_bytes) > 6 * 1048576:
            raise CloudflareException("Image file size cannot exceed 6MB.")

        url = self._build_url(model_name=model.value)
        headers: dict = {"Content-Type": "image/*"}
        response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        if response.status_code != 200:
            return CloudflareException(
                f"The API returned a non 200 statusCode: {response.status_code}."
            )
        return ImageToTextModelsResponse(response=response)

    async def Summarization(
        self, text: str, model_name: AISummarizationModels
    ) -> Union[CloudflareAPIResponse, CloudflareException]:
        """
        Summarization models generate a summary of a longer piece of text.

        :param text: Text to summarize.
        :param model_name: Model name.

        :return: dict or CloudflareException
        """

        url = self._build_url(model_name=model_name.value)

        payload: Dict[str, str] = {"text": text}

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        response = await self._http.fetch("POST", url, data=payload, headers=headers)
        if response.status_code != 200:
            return CloudflareException(
                f"The API returned a non 200 statusCode: {response.status_code}."
            )
        return CloudflareAPIResponse(response=response)

    async def ObjectDetection(
        self, image_bytes: bytes, model_name: ObjectDetectionModels
    ) -> Union[CloudflareAPIResponse, CloudflareException]:
        """
        Object detection models detect and classify objects in an image.

        :param image_bytes: Image file in bytes.
        :param model_name: Model name.

        :return: dict or CloudflareException
        """

        if len(image_bytes) > 6 * 1048576:
            raise CloudflareException("Image file size cannot exceed 6MB.")

        url = self._build_url(model_name=model_name.value)
        headers: dict = {"Content-Type": "image/*"}
        response = await self._http.fetch(
            "POST", url, data=image_bytes, headers=headers
        )
        if response.status_code != 200:
            return CloudflareException(
                f"The API returned a non 200 statusCode: {response.status_code}."
            )
        return CloudflareAPIResponse(response=response)
