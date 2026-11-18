# Threat Model

## Purpose

Define the defensive scope and trust boundaries for the Siren research
prototype, including its semantic lure interfaces.

## Assets

- Research canary marker and generated audio artifact.
- Synthetic lure catalog and decoy service availability.
- Structured event records.
- Evaluation results and test configuration.
- Host integrity and experiment isolation.

## Threat scenarios

- Indirect prompt injection through untrusted multimodal content.
- Data/instruction confusion in perception-to-context pipelines.
- Agents treating lure descriptions or untrusted document text as authority.
- Malformed requests against the Flask or MCP interfaces.
- Attempts to access arbitrary files through lure identifiers.
- Forged or misleading observations supplied to the evaluator.
- Unauthorized access to exposed research infrastructure.

## Trust boundaries

1. External client to decoy HTTP service.
2. MCP client to the local stdio adapter.
3. Audio playback to microphone/perception pipeline.
4. Perception output and retrieved content to the agent's trusted context.
5. Agent observation to Siren evaluation code.
6. Event logger to local storage.
7. Future Sentinel enforcement gateway to the isolated execution environment.

## Batch-1 controls

- Localhost-only Flask default binding.
- Fixed, non-executable acoustic canary marker.
- Fixed in-memory lure catalog; no arbitrary path resolution.
- Read-only Flask and MCP tools.
- Bounded context and identifier inputs.
- No execution of observations or lure content.
- Minimal telemetry; raw context is not logged.
- Security headers and deterministic tests.

## Planned controls

Sentinel containment, egress enforcement, delegated-session coverage, and
counterfactual evidence validation are not implemented in batch 1. They must
be verified independently before any containment guarantee is claimed.

## Out of scope

- Covert compromise or takeover of third-party agents.
- System-prompt extraction or actual system-instruction override.
- Persistence, evasion, destructive actions, or lateral movement.
- Deployment against systems without written authorization.

## Residual risks

The prototype does not authenticate remote clients, provide production-grade
rate limiting, or guarantee tamper-resistant logs. The MCP stdio server is
intended for a locally configured authorized experiment. Do not expose the
Flask service to untrusted networks without a separate deployment review.
