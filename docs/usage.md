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

## SDK and client responsibilities

The SDK constructs and manages a client. Access it through `sdk.client` when
the SDK is not used as a context manager:

```python
sdk = SyncChilePublicMarketSDK(ticket="...")
try:
    tenders = sdk.client.get_tenders()
finally:
    sdk.close()
```

Context managers return the managed client directly:

```python
with SyncChilePublicMarketSDK(ticket="...") as client:
    tenders = client.get_tenders()
```

Endpoint methods belong to client classes; SDK classes only own construction
and lifecycle.

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

## Timeouts

Use the native `httpx.Timeout` type to set independent connect, read, write,
and connection-pool limits:

```python
import httpx

from chile_public_market_sdk import ClientConfig, SyncChilePublicMarketSDK

config = ClientConfig(
    timeout=httpx.Timeout(connect=5, read=30, write=10, pool=5),
)
sdk = SyncChilePublicMarketSDK(config=config)
```

For retries, custom transports, or HTTP instrumentation, inject a configured
`httpx.Client` or `httpx.AsyncClient`. The SDK uses that instance directly and
does not replace its behavior.

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
