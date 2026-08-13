#include "heartlight_synaptic.h"

#include <math.h>

heartlight_synaptic_config heartlight_synaptic_default_config(void) {
    heartlight_synaptic_config config = {0.08, 0.002, 0.9, -1.0, 1.0};
    return config;
}

static double clamp_weight(double value, double min_weight, double max_weight) {
    if (value < min_weight) return min_weight;
    if (value > max_weight) return max_weight;
    return value;
}

int heartlight_synaptic_step(
    heartlight_synaptic_state state,
    heartlight_synaptic_input input,
    heartlight_synaptic_config config,
    heartlight_synaptic_state* out_state
) {
    if (!out_state || !isfinite(config.learning_rate) || config.learning_rate < 0.0 ||
        !isfinite(config.decay) || config.decay < 0.0 || config.decay > 1.0 ||
        !isfinite(config.trace_decay) || config.trace_decay < 0.0 || config.trace_decay > 1.0 ||
        !isfinite(config.min_weight) || !isfinite(config.max_weight) || config.min_weight > config.max_weight ||
        !isfinite(state.weight) || !isfinite(state.eligibility) ||
        !isfinite(input.pre) || !isfinite(input.post) || !isfinite(input.reward)) {
        return -1;
    }

    out_state->eligibility = config.trace_decay * state.eligibility + input.pre * input.post;
    out_state->weight = clamp_weight(
        (1.0 - config.decay) * state.weight + config.learning_rate * input.reward * out_state->eligibility,
        config.min_weight,
        config.max_weight
    );
    return 0;
}
