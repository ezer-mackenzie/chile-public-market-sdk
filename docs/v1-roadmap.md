# Hoja de ruta hacia v1.0.0

La versión `0.1.0` establece la arquitectura y cubre los endpoints públicos
documentados. Para declarar estabilidad `v1.0.0` faltan los siguientes hitos.

## Contrato

- Validar fixtures anonimizados obtenidos con un ticket real para cada endpoint.
- Completar campos tipados de los payloads detallados de licitación y orden de compra.
- Crear pruebas de contrato periódicas contra producción sin publicar el ticket.
- Definir por escrito qué cambios constituyen ruptura de compatibilidad.

## Resiliencia

- Definir una política de reintentos opt-in para 429, 500 y 503.
- Exponer métricas o hooks de observabilidad sin incluir el ticket.
- Probar timeouts, desconexiones y respuestas no JSON.

## Compatibilidad

- Ejecutar CI en Python 3.12, 3.13 y 3.14.
- Probar el wheel en Linux, macOS y Windows.
- Mantener una matriz de payloads históricos de API v1.

## Distribución

- Confirmar disponibilidad del nombre en PyPI.
- Configurar publicación confiable (Trusted Publishing).
- Añadir changelog y automatización de releases firmados.
- Publicar documentación versionada.

## Calidad y gobierno

- Alcanzar al menos 90% de cobertura, especialmente en el cliente asíncrono.
- Revisar API pública, nombres y docstrings antes de congelarla.
- Establecer soporte, deprecaciones y tiempos de respuesta de seguridad.
- Confirmar licencia y atribución del proyecto.
