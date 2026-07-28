"""Purchase order models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from .base import ChilePublicMarketModel
from .common import LineItem, Organization, Supplier


class PurchaseOrderDates(ChilePublicMarketModel):
    created_at: datetime | None = None
    sent_at: datetime | None = None
    accepted_at: datetime | None = None
    cancelled_at: datetime | None = None
    last_modified_at: datetime | None = None


class PurchaseOrder(ChilePublicMarketModel):
    code: str
    name: str | None = None
    status_code: int | None = None
    status: str | None = None
    sent_at: datetime | str | None = None
    total: Decimal | None = None
    currency: str | None = None
    tender_code: str | None = None
    type_code: str | int | None = None
    type: str | None = None
    supplier_status_code: int | None = None
    supplier_status: str | None = None
    dates: PurchaseOrderDates | None = None
    has_items: str | bool | None = None
    average_rating: Decimal | None = None
    rating_count: int | None = None
    discounts: Decimal | None = None
    charges: Decimal | None = None
    net_total: Decimal | None = None
    vat_percentage: Decimal | None = None
    taxes: Decimal | None = None
    funding_source: str | None = None
    country: str | None = None
    shipping_type: str | None = None
    payment_method: str | None = None
    buyer: Organization | None = None
    supplier: Supplier | None = None
    items: list[LineItem] = Field(default_factory=list)

    @field_validator("items", mode="before")
    @classmethod
    def unpack_items(cls, value: object) -> object:
        if isinstance(value, dict):
            return value.get("items", [])
        return value


class PurchaseOrderResponse(ChilePublicMarketModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[PurchaseOrder] = Field(default_factory=list)
