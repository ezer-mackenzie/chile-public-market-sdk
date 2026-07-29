"""HTTPX transport adapters and structural contracts."""

from .async_ import AsyncTransport
from .protocols import AsyncTransportProtocol, SyncTransportProtocol
from .sync import SyncTransport

__all__ = [
    "AsyncTransport",
    "AsyncTransportProtocol",
    "SyncTransport",
    "SyncTransportProtocol",
]
