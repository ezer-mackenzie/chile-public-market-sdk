# Public API inventory

This page defines the stable public Python surface for the `1.x` line. Anything
not listed here is internal until explicitly promoted.

## Top-level classes

Import these names from `chile_public_market_sdk`:

| Name | Purpose |
|---|---|
| `SyncChilePublicMarketClient` | Low-level synchronous HTTP client |
| `AsyncChilePublicMarketClient` | Low-level asynchronous HTTP client |
| `SyncChilePublicMarketSDK` | Constructs and owns a synchronous client |
| `AsyncChilePublicMarketSDK` | Constructs and owns an asynchronous client |
| `ClientConfig` | Immutable client configuration |

## Resource methods

Both clients expose equivalent resource operations:

- `get_tenders`
- `get_purchase_orders`
- `find_supplier`
- `get_buyers`
- `get_agile_purchases`
- `get_agile_purchase`

Only lifecycle syntax differs: synchronous clients use `with` and `close()`;
asynchronous clients use `async with` and `aclose()`.

## Exceptions

- `ChilePublicMarketError`
- `ConfigurationError`
- `RequestValidationError`
- `TransportError`
- `RequestTimeoutError`
- `NetworkError`
- `ResponseValidationError`
- `APIError`
- `AuthenticationError`
- `NotFoundError`
- `RateLimitError`

## Models

The stable model exports currently include:

- `Tender` and `TenderResponse`
- `PurchaseOrder` and `PurchaseOrderResponse`
- `Company` and `CompanyResponse`
- `AgilePurchaseSummary`, `AgilePurchasePage`, and `AgilePurchaseDetail`
- `AgileError` and `AgileEnvelope`

Models accept upstream Spanish keys but always expose and serialize their
declared fields in English. Additional upstream fields are preserved because
models use `extra="allow"`.

## Version

`chile_public_market_sdk.__version__` is read from installed package metadata.
`pyproject.toml` is the single version source used to build that metadata.

Changes to this inventory follow the [support and deprecation
policy](support.md).
