from __future__ import annotations

from typing import Any

import httpx
import pytest

from chile_public_market_sdk import AsyncMercadoPublicoClient


@pytest.mark.asyncio
async def test_async_get_tenders(tender_payload: dict[str, Any]) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["ticket"] == "secret"
        return httpx.Response(200, json=tender_payload)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    sdk = AsyncMercadoPublicoClient(ticket="secret", http_client=http_client)
    result = await sdk.get_tenders(code="1509-5-L114")
    assert result.count == 1
    await http_client.aclose()
