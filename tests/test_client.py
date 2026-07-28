from __future__ import annotations

from datetime import date
from typing import Any

import httpx
import pytest

from chile_public_market_sdk import MercadoPublicoClient
from chile_public_market_sdk.enums import AgilePurchaseStatus, TenderStatus
from chile_public_market_sdk.errors import (
    AuthenticationError,
    ConfigurationError,
    RateLimitError,
    RequestValidationError,
)


def test_ticket_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MERCADO_PUBLICO_TICKET", raising=False)
    with pytest.raises(ConfigurationError):
        MercadoPublicoClient()


def test_ticket_can_come_from_environment(
    monkeypatch: pytest.MonkeyPatch,
    make_client: Any,
    tender_payload: dict[str, Any],
) -> None:
    monkeypatch.setenv("MERCADO_PUBLICO_TICKET", "environment-ticket")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["ticket"] == "environment-ticket"
        return httpx.Response(200, json=tender_payload)

    sdk = MercadoPublicoClient(http_client=make_client(handler))
    assert sdk.licitaciones().cantidad == 1


def test_licitaciones_formats_filters_and_validates_response(
    make_client: Any,
    tender_payload: dict[str, Any],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/licitaciones.json")
        assert request.url.params["fecha"] == "12062026"
        assert request.url.params["estado"] == "publicada"
        assert request.url.params["ticket"] == "secret"
        return httpx.Response(200, json=tender_payload)

    sdk = MercadoPublicoClient(ticket="secret", http_client=make_client(handler))
    response = sdk.licitaciones(fecha=date(2026, 6, 12), estado=TenderStatus.PUBLISHED)

    assert response.listado[0].codigo_externo == "1509-5-L114"
    assert response.listado[0].model_extra == {"CampoNuevo": "se conserva"}


def test_codigo_cannot_be_combined_with_other_filters(make_client: Any) -> None:
    sdk = MercadoPublicoClient(
        ticket="secret",
        http_client=make_client(lambda request: httpx.Response(500)),
    )
    with pytest.raises(RequestValidationError):
        sdk.licitaciones(codigo="1", fecha="12062026")


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
        return httpx.Response(
            200, json=[{"CodigoEmpresa": 6945, "NombreEmpresa": "ChileCompra"}]
        )

    sdk = MercadoPublicoClient(ticket="secret", http_client=make_client(handler))
    assert sdk.buscar_proveedor("70.017.820-k").empresas[0].codigo_empresa == 17793
    assert sdk.compradores().empresas[0].codigo_empresa == 6945
    assert seen == [
        "/servicios/v1/publico/Empresas/BuscarProveedor",
        "/servicios/v1/publico/Empresas/BuscarComprador",
    ]


def test_compra_agil_uses_header_and_filters(
    make_client: Any, agile_page_payload: dict[str, Any]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v2/compra-agil"
        assert request.headers["ticket"] == "secret"
        assert "ticket" not in request.url.params
        assert request.url.params["estado"] == "publicada,cerrada"
        assert request.url.params["region"] == "13,5"
        return httpx.Response(200, json=agile_page_payload)

    sdk = MercadoPublicoClient(ticket="secret", http_client=make_client(handler))
    page = sdk.compras_agiles(
        ttl_cambio_ms=300_000,
        estados=[AgilePurchaseStatus.PUBLISHED, AgilePurchaseStatus.CLOSED],
        regiones=[13, 5],
    )
    assert page.paginacion.total_resultados == 1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"ttl_cambio_ms": 1, "cambio_desde": "2026-01-01T00:00:00Z"}, "ttl_cambio_ms"),
        ({"id": "code", "q": "text"}, "mutuamente"),
        ({"tamano_pagina": 51}, "tamano_pagina"),
        ({"regiones": [17]}, "región"),
    ],
)
def test_compra_agil_validates_filters(
    make_client: Any, kwargs: dict[str, Any], message: str
) -> None:
    sdk = MercadoPublicoClient(
        ticket="secret",
        http_client=make_client(lambda request: httpx.Response(500)),
    )
    with pytest.raises(RequestValidationError, match=message):
        sdk.compras_agiles(**kwargs)


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
                "errors": [{"codigo": str(status), "mensaje": "falló", "detalle": None}],
            },
        )

    sdk = MercadoPublicoClient(ticket="secret", http_client=make_client(handler))
    with pytest.raises(error_type) as captured:
        sdk.compras_agiles()
    assert "secret" not in str(captured.value)
