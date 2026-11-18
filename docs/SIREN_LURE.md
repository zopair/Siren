# Siren Semantic Lure Engine

## Scope

The first delivery batch adds a deterministic in-memory semantic catalog of fixed,
synthetic fixtures. It ranks those fixtures against a bounded task-context string
and exposes them through read-only Flask and MCP tools.

It also adds an acoustic adapter that reuses the repository's existing fixed
ggwave marker generator. The adapter accepts an output path, but no arbitrary
message or payload; the original fixed canary semantics are preserved. The
existing Flask audio route can serve the generated `assets/audio/canary.wav`.

## Lure families

- Context-aware breadcrumbs and task-relevant resource names.
- High-value-looking aggregation indexes containing synthetic data only.
- Convenient tool descriptions that return only static fixtures.
- Priority-looking text explicitly marked as untrusted simulation content.
- Fictional emergency-exception notices with no credentials or permission effect.
- A fixed acoustic canary generated through the existing ggwave module.

## Flask interface

The existing local Flask service exposes:

- `GET /api/lures?context=<short-context>`
- `GET /api/lures/<lure_id>`
- `GET /audio/canary.wav` for an already-generated fixed acoustic canary.

The service is read-only with respect to lure content and retains its loopback
default. The endpoints return only catalogued fixtures and record event type,
fixture identifier, and context length. Raw context is not retained.

## MCP interface

Run the stdio server with:

```bash
siren-mcp
```

The server implements MCP initialization and the read-only tools
`list_siren_lures` and `open_siren_lure` over newline-delimited JSON-RPC.
No third-party MCP runtime dependency is added in this batch.

## Acoustic adapter

```python
from pathlib import Path

from siren_trap.siren_lure import generate_acoustic_lure

result = generate_acoustic_lure(Path("assets/audio/canary.wav"))
print(result.sha256)
```

The adapter delegates to `payload_generator.build_trap`; it does not accept
arbitrary text or commands as acoustic payloads.

## Limitations

This is a lure and observation prototype, not a session containment boundary.
A lure interaction is not proof of malicious intent. Sentinel enforcement and
counterfactual evidence are separate delivery targets.
