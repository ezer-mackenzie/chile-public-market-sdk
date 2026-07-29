"""Configuration shared by synchronous and asynchronous clients."""

from __future__ import annotations

import os
from dataclasses import dataclass

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
    base_url_v1: str = V1_BASE_URL
    base_url_v2: str = V2_BASE_URL
    timeout: float = 30.0

    def resolved_ticket(self) -> str:
        value = self.ticket or os.getenv(self.ticket_env)
        if not value or not value.strip():
            raise ConfigurationError(
                f"Provide ticket=... or define the {self.ticket_env} environment variable."
            )
        return value.strip()
