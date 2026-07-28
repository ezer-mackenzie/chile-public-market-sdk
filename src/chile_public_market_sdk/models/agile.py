"""Modelos de Compra Ágil v2."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from ..enums import AgilePurchaseStatus
from .base import MercadoPublicoModel


class AgileError(MercadoPublicoModel):
    codigo: str
    mensaje: str
    detalle: str | None = None


class AgileEnvelope[PayloadT](MercadoPublicoModel):
    success: str
    trace: str | None = None
    payload: PayloadT | None = None
    errors: list[AgileError] | None = None


class AgileState(MercadoPublicoModel):
    id_estado: int
    codigo: AgilePurchaseStatus
    glosa: str


class AgileCall(MercadoPublicoModel):
    estado_convocatoria: int
    descripcion: str
    fecha_cierre_primer_llamado: datetime | None = None
    fecha_cierre_segundo_llamado: datetime | None = None


class AgileDocument(MercadoPublicoModel):
    id: str
    nombre: str


class AgileDates(MercadoPublicoModel):
    fecha_publicacion: datetime
    fecha_cierre: datetime
    fecha_ultimo_cambio: datetime
    fecha_cancelacion: datetime | None = None


class AgileInstitution(MercadoPublicoModel):
    organismo_comprador: str
    rut: str
    unidad_compra: str
    region: int | None = None
    nombre_region: str | None = None


class AgileAmounts(MercadoPublicoModel):
    moneda: str
    monto_disponible: Decimal | None = None
    monto_disponible_clp: Decimal | None = None


class AgileSummary(MercadoPublicoModel):
    total_ofertas_recibidas: int = 0
    total_demandas: int | None = None
    multa_sancion: Decimal | None = None


class AgileReasons(MercadoPublicoModel):
    motivo_cancelacion: str | None = None
    motivo_desierta: str | None = None
    motivo_seleccion: str | None = None


class AgileLinks(MercadoPublicoModel):
    detalle: str


class AgilePurchaseSummary(MercadoPublicoModel):
    codigo: str
    nombre: str
    estado: AgileState
    convocatoria: AgileCall
    documentos: list[AgileDocument] = Field(default_factory=list)
    fechas: AgileDates
    montos: AgileAmounts
    institucion: AgileInstitution
    resumen: AgileSummary
    motivos: AgileReasons
    links: AgileLinks


class AgilePagination(MercadoPublicoModel):
    total_paginas: int
    numero_pagina: int
    tamano_pagina: int
    total_resultados: int


class AgilePurchasePage(MercadoPublicoModel):
    items: list[AgilePurchaseSummary]
    paginacion: AgilePagination


class AgileDelivery(MercadoPublicoModel):
    direccion_entrega: str
    plazo_entrega_dias: int | None = None


class AgileBudget(MercadoPublicoModel):
    tipo_presupuesto: str
    moneda: str
    presupuesto_estimado: Decimal | None = None
    monto_disponible: Decimal | None = None
    monto_disponible_clp: Decimal | None = None
    valor_cambio_moneda: Decimal | None = None
    fecha_cambio_moneda: datetime | None = None


class AgilePurchaseOrderReference(MercadoPublicoModel):
    id_orden_compra: int | None = None
    id_oc: int | None = None
    codigo_orden_compra: str | None = None
    estado_orden_compra: str | None = None


class AgileRequestedProduct(MercadoPublicoModel):
    codigo_producto: int | str
    nombre: str
    descripcion: str | None = None
    cantidad: Decimal
    unidad_medida: str


class AgileQuotedProduct(MercadoPublicoModel):
    codigo_producto: int | str
    nombre_producto: str
    descripcion: str | None = None
    cantidad: Decimal
    precio_unitario: Decimal | None = None
    monto_total_producto: Decimal | None = None


class AgileQuote(MercadoPublicoModel):
    rut_proveedor: str
    razon_social: str
    es_emt: bool
    id_cotizacion: int | None = None
    codigo_empresa: str | None = None
    codigo_sucursal_empresa: str | None = None
    estado_por_comprador: str | None = None
    activo: bool | None = None
    fecha_creacion: datetime | None = None
    fecha_vigencia: datetime | None = None
    valor_neto: Decimal | None = None
    total_impuesto: Decimal | None = None
    monto_despacho: Decimal | None = None
    monto_total: Decimal | None = None
    nombre_impuesto: str | None = None
    porcentaje_impuesto: Decimal | None = None
    descripcion_cotizacion: str | None = None
    descripcion: str | None = None
    justificacion_inadmisibilidad: str | None = None
    productos_cotizados: list[AgileQuotedProduct] = Field(default_factory=list)


class AgileFlags(MercadoPublicoModel):
    considera_requisitos_medioambientales: bool
    considera_requisitos_impacto_social_economico: bool


class AgilePurchaseDetail(MercadoPublicoModel):
    codigo: str
    nombre: str
    descripcion: str
    estado: AgileState
    convocatoria: AgileCall
    fechas: AgileDates
    entrega: AgileDelivery
    documentos: list[AgileDocument] = Field(default_factory=list)
    presupuesto: AgileBudget
    orden_compra: AgilePurchaseOrderReference
    institucion: AgileInstitution
    productos_solicitados: list[AgileRequestedProduct] = Field(default_factory=list)
    proveedores_cotizando: list[AgileQuote] = Field(default_factory=list)
    resumen: AgileSummary
    motivos: AgileReasons
    flags: AgileFlags
