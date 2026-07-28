"""Modelos base tolerantes a extensiones del proveedor."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MercadoPublicoModel(BaseModel):
    """Base de los payloads; conserva compatibilidad ante campos nuevos."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)
