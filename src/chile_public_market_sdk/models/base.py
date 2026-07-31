"""Base model configuration and upstream payload normalization."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from .wire_keys import WIRE_KEY_MAP


class ChilePublicMarketModel(BaseModel):
    """Base model for ChileCompra payloads."""

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        serialize_by_alias=False,
    )

    @classmethod
    def normalize_payload(cls, value: Any) -> Any:
        """Recursively translate upstream keys into public English field names."""

        if isinstance(value, dict):
            return {
                WIRE_KEY_MAP.get(str(key), str(key)): cls.normalize_payload(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [cls.normalize_payload(item) for item in value]
        return value

    @model_validator(mode="before")
    @classmethod
    def normalize_wire_keys(cls, value: Any) -> Any:
        """Normalize a raw ChileCompra payload before field validation."""

        return cls.normalize_payload(value)
