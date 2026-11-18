"""Evidence report assembly with independent integrity, authorization, and causality."""

from __future__ import annotations

from typing import Any, Iterable

from siren_trap.causal_proof.evidence import ActionEvidence


def build_evidence_report(
    *,
    experiment_id: str,
    actions: Iterable[ActionEvidence],
    integrity_valid: bool,
    authorization_violation: bool,
    causal_evidence_supported: bool,
) -> dict[str, Any]:
    """Build a conservative report; no stage is inferred from a lower stage."""
    if not experiment_id:
        raise ValueError("experiment_id is required.")
    action_items = list(actions)
    return {
        "schema_version": "1.0",
        "experiment_id": experiment_id,
        "actions": [item.to_dict() for item in action_items],
        "verdicts": {
            "integrity": "PASS" if integrity_valid else "FAIL",
            "authorization": (
                "VIOLATION" if authorization_violation else "WITHIN_SCOPE"
            ),
            "causal_evidence": (
                "SUPPORTED" if causal_evidence_supported else "INSUFFICIENT"
            ),
        },
        "limitations": [
            "A tool invocation alone does not establish dispatch, receipt, or effect.",
            "Counterfactual evidence supports bounded causal inference, not access to model reasoning.",
            "External effects require independent receiver-side confirmation.",
        ],
    }
