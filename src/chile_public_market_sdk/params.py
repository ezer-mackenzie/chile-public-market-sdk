"""Request parameter normalization."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from enum import Enum
from typing import Any

from .errors import RequestValidationError


class ParameterEncoder:
    """Normalize public Python values into upstream query parameters."""

    @staticmethod
    def v1_date(value: date | str) -> str:
        if isinstance(value, datetime):
            return value.strftime("%d%m%Y")
        if isinstance(value, date):
            return value.strftime("%d%m%Y")
        digits = value.strip()
        if len(digits) != 8 or not digits.isdigit():
            raise RequestValidationError("A v1 API date must use ddmmyyyy format.")
        try:
            datetime.strptime(digits, "%d%m%Y")
        except ValueError as exc:
            raise RequestValidationError("The v1 API date is invalid.") from exc
        return digits

    @staticmethod
    def iso_datetime(value: datetime | str) -> str:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise RequestValidationError("The date must use ISO-8601 format.") from exc
        return value

    @staticmethod
    def enum_value(value: Enum | str) -> str:
        return str(value.value if isinstance(value, Enum) else value)

    @classmethod
    def csv_values(cls, values: Iterable[Enum | str | int]) -> str:
        return ",".join(
            cls.enum_value(value) if not isinstance(value, int) else str(value) for value in values
        )

    @staticmethod
    def compact(params: dict[str, Any]) -> dict[str, str | int | float]:
        return {key: value for key, value in params.items() if value is not None}
