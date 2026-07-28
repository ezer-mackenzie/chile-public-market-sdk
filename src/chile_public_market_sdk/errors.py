"""Excepciones públicas del SDK."""

from __future__ import annotations

from typing import Any


class MercadoPublicoError(Exception):
    """Error base del SDK."""


class ConfigurationError(MercadoPublicoError):
    """La configuración del cliente no es válida."""


class RequestValidationError(MercadoPublicoError, ValueError):
    """Los filtros entregados por el consumidor son incompatibles."""


class TransportError(MercadoPublicoError):
    """No fue posible comunicarse con Mercado Público."""


class ResponseValidationError(MercadoPublicoError):
    """La respuesta no cumple el contrato esperado."""


class APIError(MercadoPublicoError):
    """Mercado Público respondió con un error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: Any = None,
        retry_after: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details
        self.retry_after = retry_after


class AuthenticationError(APIError):
    """El ticket falta, es inválido o está inactivo."""


class NotFoundError(APIError):
    """El recurso solicitado no existe."""


class RateLimitError(APIError):
    """Se agotó la cuota asociada al ticket."""
