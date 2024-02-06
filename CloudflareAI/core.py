from typing import Optional, Union, Dict

import httpx

from .exceptions import CloudflareException
from .enums import (
    AiImageClassificationModels,
    AiSpeechRecognitionModels,
    AiTextGenerationModels,
    AiTextToImageModels,
    AiTranslationModels,
    TranslationLanguages,
)

from .types import TextGenerationPayload
from .models import (
    CloudflareAPIResponse,
    CloudflareImageResponse,
    CloudflareTranslationResponse,
    CloudflareSpeechRecognitionResponse,
    CloudflareImageClassificationResponse,
)


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

        if not self.api_key:
            raise CloudflareException("Cloudflare API key is required.")

        if not self.account_identifier:
            raise CloudflareException("Cloudflare account identifier is required.")

        self._transport = httpx.AsyncHTTPTransport(retries=self.retries)

    def _build_url(self, model_name: str) -> str:
        """
        Build the AI Model URL.

        :param model_name: Model name.

        :return: str
        """

        if not self.gateway_url:
            return f"https://api.cloudflare.com/client/v4/accounts/{self.account_identifier}/ai/run/{model_name}"

        return f"{self.gateway_url}/{model_name}"

    async def _process_stream_response(self, response: httpx.Response) -> bytes:
        """ "
        Process the stream response.

        :param response: httpx response.

        :return: bytes
        """
        data = b""
        async for chunk in response.aiter_bytes():
            data += chunk
        return data.decode("utf-8")

    async def _fetch(
        self,
        method: str,
        url: str,
        data: dict,
        headers: Optional[Dict[str, str]] = None,
        stream: Optional[bool] = False,
    ) -> Union[httpx.Response, bytes, CloudflareException]:
        """
        httpx request wrapper.
        Please note that this method is for internal use only.

        :param method: HTTP method.
        :param url: URL.
        :param data: Request data.
        :param headers: Request headers.
        :param stream: Stream response.

        :return: httpx response, StreamingResponse or CloudflareException
        """
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
        }

        if headers is not None:
            self.headers.update(headers)  # type: ignore
        async with httpx.AsyncClient(transport=self._transport) as client:
            if headers.get("Content-Type") == "application/json":  # type: ignore
                req = client.build_request(
                    method, url, headers=self.headers, json=data, timeout=self.timeout
                )
            else:
                req = client.build_request(
                    method, url, headers=self.headers, data=data, timeout=self.timeout
                )
            response = await client.send(req, stream=stream)  # type: ignore
            if response.status_code == 200:
                if stream:
                    return await self._process_stream_response(response)
                else:
                    return response
            else:
                raise CloudflareException(
                    f"Error {response.status_code}: {response.reason_phrase}"
                )

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
        response = await self._fetch("POST", url, data=image_bytes, headers=headers)  # type: ignore
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
        Family of generative text models, such as large language models (LLM), that can be adapted for a variety of natural language tasks.

        :param user_prompt: Prompt to generate text from.
        :param system_prompt: Prompt to tell the model what to do.
        :param model_name: Model enum 
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
            response = await self._fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return CloudflareAPIResponse(response=response)
        else:
            response = await self._fetch(
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
        response = await self._fetch("POST", url, data=audio_bytes, headers=headers)
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

        response = await self._fetch("POST", url, data=payload, headers=headers)
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

        response = await self._fetch("POST", url, data=payload, headers=headers)
        return CloudflareImageResponse(response=response)
