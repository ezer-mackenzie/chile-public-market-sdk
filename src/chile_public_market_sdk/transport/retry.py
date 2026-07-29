"""Retry delay calculation."""

from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import httpx

from ..config import ClientConfig


class RetryPolicy:
    """Calculate bounded retry delays from SDK configuration and responses."""

    @staticmethod
    def retry_after(response: httpx.Response, *, max_delay: float) -> float | None:
        value = response.headers.get("Retry-After")
        if value is None:
            return None
        try:
            delay = float(str(value))
        except ValueError:
            try:
                target = parsedate_to_datetime(value)
                if target.tzinfo is None:
                    target = target.replace(tzinfo=UTC)
                delay = (target - datetime.now(UTC)).total_seconds()
            except (TypeError, ValueError, OverflowError):
                return None
        return min(max(delay, 0.0), max_delay)

    @classmethod
    def delay(
        cls,
        config: ClientConfig,
        attempt: int,
        response: httpx.Response | None,
    ) -> float | None:
        if attempt >= config.retry.max_attempts:
            return None
        if response is not None:
            if response.status_code not in config.retry.retry_statuses:
                return None
            if response.status_code == 429:
                return cls.retry_after(response, max_delay=config.retry.max_delay)
        exponential_delay = config.retry.backoff_factor * float(2 ** (attempt - 1))
        return min(exponential_delay, config.retry.max_delay)
