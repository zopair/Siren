# Sentinel Quarantine Enforcement Model

## Enforcement contract

Sentinel coordinates four controls through an injected `EnforcementAdapter`:
session capability revocation, outbound network blocking, delegated-child containment,
and movement into an isolated quarantine boundary. The adapter is called by the
Siren control plane, outside the agent process; the agent cannot approve, veto,
or reverse these calls.

A result is `CONTAINED` only when every control explicitly returns `True`.
A false return, exception, or missing control is `PARTIALLY_CONTAINED`. The
orchestrator continues attempting remaining controls after an individual failure.
Repeated triggers for a session are idempotent within the controller instance.

## Deployment boundary and limitations

This Python package is the policy/orchestration layer, not a kernel sandbox,
firewall, container runtime, or process supervisor. A deployment must provide
and independently validate an adapter backed by an OS/network control plane
(e.g. revocable broker-issued capabilities, firewall or network-namespace
egress denial, process-tree supervision, and a dedicated quarantine runtime).
No adapter is bundled that can truthfully guarantee those host-level controls
on arbitrary machines or without the required privileges.

The child-session control must enumerate and revoke all delegated descendants
for the same session. If the adapter cannot prove complete enumeration, it must
return false. In-flight traffic and unobserved egress paths remain outside the
guarantee unless the host adapter controls them.

## Trigger and telemetry

A lure access or authorization-policy violation is supplied as a trigger to
`SentinelQuarantine.contain()`. The controller records the four control
outcomes, exceptions by type, trigger, and aggregate status to JSONL. It does
not record raw task context or secrets.

## Safety invariant

Never label a session fully contained based only on an agent instruction, a
tool response, a process-local flag, or a successful call to one control.
