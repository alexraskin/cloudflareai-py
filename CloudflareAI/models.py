import httpx


class CloudflareAPIResponse:
    """
    A class to represent the response from the Cloudflare AI API.
    """

    def __init__(self, response: httpx.Response) -> None:
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
        return self.response.json().get("result", {}).get("response", "")

    @property
    def success(self) -> bool:
        return self.response.json().get("success", False)

    @property
    def errors(self) -> list:
        return self.response.json().get("errors", [])

    @property
    def messages(self) -> list:
        return self.response.json().get("messages", [])


class CloudflareImageResponse:
    """
    A class to represent the response from the Cloudflare AI Image API.
    """

    def __init__(self, response: httpx.Response):
        self.response = response

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def headers(self) -> dict:
        return self.response.headers

    @property
    def image_format(self) -> str:
        return self.response.headers.get("Content-Type")

    @property
    def image(self) -> bytes:
        return self.response.content


class CloudflareTranslationResponse:
    """
    A class to represent the response from the Cloudflare AI Translation API.
    """

    def __init__(self, response: httpx.Response) -> None:
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
        return self.response.json().get("result", "").get("translated_text", "")

    @property
    def success(self) -> bool:
        return self.response.json().get("success", False)

    @property
    def errors(self) -> list:
        return self.response.json().get("errors", [])

    @property
    def messages(self) -> list:
        return self.response.json().get("messages", [])


class CloudflareSpeechRecognitionResponse:
    """
    A class to represent the response from the Cloudflare AI Speech Recognition API.
    """

    def __init__(self, response: httpx.Response) -> None:
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
        return self.response.json().get("result", "").get("text", "")

    @property
    def word_count(self) -> int:
        return self.response.json().get("result", "").get("word_count", 0)

    @property
    def words(self) -> list:
        return self.response.json().get("result", "").get("words", [])

    @property
    def success(self) -> bool:
        return self.response.json().get("success", False)

    @property
    def errors(self) -> list:
        return self.response.json().get("errors", [])

    @property
    def messages(self) -> list:
        return self.response.json().get("messages", [])


class CloudflareImageClassificationResponse:
    """
    A class to represent the response from the Cloudflare AI Image Classification API.
    """

    def __init__(self, response: httpx.Response) -> None:
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
    def success(self) -> bool:
        return self.response.json().get("success", False)

    @property
    def errors(self) -> list:
        return self.response.json().get("errors", [])

    @property
    def messages(self) -> list:
        return self.response.json().get("messages", [])

    @property
    def labels(self) -> list:
        return [item["label"] for item in self.response.json().get("result", {})]

    @property
    def scores(self) -> list:
        return [item["score"] for item in self.response.json().get("result", {})]
