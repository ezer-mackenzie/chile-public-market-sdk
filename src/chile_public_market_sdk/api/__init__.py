"""Versioned upstream Mercado Público API contracts."""

from .v1 import (
    V1_BASE_URL,
    V1_BUYERS_PATH,
    V1_PURCHASE_ORDERS_PATH,
    V1_SUPPLIERS_PATH,
    V1_TENDERS_PATH,
)
from .v2 import V2_AGILE_PURCHASES_PATH, V2_BASE_URL

__all__ = [
    "V1_BASE_URL",
    "V1_BUYERS_PATH",
    "V1_PURCHASE_ORDERS_PATH",
    "V1_SUPPLIERS_PATH",
    "V1_TENDERS_PATH",
    "V2_AGILE_PURCHASES_PATH",
    "V2_BASE_URL",
]
