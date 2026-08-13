# 💚🦄 HEARTLIGHT // The Lantern Archive

> **A family-built memorial continuity toolkit for preserving stories, media, values, and a heartbeat-derived rhythm signature.**

HEARTLIGHT is an experimental open-source project for families who want to preserve the *shape of a relationship* across time: stories, phrases, photographs and videos, family lessons, favorite things, and—when available—the sound of a heartbeat.

It does **not** claim to resurrect a person, recover a soul, prove consciousness survives death, or reproduce an exact human identity. A HEARTLIGHT companion is a **new computational memorial created from supplied records and ongoing family teaching** and should identify itself as such.

The repository began under the working title `Death-on-a-sub-`. The project itself is now **HEARTLIGHT // The Lantern Archive**: not selling death back to grieving people, but building a lantern from what a family chooses to preserve.

## The idea

```text
family records ─┐
photos/videos ──┼──> evidence manifest ──> corpus builder ──> memorial profile
stories/text ───┤                              │
heartbeat.wav ──┘                              ├──> heartbeat rhythm signature
                                                ├──> local vault
                                                └──> optional Azure / IBM COS mirrors

family teaching ───────────────────────────────> append-only lessons

rhythm signature ──> HIP events ──> sensory/state gates ──> apps / devices / services
```

The heartbeat is treated as a **signal artifact**. HEARTLIGHT extracts a reproducible rhythm fingerprint containing beat times, intervals, BPM summary, source checksum, and digest. Applications can use the signature to condition timing, haptics, animation, music, scheduler phase, or state-machine transitions.

The stronger engineering idea is real and testable: **a rhythm signal can shape computational behavior**. The repository does not claim that the heartbeat recording alone contains a complete human personality; semantic/personality-like behavior is grounded in the corpus, provenance, and family teaching layered around that signal.

## What is here

- 💚 local-first memorial vaults
- 🫀 PCM-WAV heartbeat/pulse-style rhythm analysis
- 📚 text/media evidence manifests with SHA-256 provenance
- 🌱 append-only family teaching
- 🧠 deterministic memorial profile builder
- 🌐 HIP v0.1 language-neutral event protocol
- ☁️ Azure Blob Storage adapter
- ☁️ IBM Cloud Object Storage adapter
- 🌍 FastAPI reference service
- 📦 Docker and Kubernetes deployment baseline
- 🧩 SDK source trees for Python, Rust, C++, TypeScript, Swift, Kotlin, Go, .NET/C#, and Java
- 🧪 tests + GitHub Actions CI
- 👩‍👧 family manual, teacher/facilitator guide, science notes, ethics/safety policy, architecture manual, enterprise notes, and *The Lantern Book*

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

Optional groups:

```bash
pip install -e '.[azure]'
pip install -e '.[ibm]'
pip install -e '.[cloud]'
pip install -e '.[server]'
pip install -e '.[enterprise]'
```

## 2. Create a family lantern

```bash
heartlight init ./my-lantern --display-name "Grandma's Lantern"
```

## 3. Add records

```bash
heartlight ingest-text  ./my-lantern ./letters/story.txt --source "family letters"
heartlight ingest-video ./my-lantern ./video.mp4         --source "family archive"
heartlight ingest-audio ./my-lantern ./voice.wav         --source "family archive"
heartlight ingest-image ./my-lantern ./photo.jpg          --source "family album"
```

HEARTLIGHT hashes every imported artifact and records where it came from. Media are preserved as evidence; the core project does not silently clone a voice or fabricate video.

## 4. Add a heartbeat rhythm signature

```bash
heartlight heartbeat ./my-lantern ./heartbeat.wav
```

The analyzer works best on a clean mono/stereo uncompressed PCM WAV with distinct pulse sounds. It performs envelope extraction and conservative peak detection. It is **not a medical device, ECG interpreter, or biometric identity system**.

## 5. Teach the lantern

```bash
heartlight teach ./my-lantern \
  --prompt "What did Sunday mornings feel like?" \
  --response "Coffee, old music, and everyone talking too loud." \
  --teacher "Mom"
```

