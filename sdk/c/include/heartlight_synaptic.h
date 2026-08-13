#ifndef HEARTLIGHT_SYNAPTIC_H
#define HEARTLIGHT_SYNAPTIC_H

#ifdef __cplusplus
extern "C" {
#endif

#define HEARTLIGHT_SYNAPTIC_KERNEL_VERSION "1.0"

typedef struct heartlight_synaptic_config {
    double learning_rate;
    double decay;
    double trace_decay;
    double min_weight;
    double max_weight;
} heartlight_synaptic_config;

typedef struct heartlight_synaptic_state {
    double weight;
    double eligibility;
} heartlight_synaptic_state;

typedef struct heartlight_synaptic_input {
    double pre;
    double post;
    double reward;
} heartlight_synaptic_input;

heartlight_synaptic_config heartlight_synaptic_default_config(void);
int heartlight_synaptic_step(
    heartlight_synaptic_state state,
    heartlight_synaptic_input input,
    heartlight_synaptic_config config,
    heartlight_synaptic_state* out_state
);

#ifdef __cplusplus
}
#endif

#endif
