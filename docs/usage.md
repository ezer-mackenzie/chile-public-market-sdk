# Usage guide

## Authentication

The v1 API sends the ticket as a query parameter, while Agile Purchase v2
sends it in the `ticket` header. The SDK selects the correct mechanism.

The consumer application owns and supplies the secret:

```python
from chile_public_market_sdk import SyncChilePublicMarketSDK

sdk = SyncChilePublicMarketSDK(ticket=secret_manager.get("mercado-publico"))
```

A custom environment variable is also supported:

```python
from chile_public_market_sdk import ClientConfig, SyncChilePublicMarketSDK

sdk = SyncChilePublicMarketSDK(config=ClientConfig(ticket_env="MY_TICKET"))
```

Applications that use `envyaml` should load the ticket and pass it explicitly:

```python
from envyaml import EnvYAML

from chile_public_market_sdk import SyncChilePublicMarketSDK

config = EnvYAML("env.yaml")
sdk = SyncChilePublicMarketSDK(
    ticket=config["CHILE_PUBLIC_MARKET_TICKET"],
)
```

`envyaml` is not an SDK dependency. Secret-file loading and lifecycle remain
the consumer application's responsibility.

## Custom HTTP client

```python
import httpx

from chile_public_market_sdk import SyncChilePublicMarketSDK

http_client = httpx.Client(
    timeout=httpx.Timeout(20),
    transport=httpx.HTTPTransport(retries=2),
)
sdk = SyncChilePublicMarketSDK(ticket="...", http_client=http_client)
```

When an HTTP client is injected, its creator remains responsible for closing
it and its timeout configuration.

## Timeouts and retries

Use `TimeoutConfig` to set independent connect, read, write, and connection-pool
limits. Retries are disabled by default (`max_attempts=1`) and must be enabled
explicitly:

```python
from chile_public_market_sdk import (
    ClientConfig,
    RetryConfig,
    SyncChilePublicMarketSDK,
    TimeoutConfig,
)

config = ClientConfig(
    timeout=TimeoutConfig(connect=5, read=30, write=10, pool=5),
    retry=RetryConfig(max_attempts=3, backoff_factor=0.5, max_delay=20),
)
sdk = SyncChilePublicMarketSDK(config=config)
```

The policy retries network failures and HTTP 429, 500, 502, 503, and 504
responses with exponential backoff. HTTP 429 is retried only when a valid
`Retry-After` header is present. The delay is capped by `max_delay`.

## Safe observability

Request and response hooks receive immutable SDK events. Event URLs never
contain query parameters or credentials, so the v1 ticket cannot enter logs:

```python
from chile_public_market_sdk import ClientConfig, RequestEvent, ResponseEvent


def on_request(event: RequestEvent) -> None:
    print(event.method, event.url, event.attempt)


def on_response(event: ResponseEvent) -> None:
    print(event.status_code, event.elapsed_seconds)


config = ClientConfig(
    request_hooks=(on_request,),
    response_hooks=(on_response,),
)
```

Hooks are ordinary synchronous callbacks in both clients. Keep them short and
non-blocking.

## V1 filters

`get_tenders` and `get_purchase_orders` accept `code`, `date`, `status`,
`buyer_code`, and `supplier_code`. A lookup by code cannot be combined with
other filters because it represents the logical detail operation.

## Agile Purchase

`get_agile_purchases` enforces the official constraints:

- `last_change_ttl_ms` cannot be combined with `changed_from` or
  `changed_until`;
- `external_id` and `query` are mutually exclusive;
- `page_size` must be between 10 and 50;
- region codes must be between 1 and 16.

The Agile Purchase API cannot filter by buyer organization. Filter locally
using `item.institution.tax_id` or `item.institution.buyer_organization`.
