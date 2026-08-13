# HEARTLIGHT Enterprise Profile

The reference API is intentionally small. It demonstrates the contract and local vault behavior. A production company-scale deployment should replace shared filesystem assumptions with dedicated services.

## Recommended service boundaries

| Service | Responsibility |
|---|---|
| API Gateway | authentication, rate limits, request IDs, tenant routing |
| Consent Service | authorization grants, revocation, age/guardian policies |
| Evidence Service | upload negotiation, checksums, immutable object metadata |
| Rhythm Service | heartbeat/rhythm feature extraction and versioning |
| Teaching Service | append-only family lessons and authorship |
| Profile Service | deterministic grounded profile assembly |
| HIP Event Gateway | validates and publishes HIP envelopes |
| Audit Service | append-only security/provenance events |
| Deletion Orchestrator | erasure across object stores, indexes, caches, replicas |
| Model Gateway | optional LLM/retrieval providers with mandatory disclosure policy |

## Data plane

Recommended logical stores:

- encrypted object storage: raw evidence and media
- relational database: projects, access grants, artifact metadata, consent state
- append/event store: HIP events and family teaching
- vector/search index: derived retrieval representations only
- KMS/HSM: envelope-encryption keys

Raw evidence should not be copied into every service.

## Event stream

Partition by `project_id`. Consumers should be idempotent by `event_id`.

Example:

```text
rhythm.signature.created
        |
        +--> rhythm playback/haptics service
        +--> profile metadata updater
        +--> audit ledger

teaching.lesson.appended
        |
        +--> profile rebuild queue
        +--> retrieval index updater
        +--> audit ledger
```

## Azure profile

One possible Azure mapping:

- API Management / Application Gateway
- Microsoft Entra ID / workload identity
- Blob Storage
- Event Hubs or Service Bus
- PostgreSQL / Cosmos DB depending access model
- Key Vault
- AKS or Container Apps
- Azure AI Search only for derived search indexes when appropriate

## IBM profile

One possible IBM Cloud mapping:

- Code Engine or Red Hat OpenShift on IBM Cloud
- IBM Cloud Object Storage
- IBM Event Streams
- managed database suitable for project/consent metadata
- IBM Key Protect / Hyper Protect Crypto Services
- IBM Secrets Manager

Provider mappings are examples, not lock-in requirements. HIP remains provider-neutral.

## Sensory gateway

A future sensory gateway can accept authorized sensor events such as microphone activity, touch, motion, camera-derived features, or heart-rate/pulse events. Store only what the product needs. Prefer derived features over permanently uploading raw sensor streams where possible.

The rhythm gate can be modeled as:

```text
beat event -> policy gate -> state transition -> optional UI/haptic/model action
```

## Multi-region

- use globally unique project and event IDs
- maintain a home region for mutable metadata unless conflict-resolution semantics are explicit
- replicate immutable evidence objects by policy
- avoid active/active writes to plain JSON manifests
- propagate consent revocation and deletion with higher priority than generated-content refresh

## Threat model checklist

- stolen cloud key
- guessed project identifiers
- cross-tenant data exposure
- malicious family member adding false teaching
- model output leaking raw private evidence
- prompt injection inside archived documents
- synthetic voice/avatar used outside authorized memorial context
- undeleted derived embeddings after artifact erasure
- replay/duplicate HIP events

## Production readiness gap

The included FastAPI service is a reference API, **not a turnkey multi-tenant production system**. Before public deployment add authenticated identity, authorization, tenant isolation, database-backed concurrency, encryption/key policy, audit storage, backups, deletion workflows, abuse controls, observability, and a formal privacy/legal review for the jurisdictions where the service operates.
