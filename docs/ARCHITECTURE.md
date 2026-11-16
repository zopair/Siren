# Architecture

Siren-Trap separates four concerns:

- **Transport:** ggwave creates a fixed canary audio artifact.
- **Decoy:** Flask serves a local research page and optional audio file.
- **Detection:** the canary detector classifies supplied observations.
- **Telemetry:** a JSONL logger records structured events.

The modules are intentionally decoupled. The prototype does not contain an autonomous agent controller, a remote command channel, or an execution path for received content.

## Data flow

A researcher starts a local test session, opens the decoy page, and explicitly plays the canary. The authorized test agent's observation is evaluated separately by the detection module. Events are recorded for offline analysis.
