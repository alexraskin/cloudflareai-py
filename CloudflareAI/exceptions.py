from typing import Literal


class CloudflareException(Exception):
    """Base exception class for CloudflareAI"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BadRequestError(CloudflareException):
    status_code: Literal[400] = 400


class AuthenticationError(CloudflareException):
    status_code: Literal[401] = 401


class PermissionDeniedError(CloudflareException):
    status_code: Literal[403] = 403


class NotFoundError(CloudflareException):
    status_code: Literal[404] = 404


class RateLimitError(CloudflareException):
    status_code: Literal[429] = 429


class InternalServerError(CloudflareException):
    pass
