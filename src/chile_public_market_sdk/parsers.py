"""Conversión y validación de respuestas JSON."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ValidationError

from .errors import ResponseValidationError


def decode_json(content: bytes) -> Any:
    """Decodifica JSON, tolerando BOM UTF-8 presente en servicios legados."""

    try:
        return json.loads(content.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ResponseValidationError("Mercado Público devolvió JSON inválido.") from exc


def parse_model[ModelT: BaseModel](model: type[ModelT], payload: Any) -> ModelT:
    """Valida un payload usando el modelo Pydantic indicado."""

    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        raise ResponseValidationError(
            f"La respuesta no coincide con {model.__name__}: {exc.error_count()} error(es)."
        ) from exc
