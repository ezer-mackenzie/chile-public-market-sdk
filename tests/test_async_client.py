from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from chile_public_market_sdk import AsyncChilePublicMarketClient

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
