import os
from typing import Mapping, Optional, Union

import aiofiles
import httpx
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from .errors import CloudflareException
from .models import (
    AiImageClassificationModels,
    AiSpeechRecognitionModels,
    AiTextGenerationModels,
    AiTextToImageModels,
    AiTranslationModels,
    TranslationLanguages,
)


class CloudflareAI:
    """
    Cloudflare AI API wrapper.

    :param api_key: Cloudflare API key.
    :param account_identifier: Cloudflare account identifier.
    :param retries: Number of retries. Default is 1.
    :param timeout: Timeout in seconds. Default is 60 seconds.
    """

    def __init__(
        self,
        Cloudflare_API_Key: str,
        Cloudflare_Account_Identifier: str,
        Retries: Optional[int] = 1,
        Timeout: Optional[int] = 60,
    ) -> None:
        self.api_key: str = Cloudflare_API_Key
        self.account_identifier: str = Cloudflare_Account_Identifier
        self.retries: int = Retries or 1
        self.timeout: int = Timeout or 60
        self.base_url: str = "https://api.cloudflare.com/client/v4/accounts/{account_identifier}/ai/run/{model_name}"
        self.headers: Mapping[str, str] = {
            "Authorization": f"Bearer {Cloudflare_API_Key}",
        }

        if not self.api_key:
            raise CloudflareException("Cloudflare API key is required.")

        if not self.account_identifier:
            raise CloudflareException("Cloudflare account identifier is required.")

        self.transport = httpx.AsyncHTTPTransport(retries=self.retries)

    def build_url(self, model_name: str) -> str:
        """
        Build the AI Model URL.

        :param model_name: Model name.

        :return: str
        """

        return self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )

    async def streaming_response(self, response: httpx.Response) -> StreamingResponse:
        """
        Streaming response.

        :param response: httpx response.

        :return: StreamingResponse
        """
        return StreamingResponse(
            response.aiter_bytes(),
            background=BackgroundTask(response.close),
        )

    async def _fetch(
        self,
        method: str,
        url: str,
        data: dict,
        headers: Optional[Mapping[str, str]] = None,
        stream: Optional[bool] = False,
    ) -> Union[httpx.Response, StreamingResponse, CloudflareException]:
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

        if headers is not None:
            self.headers.update(headers)  # type: ignore
        async with httpx.AsyncClient(transport=self.transport) as client:
            if headers["Content-Type"] == "application/json":  # type: ignore
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
                    return await self.streaming_response(response)
                else:
                    return response
            else:
                raise CloudflareException(
                    f"Error {response.status_code}: {response.reason_phrase}"
                )

    async def ImageClassification(
        self, image_path: str, model_name: AiImageClassificationModels
    ) -> Union[dict, CloudflareException]:
        """
        Image classification models take an image input and assigns it labels or classes.

        :param image_path: Path to the image file.
        :param model_name: Model name.

        :return: dict
        """

        url = self.build_url(model_name=model_name.value)

        check_image_path = os.path.isfile(image_path)
        if not check_image_path:
            raise CloudflareException(f"Image path {image_path} is not a file.")

        async with aiofiles.open(image_path, "rb") as img_file:
            image_data = await img_file.read()
            headers: Mapping[str, str] = {
                "Content-Type": "image/jpeg",
            }
            response = await self._fetch("POST", url, data=image_data, headers=headers)  # type: ignore
            return response.json()  # type: ignore

    async def TextGeneration(
        self,
        prompt: str,
        system_prompt: str,
        model_name: AiTextGenerationModels,
        stream: Optional[bool] = False,
        max_tokens: Optional[int] = 256,
    ) -> Union[dict, StreamingResponse, CloudflareException]:
        """
        Family of generative text models, such as large language models (LLM), that can be adapted for a variety of natural language tasks.

        :param prompt: Prompt to generate text from.
        :param system_prompt: System prompt to generate text from.

        :return: dict or CloudflareException
        """

        if len(prompt) > 4096:
            raise CloudflareException("Prompt length cannot exceed 4096 characters.")

        if max_tokens > 256:  # type: ignore
            raise CloudflareException("Max tokens cannot exceed 256.")

        url = self.build_url(model_name=model_name.value)

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": stream,
            "max_tokens": max_tokens,
        }

        headers = {
            "Content-Type": "application/json",
        }

        if not stream:
            response = await self._fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return response.json()  # type: ignore
        else:
            response = await self._fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return response  # type: ignore

    async def SpeechRecognition(
        self, audio_path: str, model_name: AiSpeechRecognitionModels
    ) -> Union[dict, CloudflareException]:
        """
        Automatic speech recognition (ASR) models convert a speech signal, typically an audio input, to text.

        :param audio_path: Path to the audio file.
        :param model_name: Model name.

        :return: dict
        """
        if not os.path.isfile(audio_path):
            raise CloudflareException(f"Audio path {audio_path} is not a file.")

        url = self.build_url(model_name=model_name.value)

        async with aiofiles.open(audio_path, "rb") as audio_file:
            audio_data: bytes = await audio_file.read()
            headers = {
                "Content-Type": "audio/wav",
            }
            response = await self._fetch("POST", url, data=audio_data, headers=headers)  # type: ignore
            return response.json()  # type: ignore

    async def Translation(
        self,
        text: str,
        source_lang: TranslationLanguages,
        target_lang: TranslationLanguages,
        model_name: AiTranslationModels,
    ) -> Union[dict, CloudflareException]:
        """
        Translation models convert a sequence of text from one language to another.

        :param text: Text to translate.
        :param source_lang: Source language.
        :param target_lang: Target language.

        :return: dict or CloudflareException
        """

        if source_lang.value == target_lang.value:
            raise CloudflareException("Source and target languages cannot be the same.")

        url = self.build_url(model_name=model_name.value)

        payload = {
            "text": text,
            "source_lang": source_lang.value,
            "target_lang": target_lang.value,
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = await self._fetch("POST", url, data=payload, headers=headers)
        return response.json()  # type: ignore

    async def TextToImage(
        self,
        prompt: str,
        model_name: AiTextToImageModels,
        steps: Optional[int] = 20,
    ) -> Union[bytes, CloudflareException]:
        """
        Text to image models generate an image from a text input.

        :param prompt: Text to generate image from.
        :param model_name: Model name.

        :return: raw image data or CloudflareException
        """

        if steps > 20: # type: ignore
            raise CloudflareException("Steps cannot exceed 20.")

        url = self.build_url(model_name=model_name.value)

        payload = {"prompt": prompt, "steps": steps}

        headers = {
            "Content-Type": "application/json",
        }

        response = await self._fetch("POST", url, data=payload, headers=headers)
        return response.content  # type: ignore
