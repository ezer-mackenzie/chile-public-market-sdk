# Guía de uso

## Autenticación

La API v1 envía el ticket como query parameter y Compra Ágil v2 lo envía en el
header `ticket`. El SDK aplica automáticamente el mecanismo correcto.

La aplicación consumidora debe proporcionar el secreto:

```python
sdk = MercadoPublico(ticket=secret_manager.get("mercado-publico"))
```

También puede usar una variable con nombre personalizado:

```python
from chile_public_market_sdk import ClientConfig, MercadoPublico

sdk = MercadoPublico(config=ClientConfig(ticket_env="MI_TICKET"))
```

## Cliente HTTP personalizado

```python
import httpx

from chile_public_market_sdk import MercadoPublico

http_client = httpx.Client(
    timeout=httpx.Timeout(20),
    transport=httpx.HTTPTransport(retries=2),
)
sdk = MercadoPublico(ticket="...", http_client=http_client)
```

Cuando se inyecta un cliente HTTP, quien lo crea conserva la responsabilidad
de cerrarlo.

## Filtros de API v1

`licitaciones` y `ordenes_de_compra` aceptan `codigo`, `fecha`, `estado`,
`codigo_organismo` y `codigo_proveedor`. Una consulta por código no se combina
con otros filtros porque representa el endpoint lógico de detalle.

## Compra Ágil

`compras_agiles` valida las restricciones oficiales:

- `ttl_cambio_ms` es incompatible con el rango `cambio_desde`/`cambio_hasta`.
- `id` y `q` son mutuamente excluyentes.
- el tamaño de página está entre 1 y 50;
- los códigos de región están entre 1 y 16.

La API no soporta filtrar Compra Ágil por organismo. Debes filtrar localmente
por `item.institucion.rut` o `item.institucion.organismo_comprador`.
