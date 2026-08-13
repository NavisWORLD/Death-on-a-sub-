using Heartlight.Hip;

namespace Heartlight.Hip.Tests;

public class SynapticKernelTests
{
    [Xunit.Fact]
    public void ConformanceV1()
    {
        var state = new SynapticState(0.2, 0.0);
        SynapticInput[] inputs =
        [
            new(0.5, 0.25, 1.0),
            new(1.0, -0.5, 0.4),
            new(0.2, 0.8, -0.25),
        ];
        double[] weights = [0.2096, 0.1967808, 0.2001622384];
        double[] traces = [0.125, -0.3875, -0.18875];
        for (var i = 0; i < inputs.Length; i++)
        {
            state = SynapticKernel.Step(state, inputs[i]);
            Xunit.Assert.InRange(Math.Abs(state.Weight - weights[i]), 0.0, 1e-12);
            Xunit.Assert.InRange(Math.Abs(state.Eligibility - traces[i]), 0.0, 1e-12);
        }
    }
}
