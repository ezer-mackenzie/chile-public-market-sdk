"""Python SDK for Chile's Mercado Público APIs."""

from importlib.metadata import PackageNotFoundError, version

from .clients import AsyncChilePublicMarketClient, SyncChilePublicMarketClient
from .config import ClientConfig
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
    "RequestTimeoutError",
    "RequestValidationError",
    "ResponseValidationError",
    "SyncChilePublicMarketClient",
    "SyncChilePublicMarketSDK",
    "TransportError",
]

try:
    __version__ = version("mercado-publico-chile-sdk")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0.0.0+unknown"
