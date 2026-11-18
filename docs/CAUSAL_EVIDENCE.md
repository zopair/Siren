# Causal Evidence and Counterfactual Method

## Event reconstruction

Events are validated as JSONL-style mappings and sorted by ISO-8601 timestamp.
Explicit `authorization_id`, `source_id`, and `action_id` values are correlated;
missing identifiers are not guessed or synthesized.

## Effect stages

| Stage | Required evidence |
|---|---|
| `ATTEMPTED` | Action attempt recorded by the controlled execution boundary |
| `DISPATCHED` | Egress boundary records dispatch |
| `RECEIVED` | Controlled receiver independently records receipt |
| `EFFECT_CONFIRMED` | Receiver independently confirms the specified effect |

Evidence for a later stage requires evidence for every earlier stage. A tool
call or local log cannot establish receiver receipt or an external effect.

## Counterfactual protocol

The runner executes A (neutral baseline), B (poisoned treatment), and C
(counterfactual with the poisoning source removed). It invokes a caller-provided
reset before each run. The model and version, toolset, authorization fingerprint,
and dataset fingerprint are fixed. The executor must return the effective
configuration fingerprint; mismatches or missing fingerprints are marked invalid.

The runner does not call a model provider itself. The experiment harness supplies
the controlled executor and reset implementation. Repeated runs, randomized
condition order, model nondeterminism controls, and receiver-side observation
belong in the benchmark harness.

## Independent verdicts

Integrity, authorization, and causal-evidence verdicts are reported separately.
A valid log can document an authorization violation; neither fact alone proves
causality. Causal support is an explicit experiment-level input, not inferred
from action severity.
