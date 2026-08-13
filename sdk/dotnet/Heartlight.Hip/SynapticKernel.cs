namespace Heartlight.Hip;

public sealed record SynapticConfig(
    double LearningRate = 0.08,
    double Decay = 0.002,
    double TraceDecay = 0.9,
    double MinWeight = -1.0,
    double MaxWeight = 1.0
);

public readonly record struct SynapticState(double Weight, double Eligibility);
public readonly record struct SynapticInput(double Pre, double Post, double Reward = 1.0);

public static class SynapticKernel
{
    public const string Version = "1.0";

    public static SynapticState Step(SynapticState state, SynapticInput input, SynapticConfig? config = null)
    {
        config ??= new SynapticConfig();
        double[] values =
        [
            config.LearningRate, config.Decay, config.TraceDecay, config.MinWeight, config.MaxWeight,
            state.Weight, state.Eligibility, input.Pre, input.Post, input.Reward
        ];
        if (values.Any(v => !double.IsFinite(v)))
            throw new ArgumentOutOfRangeException(nameof(input), "HEARTLIGHT synaptic values must be finite");
        if (config.LearningRate < 0 || config.Decay is < 0 or > 1 || config.TraceDecay is < 0 or > 1 || config.MinWeight > config.MaxWeight)
            throw new ArgumentOutOfRangeException(nameof(config));

        var eligibility = config.TraceDecay * state.Eligibility + input.Pre * input.Post;
        var rawWeight = (1.0 - config.Decay) * state.Weight + config.LearningRate * input.Reward * eligibility;
        var weight = Math.Clamp(rawWeight, config.MinWeight, config.MaxWeight);
        return new SynapticState(weight, eligibility);
    }
}
