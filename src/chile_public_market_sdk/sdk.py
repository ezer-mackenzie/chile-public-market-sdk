"""Fachadas de alto nivel del SDK."""

from .async_client import AsyncMercadoPublicoClient
from .client import MercadoPublicoClient


class MercadoPublico(MercadoPublicoClient):
    """Fachada síncrona principal."""


class AsyncMercadoPublico(AsyncMercadoPublicoClient):
    """Fachada asíncrona principal."""
