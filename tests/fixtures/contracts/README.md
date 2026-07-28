# Contract fixture provenance

Captured on 2026-07-28 from the official ChileCompra production APIs using a
private consumer ticket. Raw responses are stored only under `/tmp` and are
never committed.

| Fixture | Endpoint family | Capture |
|---|---|---|
| `tender-detail.json` | v1 tender detail | Code lookup |
| `purchase-order-detail.json` | v1 purchase-order detail | Code lookup |
| `supplier.json` | v1 supplier search | Tax-ID lookup |
| `buyers.json` | v1 buyer organizations | Listing truncated to two records |
| `agile-list.json` | v2 Agile Purchase | Seven-day change window, one retained item |
| `agile-detail.json` | v2 Agile Purchase detail | First code from captured list |

Names, tax IDs, organization and unit codes, addresses, contact details,
descriptions, URLs, and other identifying strings were replaced with
synthetic placeholders. Dates, numeric values, enum values, nullability, and
payload structure were retained for contract validation.

These fixtures must never be replaced with raw production responses.
