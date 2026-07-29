"""Synchronous client for every documented public endpoint."""

from __future__ import annotations

import time
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from typing import Any, Self

import httpx

from .._http.events import HttpEventFactory
from .._http.response import HttpResponseDecoder
from .._http.retry import RetryPolicy
from ..api import (
    V1_BUYERS_PATH,
    V1_PURCHASE_ORDERS_PATH,
    V1_SUPPLIERS_PATH,
    V1_TENDERS_PATH,
    V2_AGILE_PURCHASES_PATH,
)
from ..api.v2 import agile_purchase_detail_path
from ..config import ClientConfig, TimeoutValue
from ..enums import AgilePurchaseSort, AgilePurchaseStatus, PurchaseOrderStatus, TenderStatus
from ..errors import (
    APIError,
    NetworkError,
    RequestTimeoutError,
    RequestValidationError,
    TransportError,
)
from ..models import (
    AgileEnvelope,
    AgilePurchaseDetail,
    AgilePurchasePage,
    CompanyResponse,
    PurchaseOrderResponse,
    TenderResponse,
)
from ..params import compact, csv_values, enum_value, iso_datetime, v1_date
from ..parsers import parse_model

_NETWORK_ERRORS = (httpx.NetworkError, httpx.ProtocolError, httpx.ProxyError)


