# Security Policy

## Project security posture and threat model

Siren is an independent defensive AI security research proof of concept for
authorized experiments involving semantic lures, multimodal inputs, decoy
resources, and agent trust boundaries.

It is **not an offensive exploit tool**. It is not designed or authorized for
compromising systems, covertly controlling third-party agents, bypassing access
controls, exfiltrating data, disrupting services, or delivering harmful
instructions.

### Assets to protect

- The host running the decoy service and its local files.
- Synthetic test fixtures and research configuration.
- The integrity of canary markers, telemetry, and test results.
- The availability and isolation of the laboratory environment.
- The privacy of people and systems represented in test observations.

### Trust boundaries and assumptions

- All agent observations, decoded content, HTTP input, MCP arguments, audio
  files, and telemetry fields are untrusted.
- Canary markers and lure fixtures are inert research data. They must never be
  evaluated as code, commands, or privileged instructions.
- The semantic lure service is read-only and is not an authorization boundary.
- The decoy service is not a substitute for OS/container/network isolation.
- The Flask service binds to localhost by default. Any network exposure requires
  an independent security review, authentication, rate limiting, and explicit
  authorization.
- The MCP adapter is a local stdio process; configure it only in an authorized
  MCP client and do not expose it through an unauthenticated network bridge.
- Acoustic measurements are diagnostic only; they do not establish inaudibility,
  microphone compatibility, or successful reception.
- Sentinel session containment is not implemented in batch 1. No production or
  full-agent containment guarantee is made.

### Out of scope

- Unauthorized testing of third-party devices, agents, networks, or facilities.
- Stealthy delivery of instructions to systems outside an explicitly authorized lab.
- Exploitation, persistence, privilege escalation, credential theft, data
  exfiltration, malware, or denial of service.
- Claims that this prototype safely contains a compromised agent without
  independently verified external isolation controls.

## Supported versions

Only the latest development branch is currently supported. No stable release
has been published.

## Reporting a vulnerability

Please do not disclose exploitable details in a public issue. Use GitHub's
private vulnerability reporting feature for this repository if it is enabled.
If it is unavailable, contact the repository owner through a private channel
listed on the owner's GitHub profile and request a secure reporting route.

Include, where safe:

- Affected commit or version and component.
- Impact and required preconditions.
- Minimal reproduction steps in an isolated environment.
- Logs or proof-of-concept artifacts with secrets and personal data removed.
- Suggested mitigation, if known.

Do not attach live credentials, private keys, personal information, or raw
microphone recordings.

## Operational requirements

- Keep the Flask service bound to `127.0.0.1` unless a separate deployment
  review authorizes otherwise.
- Run experiments only against systems and equipment you own or are explicitly
  authorized to test.
- Use fixed synthetic lure data and inert canary data. Do not turn the framework
  into an arbitrary command or instruction delivery channel.
- Do not execute, evaluate, or automatically follow content observed from an
  agent or decoy endpoint.
- Minimize telemetry. Avoid storing raw audio, secrets, credentials, raw task
  context, or personal data.
- Apply OS/container isolation and network egress controls for any agent under
  test; the current lure service does not provide containment.
- Review dependency licenses, provenance, maintenance activity, and known
  vulnerabilities before upgrades.
- Report suspected accidental exposure or compromise promptly and preserve
  only the minimum evidence needed for investigation.

## Security review checklist for changes

- Does the change preserve fixed, inert canary and synthetic lure semantics?
- Does it avoid executing or forwarding untrusted content?
- Does it preserve localhost-only defaults?
- Does it avoid collecting secrets, personal data, or raw audio unnecessarily?
- Are dependencies open-source, license-compatible, maintained, and free of
  known critical advisories?
- Are tests and documentation explicit about what has and has not been verified?
