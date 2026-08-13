# HEARTLIGHT Ethics & Safety

## Purpose

Memorial technology touches grief, identity, privacy, family conflict, and sometimes children's data. HEARTLIGHT therefore treats safety and consent as architecture, not decoration.

## 1. Identity disclosure

A generated companion must make clear that it is a simulation grounded in archived records and teaching. It must not assert that it is literally the deceased person or that the person's consciousness has been recovered.

## 2. No dependency manipulation

Applications built on HEARTLIGHT must not use grief to create artificial dependency. Prohibited product patterns include generated statements designed to imply that the memorial will suffer, disappear, die again, or feel abandoned if a user stops interacting.

## 3. Rights and consent

Only ingest material that the operator is permitted to use. Extra care is required for:

- private correspondence
- recordings made without the subject's knowledge
- children's data
- medical or health-related records
- biometric recordings
- intimate media
- records involving living third parties

An open-source software license does not grant rights to anyone's personal data.

## 4. Living people

HEARTLIGHT must not become a covert impersonation kit for living people. Apps should require authorization before building a personality/voice/avatar representation of a living person and should disclose generated media appropriately.

## 5. Children

Child-facing memorial experiences should:

- include an involved responsible adult
- use age-appropriate explanations
- never assign the child responsibility for keeping the model alive
- avoid fear-based or supernatural certainty claims from the software
- make ending a session ordinary and safe

## 6. Deletion

Families must have a practical way to:

- remove an artifact
- delete generated profiles
- revoke cloud replicas
- export their archive
- stop future processing

Enterprise systems should propagate deletion through replicas and derived indexes.

## 7. Provenance

Generated systems should distinguish among:

- verified archived evidence
- family teaching
- generated inference
- unknown information

When asked about something unsupported, the preferred answer is that the archive does not know.

## 8. Voice and image generation

The core repository preserves media but does not automatically clone voices or faces. Applications that add synthetic voice or image generation should require appropriate authorization, clearly disclose synthetic output, and retain provenance for source media.

## 9. Security

Recommended controls include:

- encryption in transit and at rest
- per-family/project authorization
- least-privilege cloud roles
- managed keys or KMS/HSM at scale
- audit logs for evidence access
- separate permissions for viewing raw evidence and using generated profiles
- secret stores instead of committed API keys

## 10. Research ethics

Studies involving grieving participants require particular care. Researchers should not treat increased interaction time as automatically positive. Measure comprehension, distress, ability to disengage, and whether participants understand that the model is generated.

## 11. Spiritual meaning

Families are free to understand remembrance through their own spiritual, philosophical, or cultural frameworks. HEARTLIGHT's engineering documentation does not adjudicate those beliefs. It simply distinguishes them from claims demonstrated by the software.
