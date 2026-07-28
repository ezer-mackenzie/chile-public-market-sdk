"""Buyer and supplier company models."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from .base import MercadoPublicoModel, _normalize_wire_keys


class Company(MercadoPublicoModel):
    company_code: str | int | None = None
    company_name: str | None = None
    tax_id: str | None = None


class CompanyResponse(MercadoPublicoModel):
    companies: list[Company] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_shape(cls, value: Any) -> Any:
        normalized = _normalize_wire_keys(value)
        if isinstance(normalized, list):
            return {"companies": normalized}
        if isinstance(normalized, dict):
            if "companies" in normalized:
                return normalized
            if "company_code" in normalized:
                return {"companies": [normalized]}
        return normalized
