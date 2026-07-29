"""Synchronous HTTPX transport adapter."""

import time
from collections.abc import Mapping
from typing import Any

import httpx

from ..config import ClientConfig
from ..errors import NetworkError, RequestTimeoutError, TransportError
from .events import TransportEventFactory
from .protocols import Params
from .response import TransportResponseDecoder
from .retry import RetryPolicy

_NETWORK_ERRORS = (httpx.NetworkError, httpx.ProtocolError, httpx.ProxyError)


class SyncTransport:
    """Adapt `httpx.Client` to the synchronous SDK transport contract."""

    def __init__(self, client: httpx.Client, config: ClientConfig) -> None:
        self.client = client
        self.config = config

    def close(self) -> None:
        """Close the underlying HTTPX client."""

        self.client.close()

    def get(
        self,
        url: str,
        *,
        params: Params | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        for attempt in range(1, self.config.retry.max_attempts + 1):
            event = TransportEventFactory.request(url, attempt)
            for request_hook in self.config.request_hooks:
                request_hook(event)
            started = time.monotonic()
            try:
                response = self.client.get(url, params=params, headers=headers)
            except httpx.TimeoutException as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    time.sleep(delay)
                    continue
                raise RequestTimeoutError("The Mercado Público request timed out.") from exc
            except _NETWORK_ERRORS as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    time.sleep(delay)
                    continue
                raise NetworkError("Could not communicate with Mercado Público.") from exc
            except httpx.HTTPError as exc:
                raise TransportError("Could not communicate with Mercado Público.") from exc
            response_event = TransportEventFactory.response(
                url, attempt, response, time.monotonic() - started
            )
            for response_hook in self.config.response_hooks:
                response_hook(response_event)
            delay = RetryPolicy.delay(self.config, attempt, response)
            if delay is not None:
                time.sleep(delay)
                continue
            return TransportResponseDecoder.decode(response)
        raise AssertionError("Retry loop completed without a response.")  # pragma: no cover
