"""Agile Purchase v2 models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from ..enums import AgilePurchaseStatus
from .base import MercadoPublicoModel


class AgileError(MercadoPublicoModel):
    code: str
    message: str
    details: str | None = None


class AgileEnvelope[PayloadT](MercadoPublicoModel):
    success: str
    trace: str | None = None
    payload: PayloadT | None = None
    errors: list[AgileError] | None = None


class AgileState(MercadoPublicoModel):
    status_id: int
    code: AgilePurchaseStatus
    label: str


class AgileCall(MercadoPublicoModel):
    round_status: int
    description: str
    first_round_closing_at: datetime | None = None
    second_round_closing_at: datetime | None = None


class AgileDocument(MercadoPublicoModel):
    id: str
    name: str


class AgileDates(MercadoPublicoModel):
    published_at: datetime
    closing_at: datetime
    last_changed_at: datetime
    cancelled_at: datetime | None = None


class AgileInstitution(MercadoPublicoModel):
    buyer_organization: str
    tax_id: str
    purchasing_unit: str
    region: int | None = None
    region_name: str | None = None


class AgileAmounts(MercadoPublicoModel):
    currency: str
    available_amount: Decimal | None = None
    available_amount_clp: Decimal | None = None


class AgileSummary(MercadoPublicoModel):
    total_quotes_received: int = 0
    total_requests: int | None = None
    penalty_amount: Decimal | None = None


class AgileReasons(MercadoPublicoModel):
    cancellation_reason: str | None = None
    desertion_reason: str | None = None
    selection_reason: str | None = None


class AgileLinks(MercadoPublicoModel):
    details: str


class AgilePurchaseSummary(MercadoPublicoModel):
    code: str
    name: str
    status: AgileState
    call: AgileCall
    documents: list[AgileDocument] = Field(default_factory=list)
    dates: AgileDates
    amounts: AgileAmounts
    institution: AgileInstitution
    summary: AgileSummary
    reasons: AgileReasons
    links: AgileLinks


class AgilePagination(MercadoPublicoModel):
    total_pages: int
    page_number: int
    page_size: int
    total_results: int


class AgilePurchasePage(MercadoPublicoModel):
    items: list[AgilePurchaseSummary]
    pagination: AgilePagination


class AgileDelivery(MercadoPublicoModel):
    delivery_address: str
    delivery_days: int | None = None


class AgileBudget(MercadoPublicoModel):
    budget_type: str
    currency: str
    estimated_budget: Decimal | None = None
    available_amount: Decimal | None = None
    available_amount_clp: Decimal | None = None
    exchange_rate: Decimal | None = None
    exchange_rate_at: datetime | None = None


class AgilePurchaseOrderReference(MercadoPublicoModel):
    purchase_order_id: int | None = None
    purchase_order_internal_id: int | None = None
    purchase_order_code: str | None = None
    purchase_order_status: str | None = None


class AgileRequestedProduct(MercadoPublicoModel):
    product_code: int | str
    name: str
    description: str | None = None
    quantity: Decimal
    unit_of_measure: str


class AgileQuotedProduct(MercadoPublicoModel):
    product_code: int | str
    product_name: str
    description: str | None = None
    quantity: Decimal
    unit_price: Decimal | None = None
    product_total: Decimal | None = None


class AgileQuote(MercadoPublicoModel):
    supplier_tax_id: str
    legal_name: str
    is_small_business: bool
    quote_id: int | None = None
    company_code: str | None = None
    company_branch_code: str | None = None
    buyer_status: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    valid_until: datetime | None = None
    net_amount: Decimal | None = None
    tax_amount: Decimal | None = None
    shipping_amount: Decimal | None = None
    total_amount: Decimal | None = None
    tax_name: str | None = None
    tax_percentage: Decimal | None = None
    quote_description: str | None = None
    description: str | None = None
    inadmissibility_reason: str | None = None
    quoted_products: list[AgileQuotedProduct] = Field(default_factory=list)


class AgileFlags(MercadoPublicoModel):
    has_environmental_requirements: bool
    has_social_economic_requirements: bool


class AgilePurchaseDetail(MercadoPublicoModel):
    code: str
    name: str
    description: str
    status: AgileState
    call: AgileCall
    dates: AgileDates
    delivery: AgileDelivery
    documents: list[AgileDocument] = Field(default_factory=list)
    budget: AgileBudget
    purchase_order: AgilePurchaseOrderReference
    institution: AgileInstitution
    requested_products: list[AgileRequestedProduct] = Field(default_factory=list)
    quoting_suppliers: list[AgileQuote] = Field(default_factory=list)
    summary: AgileSummary
    reasons: AgileReasons
    flags: AgileFlags
