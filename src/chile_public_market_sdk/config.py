"""Configuration shared by synchronous and asynchronous clients."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field

import httpx

from .api import V1_BASE_URL, V2_BASE_URL
from .errors import ConfigurationError

DEFAULT_TICKET_ENV = "CHILE_PUBLIC_MARKET_TICKET"


@dataclass(frozen=True, slots=True)
class TimeoutConfig:
    """Timeout limits, in seconds, for each network operation."""

    connect: float = 30.0
    read: float = 30.0
    write: float = 30.0
    pool: float = 30.0

    def to_httpx(self) -> httpx.Timeout:
        """Build the equivalent HTTPX timeout configuration."""

        return httpx.Timeout(
            connect=self.connect,
            read=self.read,
            write=self.write,
            pool=self.pool,
        )


@dataclass(frozen=True, slots=True)
class RetryConfig:
    """Opt-in retry policy for transient failures."""

    max_attempts: int = 1
    backoff_factor: float = 0.5
    max_delay: float = 30.0
    retry_statuses: frozenset[int] = frozenset({429, 500, 502, 503, 504})

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ConfigurationError("max_attempts must be greater than or equal to 1.")
        if self.backoff_factor < 0 or self.max_delay < 0:
            raise ConfigurationError("Retry delays cannot be negative.")


@dataclass(frozen=True, slots=True)
class RequestEvent:
    """Sanitized metadata emitted before an HTTP attempt."""

    method: str
    url: str
    attempt: int


@dataclass(frozen=True, slots=True)
class ResponseEvent:
    """Sanitized metadata emitted after an HTTP attempt."""

    method: str
    url: str
    attempt: int
    status_code: int
    elapsed_seconds: float


type RequestHook = Callable[[RequestEvent], None]
type ResponseHook = Callable[[ResponseEvent], None]
type TimeoutValue = float | TimeoutConfig


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Immutable SDK configuration.

    An explicit ticket takes precedence over the configured environment variable.
    """

    ticket: str | None = field(default=None, repr=False)
    ticket_env: str = DEFAULT_TICKET_ENV
    base_url_v1: str = V1_BASE_URL
    base_url_v2: str = V2_BASE_URL
    timeout: TimeoutValue = 30.0
    retry: RetryConfig = field(default_factory=RetryConfig)
    request_hooks: tuple[RequestHook, ...] = ()
    response_hooks: tuple[ResponseHook, ...] = ()

    def resolved_ticket(self) -> str:
        value = self.ticket or os.getenv(self.ticket_env)
        if not value or not value.strip():
            raise ConfigurationError(
                f"Provide ticket=... or define the {self.ticket_env} environment variable."
            )
        return value.strip()

    def httpx_timeout(self) -> float | httpx.Timeout:
        """Return the timeout value accepted by HTTPX."""

        if isinstance(self.timeout, TimeoutConfig):
            return self.timeout.to_httpx()
        return self.timeout
