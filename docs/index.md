# Chile Public Market SDK

A synchronous and asynchronous Python client for every documented public
Mercado Público endpoint.

## Quick start

```python
from chile_public_market_sdk import SyncChilePublicMarketSDK

with SyncChilePublicMarketSDK(ticket="YOUR_TICKET") as client:
    response = client.get_buyers()
    print(f"Companies found: {len(response.companies)}")
```

The ticket may be omitted when `CHILE_PUBLIC_MARKET_TICKET` is defined.

## Reference

- [Usage guide](usage.md)
- [API reference](api.md)
- [Public API inventory](public-api.md)
- [Contract validation](contracts.md)
- [Architecture and compatibility](architecture.md)
- [Migrating from the initial API](migration.md)
- [Versioning policy](versioning.md)
- [Roadmap to v1.0.0](v1-roadmap.md)
