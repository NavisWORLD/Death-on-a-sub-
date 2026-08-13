package heartlight

import (
	"math"
	"testing"
)

func TestSynapticConformanceV1(t *testing.T) {
	state := SynapticState{Weight: 0.2, Eligibility: 0.0}
	inputs := []SynapticInput{{0.5, 0.25, 1.0}, {1.0, -0.5, 0.4}, {0.2, 0.8, -0.25}}
	weights := []float64{0.2096, 0.1967808, 0.2001622384}
	traces := []float64{0.125, -0.3875, -0.18875}
	for i, input := range inputs {
		state = SynapticStep(state, input, DefaultSynapticConfig())
		if math.Abs(state.Weight-weights[i]) >= 1e-12 || math.Abs(state.Eligibility-traces[i]) >= 1e-12 {
			t.Fatalf("step %d mismatch: %+v", i, state)
		}
	}
}
