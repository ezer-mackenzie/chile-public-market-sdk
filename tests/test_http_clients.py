from typing import Any

import httpx
import pytest

from chile_public_market_sdk import (
    AsyncChilePublicMarketClient,
    ClientConfig,
    NetworkError,
    RequestTimeoutError,
    SyncChilePublicMarketClient,
    TransportError,
)
from chile_public_market_sdk.core.constants.config import DEFAULT_TICKET_ENV


def test_config_repr_redacts_ticket_and_accepts_httpx_timeout() -> None:
    timeout = httpx.Timeout(connect=1, read=2, write=3, pool=4)
    config = ClientConfig(ticket="never-print-this", timeout=timeout)

    assert "never-print-this" not in repr(config)
    assert config.timeout is timeout


def test_explicit_ticket_takes_precedence_over_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(DEFAULT_TICKET_ENV, "environment")

    assert ClientConfig(ticket=" explicit ").resolved_ticket() == "explicit"


def test_sync_timeout_has_a_deterministic_public_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("read failed", request=request)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestTimeoutError, match="timed out"):
        client.get_tenders()
    http_client.close()


def test_sync_network_failure_has_a_deterministic_public_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(NetworkError, match="communicate"):
        client.get_tenders()
    http_client.close()


def test_sync_http_failure_has_a_deterministic_public_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.HTTPError("HTTP failed")

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(TransportError, match="communicate"):
        client.get_tenders()
    http_client.close()


def test_sync_client_context_manager_closes_owned_httpx_client() -> None:
    client = SyncChilePublicMarketClient(ticket="secret")

    with client as managed_client:
        assert managed_client is client
        assert not client._http_client.is_closed
    assert client._http_client.is_closed


@pytest.mark.asyncio
async def test_async_client_uses_httpx_directly(tender_payload: dict[str, Any]) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=tender_payload)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    assert (await client.get_tenders()).count == 1
    await http_client.aclose()


@pytest.mark.asyncio
async def test_async_client_context_manager_closes_owned_httpx_client() -> None:
    client = AsyncChilePublicMarketClient(ticket="secret")

    async with client as managed_client:
        assert managed_client is client
        assert not client._http_client.is_closed
    assert client._http_client.is_closed


@pytest.mark.asyncio
async def test_async_timeout_has_the_same_public_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("read failed", request=request)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestTimeoutError, match="timed out"):
        await client.get_tenders()
    await http_client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("upstream_error", "public_error"),
    [
        (httpx.ConnectError("connection failed"), NetworkError),
        (httpx.HTTPError("HTTP failed"), TransportError),
    ],
)
async def test_async_transport_failures_are_normalized(
    upstream_error: httpx.HTTPError,
    public_error: type[Exception],
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise upstream_error

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(public_error, match="communicate"):
        await client.get_tenders()
    await http_client.aclose()


@pytest.mark.asyncio
async def test_clients_do_not_close_injected_httpx_clients() -> None:
    sync_http_client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200))
    )
    async_http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200))
    )

    SyncChilePublicMarketClient(ticket="secret", http_client=sync_http_client).close()
    await AsyncChilePublicMarketClient(ticket="secret", http_client=async_http_client).aclose()

    assert not sync_http_client.is_closed
    assert not async_http_client.is_closed
    sync_http_client.close()
    await async_http_client.aclose()
