"""Synchronous high-level SDK facade."""

from ..clients.sync import SyncChilePublicMarketClient


class SyncChilePublicMarketSDK(SyncChilePublicMarketClient):
    """High-level synchronous facade for Chile's public procurement APIs."""
