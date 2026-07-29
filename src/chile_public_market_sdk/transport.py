"""Synchronous and asynchronous HTTP transport."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from .config import ClientConfig, RequestEvent, ResponseEvent
from .errors import (
    APIError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    RequestTimeoutError,
    TransportError,
)
from .parsers import ResponseParser

Params = Mapping[str, str | int | float]
_NETWORK_ERRORS = (httpx.NetworkError, httpx.ProtocolError, httpx.ProxyError)


class TransportEventFactory:
    """Create credential-free transport observability events."""

    @staticmethod
    def safe_url(url: str) -> str:
        parsed = httpx.URL(url)
        return str(parsed.copy_with(query=None, username=None, password=None))

    @classmethod
    def request(cls, url: str, attempt: int) -> RequestEvent:
        return RequestEvent(method="GET", url=cls.safe_url(url), attempt=attempt)

    @classmethod
    def response(
        cls,
        url: str,
        attempt: int,
        response: httpx.Response,
        elapsed_seconds: float,
    ) -> ResponseEvent:
        return ResponseEvent(
            method="GET",
            url=cls.safe_url(url),
            attempt=attempt,
            status_code=response.status_code,
            elapsed_seconds=elapsed_seconds,
        )


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


class TransportResponseDecoder:
    """Decode HTTP responses and map upstream failures to SDK exceptions."""

    @staticmethod
    def api_error(response: httpx.Response, payload: Any) -> APIError:
        status = response.status_code
        message = f"Mercado Público returned HTTP {status}."
        code: str | None = None
        details: Any = None

        if isinstance(payload, dict):
            errors = payload.get("errors") or payload.get("Errores")
            if isinstance(errors, list) and errors and isinstance(errors[0], dict):
                first = errors[0]
                code = str(first.get("codigo") or first.get("Codigo") or status)
                message = str(first.get("mensaje") or first.get("Mensaje") or message)
                details = first.get("detalle") or first.get("Detalle")
            else:
                message = str(
                    payload.get("mensaje")
                    or payload.get("Mensaje")
                    or payload.get("error")
                    or message
                )

        kwargs = {
            "status_code": status,
            "code": code,
            "details": details,
            "retry_after": response.headers.get("Retry-After"),
        }
        if status in (401, 403):
            return AuthenticationError(message, **kwargs)
        if status == 404:
            return NotFoundError(message, **kwargs)
        if status == 429:
            return RateLimitError(message, **kwargs)
        return APIError(message, **kwargs)

    @classmethod
    def decode(cls, response: httpx.Response) -> Any:
        try:
            payload = ResponseParser.decode_json(response.content)
        except Exception:
            if response.is_error:
                raise APIError(
                    f"Mercado Público returned HTTP {response.status_code}.",
                    status_code=response.status_code,
                    retry_after=response.headers.get("Retry-After"),
                ) from None
            raise
        if response.is_error:
            raise cls.api_error(response, payload)
        if isinstance(payload, dict) and str(payload.get("success", "")).upper() == "NOK":
            raise cls.api_error(response, payload)
        return payload


class SyncTransport:
    """`httpx.Client` adapter with normalized SDK errors."""

    def __init__(self, client: httpx.Client, config: ClientConfig) -> None:
        self.client = client
        self.config = config

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
                response = self.client.get(
                    url,
                    params=params,
                    headers=headers,
                )
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


class AsyncTransport:
    """`httpx.AsyncClient` adapter with normalized SDK errors."""

    def __init__(self, client: httpx.AsyncClient, config: ClientConfig) -> None:
        self.client = client
        self.config = config

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
                response = await self.client.get(
                    url,
                    params=params,
                    headers=headers,
                )
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
