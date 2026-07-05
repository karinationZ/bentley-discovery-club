# Cinematography + AI-Pipeline Rules + Output Formats

> **Governed by the single normative chain** — the 11 Mandatory Rules (`episode-production` §0.0) →
> `episode-production/SKILL.md` → its `references/PRODUCTION_PLAYBOOK.md` (+ the `lipsync-pro` skill for
> sync methods). This file is the WRITER's cinematography guide; where it and the chain differ, **the
> chain wins** — update this file the same day the chain changes.

Two jobs here: design shots that *read* (cinematography), and design shots the AI pipeline can
actually **make and cut together** (constraints + output formats).

## Cinematography toolkit (pick per beat, on purpose)

**Shot size** — establishing (where are we), wide (full action + space), medium (a character acting),
close-up (emotion), macro/insert (a detail: the tag, a shell, a tentacle on a paw), two-shot (the
relationship). *Vary sizes* — a string of same-size shots feels flat.

**Camera move** — slow push-in (intimacy/tension), pull-out (reveal/loneliness), pan/tilt (follow or
unveil), tracking (travel with a character), and the most important one here: **"static-with-life"** —
a held frame where the subject still breathes, blinks, ripples. A truly frozen frame reads as a bug.

**Staging & continuity** — give every shot a clear subject and some depth (foreground/background).
Keep **eyelines** connecting characters who interact, and hold **screen direction** (if Bentley chases
left-to-right, keep it) so the geography stays legible to a child.

**Lighting/mood** — warm daylight (home/safe), cool shade or dark crevice (danger), golden hour
(emotion). Mood shifts should track the story, not flicker shot to shot.

**Transitions** (this series' biggest past defect was dipping every cut to **black** — never do that):
- **Hard cut** — the default. Clean, energetic, what cartoons use.
- **Match cut** — cut on a motion or shape that continues (a lunge into a vanish) — great for momentum.
- **Crossfade (~0.4s)** — only for a real time/place jump or an emotional settle.
- **One fade in** at the very open and **one fade out** at the very end. That's the only black.

## AI-generation hard rules (Kling-3.0 i2v pipeline)

These come from real failures; honor them or the edit breaks.

- **Motion in every shot.** "Static image + slow zoom" is a defect. Specify the action: she steps, the
  water swirls, the tentacle curls, she blinks and breathes. If a beat is a held emotion, make it
  *static-with-life*, not frozen.
- **No human teeth, no human smile, ever** (canon). Dog joy = tongue out + soft eyes + tail wiggle.
  Octopus mouth stays tiny and toothless. This applies to talking shots especially.
- **Dialogue defaults to VO-over-alive, with every mouth managed (the Sync-or-Hide law).** A line plays
  over a shot of the **speaking** character whose *body* visibly acts the line — the viewer knows who's
  talking — while every readable talking mouth must either trace to a sanctioned sync tool or be staged
  so the mouth isn't readable. As the writer: give every line the correct speaker, stage non-speakers
  mouth-closed/reacting-only (Rule 9: only the speaker's mouth ever moves), and **tag the signature
  lines** — Bentley's catchphrase = a Kling-Avatar CU on the locked Talking prop; a small guest speaking
  in a two-shot may use the OmniHuman mask. (Methods live in `lipsync-pro` + playbook Part 6 — don't
  invent new ones on the page.) Never lay a long speech over a montage that cuts away from the speaker.
- **One SCENE per story beat; no clip ever repeats.** Design at the section level (§0 Continuous-Section
  Law): group the script into ~8–12 logical sections and write ONE continuous evolving scene per beat —
  never a new unrelated clip per sentence. A long section = 2–3 continuous shots of the SAME evolving
  scene. "One clip" means *no reuse*: a callback (e.g. the predator returning) uses a *different
  angle/sub-shot* — byte-identical reuse and loops are immediately visible.
- **Consistency.** Characters are generated from the locked masters and **hand-picked** (4–8 candidates
  per keyframe, never auto-batched-and-shipped); the model drifts. Keep the tag, paws (no white
  socks), docked tail, eyespots, etc. on-model. Flag any shot where two characters must share a frame
  (highest drift risk).
- **Generate only the bridge shots the story needs.** Reuse existing footage wherever a beat allows;
  generation is expensive and drifts. The bridge-shot list should be as short as the story permits —
  usually the one or two shots that *show* a connection nothing else covers (EP2: Indi + eel in one
  frame).

## Output formats (emit all four)

### 1. Beat sheet
```
| # | Act | Beat (action) | Emotional purpose | Science |
|---|-----|---------------|-------------------|---------|
| 1 | Cold open | Bentley boops a "rock" that opens an eye and vanishes in ink | curiosity → surprise | octopus ink/escape |
```

### 2. VO line list  (the format `scratch/ep<N>/make_vo.py` consumes)
```
label        | speaker | text
B_hook1      | B | Helloooo, little rock. You look like you need... a boop.
N_camo       | N | An octopus can change her color AND her texture faster than you can blink...
I_creep      | I | ...You're not chasing me anymore.
```
- Labels are stable IDs (`B_`/`I_`/`N_` + a short name). Keep a label across drafts when the beat is
  the same; mark NEW/CUT when you add or remove. Every line gets the right speaker.

### 3. EDL / cue sheet  (matches `docs/series/season_1/ep2/EP2_STORY_REPAIR_EDL.md`)
One row per beat, in final order:
```
| # | Beat | Picture (reuse path or BRIDGE) | VO | ~s | Shot / camera | Transition in | Notes (consistency/motion) |
```
- "Picture" is either an existing clip to reuse (give the path/name) or `BRIDGE` (must generate).
- "Transition in" uses C (cut) / M (match) / X (crossfade) / FI / FO — never a mid-film black dip.
- Keep each character's line over a shot of that character.
- **This table has a machine-runnable JSON twin** (`episodes/ep<N>/shotlists/ep<N>_master.json`) the
  Animatic Lock + final assemble actually run — see SKILL.md "Hand off an animatic-ready EDL". In the
  JSON, the "Picture" path becomes `src`/`over`/`still` and the "VO" **label becomes an mp3 path**
  (`N_camo` → `scratch/ep<N>/vo/N_camo.mp3`). Labels/IDs alone are not runnable.

### 4. Bridge-shot list
For each shot that must be generated: a one-paragraph **intent** (what it shows and why the story
needs it), the **reference assets** (locked character masters + any environment ref), and the
age-appropriateness note (soft menace, no gore). Keep this list minimal.

## Final production note
End the package with the **"science checked"** line (species + the 3–4 facts) and a one-line
**runtime estimate** (sum the VO + action beats). If revising an existing episode, also list which VO
labels changed (need re-recording) vs unchanged, so the team only re-records what moved.
