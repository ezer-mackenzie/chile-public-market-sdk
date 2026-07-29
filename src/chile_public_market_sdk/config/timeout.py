"""HTTP timeout configuration."""

from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class TimeoutConfig:
    """Timeout limits, in seconds, for each network operation."""

    connect: float = 30.0
    read: float = 30.0
    write: float = 30.0
    pool: float = 30.0

    def to_httpx(self) -> httpx.Timeout:
        """Build the equivalent HTTPX timeout configuration."""

        return httpx.Timeout(
            connect=self.connect,
            read=self.read,
            write=self.write,
            pool=self.pool,
        )


type TimeoutValue = float | TimeoutConfig
