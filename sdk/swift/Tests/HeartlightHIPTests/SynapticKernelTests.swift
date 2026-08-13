import XCTest
@testable import HeartlightHIP

final class SynapticKernelTests: XCTestCase {
    func testConformanceV1() throws {
        var state = SynapticState(weight: 0.2, eligibility: 0.0)
        let inputs = [
            SynapticInput(pre: 0.5, post: 0.25, reward: 1.0),
            SynapticInput(pre: 1.0, post: -0.5, reward: 0.4),
            SynapticInput(pre: 0.2, post: 0.8, reward: -0.25),
        ]
        let weights = [0.2096, 0.1967808, 0.2001622384]
        let traces = [0.125, -0.3875, -0.18875]
        for index in inputs.indices {
            state = try synapticStep(state, input: inputs[index])
            XCTAssertEqual(state.weight, weights[index], accuracy: 1e-12)
            XCTAssertEqual(state.eligibility, traces[index], accuracy: 1e-12)
        }
    }
}
