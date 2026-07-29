# Chile Public Market SDK

Unofficial, typed, synchronous and asynchronous Python SDK for Chile's
[Mercado Público APIs](https://www.chilecompra.cl/api/).

> Status: alpha (`0.4.0`). The upstream services include legacy contracts and
> may add fields. Models validate known fields while preserving new ones.

## Requirements

- Python 3.12 or newer.
- An access ticket requested through ChileCompra.

## Installation

```bash
pip install mercado-publico-chile-sdk
```

## Secure configuration

The SDK never includes or manages tickets. Pass one explicitly:

```python
from chile_public_market_sdk import SyncChilePublicMarketSDK

sdk = SyncChilePublicMarketSDK(ticket="YOUR_TICKET")
```

Or define `CHILE_PUBLIC_MARKET_TICKET`:

```bash
export CHILE_PUBLIC_MARKET_TICKET="YOUR_TICKET"
```

Git ignores `.env` and `env.yaml`. Loading them through Docker Compose,
Kubernetes, `envyaml`, `python-dotenv`, or another secret-management mechanism
is the consumer application's responsibility. The SDK itself does not read
configuration files.

## Synchronous usage

```python
from datetime import date

from chile_public_market_sdk import SyncChilePublicMarketSDK
from chile_public_market_sdk.enums import TenderStatus

with SyncChilePublicMarketSDK() as sdk:
    response = sdk.get_tenders(
        date=date(2026, 6, 12),
        status=TenderStatus.PUBLISHED,
    )
    for tender in response.items:
        print(tender.external_code, tender.name)

    order = sdk.get_purchase_orders(code="2097-241-SE14")
    supplier = sdk.find_supplier("70.017.820-k")
    buyers = sdk.get_buyers()
```

## Asynchronous usage

```python
import asyncio

from chile_public_market_sdk import AsyncChilePublicMarketSDK
from chile_public_market_sdk.enums import AgilePurchaseStatus


async def main() -> None:
    async with AsyncChilePublicMarketSDK() as sdk:
        page = await sdk.get_agile_purchases(
            last_change_ttl_ms=300_000,
            statuses=[AgilePurchaseStatus.PUBLISHED],
            page_size=50,
        )
        detail = await sdk.get_agile_purchase(page.items[0].code)
        print(detail.name)


asyncio.run(main())
```

## Endpoint coverage

| Resource | SDK method | API |
|---|---|---|
| Tenders | `get_tenders` | v1 |
| Purchase orders | `get_purchase_orders` | v1 |
| Suppliers | `find_supplier` | v1 |
| Buyer organizations | `get_buyers` | v1 |
| Agile Purchase listing and filters | `get_agile_purchases` | v2 |
| Agile Purchase details | `get_agile_purchase` | v2 |

V1 date filters accept a `date` or the original `ddmmyyyy` format. Agile
Purchase accepts ISO-8601 dates, multiple statuses and regions, pagination,
and sorting.

## Client classes and API versions

The SDK exposes separate synchronous and asynchronous classes:

- `SyncChilePublicMarketClient` / `SyncChilePublicMarketSDK`
- `AsyncChilePublicMarketClient` / `AsyncChilePublicMarketSDK`

ChileCompra endpoint contracts are versioned independently under
`chile_public_market_sdk.api.v1` and `chile_public_market_sdk.api.v2`. Future
upstream contracts will follow `api.v{version}`. SDK releases remain `0.x`
until the public Python API is stable enough for `1.0.0`.

## Errors

Every public exception inherits from `ChilePublicMarketError`:

- `ConfigurationError`: no ticket was supplied.
- `RequestValidationError`: incompatible or invalid filters.
- `AuthenticationError`: HTTP 401 or 403.
- `NotFoundError`: HTTP 404.
- `RateLimitError`: HTTP 429; exposes `retry_after`.
- `APIError`: any other API error.
- `RequestTimeoutError`: a configured timeout was exceeded.
- `NetworkError`: a connection or network protocol failed.
- `TransportError`: another HTTP transport failure.
- `ResponseValidationError`: invalid JSON or an unexpected contract.

## Reliability

Retries are opt-in. They cover connection failures and HTTP 429, 500, 502, 503,
and 504 responses. A 429 response is retried only when the server provides a
valid `Retry-After` value, which avoids repeatedly consuming a daily quota.

```python
from chile_public_market_sdk import (
    ClientConfig,
    RetryConfig,
    SyncChilePublicMarketSDK,
    TimeoutConfig,
)

config = ClientConfig(
    ticket="YOUR_TICKET",
    timeout=TimeoutConfig(connect=5, read=30, write=10, pool=5),
    retry=RetryConfig(max_attempts=3),
)

with SyncChilePublicMarketSDK(config=config) as sdk:
    tenders = sdk.get_tenders()
```

## Development

```bash
poetry install --extras "dev docs"
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry build
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before
submitting changes or reporting vulnerabilities.
