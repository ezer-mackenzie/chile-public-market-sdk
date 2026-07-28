"""Base models that tolerate upstream extensions and normalize wire keys."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

# ChileCompra exposes Spanish PascalCase, camelCase, and snake_case keys across
# its APIs. Models expose one consistent English surface while this map remains
# an internal wire-protocol concern.
WIRE_KEY_MAP = {
    "Cantidad": "count",
    "cantidad": "quantity",
    "FechaCreacion": "created_at",
    "fechaCreacion": "created_at",
    "fecha_creacion": "created_at",
    "Version": "version",
    "Listado": "items",
    "listado": "items",
    "CodigoExterno": "external_code",
    "Codigo": "code",
    "codigo": "code",
    "Nombre": "name",
    "nombre": "name",
    "CodigoEstado": "status_code",
    "codigo_estado": "status_code",
    "Estado": "status",
    "estado": "status",
    "Descripcion": "description",
    "descripcion": "description",
    "FechaCierre": "closing_at",
    "fecha_cierre": "closing_at",
    "Moneda": "currency",
    "moneda": "currency",
    "MontoEstimado": "estimated_amount",
    "monto_estimado": "estimated_amount",
    "Comprador": "buyer",
    "comprador": "buyer",
    "Proveedor": "supplier",
    "proveedor": "supplier",
    "Items": "items",
    "FechaEnvio": "sent_at",
    "fecha_envio": "sent_at",
    "Total": "total",
    "CodigoOrganismo": "organization_code",
    "codigo_organismo": "organization_code",
    "NombreOrganismo": "organization_name",
    "nombre_organismo": "organization_name",
    "CodigoEmpresa": "company_code",
    "codigoEmpresa": "company_code",
    "NombreEmpresa": "company_name",
    "nombreEmpresa": "company_name",
    "RutEmpresa": "tax_id",
    "Rut": "tax_id",
    "RUT": "tax_id",
    "rut": "tax_id",
    "NombreUnidad": "unit",
    "Unidad": "unit",
    "unidad": "unit",
    "RegionUnidad": "region",
    "Region": "region",
    "region": "region",
    "ComunaUnidad": "municipality",
    "Comuna": "municipality",
    "comuna": "municipality",
    "CodigoProveedor": "supplier_code",
    "NombreProveedor": "supplier_name",
    "Correlativo": "line_number",
    "correlativo": "line_number",
    "CodigoProducto": "product_code",
    "codigo_producto": "product_code",
    "NombreProducto": "product_name",
    "nombre_producto": "product_name",
    "UnidadMedida": "unit_of_measure",
    "unidad_medida": "unit_of_measure",
    "listaEmpresas": "companies",
    "Empresas": "companies",
    "empresas": "companies",
    "mensaje": "message",
    "detalle": "details",
    "id_estado": "status_id",
    "glosa": "label",
    "estado_convocatoria": "round_status",
    "fecha_cierre_primer_llamado": "first_round_closing_at",
    "fecha_cierre_segundo_llamado": "second_round_closing_at",
    "fecha_publicacion": "published_at",
    "fecha_ultimo_cambio": "last_changed_at",
    "fecha_cancelacion": "cancelled_at",
    "organismo_comprador": "buyer_organization",
    "unidad_compra": "purchasing_unit",
    "nombre_region": "region_name",
    "monto_disponible": "available_amount",
    "monto_disponible_clp": "available_amount_clp",
    "total_ofertas_recibidas": "total_quotes_received",
    "total_demandas": "total_requests",
    "multa_sancion": "penalty_amount",
    "motivo_cancelacion": "cancellation_reason",
    "motivo_desierta": "desertion_reason",
    "motivo_seleccion": "selection_reason",
    "tamano_pagina": "page_size",
    "numero_pagina": "page_number",
    "total_paginas": "total_pages",
    "total_resultados": "total_results",
    "direccion_entrega": "delivery_address",
    "plazo_entrega_dias": "delivery_days",
    "tipo_presupuesto": "budget_type",
    "presupuesto_estimado": "estimated_budget",
    "valor_cambio_moneda": "exchange_rate",
    "fecha_cambio_moneda": "exchange_rate_at",
    "id_orden_compra": "purchase_order_id",
    "id_oc": "purchase_order_internal_id",
    "codigo_orden_compra": "purchase_order_code",
    "estado_orden_compra": "purchase_order_status",
    "rut_proveedor": "supplier_tax_id",
    "razon_social": "legal_name",
    "es_emt": "is_small_business",
    "id_cotizacion": "quote_id",
    "codigo_sucursal_empresa": "company_branch_code",
    "estado_por_comprador": "buyer_status",
    "activo": "active",
    "fecha_vigencia": "valid_until",
    "valor_neto": "net_amount",
    "total_impuesto": "tax_amount",
    "monto_despacho": "shipping_amount",
    "monto_total": "total_amount",
    "nombre_impuesto": "tax_name",
    "porcentaje_impuesto": "tax_percentage",
    "descripcion_cotizacion": "quote_description",
    "justificacion_inadmisibilidad": "inadmissibility_reason",
    "precio_unitario": "unit_price",
    "monto_total_producto": "product_total",
    "productos_cotizados": "quoted_products",
    "productos_solicitados": "requested_products",
    "proveedores_cotizando": "quoting_suppliers",
    "considera_requisitos_medioambientales": "has_environmental_requirements",
    "considera_requisitos_impacto_social_economico": "has_social_economic_requirements",
    "orden_compra": "purchase_order",
    "institucion": "institution",
    "documentos": "documents",
    "fechas": "dates",
    "montos": "amounts",
    "resumen": "summary",
    "motivos": "reasons",
    "convocatoria": "call",
    "entrega": "delivery",
    "presupuesto": "budget",
    "seleccion": "selection",
    "paginacion": "pagination",
    "enlace": "link",
}


def _normalize_wire_keys(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            WIRE_KEY_MAP.get(str(key), str(key)): _normalize_wire_keys(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_normalize_wire_keys(item) for item in value]
    return value


class ChilePublicMarketModel(BaseModel):
    """Base model for ChileCompra payloads."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def normalize_wire_keys(cls, value: Any) -> Any:
        """Translate upstream Spanish keys into the SDK's English model surface."""

        return _normalize_wire_keys(value)
