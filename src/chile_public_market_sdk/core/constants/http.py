"""HTTP constants shared by synchronous and asynchronous clients."""

from typing import Final

import httpx

NETWORK_ERRORS: Final = (
    httpx.NetworkError,
    httpx.ProtocolError,
    httpx.ProxyError,
)
