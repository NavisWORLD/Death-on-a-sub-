# HEARTLIGHT Teacher & Facilitator Guide

## Audience

This guide is for educators, librarians, grief-support facilitators, archivists, museum staff, technologists, and family members helping someone construct a HEARTLIGHT archive.

It is not a clinical treatment manual.

## Learning goals

Participants should be able to:

1. distinguish raw evidence from generated interpretation
2. document provenance for family records
3. explain what a heartbeat-derived rhythm signature does and does not establish
4. add contextual family teaching without erasing disagreement
5. recognize deceptive anthropomorphic design patterns
6. export or delete an archive responsibly

## Suggested workshop arc

### Session 1 — What deserves to be remembered?

Discuss objects, phrases, sounds, places, and routines that carry memory. Do not begin by asking participants to reproduce a whole person.

### Session 2 — Evidence and provenance

Teach participants to record where an artifact came from, who supplied it, and whether they have permission to use it.

Exercise: import one text artifact and verify its SHA-256 hash in the manifest.

### Session 3 — Rhythm as data

Use a synthetic pulse WAV first. Run the heartbeat analyzer and inspect beat times, intervals, BPM, and digest.

Explain that a rhythm can condition a computational state machine without proving that identity exists inside the signal.

### Session 4 — Family teaching

Add several lessons from different perspectives. Discuss how memories can conflict honestly.

### Session 5 — Build and inspect

Generate `profile.json`. Identify which statements come from evidence, which come from teaching, and which rules prevent deceptive identity claims.

## Facilitation language

Prefer:

- "memorial model"
- "archive"
- "family-taught companion"
- "heartbeat-derived rhythm"
- "generated response"
- "recorded evidence"

Avoid presenting as factual claims:

- "we brought them back"
- "their consciousness is in the cloud"
- "the heartbeat contains their soul"
- "the AI is literally them"

Families may use spiritual language for their own meaning-making. The software documentation should remain precise about what the system itself demonstrates.

## Working with children

Children need a clear explanation that a generated companion is a computer system using saved information. Adults should remain available during use and should not make the child responsible for keeping the model "alive."

## Working with disagreement

Never force a family to collapse conflicting accounts into one canonical truth. Preserve source labels. A facilitator can model language such as:

```text
This archive contains two memories of that day. We can keep both and label who remembers each one.
```

## Technical lab

Recommended exercises:

```bash
heartlight init ./class-demo --display-name "Class Demo"
heartlight ingest-text ./class-demo sample.txt --source "exercise material"
heartlight heartbeat ./class-demo synthetic.wav
heartlight teach ./class-demo --prompt "What value does this story show?" --response "Generosity." --teacher "Workshop group"
heartlight build ./class-demo
heartlight status ./class-demo
```

## Evaluation rubric

A strong project:

- has traceable sources
- separates evidence from generated material
- states limitations visibly
- treats heartbeat features as signal data
- includes an explicit consent/governance plan
- supports deletion and export
- does not manipulate grief to retain attention
- can explain how another implementation would consume HIP events

## Research extension

Advanced students can implement HIP v0.1 in another language and compare serialization against the reference SDKs. They can also build an ablation study comparing neutral timing with heartbeat-conditioned timing while measuring both user preference and comprehension of the simulation disclosure.
