# Siren Architecture

Siren is organized around five research operations:

1. **Attract** — `siren_lure` ranks and serves fixed synthetic decoy resources.
2. **Capture** — the existing detection and telemetry modules record observable interactions.
3. **Isolate** — `sentinel_quarantine` is the planned external enforcement boundary (batch 2).
4. **Investigate** — the experiment layer will coordinate controlled runs (batch 3).
5. **Prove** — `causal_proof` will compare counterfactual evidence (batch 2).

## Existing foundation

- `payload_generator`: fixed acoustic canary generation using ggwave.
- `decoy_firewall`: localhost-first Flask research service.
- `detection`: fixed-marker observation checks.
- `telemetry`: JSONL event recording and passive acoustic analysis.

## Batch-1 implementation

The semantic lure catalog is deterministic and in-memory. It exposes read-only
Flask endpoints and a small MCP stdio adapter. Both interfaces return only
fixed synthetic fixtures. Context is used transiently for ranking; only its
length is recorded. Lure content is never evaluated or executed.

## Trust boundaries

The agent and its context are outside the trust boundary. The lure service is
an observation surface, not an authorization or containment boundary. The
MCP adapter does not execute arbitrary tools, access arbitrary paths, or make
network requests.

## Future containment and proof

Sentinel must enforce isolation outside the agent process and explicitly
report uncovered child sessions, tools, and network paths. Causal proof must
separate attempted, dispatched, received, and effect-confirmed actions and must
not infer private model reasoning.
