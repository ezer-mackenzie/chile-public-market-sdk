"""Cliente síncrono para todos los endpoints públicos documentados."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from typing import Any, Self

import httpx

from .config import ClientConfig
from .enums import AgilePurchaseSort, AgilePurchaseStatus, PurchaseOrderStatus, TenderStatus
from .errors import APIError, RequestValidationError
from .models import (
    AgileEnvelope,
    AgilePurchaseDetail,
    AgilePurchasePage,
    CompanyResponse,
    PurchaseOrderResponse,
    TenderResponse,
)
from .params import compact, csv_values, enum_value, iso_datetime, v1_date
from .parsers import parse_model
from .transport import SyncTransport


class MercadoPublicoClient:
    """Cliente HTTP síncrono.

    Puede recibir un `httpx.Client` para integrar instrumentación o transporte propio.
    """

    def __init__(
        self,
        ticket: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.Client | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.config = config or ClientConfig(ticket=ticket, timeout=timeout)
        self._ticket = self.config.resolved_ticket()
        self._owns_client = http_client is None
        client = http_client or httpx.Client(timeout=self.config.timeout)
        self._transport = SyncTransport(client)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._transport.client.close()

    def _v1(self, path: str, params: dict[str, Any]) -> Any:
        return self._transport.get(
            f"{self.config.base_url_v1.rstrip('/')}/{path}",
            params={**compact(params), "ticket": self._ticket},
        )

    def _v2(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._transport.get(
            f"{self.config.base_url_v2.rstrip('/')}/{path.lstrip('/')}",
            params=compact(params or {}),
            headers={"ticket": self._ticket},
        )

    def licitaciones(
        self,
        *,
        codigo: str | None = None,
        fecha: date | str | None = None,
        estado: TenderStatus | str | None = None,
        codigo_organismo: str | int | None = None,
        codigo_proveedor: str | int | None = None,
    ) -> TenderResponse:
        """Consulta licitaciones por código, fecha, estado, organismo o proveedor."""

        if codigo and any((fecha, estado, codigo_organismo, codigo_proveedor)):
            raise RequestValidationError("codigo no puede combinarse con otros filtros.")
        params = {
            "codigo": codigo,
            "fecha": v1_date(fecha) if fecha is not None else None,
            "estado": enum_value(estado) if estado is not None else None,
            "CodigoOrganismo": codigo_organismo,
            "CodigoProveedor": codigo_proveedor,
        }
        return parse_model(TenderResponse, self._v1("licitaciones.json", params))

    def ordenes_de_compra(
        self,
        *,
        codigo: str | None = None,
        fecha: date | str | None = None,
        estado: PurchaseOrderStatus | str | None = None,
        codigo_organismo: str | int | None = None,
        codigo_proveedor: str | int | None = None,
    ) -> PurchaseOrderResponse:
        """Consulta órdenes de compra usando todos los filtros de API v1."""

        if codigo and any((fecha, estado, codigo_organismo, codigo_proveedor)):
            raise RequestValidationError("codigo no puede combinarse con otros filtros.")
        params = {
            "codigo": codigo,
            "fecha": v1_date(fecha) if fecha is not None else None,
            "estado": enum_value(estado) if estado is not None else None,
            "CodigoOrganismo": codigo_organismo,
            "CodigoProveedor": codigo_proveedor,
        }
        return parse_model(PurchaseOrderResponse, self._v1("ordenesdecompra.json", params))

    def buscar_proveedor(self, rut: str) -> CompanyResponse:
        """Obtiene el código interno de un proveedor a partir de su RUT."""

        if not rut.strip():
            raise RequestValidationError("rut no puede estar vacío.")
        payload = self._v1("Empresas/BuscarProveedor", {"rutempresaproveedor": rut})
        return parse_model(CompanyResponse, payload)

    def compradores(self) -> CompanyResponse:
        """Lista todos los organismos compradores de Mercado Público."""

        return parse_model(CompanyResponse, self._v1("Empresas/BuscarComprador", {}))

    def compras_agiles(
        self,
        *,
        ttl_cambio_ms: int | None = None,
        cambio_desde: datetime | str | None = None,
        cambio_hasta: datetime | str | None = None,
        publicado_desde: datetime | str | None = None,
        publicado_hasta: datetime | str | None = None,
        estados: Iterable[AgilePurchaseStatus | str] | None = None,
        regiones: Iterable[int] | None = None,
        id: str | None = None,
        q: str | None = None,
        tamano_pagina: int = 15,
        numero_pagina: int = 1,
        ordenar_por: AgilePurchaseSort | str = AgilePurchaseSort.LAST_MODIFIED,
    ) -> AgilePurchasePage:
        """Lista Compras Ágiles con filtros y paginación."""

        if ttl_cambio_ms is not None and (cambio_desde is not None or cambio_hasta is not None):
            raise RequestValidationError(
                "ttl_cambio_ms no puede combinarse con cambio_desde/cambio_hasta."
            )
        if id and q:
            raise RequestValidationError("id y q son mutuamente excluyentes.")
        if not 1 <= tamano_pagina <= 50:
            raise RequestValidationError("tamano_pagina debe estar entre 1 y 50.")
        if numero_pagina < 1:
            raise RequestValidationError("numero_pagina debe ser mayor o igual a 1.")
        region_values = list(regiones) if regiones is not None else None
        if region_values and any(not 1 <= region <= 16 for region in region_values):
            raise RequestValidationError("Cada región debe estar entre 1 y 16.")

        params = {
            "ttl_cambio_ms": ttl_cambio_ms,
            "cambio_desde": iso_datetime(cambio_desde) if cambio_desde is not None else None,
            "cambio_hasta": iso_datetime(cambio_hasta) if cambio_hasta is not None else None,
            "publicado_desde": (
                iso_datetime(publicado_desde) if publicado_desde is not None else None
            ),
            "publicado_hasta": (
                iso_datetime(publicado_hasta) if publicado_hasta is not None else None
            ),
            "estado": csv_values(estados) if estados is not None else None,
            "region": csv_values(region_values) if region_values is not None else None,
            "id": id,
            "q": q,
            "tamano_pagina": tamano_pagina,
            "numero_pagina": numero_pagina,
            "ordenar_por": enum_value(ordenar_por),
        }
        envelope_type = AgileEnvelope[AgilePurchasePage]
        envelope = parse_model(envelope_type, self._v2("compra-agil", params))
        if envelope.payload is None:
            raise APIError("Compra Ágil devolvió una respuesta exitosa sin payload.")
        return envelope.payload

    def compra_agil(self, codigo: str) -> AgilePurchaseDetail:
        """Obtiene el detalle completo de una Compra Ágil."""

        if not codigo.strip():
            raise RequestValidationError("codigo no puede estar vacío.")
        envelope_type = AgileEnvelope[AgilePurchaseDetail]
        envelope = parse_model(envelope_type, self._v2(f"compra-agil/{codigo}"))
        if envelope.payload is None:
            raise APIError("Compra Ágil devolvió una respuesta exitosa sin payload.")
        return envelope.payload
