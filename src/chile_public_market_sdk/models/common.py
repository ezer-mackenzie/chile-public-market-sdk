"""Estructuras compartidas por la API v1."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import AliasChoices, Field

from .base import MercadoPublicoModel


class APIv1Response(MercadoPublicoModel):
    cantidad: int = Field(default=0, validation_alias=AliasChoices("Cantidad", "cantidad"))
    fecha_creacion: datetime | str | None = Field(
        default=None, validation_alias=AliasChoices("FechaCreacion", "fechaCreacion")
    )
    version: str | None = Field(default=None, validation_alias=AliasChoices("Version", "version"))
    listado: list[dict[str, Any]] = Field(
        default_factory=list, validation_alias=AliasChoices("Listado", "listado")
    )


class Organization(MercadoPublicoModel):
    codigo_organismo: str | int | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "CodigoOrganismo", "CodigoEmpresa", "codigo_organismo", "codigoEmpresa"
        ),
    )
    nombre_organismo: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "NombreOrganismo", "NombreEmpresa", "nombre_organismo", "nombreEmpresa"
        ),
    )
    rut: str | None = Field(default=None, validation_alias=AliasChoices("Rut", "RUT", "rut"))
    unidad: str | None = Field(
        default=None, validation_alias=AliasChoices("NombreUnidad", "Unidad", "unidad")
    )
    region: str | int | None = Field(
        default=None, validation_alias=AliasChoices("RegionUnidad", "Region", "region")
    )
    comuna: str | None = Field(
        default=None, validation_alias=AliasChoices("ComunaUnidad", "Comuna", "comuna")
    )


class Supplier(MercadoPublicoModel):
    codigo: str | int | None = Field(
        default=None, validation_alias=AliasChoices("Codigo", "CodigoProveedor", "codigo")
    )
    nombre: str | None = Field(
        default=None,
        validation_alias=AliasChoices("Nombre", "NombreProveedor", "nombre"),
    )
    rut: str | None = Field(default=None, validation_alias=AliasChoices("Rut", "RUT", "rut"))


class LineItem(MercadoPublicoModel):
    correlativo: int | None = Field(
        default=None, validation_alias=AliasChoices("Correlativo", "correlativo")
    )
    codigo_producto: str | int | None = Field(
        default=None, validation_alias=AliasChoices("CodigoProducto", "codigo_producto")
    )
    nombre_producto: str | None = Field(
        default=None, validation_alias=AliasChoices("NombreProducto", "nombre_producto")
    )
    descripcion: str | None = Field(
        default=None, validation_alias=AliasChoices("Descripcion", "descripcion")
    )
    cantidad: Decimal | None = Field(
        default=None, validation_alias=AliasChoices("Cantidad", "cantidad")
    )
    unidad_medida: str | None = Field(
        default=None, validation_alias=AliasChoices("UnidadMedida", "unidad_medida")
    )
