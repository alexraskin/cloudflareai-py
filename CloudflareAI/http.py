from __future__ import annotations

from typing import Dict, Optional, Union

import httpx

from .exceptions import CloudflareAPIException


class Http:
    """
    Httpx Wrapper for Cloudflare AI API.
    """

    def __init__(
        self, api_key: str, retries: Union[int, None], timeout: Union[int, None]
    ) -> None:
        self.api_key: str = api_key
        self.retries: Union[int, None] = retries
        self.timeout: Union[int, None] = timeout
        self._transport = httpx.AsyncHTTPTransport(retries=self.retries)  # type: ignore

    async def process_stream_response(self, response: httpx.Response) -> bytes:
        """
        Process the stream response.

        :param response: httpx response.

        :return: bytes
        """
        data = b""
        async for chunk in response.aiter_bytes():
            data += chunk
        return data.decode("utf-8")  # type: ignore

    async def fetch(
        self,
        method: str,
        url: str,
        data: Union[dict, bytes],
        headers: Optional[Dict[str, str]] = None,
        stream: Optional[bool] = False,
    ) -> httpx.Response:
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
                    method, url, headers=self.headers, data=data, timeout=self.timeout  # type: ignore
                )
            response = await client.send(req, stream=stream or False)
            return response
