from typing import Any

import httpx
import pytest

from chile_public_market_sdk import (
    AsyncChilePublicMarketClient,
    ClientConfig,
    RateLimitError,
    RequestTimeoutError,
    SyncChilePublicMarketClient,
)


def test_config_repr_redacts_ticket_and_accepts_httpx_timeout() -> None:
    timeout = httpx.Timeout(connect=1, read=2, write=3, pool=4)
    config = ClientConfig(ticket="never-print-this", timeout=timeout)

    assert "never-print-this" not in repr(config)
    assert config.timeout is timeout


def test_sync_client_uses_httpx_and_normalizes_api_errors() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"mensaje": "Daily quota exhausted"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RateLimitError):
        client.get_tenders()
    http_client.close()


def test_sync_timeout_has_a_deterministic_public_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("read failed", request=request)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestTimeoutError, match="timed out"):
        client.get_tenders()
    http_client.close()


@pytest.mark.asyncio
async def test_async_client_uses_httpx_directly(tender_payload: dict[str, Any]) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=tender_payload)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    assert (await client.get_tenders()).count == 1
    await http_client.aclose()
