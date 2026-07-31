# Roadmap to v1.0.0

The repository-side stability gates for `v1.0.0` are complete.

## Stable product contract

- Every documented public Mercado Público endpoint has equivalent synchronous
  and asynchronous client methods.
- HTTPX is used directly, with injectable sync and async clients.
- Pydantic validates known fields, normalizes upstream wire keys to English,
  and preserves compatible upstream additions.
- SDK facades construct and own their corresponding clients.
- Consumers supply tickets directly or through their own secret-loading
  mechanism.

## Compatibility gates

- Top-level exports, model exports, constructors, and resource method
  signatures have regression snapshots.
- Historical v1 and current v2 payload fixtures are validated offline.
- The public compatibility, support, deprecation, migration, and security
  policies are documented.
- Removing a documented public contract after `1.0.0` requires a new major
  release.

## Quality gates

- Python 3.12, 3.13, and 3.14 are covered by the CI matrix on Linux, macOS,
  and Windows.
- Ruff, strict mypy, Pyright, MkDocs strict mode, wheel builds, and clean wheel
  installation are required in CI.
- Offline coverage exceeds 95%; each sync and async client exceeds 85%.
- Protected live tests cover all endpoint families without committing raw
  responses or tickets.

## Distribution gates

- `CHANGELOG.md` records the stable release.
- The publish workflow builds wheel and sdist artifacts when a GitHub Release is
  published or the workflow is started manually, then uploads them through PyPI
  Trusted Publishing.
- The repository owner must configure the `pypi` GitHub environment and the
  matching PyPI Trusted Publisher before pushing the stable tag.
- Versioned documentation hosting remains a repository-owner deployment task.

## Definition of stable

After `v1.0.0`, removals or renames of documented methods, parameters, model
fields, enums, exceptions, imports, or serialized English field names require
a new major version. Compatible additions ship in minor releases and compatible
fixes ship in patch releases.