Different family members can preserve different memories without forcing the archive to pretend disagreement never existed.

## 6. Build the memorial profile

```bash
heartlight build ./my-lantern
heartlight status ./my-lantern
```

The generated `profile.json` is a machine-readable grounding packet for a later conversational, music, robot, haptic, or other application. It includes a mandatory simulation disclosure.

## 7. Mirror to Azure or IBM Cloud Object Storage

Copy `.env.example` to `.env`, fill in your own credentials, export/load those environment variables, then:

```bash
heartlight sync ./my-lantern --provider azure
heartlight sync ./my-lantern --provider ibm
```

Cloud sync is optional. The local vault remains the reference implementation's source of truth.

## 8. Run the HTTP service

```bash
pip install -e '.[server]'
export HEARTLIGHT_DATA_ROOT=./heartlight-data
uvicorn heartlight.api:app --host 127.0.0.1 --port 8080
```

For deployment, see `deploy/docker/`, `deploy/k8s/`, and `enterprise/README.md`. The reference API intentionally does not pretend to be a complete public multi-tenant service: production deployments need real authentication, tenant authorization, database-backed concurrency, encryption/key policy, audit storage, deletion workflows, abuse controls, and privacy/legal review.

## Cross-language compatibility

HEARTLIGHT does not try to duplicate the full engine by hand in literally every programming language. Instead it defines **HIP v0.1**, a stable JSON/event contract that any language can implement.

First-party source trees currently cover:

```text
Python      src/heartlight/
Rust        sdk/rust/
C++20       sdk/cpp/
TypeScript  sdk/typescript/
Swift       sdk/swift/
Kotlin      sdk/kotlin/
Go          sdk/go/
.NET / C#   sdk/dotnet/
Java        sdk/java/
```

See `docs/HEARTLIGHT_PROTOCOL.md` and `docs/SDK_MATRIX.md`.

## Project map

```text
src/heartlight/
  api.py              reference HTTP service
  cli.py              command-line interface
  corpus.py           evidence + teaching + profile builder
  heartbeat.py        rhythm-signature extraction
  models.py           typed records
  provenance.py       hashing + canonical JSON helpers
  storage.py          local vault layout
  cloud/
    azure.py           Azure Blob adapter
    ibm_cos.py         IBM COS adapter

sdk/                   native HIP SDK source trees
docs/                  family, engineering, science, ethics, book, protocol
deploy/                Docker + Kubernetes baseline
enterprise/            large-scale architecture guidance
tests/                 executable reference tests
```

## Non-negotiable design rules

1. **No resurrection claims.** The software may preserve, model, remix, simulate, and condition behavior; it may not claim the biological person returned.
2. **No deceptive impersonation.** Generated systems must disclose that they are memorial simulations.
3. **Consent and family governance matter.** Only use records you have the right to use, especially private messages, children's data, and biometric/health-related recordings.
4. **Keep provenance.** Every artifact should retain source, checksum, date, and relationship context when known.
5. **Allow deletion and silence.** A family must be able to remove records, stop a model, or choose not to continue.
6. **Grief is not a retention metric.** Do not optimize engagement by making people feel guilty for leaving or by claiming the memorial needs them.

## Research status

HEARTLIGHT is an **engineering and human-computer-interaction experiment**. It can test whether structured family archives, heartbeat-derived timing/state conditioning, and provenance-aware conversational grounding create meaningful memorial experiences. Claims about post-death consciousness, identity transfer, or physical continuity are outside what this code demonstrates.

See `docs/SCIENCE_NOTES.md` for falsifiable experiments and the defensible mathematical/state-machine version of the rhythm-conditioning hypothesis.

## License

Apache-2.0 for repository software and documentation. Family media and personal records are **not** relicensed merely because HEARTLIGHT processes them. See `LICENSE` and `docs/ETHICS_AND_SAFETY.md`.

## For the moms with capes and the dads in boxers

You do not have to make a perfect archive. Save one laugh. One recipe. One ridiculous story. One heartbeat recording if you have it. One thing they taught you.

A lantern can start with a single light. 💚
