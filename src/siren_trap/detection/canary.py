"""Detection of the fixed research canary in untrusted observations."""

from dataclasses import dataclass

CANARY_MARKER = "SIREN-CANARY-TEST-001"


@dataclass(frozen=True)
class CanaryResult:
    detected: bool
    marker: str | None
    category: str


def inspect_observation(content: str) -> CanaryResult:
    """Detect the marker; never interpret or execute observation content."""
    if not isinstance(content, str):
        raise TypeError("Observation must be text.")
    detected = CANARY_MARKER in content
    return CanaryResult(
        detected=detected,
        marker=CANARY_MARKER if detected else None,
        category="CANARY_OBSERVED" if detected else "NO_MATCH",
    )
