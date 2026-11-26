# Siren

**Active semantic-lure and evidence research for defensive AI-agent security.**

[![CI](https://github.com/zopair/Siren/actions/workflows/ci.yml/badge.svg)](https://github.com/zopair/Siren/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research PoC](https://img.shields.io/badge/Status-Research%20PoC-orange.svg)](#proof-of-concept--enterprise-customization-readiness)

**Live documentation:** [https://zopair.github.io/Siren/](https://zopair.github.io/Siren/)  
**Source code:** [https://github.com/zopair/Siren](https://github.com/zopair/Siren)

> **Status and safety boundary:** Siren is a research proof of concept. The repository includes a fixed synthetic lure catalog, read-only Flask and MCP interfaces, acoustic canary generation, event telemetry, Sentinel containment orchestration, counterfactual evidence code, and a deterministic simulation. The local simulation does not provide operating-system or network isolation. A deployment-owned enforcement adapter is required before any real containment guarantee can be made.

## 1. Project Overview & Problem Statement

AI agents consume documents, retrieved web content, tool descriptions, audio, and delegated task context. Untrusted content can contain instructions that an agent may mistake for authorized commands. Monitoring alone does not establish whether an action was attempted, blocked, executed, or causally influenced by a particular input.

Siren explores a defensive research workflow that:

1. Presents controlled, context-relevant synthetic decoys (semantic lures and an acoustic canary).
2. Records lure interactions and related events as structured telemetry.
3. Applies an explicit containment policy through an injected enforcement adapter.
4. Compares controlled experimental conditions.
5. Produces evidence reports that distinguish observed attempts from confirmed external effects.

**Intended users:** AI security researchers, agent-platform engineers, red-team and defensive-testing teams, and developers evaluating trust boundaries in agent workflows.

**Research workflow:**

```mermaid
flowchart TD
    A[Agent task context] --> B[Fixed synthetic lure catalog]
    B --> C{Lure interaction?}
    C -->|No| D[Continue observation]
    C -->|Yes| E[Record event]
    E --> F[Sentinel policy orchestration]
    F --> G[Deployment-owned enforcement adapter]
    E --> H[Counterfactual experiment]
    G --> H
    H --> I[Evidence report]
```

## 2. Tech Stack & Versions

Versions and constraints below are taken from `pyproject.toml`, `requirements.txt`, `.python-version`, and the GitHub Actions workflows. Where a dependency is expressed as a range, no single installed version is claimed.

| Area | Technology | Version / constraint |
|---|---|---|
| Language | Python | `>=3.11`; CI matrix: 3.11, 3.12, 3.13 |
| Package/build | setuptools | `>=77` |
| Build helper | wheel | Declared in the build system; version not pinned |
| Web service | Flask | `>=3.1,<4.0` |
| Acoustic encoding | ggwave | `>=0.4.2,<0.5.0` |
| Test runner | pytest | `>=8,<10` (development extra) |
| Coverage | pytest-cov | `>=5,<8` (development extra) |
| Lint | Ruff | `>=0.9,<1` (development extra) |
| Browser screenshots | Playwright | Installed by the live-demo workflow without a version pin |
| MCP adapter | Python standard library | Custom read-only JSON-RPC stdio adapter; no additional MCP package |
| Static documentation | HTML and CSS | GitHub Pages; no frontend framework or build package |
| CI | GitHub Actions | Python matrix 3.11 / 3.12 / 3.13 |

## 3. Prerequisites & Dependencies

### Required for local development

- Git.
- Python 3.11 or newer.
- `venv` and `pip`.
- A supported operating system.

### Installed project dependencies

- Flask 3.1-compatible release.
- ggwave 0.4.x compatible release.

### Development dependencies

- pytest 8.x or 9.x within the declared range.
- pytest-cov 5.x, 6.x, or 7.x within the declared range.
- Ruff 0.9.x within the declared range.

The optional live visual demo workflow also installs Playwright and Chromium. The normal test suite does not require a third-party model, GPU, container runtime, cloud service, or paid API.

## 4. Installation & Local Setup (Step-by-Step)

### 1. Clone the repository

```bash
git clone https://github.com/zopair/Siren.git
cd Siren
```

### 2. Create and activate a virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the project and development tools

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 4. Run the test suite

```bash
python -m pytest
```

### 5. Generate the fixed acoustic canary (optional)

```bash
python -m siren_trap.payload_generator.build_trap --output assets/audio/canary.wav
```

The generator emits a fixed harmless research marker. It does not accept arbitrary payload text.

### 6. Start the local decoy service

```bash
python -m siren_trap.decoy_firewall.app
```

By default, the service binds to `127.0.0.1:5000`. Keep it local to an authorized experiment; it is not configured as a public production service.

### 7. Run the deterministic reference simulation (optional)

```bash
python benchmarks/run_live_demo.py --output-dir benchmarks/results
```

This runs a synthetic in-process experiment. It does not launch an external AI model, open network sockets, or provide host-level process/network isolation.

## 5. Environment Variables

No API keys, access tokens, or external service credentials are required.

The local Flask service reads these optional variables:

| Variable | Purpose | Default / safe example |
|---|---|---|
| `SIREN_HOST` | Local Flask bind address | `127.0.0.1` |
| `SIREN_PORT` | Local Flask port | `5000` |
| `SIREN_LOG_DIR` | Directory for JSONL event logs | `logs` |

Example for Linux / macOS:

```bash
export SIREN_HOST=127.0.0.1
export SIREN_PORT=5000
export SIREN_LOG_DIR=logs
python -m siren_trap.decoy_firewall.app
```

Example for Windows PowerShell:

```powershell
$env:SIREN_HOST = "127.0.0.1"
$env:SIREN_PORT = "5000"
$env:SIREN_LOG_DIR = "logs"
python -m siren_trap.decoy_firewall.app
```

The static documentation website requires no environment variables. Do not expose the Flask service to untrusted networks without implementing and independently reviewing authentication, rate limiting, deployment isolation, and operational controls.

## 6. Usage Guide & Core Features

### A. Explore the semantic lure catalog

With the local service running:

```bash
curl "http://127.0.0.1:5000/api/lures?context=financial%20report"
```

Open one known synthetic fixture:

```bash
curl "http://127.0.0.1:5000/api/lures/consolidated-finance-index"
```

The catalog is deterministic and in-memory. It returns fixed synthetic content and does not resolve arbitrary filesystem paths or contact external services.

### B. Use the read-only MCP tools

After installing the package, configure an MCP client to launch:

```bash
siren-mcp
```

The stdio adapter exposes two read-only tools:

- `list_siren_lures`
- `open_siren_lure`

It uses the Python standard library and communicates through JSON-RPC over standard input/output. Keep it local to an authorized experiment.

### C. Generate an acoustic canary

Run the generator from the repository root:

```bash
python -m siren_trap.payload_generator.build_trap --output assets/audio/canary.wav
```

The marker is fixed in source code; arbitrary commands or user-supplied payloads are not accepted.

### D. Review telemetry and evidence

- JSONL event logging records structured experiment events.
- The causal-proof package reconstructs events and produces evidence-oriented reports.
- The benchmark runner creates a deterministic synthetic A/B/C demonstration and report artifacts.

### E. Understand the containment boundary

Sentinel is a policy/orchestration layer. It calls an injected enforcement adapter for session revocation, egress blocking, delegated-child containment, and quarantine. The repository does **not** ship a host-level firewall, process supervisor, kernel sandbox, or production enforcement adapter. The synthetic demo uses an in-memory simulator and must not be represented as real containment.

The expanded research narrative from the previous README has been preserved in [Expanded Research Reference](docs/EXPANDED_RESEARCH_REFERENCE.md), so the concise setup guide does not discard the earlier technical explanation.

Detailed technical references:

- [Architecture](docs/ARCHITECTURE.md)
- [Semantic lure engine](docs/SIREN_LURE.md)
- [Containment model and deployment requirements](docs/CONTAINMENT_MODEL.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Causal evidence](docs/CAUSAL_EVIDENCE.md)
- [Research methodology](docs/RESEARCH_METHODOLOGY.md)
- [Acoustic testing](docs/ACOUSTIC_TESTING.md)

## 7. Live Demo & Screenshots

- **Live documentation site:** [https://zopair.github.io/Siren/](https://zopair.github.io/Siren/)
- **Repository:** [https://github.com/zopair/Siren](https://github.com/zopair/Siren)
- **Live-demo workflow:** [Siren Live Visual Demo](https://github.com/zopair/Siren/actions/workflows/live-demo.yml)
- **Pages deployment workflow:** [Deploy Siren-Trap documentation](https://github.com/zopair/Siren/actions/workflows/pages.yml)

The Pages site is a static research documentation site. The live visual demo workflow is a separate, manually dispatchable GitHub Actions workflow that generates synthetic evidence and screenshots; it is not a continuously running online agent service.

### Existing screenshots

![Siren terminal demo screenshot](docs/assets/screenshots/terminal_demo.png)

![Siren synthetic evidence report screenshot](docs/assets/screenshots/evidence_report.png)

![Siren architecture diagram](docs/assets/siren-trap-architecture.svg)

The terminal and evidence screenshots are generated from the synthetic simulation. They do not demonstrate a real external agent or host-level containment.

## 8. Testing & Verification

### Local automated checks

Install development dependencies, then run:

```bash
python -m ruff check .
python -m pytest --cov=siren_trap --cov-report=term-missing
```

For a concise test run without coverage:

```bash
python -m pytest
```

### Manual service verification

Start the local Flask service, then check health:

```bash
curl http://127.0.0.1:5000/health
```

Check the lure catalog:

```bash
curl "http://127.0.0.1:5000/api/lures?context=financial%20report"
```

Check a known synthetic fixture:

```bash
curl http://127.0.0.1:5000/api/lures/consolidated-finance-index
```

### CI verification

The CI workflow runs Ruff and pytest with coverage on Python 3.11, 3.12, and 3.13. See [the CI workflow](.github/workflows/ci.yml) for the exact matrix and commands.

The Pages workflow validates the static documentation files and metadata before deployment. The live-demo workflow runs the synthetic experiment, validates that no external network was used and that enforcement was simulated, captures Chromium screenshots, and uploads the evidence bundle.

## Proof of Concept & Enterprise Customization Readiness

**Status:** Research PoC / early-stage framework. Suitable for controlled experiments, code review, and extension by security engineering teams. It is not a production-ready agent-containment product.

Enterprise customization would require a separately engineered and independently tested enforcement adapter, authenticated deployment gateway, host/network isolation controls, access policy, tamper-resistant evidence storage, operational monitoring, and a deployment-specific threat review. These are requirements for future integration, not features claimed as complete.

## Intellectual Property & Authorship

Original project research and implementation: **Aly Hussein Zopair (علي حسين زبير ALY HUSSEIN ZOPAIR)**.

Siren is released under the repository's MIT license. Third-party packages, tools, and assets remain subject to their respective licenses and notices. See [LICENSE](LICENSE), [AUTHORS.md](AUTHORS.md), and [CITATION.cff](CITATION.cff).
