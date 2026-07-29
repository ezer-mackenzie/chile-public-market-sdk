import pytest

from chile_public_market_sdk import (
    AsyncChilePublicMarketClient,
    AsyncChilePublicMarketSDK,
    SyncChilePublicMarketClient,
    SyncChilePublicMarketSDK,
)


def test_sync_sdk_constructs_and_manages_its_client() -> None:
    sdk = SyncChilePublicMarketSDK(ticket="secret")

    assert type(sdk.client) is SyncChilePublicMarketClient
    with sdk as client:
        assert client is sdk.client
        assert not client._http_client.is_closed
    assert sdk.client._http_client.is_closed


@pytest.mark.asyncio
async def test_async_sdk_constructs_and_manages_its_client() -> None:
    sdk = AsyncChilePublicMarketSDK(ticket="secret")

    assert type(sdk.client) is AsyncChilePublicMarketClient
    async with sdk as client:
        assert client is sdk.client
        assert not client._http_client.is_closed
    assert sdk.client._http_client.is_closed


def test_sdk_classes_use_composition_instead_of_client_inheritance() -> None:
    assert not issubclass(SyncChilePublicMarketSDK, SyncChilePublicMarketClient)
    assert not issubclass(AsyncChilePublicMarketSDK, AsyncChilePublicMarketClient)
