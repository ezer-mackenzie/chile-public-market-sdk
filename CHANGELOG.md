# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.4.0] - 2026-07-29

### Added

- Added granular connect, read, write, and pool timeout configuration.
- Added opt-in retries for transient network failures and retryable HTTP
  statuses.
- Added safe request and response observability events with credential-free
  URLs.
- Added deterministic `RequestTimeoutError` and `NetworkError` exceptions.
- Added sync and async resilience regression tests.

### Security

- Redacted the ticket from `ClientConfig` representations and observability
  events.
- Required a valid `Retry-After` header before retrying HTTP 429 responses.

## [0.3.1] - 2026-07-29

### Changed

- Removed `envyaml` from runtime dependencies and SDK configuration.
- Limited built-in ticket resolution to an explicit `ticket` or the configured
  environment variable.
- Documented consumer-side `envyaml` usage without coupling the SDK to it.

## [0.3.0] - 2026-07-28

### Added

- Added `envyaml` support for loading a ticket from `env.yaml`.
- Added anonymized production contract fixtures for every endpoint family.
- Added offline contract regression tests and optional scheduled live tests.
- Added typed tender dates, awards, buyer details, and line-item contracts.
- Added typed purchase-order dates, financial data, buyer, supplier, and items.

### Fixed

- Enforced the real Agile Purchase page-size range of 10 to 50.
- Allowed Agile Purchase details without a purchase-order object.

## [0.2.0] - 2026-07-28

### Changed

- Renamed public classes to explicit English sync and async names.
- Separated synchronous and asynchronous clients into dedicated modules.
- Moved upstream endpoint contracts into versioned `api/v1.py` and `api/v2.py`
  modules.
- Renamed the default ticket variable to `CHILE_PUBLIC_MARKET_TICKET`.
- Added an explicit SDK and upstream API versioning policy.
- Defined English field names as the model serialization format.

### Added

- Added an explicit public API inventory.
- Added regression snapshots for top-level exports and sync/async signatures.
- Added versioned upstream contract modules for ChileCompra API v1 and v2.

## [0.1.0] - 2026-07-28

### Added

- Initial typed synchronous and asynchronous clients.
- Coverage for tenders, purchase orders, suppliers, buyers, and Agile Purchase.
- Pydantic response models, normalized errors, tests, and documentation.
