"""Configuration shared by synchronous and asynchronous clients."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .errors import ConfigurationError

DEFAULT_V1_URL = "https://api.mercadopublico.cl/servicios/v1/publico"
DEFAULT_V2_URL = "https://api2.mercadopublico.cl/v2"
DEFAULT_TICKET_ENV = "MERCADO_PUBLICO_TICKET"


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Immutable SDK configuration.

    An explicit ticket takes precedence over the configured environment variable.
    """

    ticket: str | None = None
    ticket_env: str = DEFAULT_TICKET_ENV
    base_url_v1: str = DEFAULT_V1_URL
    base_url_v2: str = DEFAULT_V2_URL
    timeout: float = 30.0

    def resolved_ticket(self) -> str:
        value = self.ticket or os.getenv(self.ticket_env)
        if not value or not value.strip():
            raise ConfigurationError(
                f"Provide ticket=... or define the {self.ticket_env} environment variable."
            )
        return value.strip()
