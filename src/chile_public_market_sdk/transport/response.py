"""HTTP response decoding and SDK error mapping."""

from typing import Any

import httpx

from ..errors import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)
from ..parsers import ResponseParser


class TransportResponseDecoder:
    """Decode HTTP responses and map upstream failures to SDK exceptions."""

    @staticmethod
    def api_error(response: httpx.Response, payload: Any) -> APIError:
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

    @classmethod
    def decode(cls, response: httpx.Response) -> Any:
        try:
            payload = ResponseParser.decode_json(response.content)
        except Exception:
            if response.is_error:
                raise APIError(
                    f"Mercado Público returned HTTP {response.status_code}.",
                    status_code=response.status_code,
                    retry_after=response.headers.get("Retry-After"),
                ) from None
            raise
        if response.is_error:
            raise cls.api_error(response, payload)
        if isinstance(payload, dict) and str(payload.get("success", "")).upper() == "NOK":
            raise cls.api_error(response, payload)
        return payload
