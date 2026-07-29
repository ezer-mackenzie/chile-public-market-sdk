"""Structural contracts for synchronous and asynchronous transports."""

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

type Params = Mapping[str, str | int | float]


@runtime_checkable
class SyncTransportProtocol(Protocol):
    """Transport contract consumed by the synchronous client."""

    def get(
        self,
        url: str,
        *,
        params: Params | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any: ...

    def close(self) -> None: ...


@runtime_checkable
class AsyncTransportProtocol(Protocol):
    """Transport contract consumed by the asynchronous client."""

    async def get(
        self,
        url: str,
        *,
        params: Params | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any: ...

    async def aclose(self) -> None: ...
