# Roadmap to v1.0.0

Version `0.2.0` establishes the English public API, architecture boundaries,
serialization policy, and public-surface regression tests. The following
milestones are required before declaring `v1.0.0` stable.

## Completed in v0.2.0

- English-only public classes, methods, parameters, attributes, and docs.
- Separate synchronous and asynchronous clients and facades.
- Versioned upstream API contracts under `api/v{version}.py`.
- English model serialization with Spanish wire-key normalization.
- Public API inventory and signature snapshot tests.
- One canonical editable version source in `pyproject.toml`.

## Completed in v0.3.0

- Real-service validation for all six endpoint contracts.
- Anonymized fixtures with documented provenance.
- Typed detailed tender and purchase-order domain sections.
- Offline contract regression tests.
- Optional weekly live-contract CI using a protected secret.
- Consumer-owned secret loading with no configuration-file runtime dependency.

## Completed in v0.4.0

- Granular connect, read, write, and pool timeout configuration.
- Opt-in retries for transient network and server failures.
- `Retry-After` support without blind daily-quota retries.
- Sanitized request and response observability hooks.
- Deterministic timeout and network exception types.
- Sync and async resilience regression tests.

## Completed in v0.7.0

- Direct HTTPX integration without transport wrappers.
- Canonical `clients/` and shared `core/` package boundaries.
- Ruff, strict mypy, and Pyright static-analysis gates.
- Expanded sync/async, parser, parameter, network, and error coverage.
- More than 90% total offline test coverage.

## Completed in v0.8.0

- CI matrix for Python 3.12, 3.13, and 3.14.
- Offline tests on Linux, macOS, and Windows.
- Ruff, strict mypy, Pyright, MkDocs, and coverage gates.
- One canonical distribution build per workflow.
- Clean wheel-install smoke tests across the complete platform matrix.
- Isolated weekly live-contract validation with a protected ticket.

## Release-candidate compatibility

- Maintain a fixture matrix for historical v1 payload shapes.
- Freeze supported public import paths and signatures.

## Distribution

- Confirm the distribution name on PyPI.
- Configure Trusted Publishing.
- Add a changelog and signed or provenance-attested releases.
- Publish versioned documentation.

## Quality and governance

- Reach at least 90% coverage, especially in the async client.
- Review and freeze all public names and docstrings.
- Publish support and deprecation policies.
- Complete license, attribution, and security reviews.

The detailed engineering roadmap and release gates are maintained outside the
repository at `/tmp/chile-public-market-sdk-v1-roadmap.md` during this planning
cycle.
