"""Modelos para compradores y proveedores."""

from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, Field, model_validator

from .base import MercadoPublicoModel


class Company(MercadoPublicoModel):
    codigo_empresa: str | int | None = Field(
        default=None, validation_alias=AliasChoices("CodigoEmpresa", "codigoEmpresa")
    )
    nombre_empresa: str | None = Field(
        default=None, validation_alias=AliasChoices("NombreEmpresa", "nombreEmpresa")
    )
    rut: str | None = Field(
        default=None,
        validation_alias=AliasChoices("RutEmpresa", "RUT", "Rut", "rut"),
    )


class CompanyResponse(MercadoPublicoModel):
    empresas: list[Company] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_shape(cls, value: Any) -> Any:
        if isinstance(value, list):
            return {"empresas": value}
        if isinstance(value, dict):
            for key in ("listaEmpresas", "Listado", "listado", "Empresas"):
                if key in value:
                    return {"empresas": value[key], **value}
            if "CodigoEmpresa" in value or "codigoEmpresa" in value:
                return {"empresas": [value]}
        return value
