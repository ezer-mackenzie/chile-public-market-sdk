# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Renamed public classes to explicit English sync and async names.
- Separated synchronous and asynchronous clients into dedicated modules.
- Moved upstream endpoint contracts into versioned `api/v1.py` and `api/v2.py`
  modules.
- Renamed the default ticket variable to `CHILE_PUBLIC_MARKET_TICKET`.
- Added an explicit SDK and upstream API versioning policy.

## [0.1.0] - Unreleased

### Added

- Initial typed synchronous and asynchronous clients.
- Coverage for tenders, purchase orders, suppliers, buyers, and Agile Purchase.
- Pydantic response models, normalized errors, tests, and documentation.
