"""Mercado Público upstream API v2 contract."""

V2_BASE_URL = "https://api2.mercadopublico.cl/v2"
V2_AGILE_PURCHASES_PATH = "compra-agil"


def agile_purchase_detail_path(code: str) -> str:
    """Build the upstream v2 detail path for an Agile Purchase."""

    return f"{V2_AGILE_PURCHASES_PATH}/{code}"
