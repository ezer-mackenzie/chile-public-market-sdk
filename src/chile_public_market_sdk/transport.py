"""Synchronous and asynchronous HTTP transport."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from .errors import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    TransportError,
)
from .parsers import decode_json

Params = Mapping[str, str | int | float]


def _api_error(response: httpx.Response, payload: Any) -> APIError:
    status = response.status_code
    message = f"Mercado Público returned HTTP {status}."
    code: str | None = None
    details: Any = None

    if isinstance(payload, dict):
        errors = payload.get("errors") or payload.get("Errores")
        if isinstance(errors, list) and errors and isinstance(errors[0], dict):
            first = errors[0]
            code = str(first.get("codigo") or first.get("Codigo") or status)
            message = str(first.get("mensaje") or first.get("Mensaje") or message)
            details = first.get("detalle") or first.get("Detalle")
        else:
            message = str(
                payload.get("mensaje")
                or payload.get("Mensaje")
                or payload.get("error")
                or message
            )

    kwargs = {
        "status_code": status,
        "code": code,
        "details": details,
        "retry_after": response.headers.get("Retry-After"),
    }
    if status in (401, 403):
        return AuthenticationError(message, **kwargs)
    if status == 404:
        return NotFoundError(message, **kwargs)
    if status == 429:
        return RateLimitError(message, **kwargs)
    return APIError(message, **kwargs)


def _decode_response(response: httpx.Response) -> Any:
    try:
        payload = decode_json(response.content)
    except Exception:
        if response.is_error:
            raise APIError(
                f"Mercado Público returned HTTP {response.status_code}.",
                status_code=response.status_code,
                retry_after=response.headers.get("Retry-After"),
            ) from None
        raise
    if response.is_error:
        raise _api_error(response, payload)
    if isinstance(payload, dict) and str(payload.get("success", "")).upper() == "NOK":
        raise _api_error(response, payload)
    return payload


class SyncTransport:
    """`httpx.Client` adapter with normalized SDK errors."""

    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def get(
        self,
        url: str,
        *,
        params: Params | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        try:
            response = self.client.get(url, params=params, headers=headers)
        except httpx.HTTPError as exc:
            raise TransportError("Could not communicate with Mercado Público.") from exc
        return _decode_response(response)


class AsyncTransport:
    """`httpx.AsyncClient` adapter with normalized SDK errors."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get(
        self,
        url: str,
        *,
        params: Params | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        try:
            response = await self.client.get(url, params=params, headers=headers)
        except httpx.HTTPError as exc:
            raise TransportError("Could not communicate with Mercado Público.") from exc
        return _decode_response(response)
