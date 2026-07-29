"""Python SDK for Chile's Mercado Público APIs."""

from importlib.metadata import PackageNotFoundError, version

from .async_client import AsyncChilePublicMarketClient
from .config import ClientConfig, RequestEvent, ResponseEvent, RetryConfig, TimeoutConfig
from .errors import (
    APIError,
    AuthenticationError,
    ChilePublicMarketError,
    ConfigurationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    RequestTimeoutError,
    RequestValidationError,
    ResponseValidationError,
    TransportError,
)
from .sdk import AsyncChilePublicMarketSDK, SyncChilePublicMarketSDK
from .sync_client import SyncChilePublicMarketClient

__all__ = [
    "APIError",
    "AsyncChilePublicMarketClient",
    "AsyncChilePublicMarketSDK",
    "AuthenticationError",
    "ChilePublicMarketError",
    "ClientConfig",
    "ConfigurationError",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    "RequestEvent",
    "RequestTimeoutError",
    "RequestValidationError",
    "ResponseEvent",
    "ResponseValidationError",
    "RetryConfig",
    "SyncChilePublicMarketClient",
    "SyncChilePublicMarketSDK",
    "TimeoutConfig",
    "TransportError",
]

try:
    __version__ = version("mercado-publico-chile-sdk")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0.0.0+unknown"
