# Chile Public Market SDK

A synchronous and asynchronous Python client for every documented public
Mercado Público endpoint.

## Quick start

```python
from chile_public_market_sdk import SyncChilePublicMarketSDK

with SyncChilePublicMarketSDK(ticket="YOUR_TICKET") as sdk:
    response = sdk.get_tenders(code="1509-5-L114")
    print(response.items[0].name)
```

The ticket may be omitted when `CHILE_PUBLIC_MARKET_TICKET` is defined.

## Reference

- [Usage guide](usage.md)
- [API reference](api.md)
- [Public API inventory](public-api.md)
- [Architecture and compatibility](architecture.md)
- [Migrating from the initial API](migration.md)
- [Versioning policy](versioning.md)
- [Roadmap to v1.0.0](v1-roadmap.md)
