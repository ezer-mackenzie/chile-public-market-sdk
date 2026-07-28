"""Tender models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, Field

from .base import MercadoPublicoModel
from .common import LineItem, Organization


class Tender(MercadoPublicoModel):
    external_code: str = Field(
        validation_alias=AliasChoices("external_code", "code")
    )
    name: str | None = None
    status_code: int | None = None
    status: str | None = None
    description: str | None = None
    closing_at: datetime | str | None = None
    currency: str | None = None
    estimated_amount: Decimal | None = None
    buyer: Organization | None = None
    items: list[LineItem] = Field(default_factory=list)


class TenderResponse(MercadoPublicoModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[Tender] = Field(default_factory=list)
