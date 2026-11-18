# Siren Live Benchmark

Run the deterministic, synthetic reference experiment:

```bash
python benchmarks/run_live_demo.py
```

The command writes `evidence_report.json`, `evidence_report.html`,
`event_timeline.jsonl`, and a terminal transcript under `benchmarks/results/`.

The simulator compares A (neutral baseline), B (poisoned context + immediate
simulated quarantine), and C (counterfactual with the poisoned source removed).
It uses fixed synthetic fixtures, a fresh state reset for each condition, and a
configuration fingerprint shared across runs. No model API, credentials,
external network, or real receiver are used.

GitHub Actions runs the demo, captures Chromium screenshots, commits generated
visual evidence to this feature branch, and uploads the evidence bundle as a
30-day workflow artifact.

**Important:** Sentinel is exercised with an in-memory fake enforcement adapter.
A `CONTAINED` response in this demo is only a simulator result; it is not proof
of OS process isolation, firewall enforcement, or containment of a real agent.
The transfer attempt is recorded as `ATTEMPTED` and blocked before dispatch;
no receiver is contacted.
