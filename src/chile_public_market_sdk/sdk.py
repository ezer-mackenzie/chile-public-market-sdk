"""High-level SDK facades."""

from .async_client import AsyncMercadoPublicoClient
from .client import MercadoPublicoClient


class MercadoPublico(MercadoPublicoClient):
    """Primary synchronous facade."""


class AsyncMercadoPublico(AsyncMercadoPublicoClient):
    """Primary asynchronous facade."""
