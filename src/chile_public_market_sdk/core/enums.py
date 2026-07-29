"""Shared enumerations documented by Mercado Público."""

from enum import IntEnum, StrEnum


class TenderStatusCode(IntEnum):
    PUBLISHED = 5
    CLOSED = 6
    DESERTED = 7
    AWARDED = 8
    REVOKED = 18
    SUSPENDED = 19


class TenderStatus(StrEnum):
    ACTIVE = "activas"
    PUBLISHED = "publicada"
    CLOSED = "cerrada"
    DESERTED = "desierta"
    AWARDED = "adjudicada"
    REVOKED = "revocada"
    SUSPENDED = "suspendida"
    ALL = "todos"


class PurchaseOrderStatusCode(IntEnum):
    SENT_TO_SUPPLIER = 4
    IN_PROCESS = 5
    ACCEPTED = 6
    CANCELLED = 9
    RECEIVED = 12
    PENDING_RECEIPT = 13
    PARTIALLY_RECEIVED = 14
    INCOMPLETE_RECEIPT = 15


class PurchaseOrderStatus(StrEnum):
    SENT_TO_SUPPLIER = "enviadaproveedor"
    ACCEPTED = "aceptada"
    CANCELLED = "cancelada"
    RECEIVED = "recepcionconforme"
    PENDING_RECEIPT = "pendienterecepcion"
    PARTIALLY_RECEIVED = "recepcionaceptadacialmente"
    INCOMPLETE_RECEIPT = "recepecionconformeincompleta"
    ALL = "todos"


class AgilePurchaseStatus(StrEnum):
    PUBLISHED = "publicada"
    CLOSED = "cerrada"
    DESERTED = "desierta"
    CANCELLED = "cancelada"
    SUPPLIER_SELECTED = "proveedor_seleccionado"
    PURCHASE_ORDER_ISSUED = "oc_emitida"


class AgilePurchaseSort(StrEnum):
    LAST_MODIFIED = "FechaUltimaModificacion"
    PUBLICATION_DATE = "FechaPublicacion"
