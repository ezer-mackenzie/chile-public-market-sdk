from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx
import pytest


@pytest.fixture
def make_client() -> Callable[[Callable[[httpx.Request], httpx.Response]], httpx.Client]:
    def factory(handler: Callable[[httpx.Request], httpx.Response]) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(handler))

    return factory


@pytest.fixture
def tender_payload() -> dict[str, Any]:
    return {
        "Cantidad": 1,
        "FechaCreacion": "2026-06-12T10:00:00",
        "Version": "v1",
        "Listado": [
            {
                "CodigoExterno": "1509-5-L114",
                "Nombre": "Office supplies",
                "CodigoEstado": 5,
                "Estado": "Publicada",
                "CampoNuevo": "preserved",
            }
        ],
    }

@pytest.fixture
def agile_page_payload() -> dict[str, Any]:
    return {
        "success": "OK",
        "trace": None,
        "errors": None,
        "payload": {
            "items": [
                {
                    "codigo": "1057539-228-COT26",
                    "nombre": "Electrical supplies",
                    "estado": {"id_estado": 1, "codigo": "publicada", "glosa": "Publicada"},
                    "convocatoria": {
                        "estado_convocatoria": 1,
                        "descripcion": "Primer llamado",
                    },
                    "documentos": [],
                    "fechas": {
                        "fecha_publicacion": "2026-01-19T00:00:00Z",
                        "fecha_cierre": "2026-01-20T00:00:00Z",
                        "fecha_ultimo_cambio": "2026-01-19T01:00:00Z",
                        "fecha_cancelacion": None,
                    },
                    "montos": {
                        "moneda": "CLP",
                        "monto_disponible": 100000,
                        "monto_disponible_clp": 100000,
                    },
                    "institucion": {
                        "organismo_comprador": "Public organization",
                        "rut": "60.000.000-0",
                        "unidad_compra": "Unidad",
                        "region": 13,
                        "nombre_region": "Metropolitana",
                    },
                    "resumen": {"total_ofertas_recibidas": 0},
                    "motivos": {
                        "motivo_cancelacion": None,
                        "motivo_desierta": None,
                        "motivo_seleccion": None,
                    },
                    "links": {"detalle": "/v2/compra-agil/1057539-228-COT26"},
                }
            ],
            "paginacion": {
                "total_paginas": 1,
                "numero_pagina": 1,
                "tamano_pagina": 15,
                "total_resultados": 1,
            },
        },
    }
