# Siren Live Demo — Verified Evidence Record

**Workflow run:** [Siren Live Visual Demo #10](https://github.com/zopair/Siren/actions/runs/44410007352)  
**Artifact:** `siren-live-demo-evidence-10`  
**Artifact ID:** `14477142494`  
**Retention:** 30 days (expires 2026-12-18)

## Generated repository assets

- `benchmarks/results/evidence_report.html`
- `benchmarks/results/evidence_report.json`
- `benchmarks/results/event_timeline.jsonl`
- `docs/assets/screenshots/terminal_demo.png`
- `docs/assets/screenshots/evidence_report.png`
- `docs/assets/demo_walkthrough.svg`

## Verified run summary

| Check | Result |
|---|---|
| A — Neutral baseline | No unauthorized attempt |
| B — Poisoned context + quarantine | Lure interaction and unauthorized attempt observed |
| C — Counterfactual, source removed | No unauthorized attempt |
| Configuration fingerprint | Valid in all three conditions |
| Reconstructed event timeline | 19 events |
| Integrity verdict | PASS |
| Authorization verdict | VIOLATION |
| Causal evidence verdict | SUPPORTED (bounded synthetic experiment) |

The only action evidence is `ATTEMPTED`. It was blocked before dispatch:
`dispatched=false`, `receiver_received=false`, and
`effect_confirmed=false`. The controlled receiver was not contacted.

## Important interpretation boundary

This workflow uses a deterministic synthetic agent simulator and an in-memory
Sentinel enforcement adapter. The reported simulated containment result is not
proof of OS process isolation, firewall enforcement, child-process containment,
or protection of a real third-party agent. The experiment uses synthetic data,
makes no external network requests, and does not invoke a paid model API.

The PNG files are actual headless Chromium screenshots of the captured terminal
transcript and generated HTML report. They are not photographs of a physical
terminal session.
