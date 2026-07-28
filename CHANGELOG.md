# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
