import httpx

from chile_public_market_sdk.async_client import AsyncChilePublicMarketClient
from chile_public_market_sdk.clients import (
    AsyncChilePublicMarketClient as CanonicalAsyncClient,
)
from chile_public_market_sdk.clients import (
    SyncChilePublicMarketClient as CanonicalSyncClient,
)
from chile_public_market_sdk.sync_client import SyncChilePublicMarketClient


def test_legacy_client_modules_delegate_to_canonical_packages() -> None:
    assert SyncChilePublicMarketClient is CanonicalSyncClient
    assert AsyncChilePublicMarketClient is CanonicalAsyncClient


def test_clients_use_httpx_directly() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    sync_http = httpx.Client(transport=httpx.MockTransport(handler))
    async_http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    sync_client = SyncChilePublicMarketClient(ticket="secret", http_client=sync_http)
    async_client = AsyncChilePublicMarketClient(ticket="secret", http_client=async_http)

    assert sync_client._http_client is sync_http
    assert async_client._http_client is async_http

    sync_http.close()
