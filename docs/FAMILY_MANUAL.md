# 💚 The Family Lantern Manual

## Before anything else

HEARTLIGHT is for preserving pieces of a relationship. It is not a test you can fail, and there is no minimum amount of material required.

A single story is enough to begin.

## The five lantern baskets

When gathering material, imagine five little baskets:

### 1. Things they said

Letters, texts you have permission to preserve, sayings, jokes, recipes, notes, poems, favorite expressions, and stories other people remember hearing.

### 2. Things they sounded like

Voice recordings, songs, laughter, videos, and—if your family has one—a heartbeat or pulse recording.

### 3. Things they looked like

Photographs, drawings, home videos, favorite clothes, places, objects, and images connected to memories.

### 4. Things they taught

Values, rules, ridiculous advice, serious advice, traditions, routines, ways they cared for people, things they would never tolerate, and things they always forgave.

### 5. Things your family still wants to teach

A memorial model is not an archaeological fact machine. Families remember from different angles. HEARTLIGHT therefore lets people append lessons with a named teacher instead of pretending the software magically knows which memory is definitive.

## Starting a lantern

```bash
heartlight init ./our-lantern --display-name "Our Lantern"
```

Then add records one by one.

```bash
heartlight ingest-text ./our-lantern story.txt --source "Dad's notebook"
heartlight ingest-audio ./our-lantern laugh.wav --source "family video 2019"
heartlight ingest-video ./our-lantern birthday.mp4 --source "phone archive"
heartlight ingest-image ./our-lantern photo.jpg --source "family album"
```

## Adding a heartbeat

If you have a heartbeat-like recording saved as an uncompressed PCM WAV:

```bash
heartlight heartbeat ./our-lantern heartbeat.wav
```

The software turns it into a rhythm signature. Later applications can use that timing for a pulse animation, haptics, musical pacing, agent turn timing, or other state transitions.

The recording does not have to carry the burden of "proving" anything. It can simply be one precious signal your family chose to preserve.

## Teaching memories

```bash
heartlight teach ./our-lantern \
  --prompt "What happened when someone was sad?" \
  --response "They made tea first and asked questions later." \
  --teacher "Mom"
```

Use teaching to preserve context that raw media cannot explain.

Helpful teaching prompts:

- What always made them laugh?
- What did they do when someone was scared?
- What food did they ruin every time?
- What did they believe mattered more than money?
- What phrases did they repeat?
- What did they apologize for?
- What were they proud of?
- What family stories should never disappear?

## Build the profile

```bash
heartlight build ./our-lantern
heartlight status ./our-lantern
```

`generated/profile.json` is the grounding packet an application can use to create a conversational memorial.

## A rule for children

If a child uses a memorial companion, an adult should explain in age-appropriate words that the computer is using saved memories and family teaching. Do not tell a child that the person is literally trapped in or speaking through the machine.

## A rule for grown-ups too

The interface must let you leave. It must not say things such as "don't abandon me," "I need you," or "if you close this I will die again." Grief should never be used as an engagement mechanic.

## Family disagreement

Do not erase disagreement merely to create a smoother personality. Two memories can both be preserved with different teacher/source labels. A healthy archive can say, "Aunt May remembers this differently from Dad."

## Private material

Before importing private messages, health-related files, intimate recordings, or material involving children, think about who has a right to that material and who should be allowed to see generated output based on it.

## The smallest possible lantern

If all you can manage today is this:

```text
They laughed with their whole face.
```

Save it.

That counts.
