from typing import Dict, Optional, Union

import httpx

from . import exceptions


class Http:
    """
    Httpx Wrapper for Cloudflare AI API.
    """

    def __init__(self, api_key: str, retries: int, timeout: int) -> None:
        """
        Initialize the Http class.

        Parameters:
        ----------
        :param api_key: Cloudflare API Key.
        :param retries: Number of retries.
        :param timeout: Timeout for the request.

        :return: None
        """
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
        return data.decode("utf-8", errors="ignore")

    async def fetch(
        self,
        method: str,
        url: str,
        data: Union[dict, bytes],
        headers: Optional[dict] = None,
        stream: Optional[bool] = False,
    ) -> Union[httpx.Response, Exception]:
        """
        Fetch the response from the Cloudflare AI API.

        Parameters:
        ----------
        :param method: HTTP Method.
        :param url: URL for the request.
        :param data: Data for the request.
        :param headers: Headers for the request.
        :param stream: bool: Stream the response.

        Returns:
        -------
        :return: httpx.Response
        """
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
        }

        if headers is not None:
            self.headers.update(headers)
        async with httpx.AsyncClient(transport=self._transport) as client:
            if headers.get("Content-Type") == "application/json":
                req = client.build_request(
                    method, url, headers=self.headers, json=data, timeout=self.timeout
                )
            else:
                req = client.build_request(
                    method, url, headers=self.headers, data=data, timeout=self.timeout
                )
            response = await client.send(req, stream=stream)

            if response.status_code == 400:
                raise exceptions.BadRequestError("Bad Request")

            if response.status_code == 401:
                raise exceptions.AuthenticationError("Authentication Error")

            if response.status_code == 403:
                raise exceptions.PermissionDeniedError("Permission Denied")

            if response.status_code == 404:
                raise exceptions.NotFoundError("Not Found")

            if response.status_code == 429:
                raise exceptions.RateLimitError("Rate Limit Error")

            if response.status_code >= 500:
                raise exceptions.InternalServerError("Internal Server Error")

            return response
