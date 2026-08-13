import Foundation

public let SYNAPTIC_KERNEL_VERSION = "1.0"

public struct SynapticConfig: Codable, Sendable {
    public var learningRate: Double
    public var decay: Double
    public var traceDecay: Double
    public var minWeight: Double
    public var maxWeight: Double

    public init(learningRate: Double = 0.08, decay: Double = 0.002, traceDecay: Double = 0.9, minWeight: Double = -1.0, maxWeight: Double = 1.0) {
        self.learningRate = learningRate
        self.decay = decay
        self.traceDecay = traceDecay
        self.minWeight = minWeight
        self.maxWeight = maxWeight
    }
}

public struct SynapticState: Codable, Sendable {
    public var weight: Double
    public var eligibility: Double
    public init(weight: Double = 0.0, eligibility: Double = 0.0) {
        self.weight = weight
        self.eligibility = eligibility
    }
}

public struct SynapticInput: Codable, Sendable {
    public var pre: Double
    public var post: Double
    public var reward: Double
    public init(pre: Double, post: Double, reward: Double = 1.0) {
        self.pre = pre
        self.post = post
        self.reward = reward
    }
}

public enum SynapticError: Error { case invalidValue }

public func synapticStep(_ state: SynapticState, input: SynapticInput, config: SynapticConfig = SynapticConfig()) throws -> SynapticState {
    let values = [config.learningRate, config.decay, config.traceDecay, config.minWeight, config.maxWeight, state.weight, state.eligibility, input.pre, input.post, input.reward]
    guard values.allSatisfy({ $0.isFinite }), config.learningRate >= 0,
          (0...1).contains(config.decay), (0...1).contains(config.traceDecay),
          config.minWeight <= config.maxWeight else { throw SynapticError.invalidValue }
    let eligibility = config.traceDecay * state.eligibility + input.pre * input.post
    let rawWeight = (1.0 - config.decay) * state.weight + config.learningRate * input.reward * eligibility
    let weight = max(config.minWeight, min(config.maxWeight, rawWeight))
    return SynapticState(weight: weight, eligibility: eligibility)
}
