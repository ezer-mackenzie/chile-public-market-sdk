from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from chile_public_market_sdk import AsyncChilePublicMarketClient
from chile_public_market_sdk.errors import APIError, RequestValidationError

FIXTURES = Path(__file__).parent / "fixtures" / "contracts"


@pytest.mark.asyncio
async def test_async_get_tenders(tender_payload: dict[str, Any]) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["ticket"] == "secret"
        return httpx.Response(200, json=tender_payload)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    sdk = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)
    result = await sdk.get_tenders(code="1509-5-L114")
    assert result.count == 1
    await http_client.aclose()


@pytest.mark.asyncio
async def test_async_v1_resource_routes() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("ordenesdecompra.json"):
            return httpx.Response(200, json={"Cantidad": 0, "Listado": []})
        if request.url.path.endswith("BuscarProveedor"):
            return httpx.Response(200, json={"CodigoEmpresa": 10, "NombreEmpresa": "Supplier"})
        return httpx.Response(200, json=[{"CodigoEmpresa": 20, "NombreEmpresa": "Buyer"}])

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    assert (await client.get_purchase_orders()).count == 0
    assert (await client.find_supplier("76.000.000-0")).companies[0].company_code == 10
    assert (await client.get_buyers()).companies[0].company_code == 20
    await http_client.aclose()


@pytest.mark.asyncio
async def test_async_agile_purchase_routes(agile_page_payload: dict[str, Any]) -> None:
    detail_payload = json.loads((FIXTURES / "agile-detail.json").read_text())

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["ticket"] == "secret"
        if request.url.path == "/v2/compra-agil":
            return httpx.Response(200, json=agile_page_payload)
        return httpx.Response(200, json=detail_payload)

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    assert (await client.get_agile_purchases()).pagination.total_results == 1
    assert (await client.get_agile_purchase("1057539-228-COT26")).code
    await http_client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("method_name", ["get_tenders", "get_purchase_orders"])
async def test_async_v1_code_rejects_additional_filters(method_name: str) -> None:
    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(500))
    )
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestValidationError, match="code cannot be combined"):
        await getattr(client, method_name)(code="code", date="01012026")

    await http_client.aclose()


@pytest.mark.asyncio
async def test_async_rejects_empty_resource_identifiers() -> None:
    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(500))
    )
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestValidationError, match="tax_id cannot be empty"):
        await client.find_supplier(" ")
    with pytest.raises(RequestValidationError, match="code cannot be empty"):
        await client.get_agile_purchase(" ")

    await http_client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"last_change_ttl_ms": 1, "changed_from": "2026-01-01"}, "last_change_ttl_ms"),
        ({"external_id": "code", "query": "text"}, "mutually exclusive"),
        ({"page_size": 9}, "page_size"),
        ({"page_number": 0}, "page_number"),
        ({"regions": [17]}, "region"),
    ],
)
async def test_async_agile_purchase_rejects_invalid_filters(
    kwargs: dict[str, Any],
    message: str,
) -> None:
    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(500))
    )
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(RequestValidationError, match=message):
        await client.get_agile_purchases(**kwargs)

    await http_client.aclose()


@pytest.mark.asyncio
async def test_async_agile_purchase_requires_payload() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"success": "OK", "payload": None})

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncChilePublicMarketClient(ticket="secret", http_client=http_client)

    with pytest.raises(APIError, match="without a payload"):
        await client.get_agile_purchases()
    with pytest.raises(APIError, match="without a payload"):
        await client.get_agile_purchase("1057539-228-COT26")

    await http_client.aclose()
