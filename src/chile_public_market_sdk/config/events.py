"""Safe observability event contracts."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestEvent:
    """Sanitized metadata emitted before an HTTP attempt."""

    method: str
    url: str
    attempt: int


@dataclass(frozen=True, slots=True)
class ResponseEvent:
    """Sanitized metadata emitted after an HTTP attempt."""

    method: str
    url: str
    attempt: int
    status_code: int
    elapsed_seconds: float


type RequestHook = Callable[[RequestEvent], None]
type ResponseHook = Callable[[ResponseEvent], None]
