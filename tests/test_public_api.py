from __future__ import annotations

from importlib.metadata import version
from inspect import signature

import chile_public_market_sdk
from chile_public_market_sdk import (
    AsyncChilePublicMarketClient,
    SyncChilePublicMarketClient,
)
from chile_public_market_sdk.models import TenderResponse

EXPECTED_TOP_LEVEL_EXPORTS = {
    "APIError",
    "AsyncChilePublicMarketClient",
    "AsyncChilePublicMarketSDK",
    "AuthenticationError",
    "ChilePublicMarketError",
    "ClientConfig",
    "ConfigurationError",
    "NotFoundError",
    "RateLimitError",
    "RequestValidationError",
    "ResponseValidationError",
    "SyncChilePublicMarketClient",
    "SyncChilePublicMarketSDK",
    "TransportError",
}

EXPECTED_RESOURCE_METHODS = {
    "get_tenders": ("self", "code", "date", "status", "buyer_code", "supplier_code"),
    "get_purchase_orders": (
        "self",
        "code",
        "date",
        "status",
        "buyer_code",
        "supplier_code",
    ),
    "find_supplier": ("self", "tax_id"),
    "get_buyers": ("self",),
    "get_agile_purchases": (
        "self",
        "last_change_ttl_ms",
        "changed_from",
        "changed_until",
        "published_from",
        "published_until",
        "statuses",
        "regions",
        "external_id",
        "query",
        "page_size",
        "page_number",
        "sort_by",
    ),
    "get_agile_purchase": ("self", "code"),
}


def test_top_level_public_exports_are_stable() -> None:
    assert set(chile_public_market_sdk.__all__) == EXPECTED_TOP_LEVEL_EXPORTS


def test_sync_and_async_resource_surfaces_match_snapshot() -> None:
    for client_type in (SyncChilePublicMarketClient, AsyncChilePublicMarketClient):
        actual = {
            method_name: tuple(signature(getattr(client_type, method_name)).parameters)
            for method_name in EXPECTED_RESOURCE_METHODS
        }
        assert actual == EXPECTED_RESOURCE_METHODS


def test_runtime_version_matches_distribution_metadata() -> None:
    assert chile_public_market_sdk.__version__ == version("mercado-publico-chile-sdk")
    assert chile_public_market_sdk.__version__ == "0.2.0"


def test_models_serialize_with_English_field_names() -> None:
    response = TenderResponse.model_validate(
        {
            "Cantidad": 1,
            "Listado": [{"CodigoExterno": "123-1-L126", "Nombre": "Example"}],
        }
    )

    assert response.model_dump() == {
        "count": 1,
        "created_at": None,
        "version": None,
        "items": [
            {
                "external_code": "123-1-L126",
                "name": "Example",
                "status_code": None,
                "status": None,
                "description": None,
                "closing_at": None,
                "currency": None,
                "estimated_amount": None,
                "buyer": None,
                "items": [],
            }
        ],
    }
