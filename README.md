# Mercado Público Chile SDK

SDK no oficial, tipado, síncrono y asíncrono para las APIs públicas de
[Mercado Público de Chile](https://www.chilecompra.cl/api/).

> Estado: alpha (`0.1.0`). La API upstream contiene contratos legados y puede
> agregar campos; los modelos validan los campos conocidos y conservan los adicionales.

## Requisitos

- Python 3.12 o superior.
- Un ticket de acceso solicitado en el sitio de ChileCompra.

## Instalación

```bash
pip install mercado-publico-chile-sdk
```

## Configuración segura

El SDK no incluye ni administra tickets. Puedes entregarlo explícitamente:

```python
from chile_public_market_sdk import MercadoPublico

sdk = MercadoPublico(ticket="TU_TICKET")
```

O mediante la variable `MERCADO_PUBLICO_TICKET`:

```bash
export MERCADO_PUBLICO_TICKET="TU_TICKET"
```

Los archivos `.env` están ignorados por Git. Cargarlos con Docker Compose,
Kubernetes, `env.yaml`, `python-dotenv` u otro gestor es responsabilidad de la
aplicación consumidora.

## Uso síncrono

```python
from datetime import date

from chile_public_market_sdk import MercadoPublico
from chile_public_market_sdk.enums import TenderStatus

with MercadoPublico() as sdk:
    resultado = sdk.licitaciones(
        fecha=date(2026, 6, 12),
        estado=TenderStatus.PUBLISHED,
    )
    for licitacion in resultado.listado:
        print(licitacion.codigo_externo, licitacion.nombre)

    orden = sdk.ordenes_de_compra(codigo="2097-241-SE14")
    proveedor = sdk.buscar_proveedor("70.017.820-k")
    compradores = sdk.compradores()
```

## Uso asíncrono

```python
import asyncio

from chile_public_market_sdk import AsyncMercadoPublico
from chile_public_market_sdk.enums import AgilePurchaseStatus


async def main() -> None:
    async with AsyncMercadoPublico() as sdk:
        pagina = await sdk.compras_agiles(
            ttl_cambio_ms=300_000,
            estados=[AgilePurchaseStatus.PUBLISHED],
            tamano_pagina=50,
        )
        detalle = await sdk.compra_agil(pagina.items[0].codigo)
        print(detalle.nombre)


asyncio.run(main())
```

## Cobertura de endpoints

| Recurso | Métodos del SDK | API |
|---|---|---|
| Licitaciones | `licitaciones` | v1 |
| Órdenes de compra | `ordenes_de_compra` | v1 |
| Proveedores | `buscar_proveedor` | v1 |
| Organismos compradores | `compradores` | v1 |
| Compra Ágil, listado y filtros | `compras_agiles` | v2 |
| Compra Ágil, detalle | `compra_agil` | v2 |

Los filtros de fecha aceptan `date` o el formato original `ddmmaaaa` en v1.
Compra Ágil acepta fechas ISO-8601, estados y regiones múltiples, paginación y
ordenamiento.

## Errores

Todas las excepciones heredan de `MercadoPublicoError`:

- `ConfigurationError`: falta el ticket.
- `RequestValidationError`: filtros incompatibles o inválidos.
- `AuthenticationError`: respuesta 401 o 403.
- `NotFoundError`: respuesta 404.
- `RateLimitError`: respuesta 429; expone `retry_after`.
- `APIError`: otros errores de la API.
- `TransportError`: red, DNS o timeout.
- `ResponseValidationError`: JSON inválido o contrato inesperado.

## Desarrollo

```bash
poetry install --with dev,docs
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry build
```

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y [SECURITY.md](SECURITY.md) antes
de enviar cambios o reportar vulnerabilidades.
