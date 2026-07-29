"""Asynchronous HTTPX transport adapter."""

import asyncio
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


class AsyncTransport:
    """Adapt `httpx.AsyncClient` to the asynchronous SDK transport contract."""

    def __init__(self, client: httpx.AsyncClient, config: ClientConfig) -> None:
        self.client = client
        self.config = config

    async def aclose(self) -> None:
        """Close the underlying HTTPX client."""

        await self.client.aclose()

    async def get(
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
                response = await self.client.get(url, params=params, headers=headers)
            except httpx.TimeoutException as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    await asyncio.sleep(delay)
                    continue
                raise RequestTimeoutError("The Mercado Público request timed out.") from exc
            except _NETWORK_ERRORS as exc:
                delay = RetryPolicy.delay(self.config, attempt, None)
                if delay is not None:
                    await asyncio.sleep(delay)
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
                await asyncio.sleep(delay)
                continue
            return TransportResponseDecoder.decode(response)
        raise AssertionError("Retry loop completed without a response.")  # pragma: no cover
