"""Configuration shared by synchronous and asynchronous clients."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from envyaml import EnvYAML  # type: ignore[import-untyped]

from .api import V1_BASE_URL, V2_BASE_URL
from .errors import ConfigurationError

DEFAULT_TICKET_ENV = "CHILE_PUBLIC_MARKET_TICKET"


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Immutable SDK configuration.

    An explicit ticket takes precedence over the configured environment variable.
    """

    ticket: str | None = None
    ticket_env: str = DEFAULT_TICKET_ENV
    env_yaml_path: str | Path | None = "env.yaml"
    base_url_v1: str = V1_BASE_URL
    base_url_v2: str = V2_BASE_URL
    timeout: float = 30.0

    def resolved_ticket(self) -> str:
        value = self.ticket or os.getenv(self.ticket_env) or self._yaml_ticket()
        if not value or not value.strip():
            raise ConfigurationError(
                f"Provide ticket=..., define {self.ticket_env}, or configure env_yaml_path."
            )
        return value.strip()

    def _yaml_ticket(self) -> str | None:
        if self.env_yaml_path is None:
            return None
        path = Path(self.env_yaml_path)
        if not path.is_file():
            return None
        config = EnvYAML(str(path), strict=False)
        value = config.get(self.ticket_env)
        return value if isinstance(value, str) else None
