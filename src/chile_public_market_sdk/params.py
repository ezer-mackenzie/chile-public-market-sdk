"""Normalización de filtros de consulta."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from enum import Enum
from typing import Any

from .errors import RequestValidationError


def v1_date(value: date | str) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d%m%Y")
    if isinstance(value, date):
        return value.strftime("%d%m%Y")
    digits = value.strip()
    if len(digits) != 8 or not digits.isdigit():
        raise RequestValidationError("La fecha de API v1 debe tener formato ddmmaaaa.")
    try:
        datetime.strptime(digits, "%d%m%Y")
    except ValueError as exc:
        raise RequestValidationError("La fecha de API v1 no es válida.") from exc
    return digits


def iso_datetime(value: datetime | str) -> str:
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RequestValidationError("La fecha debe usar formato ISO-8601.") from exc
    return value


def enum_value(value: Enum | str) -> str:
    return str(value.value if isinstance(value, Enum) else value)


def csv_values(values: Iterable[Enum | str | int]) -> str:
    return ",".join(
        enum_value(value) if not isinstance(value, int) else str(value) for value in values
    )


def compact(params: dict[str, Any]) -> dict[str, str | int | float]:
    return {key: value for key, value in params.items() if value is not None}
