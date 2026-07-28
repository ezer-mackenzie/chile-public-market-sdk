# Contract validation

Version 0.3.0 validates every endpoint family against the official production
services. Raw responses never enter the repository.

## Fixture policy

Committed fixtures preserve payload structure, types, enum values, dates,
numeric values, and nullability. Names, tax IDs, organization codes,
addresses, contacts, descriptions, and URLs are replaced with synthetic
values.

See `tests/fixtures/contracts/README.md` for endpoint-level provenance.

## Offline tests

```bash
poetry run pytest tests/test_contract_fixtures.py
```

These tests are deterministic and do not require a ticket.

## Live tests

Live tests are opt-in and consume the configured ticket:

```bash
CHILE_PUBLIC_MARKET_TICKET="..." \
RUN_LIVE_CONTRACT_TESTS=1 \
poetry run pytest -m live
```

GitHub Actions runs them weekly when the repository secret
`CHILE_PUBLIC_MARKET_TICKET` is configured.
