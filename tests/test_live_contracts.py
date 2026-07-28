from __future__ import annotations

import os

import pytest

from chile_public_market_sdk import SyncChilePublicMarketClient

pytestmark = pytest.mark.live


@pytest.fixture
def live_client() -> SyncChilePublicMarketClient:
    if os.getenv("RUN_LIVE_CONTRACT_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_CONTRACT_TESTS=1 to call production contracts.")
    return SyncChilePublicMarketClient()


def test_live_v1_contracts(live_client: SyncChilePublicMarketClient) -> None:
    assert live_client.get_tenders(code="1509-5-L114").items
    assert live_client.get_purchase_orders(code="2097-241-SE14").items
    assert live_client.find_supplier("70.017.820-k").companies
    assert live_client.get_buyers().companies


def test_live_v2_contracts(live_client: SyncChilePublicMarketClient) -> None:
    page = live_client.get_agile_purchases(
        last_change_ttl_ms=300_000,
        page_size=10,
    )
    if page.items:
        assert live_client.get_agile_purchase(page.items[0].code).code
