package heartlight

import "math"

const SynapticKernelVersion = "1.0"

type SynapticConfig struct {
	LearningRate float64 `json:"learning_rate"`
	Decay        float64 `json:"decay"`
	TraceDecay   float64 `json:"trace_decay"`
	MinWeight    float64 `json:"min_weight"`
	MaxWeight    float64 `json:"max_weight"`
}

type SynapticState struct {
	Weight      float64 `json:"weight"`
	Eligibility float64 `json:"eligibility"`
}

type SynapticInput struct {
	Pre    float64 `json:"pre"`
	Post   float64 `json:"post"`
	Reward float64 `json:"reward"`
}

func DefaultSynapticConfig() SynapticConfig {
	return SynapticConfig{LearningRate: 0.08, Decay: 0.002, TraceDecay: 0.9, MinWeight: -1.0, MaxWeight: 1.0}
}

func SynapticStep(state SynapticState, input SynapticInput, config SynapticConfig) SynapticState {
	values := []float64{config.LearningRate, config.Decay, config.TraceDecay, config.MinWeight, config.MaxWeight, state.Weight, state.Eligibility, input.Pre, input.Post, input.Reward}
	for _, value := range values {
		if math.IsNaN(value) || math.IsInf(value, 0) {
			panic("HEARTLIGHT synaptic values must be finite")
		}
	}
	if config.LearningRate < 0 || config.Decay < 0 || config.Decay > 1 || config.TraceDecay < 0 || config.TraceDecay > 1 || config.MinWeight > config.MaxWeight {
		panic("invalid HEARTLIGHT synaptic config")
	}
	eligibility := config.TraceDecay*state.Eligibility + input.Pre*input.Post
	weight := (1-config.Decay)*state.Weight + config.LearningRate*input.Reward*eligibility
	weight = math.Max(config.MinWeight, math.Min(config.MaxWeight, weight))
	return SynapticState{Weight: weight, Eligibility: eligibility}
}
