"""Tender models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, Field, field_validator

from .base import ChilePublicMarketModel
from .common import LineItem, Organization


class TenderDates(ChilePublicMarketModel):
    created_at: datetime | None = None
    closing_at: datetime | None = None
    forum_start_at: datetime | None = None
    forum_end_at: datetime | None = None
    answers_published_at: datetime | None = None
    technical_opening_at: datetime | None = None
    financial_opening_at: datetime | None = None
    published_at: datetime | None = None
    awarded_at: datetime | None = None
    estimated_award_at: datetime | None = None
    physical_support_at: datetime | None = None
    evaluation_at: datetime | None = None
    estimated_signature_at: datetime | None = None
    user_dates_at: datetime | None = None
    site_visit_at: datetime | None = None
    documents_due_at: datetime | None = None


class TenderAward(ChilePublicMarketModel):
    type: int | None = None
    date: datetime | None = None
    number: str | None = None
    bidder_count: int | None = None
    record_url: str | None = None


class Tender(ChilePublicMarketModel):
    external_code: str = Field(validation_alias=AliasChoices("external_code", "code"))
    name: str | None = None
    status_code: int | None = None
    status: str | None = None
    description: str | None = None
    closing_at: datetime | str | None = None
    currency: str | None = None
    estimated_amount: Decimal | None = None
    buyer: Organization | None = None
    dates: TenderDates | None = None
    award: TenderAward | None = None
    closing_days: str | int | None = None
    is_informed: int | bool | None = None
    type_code: int | None = None
    type: str | None = None
    call_type: str | int | None = None
    stages: int | None = None
    stage_status: str | int | None = None
    requires_comptroller_review: str | int | bool | None = None
    offer_publicity_status: int | bool | None = None
    publicity_justification: str | None = None
    contract_type: str | int | None = None
    is_public_work: str | int | bool | None = None
    complaint_count: int | None = None
    evaluation_time_unit: int | None = None
    visit_address: str | None = None
    delivery_address: str | None = None
    estimate_type: int | str | None = None
    funding_source: str | None = None
    is_amount_visible: int | bool | None = None
    time_value: str | int | None = None
    time_unit: str | int | None = None
    payment_terms_code: int | None = None
    payment_type: str | int | None = None
    payment_contact_name: str | None = None
    payment_contact_email: str | None = None
    contract_contact_name: str | None = None
    contract_contact_email: str | None = None
    contract_contact_phone: str | None = None
    contracting_prohibition: str | None = None
    allows_subcontracting: str | int | bool | None = None
    contract_duration_unit: int | None = None
    contract_duration: str | int | None = None
    contract_duration_type: str | None = None
    estimated_amount_justification: str | None = None
    contract_observation: str | None = None
    extends_deadline: int | bool | None = None
    uses_standard_terms: int | bool | None = None
    tender_contract_time_unit: str | int | None = None
    renewal_time_value: str | int | None = None
    renewal_time_period: str | None = None
    is_renewable: int | bool | None = None
    bip_code: str | None = None
    items: list[LineItem] = Field(default_factory=list)

    @field_validator("items", mode="before")
    @classmethod
    def unpack_items(cls, value: object) -> object:
        if isinstance(value, dict):
            return value.get("items", [])
        return value


class TenderResponse(ChilePublicMarketModel):
    count: int = 0
    created_at: datetime | str | None = None
    version: str | None = None
    items: list[Tender] = Field(default_factory=list)
