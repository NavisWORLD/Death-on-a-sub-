use serde::{Deserialize, Serialize};

pub const SYNAPTIC_KERNEL_VERSION: &str = "1.0";

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub struct SynapticConfig {
    pub learning_rate: f64,
    pub decay: f64,
    pub trace_decay: f64,
    pub min_weight: f64,
    pub max_weight: f64,
}

impl Default for SynapticConfig {
    fn default() -> Self {
        Self {
            learning_rate: 0.08,
            decay: 0.002,
            trace_decay: 0.9,
            min_weight: -1.0,
            max_weight: 1.0,
        }
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub struct SynapticState {
    pub weight: f64,
    pub eligibility: f64,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub struct SynapticInput {
    pub pre: f64,
    pub post: f64,
    pub reward: f64,
}

pub fn synaptic_step(state: SynapticState, sample: SynapticInput, config: SynapticConfig) -> SynapticState {
    assert!(config.learning_rate.is_finite() && config.learning_rate >= 0.0);
    assert!(config.decay.is_finite() && (0.0..=1.0).contains(&config.decay));
    assert!(config.trace_decay.is_finite() && (0.0..=1.0).contains(&config.trace_decay));
    assert!(config.min_weight.is_finite() && config.max_weight.is_finite());
    assert!(config.min_weight <= config.max_weight);
    assert!(state.weight.is_finite() && state.eligibility.is_finite());
    assert!(sample.pre.is_finite() && sample.post.is_finite() && sample.reward.is_finite());

    let eligibility = config.trace_decay * state.eligibility + sample.pre * sample.post;
    let weight = ((1.0 - config.decay) * state.weight
        + config.learning_rate * sample.reward * eligibility)
        .clamp(config.min_weight, config.max_weight);
    SynapticState { weight, eligibility }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn conformance_v1() {
        let config = SynapticConfig::default();
        let mut state = SynapticState { weight: 0.2, eligibility: 0.0 };
        let steps = [
            (SynapticInput { pre: 0.5, post: 0.25, reward: 1.0 }, 0.2096, 0.125),
            (SynapticInput { pre: 1.0, post: -0.5, reward: 0.4 }, 0.1967808, -0.3875),
            (SynapticInput { pre: 0.2, post: 0.8, reward: -0.25 }, 0.2001622384, -0.18875),
        ];
        for (sample, expected_weight, expected_eligibility) in steps {
            state = synaptic_step(state, sample, config);
            assert!((state.weight - expected_weight).abs() < 1e-12);
            assert!((state.eligibility - expected_eligibility).abs() < 1e-12);
        }
    }
}
