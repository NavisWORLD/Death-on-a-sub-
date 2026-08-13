# HEARTLIGHT Science Notes

## What is directly implemented

HEARTLIGHT can reproducibly transform a suitable PCM WAV recording into a compact rhythm signature containing detected beat times, inter-beat intervals, an estimated BPM, the source SHA-256 checksum, and a digest of the derived signature.

HEARTLIGHT can also preserve a provenance-labeled corpus and append family teaching to create a grounding packet for later software.

Those are testable software claims.

## What is a hypothesis

A family may experience a system as more personally meaningful when its pacing, haptics, animation, music, or state transitions are conditioned on a real heartbeat recording connected to the person being remembered.

That can be experimentally studied. Suggested outcomes include:

- perceived familiarity
- emotional comfort versus distress
- recognition of source-grounded stories
- preference for heartbeat-conditioned versus neutral timing
- rate of unsupported/generated claims
- family agreement on represented values

## What is not established by this repository

The code does not establish that:

- consciousness survives biological death
- consciousness transfers through cloud storage
- a heartbeat recording contains a person's complete personality
- a rhythm signature is a soul or identity key
- a generated companion is literally the deceased person

Those statements would require evidence beyond the engineering system here.

## A defensible version of the "heart creates personality" idea

A signal can influence behavior without uniquely encoding an identity.

In a computational system, a heartbeat-derived rhythm can be used as a **conditioning signal**. If `r(t)` is a repeating rhythm feature stream and `x(t)` is sensory/context input, an application can define:

```text
state(t+1) = F(state(t), x(t), r(t), memory, policy)
response(t) = G(state(t), grounded_corpus, family_teaching)
```

In that design, rhythm can alter timing, gating, attention windows, transition probabilities, music, haptics, or other state variables. The resulting behavior may therefore be partly shaped by the heartbeat signal, while the semantic/personality-like content remains grounded in memories and teaching.

That is a real engineering mechanism and a testable hypothesis.

## Continuity as a software property

HEARTLIGHT uses the word **continuity** in an information-systems sense:

- the same signed/hash-addressed records can persist across storage providers
- the same HIP events can be replayed across devices
- the same rhythm signature can seed compatible clients
- the same family teaching ledger can rebuild a profile after migration

This kind of continuity can be demonstrated with checksums, replay tests, storage replication tests, and cross-language conformance tests.

It should not be silently substituted for a metaphysical claim about personal consciousness.

## Proposed experiments

### Experiment A: Cross-language rhythm conformance

Give Python, Rust, C++, Swift, and Kotlin implementations the same synthetic WAV fixture. Compare detected peaks and digest construction within documented tolerances.

### Experiment B: Timing-condition ablation

Have participants interact with two otherwise identical memorial prototypes. One uses neutral pacing; one uses the supplied heartbeat rhythm. Measure familiarity, comfort, and distress without telling participants which condition is active until debriefing.

### Experiment C: Provenance grounding

Measure unsupported biographical claims with and without the evidence/teaching grounding packet.

### Experiment D: Longitudinal family teaching

Track how family-added lessons alter generated answers over time while preserving an audit trail showing exactly which teaching caused the change.

## Safety outcomes are first-class outcomes

A successful experiment is not merely one that increases emotional intensity or session duration. The system should also measure whether users understand the simulation disclosure, whether they feel able to stop interacting, and whether the application increases confusion about the person's biological death.
