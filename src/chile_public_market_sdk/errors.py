"""Public SDK exceptions."""

from __future__ import annotations

from typing import Any


class ChilePublicMarketError(Exception):
    """Base exception for every SDK error."""


class ConfigurationError(ChilePublicMarketError):
    """The client configuration is invalid."""


class RequestValidationError(ChilePublicMarketError, ValueError):
    """The supplied request filters are invalid or incompatible."""


class TransportError(ChilePublicMarketError):
    """The client could not communicate with Mercado Público."""


class RequestTimeoutError(TransportError):
    """A Mercado Público request exceeded a configured timeout."""


class NetworkError(TransportError):
    """A connection or network protocol failure interrupted the request."""


class ResponseValidationError(ChilePublicMarketError):
    """The response does not match the expected contract."""


class APIError(ChilePublicMarketError):
    """Mercado Público returned an error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: Any = None,
        retry_after: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details
        self.retry_after = retry_after


class AuthenticationError(APIError):
    """The ticket is missing, invalid, or inactive."""


class NotFoundError(APIError):
    """The requested resource does not exist."""


class RateLimitError(APIError):
    """The quota associated with the ticket has been exhausted."""
