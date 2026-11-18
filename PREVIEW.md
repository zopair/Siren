# Siren-Trap — Preview Readiness

## What to preview
Siren-Trap is an alpha defensive research framework for controlled acoustic canary experiments, local decoy observation, and privacy-conscious security telemetry. It is not an agent-control product or production containment system.

## Fast local preview
Requirements: Python 3.11–3.13 and a platform supported by the upstream ggwave package.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest --cov=siren_trap --cov-report=term-missing
python -m siren_trap.payload_generator.build_trap --output assets/audio/canary.wav
python -m siren_trap.decoy_firewall.app
```

Open http://127.0.0.1:5000 on the same machine. Analyze only an authorized, controlled 16-bit PCM WAV recording with sample rate above 40 kHz.

## Suggested 5-minute walkthrough
1. Explain the threat model and the fixed inert marker.
2. Generate the test WAV artifact.
3. Open the loopback-only decoy service.
4. Submit a benign observation containing the known marker and inspect the detection result.
5. Review JSONL telemetry and passive spectral-analysis output.
6. Explain the difference between artifact generation, transport, decoding, observation, and policy handling.

## Preview acceptance
- [ ] Ruff and the complete pytest suite pass.
- [ ] Canary artifact is generated and its hash recorded.
- [ ] Decoy service binds to loopback by default.
- [ ] Detection never executes or follows marker content.
- [ ] Telemetry excludes secrets and unrelated personal data.
- [ ] Hardware/receiver limitations are stated in the demo.

## Known limits to disclose
The project is an alpha research prototype. A generated WAV or spectral peak does not prove audibility, successful transmission, receiver compatibility, decoding, agent interpretation, or policy failure. Encoder/decoder round-trip validation, hardware compatibility matrix, reproducible agent-evaluation adapters, and an independently reviewed isolated deployment profile remain pending. Never expose the decoy service without a separate security review.

## Reviewer evidence
Attach CI results, Python/platform versions, artifact SHA-256, sanitized JSONL events, and a short recording of the local-only demonstration. Do not upload raw microphone recordings without a reviewed need and consent.
