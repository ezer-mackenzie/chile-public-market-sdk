# Security policy

## Reporting a vulnerability

Do not open a public issue for vulnerabilities that could expose API tickets,
consumer data, or credentials. Report the issue privately through GitHub's
security advisory feature for this repository.

Include the affected version, reproduction steps, impact, and any suggested
mitigation. Do not include a real Mercado Público ticket.

## Secret handling

The SDK accepts a ticket from the consumer and does not persist it. `.env` and
`env.yaml` are ignored, but consumers should prefer a dedicated secret manager
in production. Exceptions, logs, fixtures, and bug reports must redact tickets.

Only supported, non-yanked releases receive security fixes. See
[`docs/support.md`](docs/support.md) for the release support window and
deprecation policy.
