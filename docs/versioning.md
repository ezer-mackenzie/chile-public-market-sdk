# Versioning policy

The project uses Semantic Versioning for SDK releases and explicit `v{version}`
modules for upstream ChileCompra contracts. These are separate version axes.

## SDK versions

- `0.x.y`: the SDK is pre-stable. Public names may still change, and every
  breaking change must be documented in the migration guide.
- `1.0.0`: the first stable SDK contract. From this release onward, breaking
  public API changes require a new major SDK version.
- Patch releases fix compatible defects.
- Minor releases add backward-compatible functionality.

The package exposes its current release through
`chile_public_market_sdk.__version__`.

## Upstream API versions

ChileCompra currently exposes different resources through upstream API v1 and
v2. Their paths and base URLs live in explicit modules:

```text
chile_public_market_sdk/api/v1.py
chile_public_market_sdk/api/v2.py
```

New upstream contracts must be added as `api/v{version}.py`. Client methods
must import paths and base URLs from those modules instead of embedding
versioned URLs directly.

An upstream v2 endpoint does not imply SDK version 2.0.0. Likewise, SDK
version 1.0.0 may support multiple ChileCompra API versions.
