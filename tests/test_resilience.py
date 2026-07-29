from __future__ import annotations

from typing import Any

import httpx
import pytest

from chile_public_market_sdk import (
    AsyncChilePublicMarketClient,
    ClientConfig,
    RateLimitError,
    RequestEvent,
    RequestTimeoutError,
    ResponseEvent,
    RetryConfig,
    SyncChilePublicMarketClient,
    TimeoutConfig,
)


def test_config_repr_redacts_ticket_and_builds_granular_timeout() -> None:
    config = ClientConfig(
        ticket="never-print-this",
        timeout=TimeoutConfig(connect=1, read=2, write=3, pool=4),
    )

    assert "never-print-this" not in repr(config)
    timeout = config.httpx_timeout()
    assert isinstance(timeout, httpx.Timeout)
    assert timeout.connect == 1
    assert timeout.read == 2
    assert timeout.write == 3
    assert timeout.pool == 4


def test_sync_retries_transient_status_and_emits_safe_events(
    tender_payload: dict[str, Any],
) -> None:
    attempts = 0
    requests: list[RequestEvent] = []
    responses: list[ResponseEvent] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(503, text="<html>temporarily unavailable</html>")
        return httpx.Response(200, json=tender_payload)

    config = ClientConfig(
        ticket="sensitive-ticket",
        retry=RetryConfig(max_attempts=2, backoff_factor=0),
        request_hooks=(requests.append,),
        response_hooks=(responses.append,),
    )
    http_client = httpx.Client(transport=httpx.MockTransport(handler))

    with SyncChilePublicMarketClient(config=config, http_client=http_client) as client:
        assert client.get_tenders().count == 1

    assert attempts == 2
    assert [event.attempt for event in requests] == [1, 2]
    assert [event.status_code for event in responses] == [503, 200]
    assert all("sensitive-ticket" not in event.url for event in requests + responses)
    assert all("?" not in event.url for event in requests + responses)


def test_429_without_retry_after_is_not_retried() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(429, json={"mensaje": "Daily quota exhausted"})

    config = ClientConfig(
        ticket="secret",
        retry=RetryConfig(max_attempts=3, backoff_factor=0),
    )
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(config=config, http_client=http_client)

    with pytest.raises(RateLimitError):
        client.get_tenders()
    assert attempts == 1
    http_client.close()


def test_timeout_has_a_deterministic_public_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("read failed", request=request)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = SyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestTimeoutError, match="timed out"):
        client.get_tenders()
    http_client.close()


@pytest.mark.asyncio
async def test_async_retry_matches_sync_behavior(tender_payload: dict[str, Any]) -> None:
    attempts = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise httpx.ConnectError("connection failed", request=request)
        return httpx.Response(200, json=tender_payload)

    config = ClientConfig(
        ticket="secret",
        retry=RetryConfig(max_attempts=2, backoff_factor=0),
    )
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(config=config, http_client=http_client)

    assert (await client.get_tenders()).count == 1
    assert attempts == 2
    await http_client.aclose()
