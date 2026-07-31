"""Client configuration shared by synchronous and asynchronous clients."""

import os
from dataclasses import dataclass, field

from ..core.constants.api import V1_BASE_URL, V2_BASE_URL
from ..core.constants.config import DEFAULT_TICKET_ENV
from ..core.types import TimeoutValue
from ..errors import ConfigurationError


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
