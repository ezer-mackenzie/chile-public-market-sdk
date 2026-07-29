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

## Contract completeness

- Validate anonymized real-service fixtures for every endpoint.
- Fully type detailed tender and purchase-order payloads.
- Run periodic contract tests without exposing the ticket.
- Document what constitutes a breaking change.

## Reliability

- Define an opt-in retry policy for HTTP 429, 500, and 503.
- Expose observability hooks that always redact the ticket.
- Test timeouts, disconnects, malformed JSON, and upstream schema drift.

## Compatibility

- Run CI on Python 3.12, 3.13, and 3.14.
- Test wheels on Linux, macOS, and Windows.
- Maintain a fixture matrix for historical v1 payload shapes.

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
