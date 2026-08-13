#pragma once

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace heartlight {

inline constexpr const char* SYNAPTIC_KERNEL_VERSION = "1.0";

struct SynapticConfig {
    double learning_rate{0.08};
    double decay{0.002};
    double trace_decay{0.9};
    double min_weight{-1.0};
    double max_weight{1.0};
};

struct SynapticState {
    double weight{0.0};
    double eligibility{0.0};
};

struct SynapticInput {
    double pre{};
    double post{};
    double reward{1.0};
};

inline SynapticState synaptic_step(SynapticState state, SynapticInput sample, SynapticConfig config = {}) {
    const auto finite = [](double value) { return std::isfinite(value); };
    if (!finite(config.learning_rate) || config.learning_rate < 0.0 ||
        !finite(config.decay) || config.decay < 0.0 || config.decay > 1.0 ||
        !finite(config.trace_decay) || config.trace_decay < 0.0 || config.trace_decay > 1.0 ||
        !finite(config.min_weight) || !finite(config.max_weight) || config.min_weight > config.max_weight ||
        !finite(state.weight) || !finite(state.eligibility) ||
        !finite(sample.pre) || !finite(sample.post) || !finite(sample.reward)) {
        throw std::invalid_argument("invalid HEARTLIGHT synaptic value");
    }

    const double eligibility = config.trace_decay * state.eligibility + sample.pre * sample.post;
    const double raw_weight = (1.0 - config.decay) * state.weight
        + config.learning_rate * sample.reward * eligibility;
    return {std::clamp(raw_weight, config.min_weight, config.max_weight), eligibility};
}

} // namespace heartlight
