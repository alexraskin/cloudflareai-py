from __future__ import annotations

from typing import Dict, Optional, Union

import httpx

from .exceptions import CloudflareException


class Http:
    """
    Http Client for Cloudflare AI API.
    """

    def __init__(self, api_key: str, retries: int, timeout: int) -> None:
        self.api_key: str = api_key
        self.retries: int = retries
        self.timeout: int = timeout
        self._transport = httpx.AsyncHTTPTransport(retries=self.retries)

    async def process_stream_response(self, response: httpx.Response) -> bytes:
        """
        Process the stream response.

        :param response: httpx response.

        :return: bytes
        """
        data = b""
        async for chunk in response.aiter_bytes():
            data += chunk
        return data.decode("utf-8")

    async def fetch(
        self,
        method: str,
        url: str,
        data: dict,
        headers: Optional[Dict[str, str]] = None,
        stream: Optional[bool] = False,
    ) -> Union[httpx.Response, bytes, CloudflareException]:
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
                    return await self.process_stream_response(response)
                else:
                    return response
            else:
                raise CloudflareException(
                    f"Error {response.status_code}: {response.reason_phrase}"
                )
