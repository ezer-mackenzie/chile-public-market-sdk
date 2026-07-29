"""JSON response decoding and validation."""

from __future__ import annotations

import json
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from .errors import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ResponseValidationError,
)


class ResponseParser:
    """Decode and validate upstream response payloads."""

    @staticmethod
    def decode_json(content: bytes) -> Any:
        """Decode JSON while tolerating the UTF-8 BOM returned by legacy services."""

        try:
            return json.loads(content.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ResponseValidationError("Mercado Público returned invalid JSON.") from exc

    @staticmethod
    def parse_model[ModelT: BaseModel](model: type[ModelT], payload: Any) -> ModelT:
        """Validate a payload against the supplied Pydantic model."""

        try:
            return model.model_validate(payload)
        except ValidationError as exc:
            raise ResponseValidationError(
                f"The response does not match {model.__name__}: {exc.error_count()} error(s)."
            ) from exc

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
    def decode_response(cls, response: httpx.Response) -> Any:
        """Decode an HTTPX response and normalize upstream API errors."""

        try:
            payload = cls.decode_json(response.content)
        except ResponseValidationError:
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
