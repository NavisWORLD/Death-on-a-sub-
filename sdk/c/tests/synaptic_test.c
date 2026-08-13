#include "heartlight_synaptic.h"

#include <assert.h>
#include <math.h>

int main(void) {
    heartlight_synaptic_config config = heartlight_synaptic_default_config();
    heartlight_synaptic_state state = {0.2, 0.0};
    const heartlight_synaptic_input samples[] = {
        {0.5, 0.25, 1.0},
        {1.0, -0.5, 0.4},
        {0.2, 0.8, -0.25},
    };
    const double weights[] = {0.2096, 0.1967808, 0.2001622384};
    const double traces[] = {0.125, -0.3875, -0.18875};
    for (int i = 0; i < 3; ++i) {
        heartlight_synaptic_state next;
        assert(heartlight_synaptic_step(state, samples[i], config, &next) == 0);
        assert(fabs(next.weight - weights[i]) < 1e-12);
        assert(fabs(next.eligibility - traces[i]) < 1e-12);
        state = next;
    }
    return 0;
}
