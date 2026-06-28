---
title: Talking / Lip-Sync Method — PRODUCTION STANDARD
status: MANDATORY DEFAULT for every episode — do not re-explore
proven: Ep1 (original), re-proven Ep2 v13 (2026-06-26, owner-approved "looks amazing")
applies_to: every Bentley (and guest) on-screen dialogue shot, all episodes
---

# Talking / Lip-Sync Method (PRODUCTION STANDARD)

> **THE RULE:** every talking shot = **Kling-Avatar driven from a TIGHT, BRIGHT, FRONT-FACING FACE
> close-up keyframe.** This is the default for all episodes. It is solved. Do **not** run model
> bake-offs or "is lip-sync possible" reviews again — follow this.

## Why this is the method (and why the alternatives fail — already tested, don't retest)
- **Kling-Avatar** (`kling/ai-avatar-standard`) is **audio-driven** → real, word-synced lip-sync, and it
  stays **on-model** — *but only if fed a tight front-facing face CU.* It is **human-face-biased**: a
  **wide / dim / small / side-angle** keyframe makes it invent the face → **CARICATURE** (bulging eyes,
  human grin). The keyframe framing is the single decisive variable.
- **Kling 3.0 / Seedance i2v** (no audio) → on-model but the mouth **flaps out of sync** ("coughing");
  i2v can't read the audio. Rejected.
- **Seedance-2 audio-lipsync** → same human-face caricature as Avatar, and costlier. Rejected.
- Net: **Avatar + tight face-CU keyframe is the only combination that is both on-model and synced.**

## Implementation

### Model call (KIE, ~40 cr / line)
```python
kie_client.run("kling/ai-avatar-standard",
    {"image_url": <tight_face_CU_keyframe_url>,
     "audio_url": <clean_single_speaker_line_url>,
     "prompt": <avatar_prompt>}, timeout=1200, poll=10)
```
Then **grade** (Avatar darkens output):
`eq=brightness=0.05:saturation=1.14:contrast=1.05,unsharp=3:3:0.4:3:3:0.0,format=yuv420p`

### 1. Per-line clean audio (the lip-sync driver AND the played audio)
Each line is a **separate, single-speaker** clean file (e.g. `vo/labels/<LABEL>.mp3`). The Avatar syncs
to this file, and this same file plays in the cut — so the lip-sync matches by construction. Locked
voices via ElevenLabs (`bentley/shared/eleven.py`): **Bentley = LauraZ `jkNABRZGatAuwawcS9xX`**, model
`eleven_v3`, settings `stability 0.3, similarity 0.75, style 0.6, speed 1.12`, then EQ/loudnorm clean
(`highpass=85, …, loudnorm=I=-16:TP=-1.5:LRA=11`).

### 2. Expression face-CU keyframe set (hand-picked once per episode, reused across all lines)
Generate ~6 **tight front-facing face CUs** covering the emotional range, from the locked master via
`gpt-image-2-image-to-image` (refs: `Bentley_MASTER_pixar.png` + turnaround + the Ep1 framing reference
`assets/approved/bentley/N6_kie_key_bright2.png`). **Hand-pick the on-model one per expression — never
auto-batch.**

**Keyframe prompt (COMMON, prepend to each expression):**
> Tight head-and-shoulders FACE close-up of Bentley the red-fawn Boxer puppy, looking straight at the
> camera, front-facing, BRIGHT daylight on her face (the framing of a talking-to-camera shot). Mid-speech
> with her mouth slightly open — a soft natural small-dog mouth, a little tongue and tiny puppy teeth ok,
> but NO human grin, NO human smile, NO bulging eyes. On-model: black face mask, grey chin, NORMAL-sized
> round brown eyes, floppy folded-down ears, white chest blaze, teal collar, gold paw-print tag. Warm
> bright tide-pool background, soft cartoony-Pixar render. Keep her EXACTLY on-model, do not redraw or
> restyle her. No text, no watermark.

**Expression tags (append one):** `curious` (bright, eyes wide/sparkling, ears perked, slight head-tilt) ·
`delighted` (joyful, eyes shining, ears up) · `reassuring` (warm, soft loving eyes, calm/tender) ·
`playful` (cheeky sparkle, bright/fun) · `calm` (attentive, present, listening) · `awe` (wide-eyed wonder).

### 3. Avatar each line (map line → expression → keyframe)
Assign every line an expression, drive the Avatar from that expression's keyframe.
**Avatar prompt template:**
> Bentley the red-fawn Boxer puppy speaks straight to camera **{TONE}**; soft natural small-dog mouth
> movements in time with her words, ears floppy down, no human teeth, no human grin. Bright daylight on
> her face. Keep her exact look, do not redraw her.

`{TONE}` per expression: curious = "with bright curious energy and a gentle head-tilt, eyes sparkling";
delighted = "with delighted joyful energy, eyes shining with happiness"; reassuring = "warmly and gently,
soft loving reassuring eyes, calm and tender"; playful = "with playful cheeky energy, bright and fun";
calm = "calmly and present, gentle attentive eyes"; awe = "with wide-eyed wonder and surprise".

### 4. Edit — intercut, don't cut-per-line
Weave the talking CUs into **held** scene/two-shots. Do NOT cut on every line (that's choppy — the #1
pacing complaint). Hold a scene, intercut Bentley's talking CU on her lines.

## Workflow (ordered)
1. Lock the per-line clean VO (one speaker per file).
2. Generate the 6 expression face-CU keyframes → **hand-pick** the on-model one each.
3. Map every line → expression.
4. (New keyframes) Avatar **one** line to confirm on-model + synced, then batch the rest.
5. Avatar all lines (parallel, ~4 workers) → grade each.
6. Intercut talking CUs into held, smoothly-transitioned scenes.
7. QA (below), mix, deliver.

## Cost
~6 cr / keyframe still × ~6 + ~40 cr / line Avatar. (Ep2: 6 keys = 72 cr after candidates; 43 lines ≈
1,720 cr.) Avatar is **cheaper than Kling 3.0 video** (70 cr) per shot.

## QA (per talking CU)
- [ ] On-model: NORMAL-sized eyes (no bulge), correct proportions, black mask, floppy ears, teal collar.
- [ ] Mouth moves **in sync** with the words (it's audio-driven — it will).
- [ ] Natural dog mouth, small puppy teeth OK, **NO human grin / human smile**.
- [ ] Keyframe was a tight front-facing face CU (if it caricatured, the keyframe was wrong — regenerate it,
      do not blame the model).

## Reference implementation (reusable scripts)
- Keyframe set: `scratch/ep2/talking_v13/talk_keys.py`
- Avatar batch + grade + line→expression map: `scratch/ep2/talking_v13/talk_avatars.py`
- Single-line proof / new-keyframe check: `scratch/ep2/talk_sample/ep1method.py`

See also: `episode-production` skill §5 (enforces this), memory `bentley-talking-shots`,
and `VIDEO_COST_BLUEPRINT.md` (Avatar is the locked talking tier).
