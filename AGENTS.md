# Repository guidance for coding agents

## Project scope

This repository contains the unofficial Chile Public Market SDK, a typed
Python 3.12+ library for ChileCompra's public Mercado Público APIs. The package
supports synchronous and asynchronous usage through HTTPX and validates
responses with Pydantic.

All source code, identifiers, docstrings, tests, commit messages, and
repository documentation must be written in English.

## Package structure

- `src/chile_public_market_sdk/clients/` contains the canonical synchronous and
  asynchronous HTTP clients.
- `src/chile_public_market_sdk/sdk/` contains the client-owning SDK facades.
- `src/chile_public_market_sdk/config/` contains public client configuration.
- `src/chile_public_market_sdk/core/` contains shared enums, types, and
  internal constants.
- `src/chile_public_market_sdk/models/` contains Pydantic response models.
- `src/chile_public_market_sdk/api/` contains dynamic upstream path helpers.
- `tests/fixtures/contracts/` contains anonymized contract fixtures.
- `docs/` contains the English user and architecture documentation.
- `tmp/` may contain local planning notes and must not be committed.

## Architecture rules

- Use `httpx.Client` and `httpx.AsyncClient` directly. Do not introduce a
  transport abstraction, HTTP wrapper, or compatibility shim.
- Keep synchronous and asynchronous clients as explicit separate classes with
  equivalent public endpoint methods.
- SDK classes construct, own, and close their corresponding client. Endpoint
  behavior belongs to client classes.
- Use `ResponseParser` directly for response decoding, validation, and API
  error normalization.
- Use `ParameterEncoder` directly for wire-format query values. Do not create
  module-level aliases for its methods.
- Put shared immutable values in `core/constants/` and import their concrete
  modules directly. Do not add convenience reexports for internal constants.
- Put shared enums and type aliases in `core/`.
- Keep classes focused and avoid placing unrelated classes in one module.
- Prefer a private static or class method when behavior belongs to an existing
  class. Avoid abstractions that only rename a library call.
- Preserve unknown upstream response fields through the base Pydantic model.
- Keep the public Python API and serialized model field names in English while
  retaining Spanish names only at the upstream wire boundary.

## Public compatibility

The `1.x` API is stable. Treat documented imports, constructors, methods,
parameters, model exports, exceptions, enums, and serialized English field
names as compatibility commitments.

- Compatible additions belong in a minor release.
- Compatible fixes belong in a patch release.
- Breaking public changes require a new major release.
- Document deprecations and emit `DeprecationWarning` for at least one minor
  release before removal in the next major release.

Update public API snapshot tests whenever an intentional compatible addition is
made. Never weaken a snapshot merely to make an accidental breaking change
pass.

## Secrets and live services

- Never commit or print a real Mercado Público ticket.
- Keep `.env`, `env.yaml`, raw production responses, coverage output, build
  output, and local editor configuration out of commits.
- The SDK must not depend on `envyaml`, `python-dotenv`, or another secret-file
  loader. Consumers pass a ticket directly or load it with their own tooling.
- Live contract tests are opt-in and read-only. Run them only when explicitly
  authorized and when `CHILE_PUBLIC_MARKET_TICKET` is supplied securely.
- Anonymize production-derived fixtures before committing them.

## Required validation

Install development and documentation dependencies with:

```bash
poetry install --extras "dev docs"
```

Before committing, run the checks relevant to the change. Before a release,
run the complete gate:

```bash
poetry run ruff format --check src tests
poetry run ruff check .
poetry run mypy
poetry run pyright
poetry run pytest -m "not live" \
  --cov=chile_public_market_sdk \
  --cov-report=xml \
  --cov-fail-under=95
poetry run mkdocs build --strict
poetry build
```

Maintain at least 95% total offline coverage and at least 85% coverage in each
client module. Add sync and async tests for endpoint behavior when applicable.

## Documentation

- Keep documentation in English.
- Use the installed import path `chile_public_market_sdk`, never
  `src.chile_public_market_sdk`.
- Use placeholders such as `YOUR_TICKET`; never include working credentials.
- Clearly state that the project is unofficial and is not endorsed or
  supported by ChileCompra or Mercado Público.
- Update `README.md`, MkDocs pages, public API inventory, migration guidance,
  support policy, roadmap, and changelog when their contracts are affected.

## Commits and releases

- Preserve unrelated user changes in a dirty worktree.
- Do not commit `.env`, `env.yaml`, `tmp/`, `dist/`, `site/`, coverage files,
  or editor settings.
- Group changes by feature or module and use Conventional Commit messages such
  as `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `ci:`, and `chore:`.
- Keep release metadata changes in a final `chore: release version X.Y.Z`
  commit.
- Keep `pyproject.toml` and `CHANGELOG.md` synchronized for releases.
- Create an annotated `vX.Y.Z` tag only after the exact release commit passes
  all quality, contract, documentation, build, and wheel smoke checks.
- Never rewrite or move an existing release tag.
