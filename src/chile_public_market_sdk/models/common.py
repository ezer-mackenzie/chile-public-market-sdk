"""Models shared by the v1 API."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import AliasChoices, Field

from .base import MercadoPublicoModel


class APIv1Response(MercadoPublicoModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)


class Organization(MercadoPublicoModel):
    organization_code: str | int | None = Field(
        default=None,
        validation_alias=AliasChoices("organization_code", "company_code"),
    )
    organization_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("organization_name", "company_name"),
    )
    tax_id: str | None = None
    unit: str | None = None
    region: str | int | None = None
    municipality: str | None = None


class Supplier(MercadoPublicoModel):
    code: str | int | None = None
    name: str | None = None
    tax_id: str | None = None


class LineItem(MercadoPublicoModel):
    line_number: int | None = None
    product_code: str | int | None = None
    product_name: str | None = None
    description: str | None = None
    quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("quantity", "count"),
    )
    unit_of_measure: str | None = None
