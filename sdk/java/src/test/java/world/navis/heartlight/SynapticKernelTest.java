package world.navis.heartlight;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class SynapticKernelTest {
    @Test
    void conformanceV1() {
        var state = new SynapticKernel.State(0.2, 0.0);
        var inputs = new SynapticKernel.Input[] {
            new SynapticKernel.Input(0.5, 0.25, 1.0),
            new SynapticKernel.Input(1.0, -0.5, 0.4),
            new SynapticKernel.Input(0.2, 0.8, -0.25)
        };
        double[] weights = {0.2096, 0.1967808, 0.2001622384};
        double[] traces = {0.125, -0.3875, -0.18875};
        for (int i = 0; i < inputs.length; i++) {
            state = SynapticKernel.step(state, inputs[i]);
            assertEquals(weights[i], state.weight(), 1e-12);
            assertEquals(traces[i], state.eligibility(), 1e-12);
        }
    }
}
