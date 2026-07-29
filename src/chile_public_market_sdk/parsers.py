"""JSON response decoding and validation."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ValidationError

from .errors import ResponseValidationError


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


def decode_json(content: bytes) -> Any:
    """Compatibility wrapper for JSON response decoding."""

    return ResponseParser.decode_json(content)


def parse_model[ModelT: BaseModel](model: type[ModelT], payload: Any) -> ModelT:
    """Compatibility wrapper for Pydantic response validation."""

    return ResponseParser.parse_model(model, payload)
