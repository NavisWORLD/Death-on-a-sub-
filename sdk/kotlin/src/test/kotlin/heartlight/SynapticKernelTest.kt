package heartlight

import kotlin.math.abs
import kotlin.test.Test
import kotlin.test.assertTrue

class SynapticKernelTest {
    @Test
    fun conformanceV1() {
        var state = SynapticState(0.2, 0.0)
        val inputs = listOf(
            SynapticInput(0.5, 0.25, 1.0),
            SynapticInput(1.0, -0.5, 0.4),
            SynapticInput(0.2, 0.8, -0.25),
        )
        val weights = listOf(0.2096, 0.1967808, 0.2001622384)
        val traces = listOf(0.125, -0.3875, -0.18875)
        inputs.forEachIndexed { index, input ->
            state = synapticStep(state, input)
            assertTrue(abs(state.weight - weights[index]) < 1e-12)
            assertTrue(abs(state.eligibility - traces[index]) < 1e-12)
        }
    }
}
