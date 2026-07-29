"""Credential-free transport event construction."""

import httpx

from ..config import RequestEvent, ResponseEvent


class TransportEventFactory:
    """Create credential-free transport observability events."""

    @staticmethod
    def safe_url(url: str) -> str:
        parsed = httpx.URL(url)
        return str(parsed.copy_with(query=None, username=None, password=None))

    @classmethod
    def request(cls, url: str, attempt: int) -> RequestEvent:
        return RequestEvent(method="GET", url=cls.safe_url(url), attempt=attempt)

    @classmethod
    def response(
        cls,
        url: str,
        attempt: int,
        response: httpx.Response,
        elapsed_seconds: float,
    ) -> ResponseEvent:
        return ResponseEvent(
            method="GET",
            url=cls.safe_url(url),
            attempt=attempt,
            status_code=response.status_code,
            elapsed_seconds=elapsed_seconds,
        )
