"""Client configuration shared by synchronous and asynchronous clients."""

import os
from dataclasses import dataclass, field

import httpx

from ..api import V1_BASE_URL, V2_BASE_URL
from ..errors import ConfigurationError

DEFAULT_TICKET_ENV = "CHILE_PUBLIC_MARKET_TICKET"
type TimeoutValue = float | httpx.Timeout


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Immutable SDK configuration."""

    ticket: str | None = field(default=None, repr=False)
    ticket_env: str = DEFAULT_TICKET_ENV
    base_url_v1: str = V1_BASE_URL
    base_url_v2: str = V2_BASE_URL
    timeout: TimeoutValue = 30.0

    def resolved_ticket(self) -> str:
        """Resolve an explicit ticket before consulting the environment."""

        value = self.ticket or os.getenv(self.ticket_env)
        if not value or not value.strip():
            raise ConfigurationError(
                f"Provide ticket=... or define the {self.ticket_env} environment variable."
            )
        return value.strip()
