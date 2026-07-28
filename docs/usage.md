# Usage guide

## Authentication

The v1 API sends the ticket as a query parameter, while Agile Purchase v2
sends it in the `ticket` header. The SDK selects the correct mechanism.

The consumer application owns and supplies the secret:

```python
from chile_public_market_sdk import MercadoPublico

sdk = MercadoPublico(ticket=secret_manager.get("mercado-publico"))
```

A custom environment variable is also supported:

```python
from chile_public_market_sdk import ClientConfig, MercadoPublico

sdk = MercadoPublico(config=ClientConfig(ticket_env="MY_TICKET"))
```

## Custom HTTP client

```python
import httpx

from chile_public_market_sdk import MercadoPublico

http_client = httpx.Client(
    timeout=httpx.Timeout(20),
    transport=httpx.HTTPTransport(retries=2),
)
sdk = MercadoPublico(ticket="...", http_client=http_client)
```

When an HTTP client is injected, its creator remains responsible for closing
it.

## V1 filters

`get_tenders` and `get_purchase_orders` accept `code`, `date`, `status`,
`buyer_code`, and `supplier_code`. A lookup by code cannot be combined with
other filters because it represents the logical detail operation.

## Agile Purchase

`get_agile_purchases` enforces the official constraints:

- `last_change_ttl_ms` cannot be combined with `changed_from` or
  `changed_until`;
- `external_id` and `query` are mutually exclusive;
- `page_size` must be between 1 and 50;
- region codes must be between 1 and 16.

The Agile Purchase API cannot filter by buyer organization. Filter locally
using `item.institution.tax_id` or `item.institution.buyer_organization`.
