"""Mercado Público upstream API v2 contract."""

from ..core.constants.api import V2_AGILE_PURCHASES_PATH


def agile_purchase_detail_path(code: str) -> str:
    """Build the upstream v2 detail path for an Agile Purchase."""

    return f"{V2_AGILE_PURCHASES_PATH}/{code}"
