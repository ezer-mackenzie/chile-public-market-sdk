"""Purchase order models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from .base import MercadoPublicoModel
from .common import LineItem, Organization, Supplier


class PurchaseOrder(MercadoPublicoModel):
    code: str
    name: str | None = None
    status_code: int | None = None
    status: str | None = None
    sent_at: datetime | str | None = None
    total: Decimal | None = None
    currency: str | None = None
    buyer: Organization | None = None
    supplier: Supplier | None = None
    items: list[LineItem] = Field(default_factory=list)


class PurchaseOrderResponse(MercadoPublicoModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[PurchaseOrder] = Field(default_factory=list)
