# 💚🦄 HEARTLIGHT // The Lantern Archive

> **A family-built memorial continuity toolkit for preserving stories, media, values, and a heartbeat-derived rhythm signature.**

HEARTLIGHT is an experimental open-source project for families who want to preserve the *shape of a relationship* across time: the stories someone told, the phrases they used, photographs and videos, family lessons, favorite things, and—when available—the sound of a heartbeat.

It does **not** claim to resurrect a person, recover a soul, prove consciousness survives death, or reproduce an exact human identity. A HEARTLIGHT companion is a **new computational memorial created from supplied records and ongoing family teaching**. It should always identify itself as such.

The original working title of this repository was `Death-on-a-sub-`. The project name is now **HEARTLIGHT // The Lantern Archive** because the goal is not to sell death back to grieving people. The goal is to build a lantern from what they choose to preserve.

## The idea

```text
family records ─┐
photos/videos ──┼──> evidence manifest ──> corpus builder ──> memorial profile
stories/text ───┤                              │
heartbeat.wav ──┘                              ├──> heartbeat rhythm signature
                                                ├──> local encrypted-ready vault
                                                └──> optional Azure / IBM COS mirrors

family teaching ───────────────────────────────> append-only lessons
```

The heartbeat is treated as a **signal artifact**, not a metaphysical identifier. HEARTLIGHT extracts a reproducible rhythm fingerprint (beat times, intervals, BPM summary, and digest) from a suitable WAV recording. That signature can be used as a timing motif, UI pulse, provenance anchor, or synchronization seed.

## What this repository provides

- 💚 local-first memorial vaults
- 🫀 WAV heartbeat/pulse-style signal analysis
- 📚 text and media corpus manifests with SHA-256 provenance
- 🌱 append-only family teaching records
- 🧠 a deterministic memorial profile builder
- ☁️ optional Microsoft Azure Blob Storage adapter
- ☁️ optional IBM Cloud Object Storage adapter
- 🔐 explicit provenance and anti-impersonation metadata
- 🧪 unit tests and GitHub Actions CI
- 👩‍👧 family manual, teacher/facilitator guide, architecture notes, science notes, and a small book

## 1. Install

Requires Python 3.10+.

```bash
git clone https://github.com/NavisWORLD/Death-on-a-sub-.git
cd Death-on-a-sub-
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

Optional cloud adapters:

```bash
pip install -e '.[azure]'
pip install -e '.[ibm]'
# or both
pip install -e '.[cloud]'
```

## 2. Create a family lantern

```bash
heartlight init ./my-lantern --display-name "Grandma's Lantern"
```

This creates a local vault with a manifest, evidence folder, corpus folder, lessons ledger, heartbeat folder, and generated profile folder.

## 3. Add records

```bash
heartlight ingest-text ./my-lantern ./letters/story.txt --source "family letters"
heartlight ingest-media ./my-lantern ./video.mp4 --kind video --source "family archive"
heartlight ingest-media ./my-lantern ./voice.wav --kind audio --source "family archive"
```

HEARTLIGHT hashes every imported artifact and records where it came from. Media files are preserved as evidence; the core project does not secretly clone a voice or fabricate video.

## 4. Add a heartbeat rhythm signature

```bash
heartlight heartbeat ./my-lantern ./heartbeat.wav
```

The analyzer works best on a clean mono/stereo PCM WAV in which pulse sounds are distinct. It performs envelope extraction and conservative peak detection. It is **not a medical device**, ECG interpreter, or biometric identity system.

## 5. Teach the lantern

```bash
heartlight teach ./my-lantern \
  --prompt "What did Sunday mornings feel like?" \
  --response "Coffee, old music, and everyone talking too loud." \
  --teacher "Mom"
```

Teaching is append-only and source-labeled. Different family members can preserve different memories without pretending disagreements never existed.

## 6. Build the memorial profile

```bash
heartlight build ./my-lantern
heartlight status ./my-lantern
```

The generated `profile.json` is a machine-readable grounding packet for a future conversational layer. It includes a mandatory disclosure telling downstream systems that they are simulations based on records and family teaching.

## 7. Mirror to Azure or IBM Cloud Object Storage

Copy `.env.example` to `.env`, fill in your own credentials, then:

```bash
heartlight sync ./my-lantern --provider azure
heartlight sync ./my-lantern --provider ibm
```

Cloud sync is optional. The local vault remains the source of truth.

## Project map

```text
src/heartlight/
  cli.py              command-line interface
  corpus.py           evidence + teaching + profile builder
  heartbeat.py        rhythm-signature extraction
  models.py           typed project records
  provenance.py       hashing + canonical JSON helpers
  storage.py          local vault layout
  cloud/
    azure.py           Azure Blob adapter
    ibm_cos.py         IBM COS adapter

docs/
  ARCHITECTURE.md
  FAMILY_MANUAL.md
  TEACHER_GUIDE.md
  SCIENCE_NOTES.md
  ETHICS_AND_SAFETY.md
  THE_LANTERN_BOOK.md
```

## Non-negotiable design rules

1. **No resurrection claims.** The software may preserve, model, remix, or simulate; it may not claim the biological person returned.
2. **No deceptive impersonation.** Generated systems must disclose that they are memorial simulations.
3. **Consent and family governance matter.** Only use records you have the right to use, especially private messages, children’s data, and biometric/health-related recordings.
4. **Keep provenance.** Every artifact should retain source, checksum, date, and relationship context when known.
5. **Allow deletion and silence.** A family must be able to remove records, stop a model, or decide not to continue.
6. **Grief is not a retention metric.** Do not optimize engagement by making people feel guilty for leaving or by claiming the memorial needs them.

## Research status

HEARTLIGHT is an **engineering and human-computer-interaction experiment**. It can test whether structured family archives, heartbeat-derived timing motifs, and provenance-aware conversational grounding create meaningful memorial experiences. Claims about post-death consciousness, identity transfer, or physical continuity are outside what this code demonstrates.

## License

Apache-2.0 for the software. Family media and personal records are **not** relicensed merely because this software processes them. See `LICENSE` and `docs/ETHICS_AND_SAFETY.md`.

## For the moms with capes and the dads in boxers

You do not have to make a perfect archive. Save one laugh. One recipe. One ridiculous story. One heartbeat recording if you have it. One thing they taught you. A lantern can start with a single light.
