# Architecture and compatibility

The SDK separates five responsibilities:

1. `ClientConfig` resolves configuration and the ticket.
2. The transport wraps `httpx` and normalizes HTTP errors.
3. Parsers decode and validate responses.
4. Pydantic models represent the public contracts.
5. Sync and async clients expose the domain API.

Models deliberately use `extra="allow"`. Mercado Público operates legacy
services, and the Agile Purchase guide documents differences between earlier
schemas and real responses. This policy validates known fields without
breaking consumers when ChileCompra adds data.

The Python API is English-only. Spanish names remain internally where required
by upstream endpoint paths, query parameters, enum values, and JSON keys.
