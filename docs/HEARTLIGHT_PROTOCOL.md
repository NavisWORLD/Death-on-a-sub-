# HEARTLIGHT Interop Protocol (HIP) v0.1

HEARTLIGHT is intentionally language-neutral. The Python package is the reference implementation, not the protocol itself.

## Core model

A HEARTLIGHT system transports four independent streams:

1. **Rhythm stream** — timing features derived from an approved heartbeat/pulse audio artifact.
2. **Evidence stream** — immutable, hash-addressed family records and media metadata.
3. **Teaching stream** — append-only lessons supplied by authorized family members.
4. **State stream** — generated memorial state, always marked as simulation output.

The rhythm stream may influence timing, UI animation, agent turn cadence, scheduler phase, or model-conditioning features. It must not be treated as proof of identity or survival of consciousness.

## Canonical event envelope

All implementations MUST be able to serialize and consume this JSON object:

```json
{
  "hip_version": "0.1",
  "event_id": "uuid",
  "project_id": "uuid",
  "event_type": "rhythm.beat",
  "timestamp": "RFC3339 UTC",
  "sequence": 42,
  "source": "heartlight-core",
  "provenance": {
    "artifact_sha256": "optional sha256",
    "producer": "component-name"
  },
  "payload": {}
}
```

## Standard event types

- `rhythm.signature.created`
- `rhythm.beat`
- `evidence.ingested`
- `teaching.lesson.appended`
- `profile.rebuilt`
- `state.updated`
- `sync.started`
- `sync.completed`
- `sync.failed`
- `consent.changed`
- `archive.deleted`

## Rhythm signature object

```json
{
  "algorithm": "heartlight-envelope-peaks-v1",
  "source_sha256": "...",
  "sample_rate": 44100,
  "duration_seconds": 12.5,
  "beat_times_seconds": [0.81, 1.59, 2.37],
  "intervals_seconds": [0.78, 0.78],
  "estimated_bpm": 76.923,
  "rhythm_digest": "..."
}
```

## Mandatory disclosure field

Any generated conversational or behavioral profile MUST retain:

```text
I am a memorial simulation generated from family-provided records and teaching.
I am not the deceased person and I do not claim that their consciousness returned.
```

UI wording may be warmer, but this meaning may not be removed.

## Transport profiles

### Local

- JSON / JSONL files
- Unix domain sockets or localhost TCP
- SQLite or filesystem object store

### Device

- HTTPS + JSON
- WebSocket for live rhythm/state events
- optional protobuf transport in future revisions

### Cloud / enterprise

- HTTPS/gRPC edge API
- Kafka, Azure Event Hubs, IBM Event Streams, NATS, or compatible event bus
- object storage for media/evidence
- relational or document database for manifests and teaching ledgers
- KMS/HSM-backed key management

## Determinism

For the same input artifact and algorithm version, rhythm extraction SHOULD produce the same signature digest on all compliant implementations within documented floating-point tolerances.

## Provenance

Every artifact MUST retain:

- SHA-256 checksum
- original filename or external identifier
- declared source
- import timestamp
- content kind
- optional notes / rights / consent metadata

## Security requirements

- never embed cloud secrets in manifests
- use environment variables, managed identities, workload identities, or secret stores
- encrypt sensitive archives at rest and in transit
- keep public/generated assets separate from private evidence
- provide deletion/export paths
- record consent changes

## Compatibility strategy

Rather than claiming support for literally every language, HIP defines a small stable contract. Native SDKs can implement the contract in Rust, C++, TypeScript, Swift, Kotlin, Java, C#, Go, Python, or any language that can encode JSON and SHA-256.
