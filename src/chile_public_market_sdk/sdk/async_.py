"""Asynchronous high-level SDK facade."""

import httpx

from ..clients.async_ import AsyncChilePublicMarketClient
from ..config import ClientConfig
from ..core.types import TimeoutValue


class AsyncChilePublicMarketSDK:
    """Construct and manage an asynchronous Mercado Público client."""

    def __init__(
        self,
        ticket: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.AsyncClient | None = None,
        timeout: TimeoutValue = 30.0,
    ) -> None:
        self.client = AsyncChilePublicMarketClient(
            ticket=ticket,
            config=config,
            http_client=http_client,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncChilePublicMarketClient:
        return self.client

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close resources owned by the underlying client."""

        await self.client.aclose()
