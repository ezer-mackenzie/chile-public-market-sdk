"""High-level SDK facades."""

from .async_client import AsyncChilePublicMarketClient
from .sync_client import SyncChilePublicMarketClient


class SyncChilePublicMarketSDK(SyncChilePublicMarketClient):
    """Primary synchronous facade."""


class AsyncChilePublicMarketSDK(AsyncChilePublicMarketClient):
    """Primary asynchronous facade."""
