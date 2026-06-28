# Talking Character Framework

Shared, reusable character-animation logic for **all** episodes. It codifies everything we paid to
learn in Episodes 1–2 so future episodes inherit it automatically instead of re-solving it.

> **Rule of thumb:** episode-specific code (which lines, which scene, VO paths) stays in the episode.
> Everything reusable — characters, anatomy, rules, prompts, the render pipeline — lives **here**.

## Why this exists
Every episode kept re-hitting the same walls: AI avatars putting **human teeth** in an octopus's
mouth, a **five-fingered hand** on a tentacle, a **human smile** on a dog; off-model characters from
drifted close-ups; frozen backgrounds on talking shots; hallucinated on-screen text. Those fixes now
live in code and prompts, applied by default.

## The core lesson (baked into `anatomy.py`)
Audio/avatar models are trained on **humans**, so they leak human anatomy into non-human characters.
A negative prompt alone is weak. **Positively DESCRIBE the correct non-human anatomy, THEN ban the
human version.** Every `AnatomyProfile` carries both halves; every built prompt does this for free.

## Components
| Module | What it holds |
|---|---|
| `anatomy.py` | `AnatomyProfile` + `DOG`, `CEPHALOPOD` (describe-correct + ban-human). Add `INSECT` for Ep3 ants. |
| `characters.py` | `Character` registry — `BENTLEY`, `INDI`: anatomy + voice + **approved master** + MUST-HAVE/MUST-NEVER. |
| `rules.py` | The 7 rule categories, with sources + injectable prompt fragments (see below). |
| `prompts.py` | `talking_prompt()` / `motion_prompt()` builders + `EMOTION_TEMPLATES`, `CAMERA_TEMPLATES`, `TRANSITION_TEMPLATES`. |
| `pipeline.py` | `talk()`, parallel `batch()`, `derive_keyframe()` (KIE Kling-Avatar + nano-banana-pro). |

## The 7 rules (`rules.py`)
1. **animation** — the world breathes; native speed; purposeful motion; on-model through the whole clip.
2. **lip_sync** — Kling-Avatar driven by locked VO; bright near-closed-mouth keyframe; avatar **darkens** (grade lifts) & **freezes** backgrounds (split the beat); short exclamations hallucinate text → use VO-over-action.
3. **eye_contact** — eyes do the acting; soft, blinking, engaged; never a dead/bug-eyed stare.
4. **expression** — species-true body language (dog: ears/tail/tongue; octopus: colour/posture/arms), not human faces.
5. **camera** — locked/minimal for talking CUs; vary framing between adjacent shots.
6. **transition** — hard cuts on the beat; continuous ambient+music bed; no match-jump; don't re-anchor a cue.
7. **consistency** — **always derive from the APPROVED MASTER**, never a drifted CU; QA mid-frames vs MUST-HAVE/MUST-NEVER; one grade.

Sourced from `youtube_vault/Lessons Learned.md`, `youtube_vault/Rules/Animation Rules.md`,
`docs/rules/MASTER_PROP_RULES.md`.

## Quick start (an episode)
```python
from bentley.character_framework import talk, batch, derive_keyframe, BENTLEY, INDI

# one talking shot (defaults the keyframe to the character's approved master, builds the prompt)
talk(BENTLEY, "scratch/ep3/vo/B_line.mp3", "scratch/ep3/talking/B_line.mp4", emotion="tender")

# many in parallel (hosts the keyframe once); items = (vo, out) or (vo, out, emotion)
batch(INDI, [("vo/I1.mp3", "out/I1.mp4", "shy"), ("vo/I2.mp3", "out/I2.mp4", "worried")])

# make an in-scene talking keyframe EDITED FROM THE MASTER (never a drifted CU)
derive_keyframe(BENTLEY, scene="a bright tide-pool, medium close-up", out="scratch/ep3/bentley_talkkey.png")
```
`talking_prompt(character, emotion, camera)` returns the exact prompt if you want to inspect/tweak it.

## Add a new character (e.g. the Ep3 ant)
1. Add an `AnatomyProfile` in `anatomy.py` (e.g. `INSECT`: six legs, mandibles, no human teeth/hands).
2. Add a `Character` in `characters.py` bound to that profile, its voice fn, and its **approved master**.
3. Done — every prompt, pipeline call and QA gate inherits it. Add an episode driver that calls `batch()`.

## Where episode code lives
The per-episode driver (line list, emotions, keyframes, VO/out paths) stays in the episode, e.g.
`scratch/ep2/talk_ep2.py`. It imports this framework and supplies only episode specifics.
