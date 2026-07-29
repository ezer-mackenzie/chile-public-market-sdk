# Architecture and compatibility

The SDK separates five responsibilities:

1. `ClientConfig` resolves configuration and the ticket.
2. The transport wraps `httpx`, applies retry policy, emits sanitized events,
   and normalizes HTTP errors.
3. Parsers decode and validate responses.
4. Pydantic models represent the public contracts.
5. Sync and async clients expose the domain API.

Stateless transformations are grouped in focused classes:

- `ParameterEncoder` owns upstream query-value formatting.
- `ResponseParser` owns JSON decoding and Pydantic validation.
- `RetryPolicy` owns retry eligibility and delay calculation.
- `TransportEventFactory` creates credential-free observability events.
- `TransportResponseDecoder` maps HTTP payloads to values or SDK exceptions.

These classes use static methods for isolated transformations and class methods
where one operation composes other behavior from the same class. Existing
module-level parameter and parser helpers delegate to them for compatibility.

## Package layout

- `clients/` contains the canonical synchronous and asynchronous clients.
- `config/` separates client, timeout, retry, and event configuration.
- `sdk/` contains the two high-level facades.
- `transport/` separates HTTPX adapters, protocols, retry calculation,
  response decoding, and safe event construction.
- `models/` and `api/` retain domain contracts and upstream API versions.

The old `sync_client` and `async_client` modules are compatibility shims. New
internal code imports clients from `clients.sync` or `clients.async_`.

`SyncTransportProtocol` and `AsyncTransportProtocol` are structural interfaces.
The clients depend only on their respective `get` and close operations, so the
sync/async distinction is checked statically without coupling clients to a
specific transport implementation.

Models deliberately use `extra="allow"`. Mercado Público operates legacy
services, and the Agile Purchase guide documents differences between earlier
schemas and real responses. This policy validates known fields without
breaking consumers when ChileCompra adds data.

The Python API is English-only. Spanish names remain internally where required
by upstream endpoint paths, query parameters, enum values, and JSON keys.

Synchronous and asynchronous usage is explicit at both layers:

- `SyncChilePublicMarketClient` and `AsyncChilePublicMarketClient` provide the
  HTTP client API.
- `SyncChilePublicMarketSDK` and `AsyncChilePublicMarketSDK` provide the
  high-level facades.

Upstream endpoint contracts are isolated in `api/v1.py` and `api/v2.py`.

HTTPX clients own connection pooling and timeout enforcement. SDK observability
hooks intentionally receive reduced immutable events instead of raw HTTPX
requests because v1 authentication is carried in the query string.

The transport adapters do not reproduce HTTPX networking. They call
`httpx.Client` or `httpx.AsyncClient`, then apply SDK-specific retry,
observability, response validation, and exception semantics around the result.
