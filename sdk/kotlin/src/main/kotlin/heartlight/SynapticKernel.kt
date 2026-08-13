package heartlight

import kotlin.math.max
import kotlin.math.min

const val SYNAPTIC_KERNEL_VERSION: String = "1.0"

data class SynapticConfig(
    val learningRate: Double = 0.08,
    val decay: Double = 0.002,
    val traceDecay: Double = 0.9,
    val minWeight: Double = -1.0,
    val maxWeight: Double = 1.0,
)

data class SynapticState(val weight: Double = 0.0, val eligibility: Double = 0.0)
data class SynapticInput(val pre: Double, val post: Double, val reward: Double = 1.0)

fun synapticStep(
    state: SynapticState,
    input: SynapticInput,
    config: SynapticConfig = SynapticConfig(),
): SynapticState {
    val values = listOf(
        config.learningRate, config.decay, config.traceDecay, config.minWeight, config.maxWeight,
        state.weight, state.eligibility, input.pre, input.post, input.reward,
    )
    require(values.all { it.isFinite() }) { "HEARTLIGHT synaptic values must be finite" }
    require(config.learningRate >= 0.0)
    require(config.decay in 0.0..1.0)
    require(config.traceDecay in 0.0..1.0)
    require(config.minWeight <= config.maxWeight)

    val eligibility = config.traceDecay * state.eligibility + input.pre * input.post
    val rawWeight = (1.0 - config.decay) * state.weight + config.learningRate * input.reward * eligibility
    val weight = max(config.minWeight, min(config.maxWeight, rawWeight))
    return SynapticState(weight, eligibility)
}
