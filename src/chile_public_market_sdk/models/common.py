"""Models shared by the v1 API."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import AliasChoices, Field

from .base import ChilePublicMarketModel


class APIv1Response(ChilePublicMarketModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)


class Organization(ChilePublicMarketModel):
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
    unit_tax_id: str | None = None
    unit_code: str | None = None
    unit_address: str | None = None
    user_tax_id: str | None = None
    user_code: str | None = None
    user_name: str | None = None
    user_role: str | None = None
    activity: str | None = None
    country: str | None = None
    contact_name: str | None = None
    contact_role: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None


class Supplier(ChilePublicMarketModel):
    code: str | int | None = None
    name: str | None = None
    tax_id: str | None = None
    activity: str | None = None
    branch_code: str | None = None
    branch_name: str | None = None
    branch_tax_id: str | None = None
    address: str | None = None
    municipality: str | None = None
    region: str | None = None
    country: str | None = None
    contact_name: str | None = None
    contact_role: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None


class LineItemAward(ChilePublicMarketModel):
    supplier_tax_id: str | None = None
    supplier_name: str | None = None
    awarded_quantity: Decimal | None = None
    unit_amount: Decimal | None = None


class LineItem(ChilePublicMarketModel):
    line_number: int | None = None
    product_code: str | int | None = None
    product_name: str | None = None
    description: str | None = None
    quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("quantity", "count"),
    )
    unit_of_measure: str | None = None
    category_code: str | int | None = None
    category: str | None = None
    product: str | None = None
    buyer_specification: str | None = None
    supplier_specification: str | None = None
    currency: str | None = None
    net_price: Decimal | None = None
    total_charges: Decimal | None = None
    total_discounts: Decimal | None = None
    total_taxes: Decimal | None = None
    total: Decimal | None = None
    award: LineItemAward | None = None
