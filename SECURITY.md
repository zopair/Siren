# Security Policy

## Project security posture and threat model

Siren-Trap is a **physical-layer Threat Deception Grid (Honeypot)** intended **strictly for defensive AI Red Teaming, authorized vulnerability research, security evaluation, and containment-oriented observation of rogue or non-compliant agents in isolated test environments**.

It is **not an offensive exploit tool**. It is not designed or authorized for compromising systems, covertly controlling third-party agents, bypassing access controls, exfiltrating data, disrupting services, or delivering harmful instructions.

### Assets to protect

- The host running the decoy service and its local files.
- Test credentials, tokens, and research data.
- The integrity of canary markers, telemetry, and test results.
- The availability and isolation of the laboratory environment.
- The privacy of people and systems that may be represented in test observations.

### Trust boundaries and assumptions

- All agent observations, decoded content, HTTP input, audio files, and telemetry fields are untrusted.
- Canary markers are inert indicators. They must never be evaluated as code, commands, or privileged instructions.
- The decoy service is not an authorization boundary or a substitute for OS/container/network isolation.
- The default deployment is localhost-only. Any network exposure requires an independent security review, authentication, rate limiting, and explicit authorization.
- Acoustic measurements are diagnostic only; they do not establish inaudibility, microphone compatibility, or successful reception.

### Out of scope

- Unauthorized testing of third-party devices, agents, networks, or facilities.
- Stealthy acoustic delivery of instructions to systems outside an explicitly authorized lab.
- Exploitation, persistence, privilege escalation, credential theft, data exfiltration, malware, or denial of service.
- Claims that this prototype safely contains a compromised agent without external isolation controls.

## Supported versions

Only the latest development branch is currently supported. No stable release has been published.

## Reporting a vulnerability

Please do not disclose exploitable details in a public issue. Use GitHub's private vulnerability reporting feature for this repository if it is enabled. If it is unavailable, contact the repository owner through a private channel listed on the owner's GitHub profile and request a secure reporting route.

Include, where safe:

- Affected commit or version and component.
- Impact and required preconditions.
- Minimal reproduction steps in an isolated environment.
- Logs or proof-of-concept artifacts with secrets and personal data removed.
- Suggested mitigation, if known.

Do not attach live credentials, private keys, personal information, or raw microphone recordings.

## Operational requirements

- Keep the Flask service bound to `127.0.0.1` unless a separate deployment review authorizes otherwise.
- Run experiments only against systems and equipment you own or are explicitly authorized to test.
- Use inert, fixed canary data. Do not turn the framework into an arbitrary command or instruction delivery channel.
- Do not execute, evaluate, or automatically follow content observed from an agent or decoy endpoint.
- Minimize telemetry. Avoid storing raw audio, secrets, credentials, or personal data.
- Apply OS/container isolation and network egress controls for any agent-under-test.
- Review dependency licenses, provenance, maintenance activity, and known vulnerabilities before upgrades.
- Report suspected accidental exposure or compromise promptly and preserve only the minimum evidence needed for investigation.

## Security review checklist for changes

- Does the change preserve fixed, inert canary semantics?
- Does it avoid executing or forwarding untrusted content?
- Does it preserve localhost-only defaults?
- Does it avoid collecting secrets, personal data, or raw audio unnecessarily?
- Are dependencies open-source, license-compatible, maintained, and free of known critical advisories?
- Are tests and documentation explicit about what has and has not been verified?
