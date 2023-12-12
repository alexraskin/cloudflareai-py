import os
import json
import httpx
import aiofiles
from io import BytesIO
from PIL import Image

from typing import Union

from .errors import CloudflareAIError
from .tools import process_streaming_response
from .const import CloudflareAIConst

class CloudflareAI:
    """
    Cloudflare AI API wrapper.

    :param api_key: Cloudflare API key.
    :param account_identifier: Cloudflare account identifier.
    """

    def __init__(self, Cloudflare_API_Key: str, Cloudflare_Account_Identifier: str) -> None:
        self.api_key: str = Cloudflare_API_Key
        self.account_identifier: str = Cloudflare_Account_Identifier
        self.base_url: str = "https://api.cloudflare.com/client/v4/accounts/{account_identifier}/ai/run/{model_name}"
        self.headers: dict = {
            "Authorization": f"Bearer {Cloudflare_API_Key}",
        }
        self.const = CloudflareAIConst()

        if not self.api_key:
            raise CloudflareAIError("Cloudflare API key is required.")
        
        if not self.account_identifier:
            raise CloudflareAIError("Cloudflare account identifier is required.")

    async def _fetch(
        self,
        method: str,
        url: str,
        data: dict,
        headers: dict = None,
        stream: str = False,
    ) -> Union[dict, CloudflareAIError]:
        """
        httpx request wrapper.

        :param method: HTTP method.
        :param url: URL.
        :param data: Request data.
        :param headers: Request headers.
        :param stream: Stream response.

        :return: dict or CloudflareAIError
        """

        if headers is not None:
            self.headers.update(headers)
        async with httpx.AsyncClient() as client:
            if headers["Content-Type"] == "application/json":
                req = client.build_request(
                    method, url, headers=self.headers, json=data, timeout=60
                )
            else:
                req = client.build_request(
                    method, url, headers=self.headers, data=data, timeout=60
                )
            response = await client.send(req, stream=stream)
            if response.status_code == 200:
                if not stream:
                    return response 
                else:
                    async for line in response.aiter_lines():
                        print(line)
            else:
                raise CloudflareAIError(
                    f"Error {response.status_code}: {response.reason_phrase}"
                )

    async def ImageClassification(
        self, image_path, model_name: str
    ) -> Union[dict, CloudflareAIError]:
        """
        Image classification models take an image input and assigns it labels or classes.

        :param image_path: Path to the image file.
        :param model_name: Model name.

        :return: dict
        """
        if model_name not in self.const.AiImageClassificationModels:
            raise CloudflareAIError(f"Model name {model_name} is not supported.")

        url = self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )

        check_image_path = os.path.isfile(image_path)
        if not check_image_path:
            raise CloudflareAIError(f"Image path {image_path} is not a file.")

        async with aiofiles.open(image_path, "rb") as img_file:
            image_data = await img_file.read()
            headers = {
                "Content-Type": "image/jpeg",
            }
            response = await self._fetch("POST", url, data=image_data, headers=headers)
            return response.json()

    async def TextGeneration(
        self,
        prompt: str,
        system_prompt: str,
        model_name: str,
        stream: bool = False,
        max_tokens: int = 256,
    ) -> dict:
        """
        Family of generative text models, such as large language models (LLM), that can be adapted for a variety of natural language tasks.

        :param prompt: Prompt to generate text from.
        :param system_prompt: System prompt to generate text from.

        :return: dict
        """
        if model_name not in self.const.AiTextGenerationModels:
            raise CloudflareAIError(f"Model name {model_name} is not supported.")

        if len(prompt) > 4096:
            raise CloudflareAIError("Prompt length cannot exceed 4096 characters.")

        url = self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )
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

        if stream:
            response = await self._fetch(
                "POST", url, headers=headers, data=payload, stream=stream
            )
            return
        else:
            response = await self._fetch("POST", url, headers=headers, data=payload)
            return response.json()

    async def SpeechRecognition(
        self, audio_path: str, model_name: str
    ) -> Union[dict, CloudflareAIError]:
        """
        Automatic speech recognition (ASR) models convert a speech signal, typically an audio input, to text.

        :param audio_path: Path to the audio file.
        :param model_name: Model name.

        :return: dict
        """
        if model_name not in self.const.AiSpeechRecognitionModels:
            raise CloudflareAIError(f"Model name {model_name} is not supported.")

        if not os.path.isfile(audio_path):
            raise CloudflareAIError(f"Audio path {audio_path} is not a file.")

        url = self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )

        async with aiofiles.open(audio_path, "rb") as audio_file:
            audio_data = await audio_file.read()
            headers = {
                "Content-Type": "audio/wav",
            }
            response = await self._fetch("POST", url, data=audio_data, headers=headers)
            return response.json()

    async def Translation(
        self, text: str, source_lang: str, target_lang: str, model_name: str
    ) -> Union[dict, CloudflareAIError]:
        """
        Translation models convert a sequence of text from one language to another.

        :param text: Text to translate.
        :param source_lang: Source language.
        :param target_lang: Target language.

        :return: dict or CloudflareAIError
        """
        if model_name not in self.const.AiTranslationModels:
            raise CloudflareAIError(f"Model name {model_name} is not supported.")

        if (
            source_lang not in self.const.TranslationLanguages
            or target_lang not in self.const.TranslationLanguages
        ):
            raise CloudflareAIError(
                f"Language {source_lang} or {target_lang} is not supported."
            )

        url = self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )
        payload = {"text": text, "source_lang": source_lang, "target_lang": target_lang}

        headers = {
            "Content-Type": "application/json",
        }

        response = await self._fetch("POST", url, headers=headers, data=payload)
        return response.json()

    async def TextToImage(
        self, prompt: str, model_name: str, steps: int = 20
    ) -> Union[dict, CloudflareAIError]:
        """
        Text to image models generate an image from a text input.

        :param prompt: Text to generate image from.
        :param model_name: Model name.

        :return: dict or CloudflareAIError
        """
        if model_name not in self.const.AiTextToImageModels:
            raise CloudflareAIError(f"Model name {model_name} is not supported.")

        url = self.base_url.format(
            account_identifier=self.account_identifier, model_name=model_name
        )
        payload = {"prompt": prompt, "steps": steps}

        headers = {
            "Content-Type": "application/json",
        }

        response = await self._fetch("POST", url, headers=headers, data=payload)
        image = Image.open(BytesIO(response.content))
        return image.save(f"{str(prompt).replace(' ', '-')}.png")
