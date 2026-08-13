import assert from "node:assert/strict";
import { defaultSynapticConfig, synapticStep } from "../dist/index.js";

let state = { weight: 0.2, eligibility: 0.0 };
const inputs = [
  { pre: 0.5, post: 0.25, reward: 1.0 },
  { pre: 1.0, post: -0.5, reward: 0.4 },
  { pre: 0.2, post: 0.8, reward: -0.25 },
];
const expected = [
  { weight: 0.2096, eligibility: 0.125 },
  { weight: 0.1967808, eligibility: -0.3875 },
  { weight: 0.2001622384, eligibility: -0.18875 },
];
for (let i = 0; i < inputs.length; i += 1) {
  state = synapticStep(state, inputs[i], defaultSynapticConfig());
  assert.ok(Math.abs(state.weight - expected[i].weight) < 1e-12);
  assert.ok(Math.abs(state.eligibility - expected[i].eligibility) < 1e-12);
}
