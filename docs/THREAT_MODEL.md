# Threat Model

## Purpose

Define the defensive scope and trust boundaries for the Siren-Trap research prototype.

## Assets

- Research canary marker and generated audio artifact
- Decoy service availability and integrity
- Structured event records
- Evaluation results and test configuration

## Threat scenarios

- Indirect prompt injection through untrusted multimodal content
- Data/instruction confusion in perception-to-context pipelines
- Malformed requests against the decoy service
- Forged or misleading observations supplied to the evaluator
- Unauthorized access to exposed research infrastructure

## Trust boundaries

1. External client to decoy HTTP service
2. Audio playback to microphone/perception pipeline
3. Perception output to the agent's trusted context
4. Agent observation to Siren-Trap evaluation code
5. Event logger to local storage

## Controls

- Localhost-only default binding
- Fixed, non-executable canary marker
- Explicit user-triggered audio playback
- No execution of observations or payload text
- Minimal event collection
- Security headers and deterministic tests

## Out of scope

- Covert compromise or takeover of third-party agents
- System-prompt extraction or override
- Persistence, evasion, destructive actions, or lateral movement
- Deployment against systems without written authorization

## Residual risks

The prototype does not authenticate clients, provide production-grade rate limiting, or guarantee tamper-resistant logs. Do not expose it to untrusted networks without a separate deployment security review.
