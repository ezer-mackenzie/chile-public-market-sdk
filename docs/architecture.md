# Diseño y compatibilidad

El SDK separa cinco responsabilidades:

1. `ClientConfig` resuelve configuración y ticket.
2. El transporte encapsula `httpx` y normaliza errores HTTP.
3. Los parsers decodifican y validan respuestas.
4. Los modelos Pydantic representan contratos públicos.
5. Los clientes exponen la API de dominio sync y async.

Los modelos usan `extra="allow"` deliberadamente. Mercado Público mantiene
servicios legados y la guía de Compra Ágil advierte que algunos campos reales
difieren de versiones previas de la documentación. Este comportamiento valida
campos conocidos sin romper al consumidor cuando ChileCompra agrega datos.
