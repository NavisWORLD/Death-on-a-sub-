export const SYNAPTIC_KERNEL_VERSION = "1.0" as const;

export type SynapticConfig = {
  learning_rate: number;
  decay: number;
  trace_decay: number;
  min_weight: number;
  max_weight: number;
};

export type SynapticState = { weight: number; eligibility: number };
export type SynapticInput = { pre: number; post: number; reward: number };

export const defaultSynapticConfig = (): SynapticConfig => ({
  learning_rate: 0.08,
  decay: 0.002,
  trace_decay: 0.9,
  min_weight: -1.0,
  max_weight: 1.0,
});

export function synapticStep(
  state: SynapticState,
  input: SynapticInput,
  config: SynapticConfig = defaultSynapticConfig(),
): SynapticState {
  const values = [
    config.learning_rate,
    config.decay,
    config.trace_decay,
    config.min_weight,
    config.max_weight,
    state.weight,
    state.eligibility,
    input.pre,
    input.post,
    input.reward,
  ];
  if (!values.every(Number.isFinite)) throw new TypeError("HEARTLIGHT synaptic values must be finite");
  if (
    config.learning_rate < 0 ||
    config.decay < 0 || config.decay > 1 ||
    config.trace_decay < 0 || config.trace_decay > 1 ||
    config.min_weight > config.max_weight
  ) throw new RangeError("invalid HEARTLIGHT synaptic config");

  const eligibility = config.trace_decay * state.eligibility + input.pre * input.post;
  const rawWeight = (1 - config.decay) * state.weight + config.learning_rate * input.reward * eligibility;
  const weight = Math.max(config.min_weight, Math.min(config.max_weight, rawWeight));
  return { weight, eligibility };
}
