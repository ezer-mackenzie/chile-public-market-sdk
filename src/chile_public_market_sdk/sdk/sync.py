"""Synchronous high-level SDK facade."""

import httpx

from ..clients.sync import SyncChilePublicMarketClient
from ..config import ClientConfig
from ..core.types import TimeoutValue


class SyncChilePublicMarketSDK:
    """Construct and manage a synchronous Mercado Público client."""

    def __init__(
        self,
        ticket: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.Client | None = None,
        timeout: TimeoutValue = 30.0,
    ) -> None:
        self.client = SyncChilePublicMarketClient(
            ticket=ticket,
            config=config,
            http_client=http_client,
            timeout=timeout,
        )

    def __enter__(self) -> SyncChilePublicMarketClient:
        return self.client

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """Close resources owned by the underlying client."""

        self.client.close()
