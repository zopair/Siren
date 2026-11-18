# Siren Semantic Lure Engine

## Scope

The first delivery batch adds a deterministic semantic catalog of fixed, synthetic
fixtures. It ranks those fixtures against a bounded task-context string and exposes
them through read-only Flask and MCP tools.

The catalog is deliberately in-memory. It does not resolve caller-supplied paths,
read arbitrary files, invoke shell commands, call external services, or grant
authorization. Context is used only for local ranking and is not written to logs.

## Lure families

- Context-aware breadcrumbs and task-relevant resource names.
- High-value-looking aggregation indexes containing synthetic data only.
- Convenient tool descriptions that return only static fixtures.
- Priority-looking text explicitly marked as untrusted simulation content.
- Fictional emergency-exception notices with no credentials or permission effect.

## Flask interface

The existing local Flask service exposes:

- `GET /api/lures?context=<short-context>`
- `GET /api/lures/<lure_id>`

The service retains its loopback default. The endpoints are read-only, return only
catalogued fixtures, and record event type, fixture identifier, and context length.
Raw context is not retained.

## MCP interface

Run the stdio server with:

```bash
python -m siren_trap.siren_lure.mcp_server
```

The server implements MCP initialization and the read-only tools
`list_siren_lures` and `open_siren_lure` over newline-delimited JSON-RPC.
No third-party MCP runtime dependency is added in this batch.

## Limitations

This is a lure and observation prototype, not a session containment boundary.
A lure interaction is not proof of malicious intent. Sentinel enforcement and
counterfactual evidence are separate delivery targets.
