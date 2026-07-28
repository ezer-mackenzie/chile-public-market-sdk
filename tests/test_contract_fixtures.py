from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from chile_public_market_sdk.models import (
    AgileEnvelope,
    AgilePurchaseDetail,
    AgilePurchasePage,
    CompanyResponse,
    PurchaseOrderResponse,
    TenderResponse,
)

FIXTURES = Path(__file__).parent / "fixtures" / "contracts"


@pytest.mark.parametrize(
    ("filename", "model"),
    [
        ("tender-detail.json", TenderResponse),
        ("purchase-order-detail.json", PurchaseOrderResponse),
        ("supplier.json", CompanyResponse),
        ("buyers.json", CompanyResponse),
        ("agile-list.json", AgileEnvelope[AgilePurchasePage]),
        ("agile-detail.json", AgileEnvelope[AgilePurchaseDetail]),
    ],
)
def test_anonymized_production_contracts(
    filename: str,
    model: type[BaseModel],
) -> None:
    payload: Any = json.loads((FIXTURES / filename).read_text(encoding="utf-8"))
    validated = model.model_validate(payload)

    assert validated is not None


def test_detailed_v1_sections_are_typed() -> None:
    tender = TenderResponse.model_validate_json(
        (FIXTURES / "tender-detail.json").read_text(encoding="utf-8")
    ).items[0]
    order = PurchaseOrderResponse.model_validate_json(
        (FIXTURES / "purchase-order-detail.json").read_text(encoding="utf-8")
    ).items[0]

    assert tender.dates is not None
    assert tender.award is not None
    assert tender.items
    assert order.dates is not None
    assert order.buyer is not None
    assert order.supplier is not None
    assert order.items
