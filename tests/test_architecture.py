import asyncio

import httpx

from chile_public_market_sdk import ClientConfig
from chile_public_market_sdk.async_client import AsyncChilePublicMarketClient
from chile_public_market_sdk.clients import (
    AsyncChilePublicMarketClient as CanonicalAsyncClient,
)
from chile_public_market_sdk.clients import (
    SyncChilePublicMarketClient as CanonicalSyncClient,
)
from chile_public_market_sdk.sync_client import SyncChilePublicMarketClient
from chile_public_market_sdk.transport import (
    AsyncTransport,
    AsyncTransportProtocol,
    SyncTransport,
    SyncTransportProtocol,
)


def test_legacy_client_modules_delegate_to_canonical_packages() -> None:
    assert SyncChilePublicMarketClient is CanonicalSyncClient
    assert AsyncChilePublicMarketClient is CanonicalAsyncClient


def test_transport_implementations_satisfy_sync_and_async_protocols() -> None:
    config = ClientConfig(ticket="secret")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    sync_client = httpx.Client(transport=httpx.MockTransport(handler))
    async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    assert isinstance(SyncTransport(sync_client, config), SyncTransportProtocol)
    assert isinstance(AsyncTransport(async_client, config), AsyncTransportProtocol)

    sync_client.close()
    asyncio.run(async_client.aclose())
