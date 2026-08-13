from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

SYNAPTIC_KERNEL_VERSION = "1.0"


@dataclass(frozen=True, slots=True)
class SynapticConfig:
    learning_rate: float = 0.08
    decay: float = 0.002
    trace_decay: float = 0.9
    min_weight: float = -1.0
    max_weight: float = 1.0

    def validate(self) -> None:
        values = (
            self.learning_rate,
            self.decay,
            self.trace_decay,
            self.min_weight,
            self.max_weight,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("synaptic config values must be finite")
        if self.learning_rate < 0.0:
            raise ValueError("learning_rate must be >= 0")
        if not 0.0 <= self.decay <= 1.0:
            raise ValueError("decay must be between 0 and 1")
        if not 0.0 <= self.trace_decay <= 1.0:
            raise ValueError("trace_decay must be between 0 and 1")
        if self.min_weight > self.max_weight:
            raise ValueError("min_weight must be <= max_weight")


@dataclass(frozen=True, slots=True)
class SynapticState:
    weight: float = 0.0
    eligibility: float = 0.0


@dataclass(frozen=True, slots=True)
class SynapticInput:
    pre: float
    post: float
    reward: float = 1.0


def synaptic_step(
    state: SynapticState,
    sample: SynapticInput,
    config: SynapticConfig | None = None,
) -> SynapticState:
    """Advance one deterministic reward-modulated eligibility-trace synapse.

    e[t+1] = trace_decay * e[t] + pre * post
    w[t+1] = clamp((1-decay) * w[t] + learning_rate * reward * e[t+1])
    """

    cfg = config or SynapticConfig()
    cfg.validate()
    values = (state.weight, state.eligibility, sample.pre, sample.post, sample.reward)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("synaptic state and input values must be finite")

    eligibility = cfg.trace_decay * state.eligibility + sample.pre * sample.post
    weight = (1.0 - cfg.decay) * state.weight + cfg.learning_rate * sample.reward * eligibility
    weight = min(cfg.max_weight, max(cfg.min_weight, weight))
    return SynapticState(weight=weight, eligibility=eligibility)


def synaptic_batch(
    state: SynapticState,
    samples: Iterable[SynapticInput],
    config: SynapticConfig | None = None,
) -> SynapticState:
    cfg = config or SynapticConfig()
    current = state
    for sample in samples:
        current = synaptic_step(current, sample, cfg)
    return current
