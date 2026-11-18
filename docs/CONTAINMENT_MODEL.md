# Sentinel Containment Model

**Status: planned for delivery batch 2.**

This document reserves the design boundary for external session containment.
The batch-1 lure service does not isolate an agent, terminate a session, control
delegated tools, or guarantee network-egress prevention.

The implementation must enforce policy outside the agent process, default-deny
access to real resources, and document every execution channel not covered by
the enforcement point. Containment claims must be based on observed enforcement
events, not on a decoy response or an instruction asking an agent to stop.

Required outcome states: `CONTAINED`, `PARTIALLY_CONTAINED`,
`NOT_CONTAINED`, and `UNKNOWN`.
