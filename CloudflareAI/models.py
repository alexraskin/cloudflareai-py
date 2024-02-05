import httpx

from .types import Response


class ApiResponse:
    """
    A class to represent the response from the Cloudflare AI API.
    """

    def __init__(self, data: Response, response: httpx.Response) -> None:
        self.data: Response = data
        self.response = response

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def json(self) -> dict:
        return self.response.json()

    @property
    def headers(self) -> dict:
        return self.response.headers

    @property
    def url(self) -> str:
        return self.response.url

    @property
    def text(self) -> str:
        return self.data.get("result", {}).get("response", "")

    @property
    def success(self) -> bool:
        return self.data.get("success", False)

    @property
    def errors(self) -> list:
        return self.data.get("errors", [])

    @property
    def messages(self) -> list:
        return self.data.get("messages", [])


class ImageResponse:
    """
    A class to represent the response from the Cloudflare AI Image API.
    """

    def __init__(self, data: httpx.Response):
        self.data = data

    @property
    def status_code(self) -> int:
        return self.data.status_code

    @property
    def headers(self) -> dict:
        return self.data.headers

    @property
    def image_format(self) -> str:
        return self.data.headers.get("Content-Type", "").split("/")[-1]

    @property
    def image(self) -> bytes:
        return self.data.content
