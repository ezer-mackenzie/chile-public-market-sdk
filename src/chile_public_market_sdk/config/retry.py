"""Retry policy configuration."""

from dataclasses import dataclass

from ..errors import ConfigurationError


@dataclass(frozen=True, slots=True)
class RetryConfig:
    """Opt-in retry policy for transient failures."""

    max_attempts: int = 1
    backoff_factor: float = 0.5
    max_delay: float = 30.0
    retry_statuses: frozenset[int] = frozenset({429, 500, 502, 503, 504})

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ConfigurationError("max_attempts must be greater than or equal to 1.")
        if self.backoff_factor < 0 or self.max_delay < 0:
            raise ConfigurationError("Retry delays cannot be negative.")
