"""Asynchronous high-level SDK facade."""

from ..clients.async_ import AsyncChilePublicMarketClient


class AsyncChilePublicMarketSDK(AsyncChilePublicMarketClient):
    """High-level asynchronous facade for Chile's public procurement APIs."""
