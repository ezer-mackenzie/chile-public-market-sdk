# Contributing

Thank you for helping improve the Chile Public Market SDK.

## Development setup

```bash
poetry install --extras "dev docs"
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry run mkdocs build --strict
poetry build
```

## Project rules

- Use English for code, public names, docstrings, tests, commit messages, and
  documentation.
- Keep Spanish only when it is part of ChileCompra's wire protocol.
- Never commit a real API ticket or an unredacted production payload.
- Add tests for every behavior change.
- Use Conventional Commits such as `feat:`, `fix:`, `test:`, `docs:`, and
  `chore:`.

## Pull requests

Keep changes focused and explain any public API or contract implications.
Update the documentation and roadmap when behavior or release requirements
change.
