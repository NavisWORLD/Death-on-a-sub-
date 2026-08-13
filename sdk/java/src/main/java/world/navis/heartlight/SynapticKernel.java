package world.navis.heartlight;

public final class SynapticKernel {
    public static final String VERSION = "1.0";

    public record Config(double learningRate, double decay, double traceDecay, double minWeight, double maxWeight) {
        public Config() { this(0.08, 0.002, 0.9, -1.0, 1.0); }
    }

    public record State(double weight, double eligibility) {}
    public record Input(double pre, double post, double reward) {}

    private SynapticKernel() {}

    public static State step(State state, Input input) {
        return step(state, input, new Config());
    }

    public static State step(State state, Input input, Config config) {
        double[] values = {
            config.learningRate(), config.decay(), config.traceDecay(), config.minWeight(), config.maxWeight(),
            state.weight(), state.eligibility(), input.pre(), input.post(), input.reward()
        };
        for (double value : values) {
            if (!Double.isFinite(value)) throw new IllegalArgumentException("HEARTLIGHT synaptic values must be finite");
        }
        if (config.learningRate() < 0 || config.decay() < 0 || config.decay() > 1 ||
            config.traceDecay() < 0 || config.traceDecay() > 1 || config.minWeight() > config.maxWeight()) {
            throw new IllegalArgumentException("invalid HEARTLIGHT synaptic config");
        }
        double eligibility = config.traceDecay() * state.eligibility() + input.pre() * input.post();
        double rawWeight = (1.0 - config.decay()) * state.weight() + config.learningRate() * input.reward() * eligibility;
        double weight = Math.max(config.minWeight(), Math.min(config.maxWeight(), rawWeight));
        return new State(weight, eligibility);
    }
}
