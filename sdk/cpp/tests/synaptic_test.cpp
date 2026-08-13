#include <cassert>
#include <cmath>
#include "heartlight/synaptic.hpp"

int main() {
    heartlight::SynapticState state{0.2, 0.0};
    const heartlight::SynapticInput samples[] = {
        {0.5, 0.25, 1.0},
        {1.0, -0.5, 0.4},
        {0.2, 0.8, -0.25},
    };
    const double weights[] = {0.2096, 0.1967808, 0.2001622384};
    const double traces[] = {0.125, -0.3875, -0.18875};
    for (int i = 0; i < 3; ++i) {
        state = heartlight::synaptic_step(state, samples[i]);
        assert(std::abs(state.weight - weights[i]) < 1e-12);
        assert(std::abs(state.eligibility - traces[i]) < 1e-12);
    }
    return 0;
}
