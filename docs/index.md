# Mercado Público Chile SDK

Cliente Python síncrono y asíncrono para todos los endpoints públicos
documentados de Mercado Público.

## Inicio rápido

```python
from chile_public_market_sdk import MercadoPublico

with MercadoPublico(ticket="TU_TICKET") as sdk:
    resultado = sdk.licitaciones(codigo="1509-5-L114")
    print(resultado.listado[0].nombre)
```

El ticket puede omitirse si existe la variable de entorno
`MERCADO_PUBLICO_TICKET`.

## Referencia

- [Guía de uso](usage.md)
- [Referencia de API](api.md)
- [Diseño y compatibilidad](architecture.md)
- [Hoja de ruta hacia v1.0.0](v1-roadmap.md)
