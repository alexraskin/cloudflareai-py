class CloudflareException(Exception):
    """Base exception class for CloudflareAI"""

    ...


class CloudflareAPIException(CloudflareException):
    """Exception raised when the Cloudflare API returns an error"""

    ...