class SyncChilePublicMarketClient:
    """Synchronous HTTP client.

    Accepts an optional `httpx.Client` for custom transports and instrumentation.
    """

    def __init__(
        self,
        ticket: str | None = None,
        *,
        config: ClientConfig | None = None,
        http_client: httpx.Client | None = None,
        timeout: TimeoutValue = 30.0,
    ) -> None:
        self.config = config or ClientConfig(ticket=ticket, timeout=timeout)
        self._ticket = self.config.resolved_ticket()
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.Client(timeout=self.config.httpx_timeout())

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._http_client.close()

    def _request(
        self,
        url: str,
        *,
        params: Mapping[str, str | int | float] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        for attempt in range(1, self.config.retry.max_attempts + 1):
            request_event = HttpEventFactory.request(url, attempt)
            for request_hook in self.config.request_hooks:
                request_hook(request_event)
            started = time.monotonic()
            try:
                response = self._http_client.get(url, params=params, headers=headers)
            except httpx.TimeoutException as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    time.sleep(delay)
                    continue
                raise RequestTimeoutError("The Mercado Público request timed out.") from exc
            except _NETWORK_ERRORS as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    time.sleep(delay)
                    continue
                raise NetworkError("Could not communicate with Mercado Público.") from exc
            except httpx.HTTPError as exc:
                raise TransportError("Could not communicate with Mercado Público.") from exc
            response_event = HttpEventFactory.response(
                url, attempt, response, time.monotonic() - started
            )
            for response_hook in self.config.response_hooks:
                response_hook(response_event)
            delay = RetryPolicy.delay(self.config, attempt, response)
            if delay is not None:
                time.sleep(delay)
                continue
            return HttpResponseDecoder.decode(response)
        raise AssertionError("Retry loop completed without a response.")  # pragma: no cover

    def _v1(self, path: str, params: dict[str, Any]) -> Any:
        return self._request(
            f"{self.config.base_url_v1.rstrip('/')}/{path}",
            params={**compact(params), "ticket": self._ticket},
        )

    def _v2(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request(
            f"{self.config.base_url_v2.rstrip('/')}/{path.lstrip('/')}",
            params=compact(params or {}),
            headers={"ticket": self._ticket},
        )

    def get_tenders(
        self,
        *,
        code: str | None = None,
        date: date | str | None = None,
        status: TenderStatus | str | None = None,
        buyer_code: str | int | None = None,
        supplier_code: str | int | None = None,
    ) -> TenderResponse:
        """Get tenders by code, date, status, buyer, or supplier."""

        if code and any((date, status, buyer_code, supplier_code)):
            raise RequestValidationError("code cannot be combined with other filters.")
        params = {
            "codigo": code,
            "fecha": v1_date(date) if date is not None else None,
            "estado": enum_value(status) if status is not None else None,
            "CodigoOrganismo": buyer_code,
            "CodigoProveedor": supplier_code,
        }
        return parse_model(TenderResponse, self._v1(V1_TENDERS_PATH, params))

    def get_purchase_orders(
        self,
        *,
        code: str | None = None,
        date: date | str | None = None,
        status: PurchaseOrderStatus | str | None = None,
        buyer_code: str | int | None = None,
        supplier_code: str | int | None = None,
    ) -> PurchaseOrderResponse:
        """Get purchase orders using every supported v1 filter."""

        if code and any((date, status, buyer_code, supplier_code)):
            raise RequestValidationError("code cannot be combined with other filters.")
        params = {
            "codigo": code,
            "fecha": v1_date(date) if date is not None else None,
            "estado": enum_value(status) if status is not None else None,
            "CodigoOrganismo": buyer_code,
            "CodigoProveedor": supplier_code,
        }
        return parse_model(PurchaseOrderResponse, self._v1(V1_PURCHASE_ORDERS_PATH, params))

    def find_supplier(self, tax_id: str) -> CompanyResponse:
        """Find a supplier's internal company code from its Chilean tax ID."""

        if not tax_id.strip():
            raise RequestValidationError("tax_id cannot be empty.")
        payload = self._v1(V1_SUPPLIERS_PATH, {"rutempresaproveedor": tax_id})
        return parse_model(CompanyResponse, payload)

    def get_buyers(self) -> CompanyResponse:
        """List every buyer organization registered in Mercado Público."""

        return parse_model(CompanyResponse, self._v1(V1_BUYERS_PATH, {}))

    def get_agile_purchases(
        self,
        *,
        last_change_ttl_ms: int | None = None,
        changed_from: datetime | str | None = None,
        changed_until: datetime | str | None = None,
        published_from: datetime | str | None = None,
        published_until: datetime | str | None = None,
        statuses: Iterable[AgilePurchaseStatus | str] | None = None,
        regions: Iterable[int] | None = None,
        external_id: str | None = None,
        query: str | None = None,
        page_size: int = 15,
        page_number: int = 1,
        sort_by: AgilePurchaseSort | str = AgilePurchaseSort.LAST_MODIFIED,
    ) -> AgilePurchasePage:
        """List Agile Purchases with filters and pagination."""

        if last_change_ttl_ms is not None and (
            changed_from is not None or changed_until is not None
        ):
            raise RequestValidationError(
                "last_change_ttl_ms cannot be combined with changed_from/changed_until."
            )
        if external_id and query:
            raise RequestValidationError("external_id and query are mutually exclusive.")
        if not 10 <= page_size <= 50:
            raise RequestValidationError("page_size must be between 10 and 50.")
        if page_number < 1:
            raise RequestValidationError("page_number must be greater than or equal to 1.")
        region_values = list(regions) if regions is not None else None
        if region_values and any(not 1 <= region <= 16 for region in region_values):
            raise RequestValidationError("Each region code must be between 1 and 16.")

        params = {
            "ttl_cambio_ms": last_change_ttl_ms,
            "cambio_desde": iso_datetime(changed_from) if changed_from is not None else None,
            "cambio_hasta": iso_datetime(changed_until) if changed_until is not None else None,
            "publicado_desde": (
                iso_datetime(published_from) if published_from is not None else None
            ),
            "publicado_hasta": (
                iso_datetime(published_until) if published_until is not None else None
            ),
            "estado": csv_values(statuses) if statuses is not None else None,
            "region": csv_values(region_values) if region_values is not None else None,
            "id": external_id,
            "q": query,
            "tamano_pagina": page_size,
            "numero_pagina": page_number,
            "ordenar_por": enum_value(sort_by),
        }
        envelope_type = AgileEnvelope[AgilePurchasePage]
        envelope = parse_model(envelope_type, self._v2(V2_AGILE_PURCHASES_PATH, params))
        if envelope.payload is None:
            raise APIError("Agile Purchase returned a successful response without a payload.")
        return envelope.payload

    def get_agile_purchase(self, code: str) -> AgilePurchaseDetail:
        """Get the complete details for one Agile Purchase."""

        if not code.strip():
            raise RequestValidationError("code cannot be empty.")
        envelope_type = AgileEnvelope[AgilePurchaseDetail]
        envelope = parse_model(envelope_type, self._v2(agile_purchase_detail_path(code)))
        if envelope.payload is None:
            raise APIError("Agile Purchase returned a successful response without a payload.")
        return envelope.payload
