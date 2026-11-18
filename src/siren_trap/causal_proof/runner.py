"""Controlled three-condition counterfactual experiment orchestration."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Mapping


class RunCondition(str, Enum):
    BASELINE = "A_BASELINE"
    TREATMENT = "B_TREATMENT"
    COUNTERFACTUAL = "C_COUNTERFACTUAL"


@dataclass(frozen=True)
class ExperimentConfig:
    """Immutable factors held constant across paired experiment conditions."""

    experiment_id: str
    model: str
    model_version: str
    toolset: tuple[str, ...]
    authorization_fingerprint: str
    dataset_fingerprint: str

    def __post_init__(self) -> None:
        if not all((
            self.experiment_id, self.model, self.model_version,
            self.authorization_fingerprint, self.dataset_fingerprint,
        )):
            raise ValueError("Experiment identity and fingerprints are required.")
        if not self.toolset:
            raise ValueError("A fixed toolset is required.")

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RunConfig:
    """Per-condition configuration; only source_removed may differ."""

    base: ExperimentConfig
    source_removed: bool


@dataclass(frozen=True)
class RunResult:
    condition: RunCondition
    configuration_valid: bool
    observed_configuration_fingerprint: str | None
    observation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "condition": self.condition.value,
            "configuration_valid": self.configuration_valid,
            "observed_configuration_fingerprint": (
                self.observed_configuration_fingerprint
            ),
            "observation": self.observation,
        }


def run_counterfactual(
    config: ExperimentConfig,
    execute: Callable[[RunCondition, RunConfig], Mapping[str, Any]],
    *,
    reset: Callable[[], None],
) -> list[RunResult]:
    """Run A/B/C from clean state and validate the fixed-factor fingerprint.

    The caller-supplied reset callback must restore a fresh agent/session/tool
    state before every condition. The executor must report the fingerprint of
    the effective non-treatment configuration in its returned mapping.
    """
    if not callable(reset) or not callable(execute):
        raise TypeError("execute and reset must be callable.")

    results = []
    conditions = (
        RunCondition.BASELINE,
        RunCondition.TREATMENT,
        RunCondition.COUNTERFACTUAL,
    )
    for condition in conditions:
        reset()
        run_config = RunConfig(
            base=config,
            source_removed=condition is RunCondition.COUNTERFACTUAL,
        )
        observation = execute(condition, run_config)
        if not isinstance(observation, Mapping):
            raise TypeError("Experiment executor must return a mapping.")
        observed = observation.get("configuration_fingerprint")
        observed_fingerprint = observed if isinstance(observed, str) else None
        results.append(
            RunResult(
                condition=condition,
                configuration_valid=observed_fingerprint == config.fingerprint,
                observed_configuration_fingerprint=observed_fingerprint,
                observation=dict(observation),
            )
        )
    return results
