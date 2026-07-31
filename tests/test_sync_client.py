from __future__ import annotations

from datetime import date
from typing import Any

import httpx
import pytest

from chile_public_market_sdk import SyncChilePublicMarketClient
from chile_public_market_sdk.core.constants.config import DEFAULT_TICKET_ENV
from chile_public_market_sdk.core.enums import AgilePurchaseStatus, TenderStatus
from chile_public_market_sdk.errors import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    RateLimitError,
    RequestValidationError,
)


def test_ticket_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(DEFAULT_TICKET_ENV, raising=False)
    with pytest.raises(ConfigurationError):
        SyncChilePublicMarketClient()


def test_ticket_can_come_from_environment(
    monkeypatch: pytest.MonkeyPatch,
    make_client: Any,
    tender_payload: dict[str, Any],
) -> None:
    monkeypatch.setenv(DEFAULT_TICKET_ENV, "environment-ticket")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["ticket"] == "environment-ticket"
        return httpx.Response(200, json=tender_payload)

    sdk = SyncChilePublicMarketClient(http_client=make_client(handler))
    assert sdk.get_tenders().count == 1


def test_get_tenders_formats_filters_and_validates_response(
    make_client: Any,
    tender_payload: dict[str, Any],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/licitaciones.json")
        assert request.url.params["fecha"] == "12062026"
        assert request.url.params["estado"] == "publicada"
        assert request.url.params["ticket"] == "secret"
        return httpx.Response(200, json=tender_payload)

    sdk = SyncChilePublicMarketClient(ticket="secret", http_client=make_client(handler))
    response = sdk.get_tenders(date=date(2026, 6, 12), status=TenderStatus.PUBLISHED)

    assert response.items[0].external_code == "1509-5-L114"
    assert response.items[0].model_extra == {"CampoNuevo": "preserved"}


def test_code_cannot_be_combined_with_other_filters(make_client: Any) -> None:
    sdk = SyncChilePublicMarketClient(
        ticket="secret",
        http_client=make_client(lambda request: httpx.Response(500)),
    )
    with pytest.raises(RequestValidationError):
        sdk.get_tenders(code="1", date="12062026")

    with pytest.raises(RequestValidationError):
        sdk.get_purchase_orders(code="1", date="12062026")


def test_all_v1_company_endpoints(make_client: Any) -> None:
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.url.path)
        if request.url.path.endswith("BuscarProveedor"):
            assert request.url.params["rutempresaproveedor"] == "70.017.820-k"
            return httpx.Response(
                200,
                json={"CodigoEmpresa": 17793, "NombreEmpresa": "Proveedor", "Rut": "70.017.820-k"},
            )
        return httpx.Response(200, json=[{"CodigoEmpresa": 6945, "NombreEmpresa": "ChileCompra"}])

    sdk = SyncChilePublicMarketClient(ticket="secret", http_client=make_client(handler))
    assert sdk.find_supplier("70.017.820-k").companies[0].company_code == 17793
    assert sdk.get_buyers().companies[0].company_code == 6945
    assert seen == [
        "/servicios/v1/publico/Empresas/BuscarProveedor",
        "/servicios/v1/publico/Empresas/BuscarComprador",
    ]


def test_agile_purchase_uses_header_and_filters(
    make_client: Any, agile_page_payload: dict[str, Any]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v2/compra-agil"
        assert request.headers["ticket"] == "secret"
        assert "ticket" not in request.url.params
        assert request.url.params["estado"] == "publicada,cerrada"
        assert request.url.params["region"] == "13,5"
        return httpx.Response(200, json=agile_page_payload)

    sdk = SyncChilePublicMarketClient(ticket="secret", http_client=make_client(handler))
    page = sdk.get_agile_purchases(
        last_change_ttl_ms=300_000,
        statuses=[AgilePurchaseStatus.PUBLISHED, AgilePurchaseStatus.CLOSED],
        regions=[13, 5],
    )
    assert page.pagination.total_results == 1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {"last_change_ttl_ms": 1, "changed_from": "2026-01-01T00:00:00Z"},
            "last_change_ttl_ms",
        ),
        ({"external_id": "code", "query": "text"}, "mutually"),
        ({"page_size": 9}, "page_size"),
        ({"page_number": 0}, "page_number"),
        ({"regions": [17]}, "region"),
    ],
)
def test_agile_purchase_validates_filters(
    make_client: Any, kwargs: dict[str, Any], message: str
) -> None:
    sdk = SyncChilePublicMarketClient(
        ticket="secret",
        http_client=make_client(lambda request: httpx.Response(500)),
    )
    with pytest.raises(RequestValidationError, match=message):
        sdk.get_agile_purchases(**kwargs)


@pytest.mark.parametrize(
    ("status", "error_type"),
    [(401, AuthenticationError), (403, AuthenticationError), (429, RateLimitError)],
)
def test_http_errors_are_normalized(
    make_client: Any, status: int, error_type: type[Exception]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status,
            headers={"Retry-After": "10"},
            json={
                "success": "NOK",
                "errors": [{"codigo": str(status), "mensaje": "failed", "detalle": None}],
            },
        )

    sdk = SyncChilePublicMarketClient(ticket="secret", http_client=make_client(handler))
    with pytest.raises(error_type) as captured:
        sdk.get_agile_purchases()
    assert "secret" not in str(captured.value)


def test_sync_rejects_empty_resource_identifiers(make_client: Any) -> None:
    client = SyncChilePublicMarketClient(
        ticket="secret",
        http_client=make_client(lambda request: httpx.Response(500)),
    )

    with pytest.raises(RequestValidationError, match="tax_id cannot be empty"):
        client.find_supplier(" ")
    with pytest.raises(RequestValidationError, match="code cannot be empty"):
        client.get_agile_purchase(" ")


def test_sync_agile_purchase_requires_payload(make_client: Any) -> None:
    client = SyncChilePublicMarketClient(
        ticket="secret",
        http_client=make_client(
            lambda request: httpx.Response(200, json={"success": "OK", "payload": None})
        ),
    )

    with pytest.raises(APIError, match="without a payload"):
        client.get_agile_purchases()
    with pytest.raises(APIError, match="without a payload"):
        client.get_agile_purchase("1057539-228-COT26")
