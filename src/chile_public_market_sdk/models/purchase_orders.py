"""Modelos de órdenes de compra."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, Field

from .base import MercadoPublicoModel
from .common import LineItem, Organization, Supplier


class PurchaseOrder(MercadoPublicoModel):
    codigo: str = Field(validation_alias=AliasChoices("Codigo", "codigo"))
    nombre: str | None = Field(
        default=None, validation_alias=AliasChoices("Nombre", "nombre")
    )
    codigo_estado: int | None = Field(
        default=None, validation_alias=AliasChoices("CodigoEstado", "codigo_estado")
    )
    estado: str | None = Field(
        default=None, validation_alias=AliasChoices("Estado", "estado")
    )
    fecha_envio: datetime | str | None = Field(
        default=None, validation_alias=AliasChoices("FechaEnvio", "fecha_envio")
    )
    total: Decimal | None = Field(
        default=None, validation_alias=AliasChoices("Total", "total")
    )
    moneda: str | None = Field(
        default=None, validation_alias=AliasChoices("Moneda", "moneda")
    )
    comprador: Organization | None = Field(
        default=None, validation_alias=AliasChoices("Comprador", "comprador")
    )
    proveedor: Supplier | None = Field(
        default=None, validation_alias=AliasChoices("Proveedor", "proveedor")
    )
    items: list[LineItem] = Field(
        default_factory=list, validation_alias=AliasChoices("Items", "items")
    )


class PurchaseOrderResponse(MercadoPublicoModel):
    cantidad: int = Field(default=0, validation_alias=AliasChoices("Cantidad", "cantidad"))
    fecha_creacion: datetime | str | None = Field(
        default=None, validation_alias=AliasChoices("FechaCreacion", "fecha_creacion")
    )
    version: str | None = Field(default=None, validation_alias=AliasChoices("Version", "version"))
    listado: list[PurchaseOrder] = Field(
        default_factory=list, validation_alias=AliasChoices("Listado", "listado")
    )
