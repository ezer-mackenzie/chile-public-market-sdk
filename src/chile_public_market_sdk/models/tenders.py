"""Modelos de licitaciones."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, Field

from .base import MercadoPublicoModel
from .common import LineItem, Organization


class Tender(MercadoPublicoModel):
    codigo_externo: str = Field(
        validation_alias=AliasChoices("CodigoExterno", "Codigo", "codigo_externo")
    )
    nombre: str | None = Field(
        default=None, validation_alias=AliasChoices("Nombre", "nombre")
    )
    codigo_estado: int | None = Field(
        default=None, validation_alias=AliasChoices("CodigoEstado", "codigo_estado")
    )
    estado: str | None = Field(
        default=None, validation_alias=AliasChoices("Estado", "estado")
    )
    descripcion: str | None = Field(
        default=None, validation_alias=AliasChoices("Descripcion", "descripcion")
    )
    fecha_cierre: datetime | str | None = Field(
        default=None, validation_alias=AliasChoices("FechaCierre", "fecha_cierre")
    )
    moneda: str | None = Field(
        default=None, validation_alias=AliasChoices("Moneda", "moneda")
    )
    monto_estimado: Decimal | None = Field(
        default=None, validation_alias=AliasChoices("MontoEstimado", "monto_estimado")
    )
    comprador: Organization | None = Field(
        default=None, validation_alias=AliasChoices("Comprador", "comprador")
    )
    items: list[LineItem] = Field(
        default_factory=list, validation_alias=AliasChoices("Items", "items")
    )


class TenderResponse(MercadoPublicoModel):
    cantidad: int = Field(default=0, validation_alias=AliasChoices("Cantidad", "cantidad"))
    fecha_creacion: datetime | str | None = Field(
        default=None, validation_alias=AliasChoices("FechaCreacion", "fecha_creacion")
    )
    version: str | None = Field(default=None, validation_alias=AliasChoices("Version", "version"))
    listado: list[Tender] = Field(
        default_factory=list, validation_alias=AliasChoices("Listado", "listado")
    )
