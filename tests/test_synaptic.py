from __future__ import annotations

import json
from pathlib import Path

import pytest

from heartlight import SynapticConfig, SynapticInput, SynapticState, synaptic_step


def test_synaptic_v1_conformance_fixture() -> None:
    fixture_path = Path(__file__).parents[1] / "sdk" / "conformance" / "synaptic-v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    config = SynapticConfig(**fixture["config"])
    state = SynapticState(**fixture["initial_state"])

    for sample_data, expected in zip(fixture["steps"], fixture["expected_states"], strict=True):
        state = synaptic_step(state, SynapticInput(**sample_data), config)
        assert state.weight == pytest.approx(expected["weight"], abs=1e-12)
        assert state.eligibility == pytest.approx(expected["eligibility"], abs=1e-12)


def test_synaptic_clamps_weight() -> None:
    config = SynapticConfig(learning_rate=10.0)
    state = synaptic_step(SynapticState(0.9, 0.0), SynapticInput(1.0, 1.0, 1.0), config)
    assert state.weight == 1.0
