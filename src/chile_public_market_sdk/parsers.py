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
    def _build_error(
        status_code: int,
        message: str,
        /,
        code: str | None = None,
        details: Any = None,
        retry_after: str | None = None,
    ) -> APIError:
        error_type: type[APIError]
        if status_code in (401, 403):
            error_type = AuthenticationError
        elif status_code == 404:
            error_type = NotFoundError
        elif status_code == 429:
            error_type = RateLimitError
        else:
            error_type = APIError

        return error_type(
            message,
            status_code=status_code,
            code=code,
            details=details,
            retry_after=retry_after,
        )

    @staticmethod
    def decode_json(content: bytes, /) -> Any:
        """Decode JSON while tolerating the UTF-8 BOM returned by legacy services."""

        try:
            return json.loads(content.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ResponseValidationError("Mercado Público returned invalid JSON.") from exc

    @staticmethod
    def parse_model[ModelT: BaseModel](
        model: type[ModelT],
        payload: Any,
        /,
    ) -> ModelT:
        """Validate a payload against the supplied Pydantic model."""

        try:
            return model.model_validate(payload)
        except ValidationError as exc:
            raise ResponseValidationError(
                f"The response does not match {model.__name__}: {exc.error_count()} error(s)."
            ) from exc

    @staticmethod
    def api_error(
        response: httpx.Response,
        payload: Any,
        /,
        message: str = "Mercado Público returned HTTP {status_code}.",
        code: str | None = None,
        details: Any = None,
        retry_after: str | None = None,
    ) -> APIError:
        """Build an API error, allowing callers to override parsed metadata."""

        status_code = response.status_code
        default_message = "Mercado Público returned HTTP {status_code}."
        use_payload_message = message == default_message
        if use_payload_message:
            message = message.format(status_code=status_code)
        retry_after = retry_after or response.headers.get("Retry-After")

        if isinstance(payload, dict):
            errors = payload.get("errors") or payload.get("Errores")
            if isinstance(errors, list) and errors and isinstance(errors[0], dict):
                first = errors[0]
                if code is None:
                    code = str(first.get("codigo") or first.get("Codigo") or status_code)
                if use_payload_message:
                    message = str(first.get("mensaje") or first.get("Mensaje") or message)
                if details is None:
                    details = first.get("detalle") or first.get("Detalle")
            elif use_payload_message:
                message = str(
                    payload.get("mensaje")
                    or payload.get("Mensaje")
                    or payload.get("error")
                    or message
                )

        return ResponseParser._build_error(
            status_code,
            message,
            code=code,
            details=details,
            retry_after=retry_after,
        )

    @classmethod
    def decode_response(cls, response: httpx.Response, /) -> Any:
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
