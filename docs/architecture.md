# Architecture and compatibility

The SDK separates five responsibilities:

1. `ClientConfig` resolves configuration and the ticket.
2. The clients call `httpx` directly and normalize request errors.
3. Parsers decode and validate responses.
4. Pydantic models represent the public contracts.
5. Sync and async clients expose the domain API.

Stateless transformations are grouped in focused classes:

- `ParameterEncoder` owns upstream query-value formatting.
- `ResponseParser` owns JSON decoding and Pydantic validation.
These classes use static methods for isolated transformations and class methods
where one operation composes other behavior from the same class. Existing
module-level parameter and parser helpers delegate to them for compatibility.

## Package layout

- `clients/` contains the synchronous and asynchronous clients.
- `core/` contains shared enums and type aliases without runtime behavior.
- `config/` contains the client configuration.
- `sdk/` contains the two high-level facades.
- `models/` and `api/` retain domain contracts and upstream API versions.

Models deliberately use `extra="allow"`. Mercado Público operates legacy
services, and the Agile Purchase guide documents differences between earlier
schemas and real responses. This policy validates known fields without
breaking consumers when ChileCompra adds data.

`ChilePublicMarketModel` owns recursive payload normalization through
`normalize_payload`. The immutable upstream-to-English key table lives
separately in `core/constants/wire_keys.py`, keeping protocol data out of base-model
behavior. Shape-specific validators reuse the base-model interface rather than
importing private normalization functions.

The Python API is English-only. Spanish names remain internally where required
by upstream endpoint paths, query parameters, enum values, and JSON keys.

Synchronous and asynchronous usage is explicit at both layers:

- `SyncChilePublicMarketClient` and `AsyncChilePublicMarketClient` provide the
  HTTP client API.
- `SyncChilePublicMarketSDK` and `AsyncChilePublicMarketSDK` construct and own
  their respective client through the public `client` attribute.

SDK facades use composition rather than inheriting from clients. Their context
managers return the managed client, and their close methods delegate lifecycle
management only. Endpoint methods remain defined exclusively on clients.

Upstream endpoint contracts are isolated in `api/v1.py` and `api/v2.py`.

There is no SDK transport abstraction. Synchronous clients call `httpx.Client`
directly and asynchronous clients call `httpx.AsyncClient` directly. HTTPX owns
connection pooling, timeout enforcement, custom transports, and instrumentation.
The SDK only converts HTTPX failures and Mercado Público error responses into
its public exception hierarchy.
