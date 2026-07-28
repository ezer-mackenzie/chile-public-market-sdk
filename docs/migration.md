# Migrating from the initial 0.1.0 API

The English API replaces the initial Spanish method, parameter, and model
attribute names. This change occurs before the first stable release.

## Client methods

| Initial name | English name |
|---|---|
| `licitaciones` | `get_tenders` |
| `ordenes_de_compra` | `get_purchase_orders` |
| `buscar_proveedor` | `find_supplier` |
| `compradores` | `get_buyers` |
| `compras_agiles` | `get_agile_purchases` |
| `compra_agil` | `get_agile_purchase` |

## Common parameters

| Initial name | English name |
|---|---|
| `codigo` | `code` |
| `fecha` | `date` |
| `estado` | `status` |
| `codigo_organismo` | `buyer_code` |
| `codigo_proveedor` | `supplier_code` |
| `ttl_cambio_ms` | `last_change_ttl_ms` |
| `cambio_desde` / `cambio_hasta` | `changed_from` / `changed_until` |
| `publicado_desde` / `publicado_hasta` | `published_from` / `published_until` |
| `estados` | `statuses` |
| `regiones` | `regions` |
| `tamano_pagina` / `numero_pagina` | `page_size` / `page_number` |
| `ordenar_por` | `sort_by` |

Response models now expose English attributes such as `count`, `items`,
`external_code`, `company_code`, and `pagination`. The upstream Spanish JSON
keys remain accepted automatically.
