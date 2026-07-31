# Chile Public Market SDK

[![codecov](https://codecov.io/gh/ezer-mackenzie/chile-public-market-sdk/graph/badge.svg)](https://codecov.io/gh/ezer-mackenzie/chile-public-market-sdk)

Unofficial, typed, synchronous and asynchronous Python SDK for Chile's
[Mercado Público APIs](https://www.chilecompra.cl/api/).

> [!WARNING]
> This is an unofficial, community-driven initiative. It is not developed,
> endorsed, or supported by ChileCompra or Mercado Público. Consumers remain
> responsible for validating its behavior against the official API contracts.

> Status: stable (`1.0.0`). The upstream services include legacy contracts and
> may add fields. Models validate known fields while preserving new ones.

## Requirements

- Python 3.12 or newer.
- An access ticket requested through ChileCompra.

## Installation

```bash
pip install chile-public-market-sdk
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
from chile_public_market_sdk import SyncChilePublicMarketSDK

ticket = "YOUR_TICKET"

with SyncChilePublicMarketSDK(ticket=ticket) as client:
    response = client.get_buyers()

    print(f"Companies found: {len(response.companies)}")
    for company in response.companies[:5]:
        print(company.company_code, company.company_name)
```

## Asynchronous usage

```python
import asyncio

from chile_public_market_sdk import AsyncChilePublicMarketSDK


async def main() -> None:
    ticket = "YOUR_TICKET"

    async with AsyncChilePublicMarketSDK(ticket=ticket) as client:
        response = await client.get_buyers()

        print(f"Companies found: {len(response.companies)}")
        for company in response.companies[:5]:
            print(company.company_code, company.company_name)


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

SDK classes construct and own a client through `sdk.client`. Their context
managers return that managed client, while endpoint methods remain on client
classes.

ChileCompra endpoint constants are grouped by upstream version in
`chile_public_market_sdk.core.constants.api`. Dynamic version-specific path
builders live under `chile_public_market_sdk.api`. SDK releases follow
Semantic Versioning independently from ChileCompra's upstream versions.

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

The SDK uses HTTPX directly. Pass a native `httpx.Timeout` for granular limits:

```python
import httpx

from chile_public_market_sdk import ClientConfig, SyncChilePublicMarketSDK

config = ClientConfig(
    ticket="YOUR_TICKET",
    timeout=httpx.Timeout(connect=5, read=30, write=10, pool=5),
)

with SyncChilePublicMarketSDK(config=config) as client:
    tenders = client.get_tenders()
```

Applications that need retries can inject an HTTPX client configured for their
own policy. The SDK does not hide HTTPX behind another transport abstraction.

## Development

```bash
poetry install --extras "dev docs"
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry run pyright
poetry build
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before
submitting changes or reporting vulnerabilities.
