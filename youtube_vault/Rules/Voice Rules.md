---
title: Voice Rules
tags:
  - rules
  - audio
  - voice
---

# Voice Rules

> [!important] The cast is locked
> Character voices are fixed. Never swap, re-cast, or re-roll a character's voice between shots or episodes — the voice *is* the character. All voices are generated with **ElevenLabs** `eleven_v3`.

## The locked cast
| Character | Voice | Treatment |
|---|---|---|
| **Bentley** | **"Laura Z"** | warm, bright, young |
| **Pip** | **"Callum"** | pitched **+10%** → small, fussy crab |
| **Theodore** (narrator) | **"Bill"** | warm, measured Nat-Geo storyteller |

> [!note] Where the IDs live
> The exact ElevenLabs voice IDs and settings (stability / similarity / style / speed) live in `pipeline.py` (`tts_bentley`, `tts_pip`, and the narrator scripts). Refer to voices by **name** in docs — never paste the IDs around.

## Voice consistency rules
- One character = **one voice, forever**. No per-shot exceptions.
- Keep the **same `eleven_v3` settings** per character every time (baked into the TTS helpers).
- Pip is **always** pitched +10% (asetrate up, atempo back) — never raw Callum.
- Every raw TTS is **cleaned/mastered** (EQ + loudnorm) before use; keep `_raw` files only as archive (they live in `assets/deprecated/voices/` after cleanup).

## Dialogue rules
- Write for the **ear of a 5-year-old**: short lines, concrete words, big feeling.
- Use `eleven_v3` **audio tags** for performance — e.g. `[warm, fond]`, `[full panic]`, `[playful, with pauses]`.
- Voice personalities: Bentley = curious / warm / brave · Pip = anxious / earnest / funny · Theodore = wonder + reassurance.
- The **narrator carries the science**; the characters carry the **feeling**.

## Character-speaking & lip-sync rules
- A **talking** shot must use its **own embedded lip-synced audio** (the Kling Avatar bakes the voice into the clip) — never re-pin a separate VO at frame 0.
- Mouth length == voice length **by construction**. Never slow-mo or freeze-pad a talking shot.
- A creature in front of **moving water** must **not** be a talking shot (it freezes the background) — split into a motion shot + a dry talking close-up. See [[Animation Rules]].

## No overlapping voices
> [!danger] One voice at a time — always
> Two voices must **never** overlap. The mix (`mix_v2_final.py`) enforces it:
> - Dialogue rides each shot's embedded audio.
> - Narration / off-screen lines are placed **chronologically and sequentially**: each starts ≥ 0.25 s after the previous voice ends **and** is capped to end ≥ 0.2 s before the next dialogue shot.
> - `verify_sync.py` proves **zero overlaps** before anything ships — a hard gate in the [[Episode QA Checklist]].

See also: [[Production Workflow]] · [[Episode QA Checklist]] · [[National Geographic Standards]]
