# HEARTLIGHT Architecture

## 1. Purpose

HEARTLIGHT is a local-first memorial continuity platform. It preserves evidence, derives an optional rhythm signature from heartbeat-like audio, records family teaching, and emits a machine-readable memorial profile that other applications can use as grounded context.

It does not claim biological resurrection or consciousness transfer.

## 2. Layers

### Lantern Vault

The local vault is the source of truth:

```text
manifest.json
evidence/
  text/
  audio/
  video/
  image/
  other/
corpus/
lessons/family_teaching.jsonl
heartbeat/
  source.wav
  signature.json
generated/profile.json
```

### Signal Layer

The heartbeat analyzer performs:

1. PCM WAV decoding
2. channel reduction to mono
3. short-window RMS envelope extraction
4. robust thresholding using median and median absolute deviation
5. refractory peak selection
6. inter-beat interval calculation
7. median BPM estimate
8. canonical signature digest

The result is a timing feature set. Applications can map the interval sequence into animation, haptics, agent pacing, musical tempo, scheduler cadence, or a state-machine clock.

### Evidence Layer

Every imported artifact receives SHA-256 provenance. Raw evidence is separated from generated outputs.

### Teaching Layer

Family teaching is append-only JSONL. A lesson contains prompt, response, teacher label, and timestamp. The system does not silently rewrite prior lessons.

### Profile Layer

`profile.json` combines:

- project identity
- mandatory simulation disclosure
- behavior rules
- heartbeat rhythm signature if present
- evidence manifest
- text corpus
- family teaching

This packet can ground an LLM or another conversational engine.

### Interop Layer

HIP v0.1 is the portable event model. Native SDKs live in `sdk/`.

## 3. The Heart-Gate model

A useful implementation metaphor is:

```text
rhythm(t) -> gate clock -> sensory event -> state update -> grounded response
```

For example, a live application can convert a recorded rhythm signature into a repeating sequence. Each beat can advance a finite-state machine or emit `rhythm.beat`. Camera, microphone, touch, motion, or other sensor events arrive independently. A policy layer can then decide which sensory events alter the current memorial state.

This is an engineering state machine. It is not evidence that the physical heart contains a complete personality.

## 4. Cloud topology

Small deployment:

```text
Phone/Desktop -> local vault -> optional Azure Blob or IBM COS
```

Family deployment:

```text
Devices -> HTTPS/WebSocket API -> event bus -> profile service
                              |-> object store
                              |-> provenance database
```

Enterprise deployment:

```text
Global edge
   |
API gateway + identity
   |
HIP ingest service ---- consent/policy service
   |
event bus (partition by project_id)
   |---------------------------|
rhythm service          corpus/profile service
   |                           |
object storage          metadata DB/vector index
   |                           |
KMS/HSM                 audit ledger
```

## 5. Scaling rules

- partition streams by `project_id`
- make event consumers idempotent by `event_id`
- keep monotonically increasing per-project sequence numbers where possible
- use immutable object keys for evidence
- cache generated profiles, never raw secrets
- separate user-facing generation from evidence ingestion permissions
- use managed/workload identities instead of static cloud keys at scale
- retain deletion tombstones long enough to propagate erasure through replicas

## 6. Provider adapters

The reference implementation includes Azure Blob and IBM Cloud Object Storage mirroring. At enterprise scale, storage adapters should sit behind a common service boundary; a project should not care whether its encrypted objects live in Azure, IBM, an S3-compatible service, or a local filesystem.

## 7. Future protocol extensions

Planned protocol directions can include:

- protobuf schemas
- gRPC service definitions
- WebSocket rhythm stream
- explicit consent records
- encryption envelopes
- signed provenance manifests
- sensor adapters
- portable vector indexes
- model-provider adapters
- export/import bundles
