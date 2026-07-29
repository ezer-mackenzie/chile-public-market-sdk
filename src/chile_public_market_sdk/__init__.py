"""Python SDK for Chile's Mercado Público APIs."""

from importlib.metadata import PackageNotFoundError, version

from .async_client import AsyncChilePublicMarketClient
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
