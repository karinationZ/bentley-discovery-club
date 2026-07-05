---
name: companion-short
description: >-
  Create a realistic, documentary-style YouTube SHORT that is the companion to a "Bentley's Big
  Adventures" cartoon episode — "the REAL science behind the adventure." Use this WHENEVER the user
  wants a Short, companion clip, "real science" video, or promo Short for an episode — e.g. "make a
  short for episode N", "a companion short", "the real octopus/hermit-crab video", "a short to drive
  views to the episode", "turn the episode's science into a short" — even if they don't say
  "documentary" or "skill". It runs the whole pipeline: mirror the episode's signature science fact,
  source FREE real footage (Pexels — never AI/Kling), preview & map clips to beats, write Bill's
  narration, build the full-bleed vertical cut with the bundled script, AND generate the YouTube title,
  description, and tags. Pairs with `episode-production` (which makes the cartoon); this makes its
  real-footage companion.
---

# Companion Short — the real science behind the cartoon

Each episode is a cartoon *story*; its companion Short is the *"…and that really happens."* A child who
watched Indi the octopus change color, then sees a REAL octopus do the exact same thing, gets the best
payoff there is: **"wait — that's REAL?!"** Delivering that payoff, plus a clean funnel back to the
episode, is the whole job. This skill exists because the format took several wrong turns before it
worked — the rules below are hard-won, not theoretical.

## The core principle — pick ONE world and stay in it
The fatal mistake is putting two visual worlds in one frame. Don't. The Short lives entirely in the
**real** world; the cartoon brand appears only in the **voice** and the **end-card**, never spliced
over the footage.

- **All real footage, full-bleed vertical** — one coherent photoreal world.
- **Brand = the narrator's voice + the end-card.** Bill (the show's grandpa narrator) carries the whole
  thing — he's the thread back to the cartoon, so the link is the viewer's *ear*, not a jarring cut. The
  only on-screen brand is a full-bleed end-card built from the episode's thumbnail.
- **Demonstrate the lesson; never recite the catchphrase.** "Stop. Look. Listen." is a *story* ritual —
  bolted onto a documentary it reads as a contrivance. Let the science *embody* it instead (camouflage =
  "you swam right past her — you just had to look"). The episode's soul, in context, unspoken.
- **Mirror the episode's signature science.** Same concept as the cartoon = the connection. Name the
  guest (Indi, Pip, …) so the tie is explicit.

## What the owner REJECTED — do not repeat (2026-06-28)
1. **Cartoon Bentley spliced into / intercut with real footage** — "two worlds collapse, no harmony,
   makes no sense." (A cartoon *end-card* is fine; cartoon *in the body* is not.)
2. **The catchphrase pulled into the doc** as a transition device — out of context.
3. **Static photos**, and **AI-generated nature footage** (Kling/Seedance) — costs more, looks worse
   (drifts/uncanny), and breaks the no-premium-for-b-roll cost law. Use real *video*.

## The workflow

### 1. Pick the science — mirror the episode
Take the episode's **signature** fact (the one the cartoon is built around) and tell it for real. EP2 =
octopus camouflage; EP1 = the hermit-crab "vacancy chain". If unsure which fact, pick the most visually
jaw-dropping one the episode actually dramatizes — not an unrelated "fresh" fact (that breaks the tie).

### 2. Source real footage — FREE, never AI
Real **video** (not stills) from **Pexels** (`https://www.pexels.com/search/videos/<animal>/`) — free,
no attribution, Made-for-Kids-safe. Either the owner drops clips into `~/Downloads`, or hunt Pexels and
show candidates *before* building (ignore the "Sponsored/iStock" column — that's paid). You need ~3–4
clips: a **hook** (a "find the animal" reveal or the most arresting shot), one or two **detail/behavior**
shots, and a **hero** shot for the close. **Never** generate nature b-roll on Kling/KIE (see "Cost").

### 3. Preview & map clips to beats
Probe each clip (`ffprobe` → width/height/duration/fps) and extract a few frames across each to judge
the *motion*, then map each to a beat. **Native-vertical clips go full-bleed; landscape clips get
center-cropped** to 1080×1920 (the bundled script handles both via the beat's `vertical` flag). Note
which clip is the hook and which is the hero. Be honest in the narration about what the footage actually
shows — don't say "watch it change color" over a clip that only shows blending.

### 4. Write the narration — Bill, ~6 beats, ≤ ~35s
Six short lines, warm grandpa wonder, ages 4–8:
1. **Hook** (cold-open on the real wonder) — a question or "watch this".
2–4. **The science** — how it works; teach exactly ONE smart word (e.g. "chromatophores → color sacs").
5. **The kicker** — the most surprising twist (e.g. "she's colorblind").
6. **The tie** — name the guest + demonstrate the lesson ("…and neither did Pip — he never finds his
   home alone."). Keep lines SHORT: the build sizes each shot to its line, so wordy lines make a baggy
   Short. Shorts reward completion — aim **≤ ~35s** total.

### 5. Build the cut — use the bundled script
`scripts/build_short.py` does the whole assembly at ~$0: caches Bill VO, reframes + **clamps** each clip
to its line, burns ONE caption per beat, builds the full-bleed thumbnail end-card, mixes VO + music,
muxes, and drops QA frames. Write a small **SPEC** (one beat per VO line) as JSON and run it:

```json
{
  "episode_no": 2,
  "thumbnail": "episodes/ep2/EP2_thumbnail.jpg",
  "out": "episodes/ep2/EP2_Short_Octopus_Camouflage.mp4",
  "clips": {"hook": "~/Downloads/reveal.mp4", "skin": "~/Downloads/macro.mp4", "hero": "~/Downloads/hero.mp4"},
  "beats": [
    {"clip": "hook", "ss": 0.3, "vertical": false, "line": "Wait... can you spot the octopus?", "cap": "Can you find the octopus?", "cy": 0.12, "size": 58},
    {"clip": "skin", "ss": 1.0, "vertical": false, "line": "She changes her color in a blink.", "cap": "color in a blink", "cy": 0.82, "size": 54},
    {"clip": "hero", "ss": 11.0, "vertical": true, "line": "...and she was right there the whole time.", "cap": "right there all along", "cy": 0.12, "size": 54}
  ]
}
```
`cy`: 0.12 = top caption, 0.82 = bottom. Reuse a clip for another beat with a *different* `ss` (not
back-to-back, or it looks like a loop). Then run from the repo root:
```
set -a; . ./.env; set +a
PYTHONPATH=. python3 .claude/skills/companion-short/scripts/build_short.py <spec.json>
```
(`.env` supplies the ElevenLabs key; VO is cached so reruns don't re-spend.) **Then look at the QA
frames** the script drops in `_qa/` — confirm every caption renders, the reframing kept the animal in
frame, and the end-card reads right. You can't listen, so ask the owner to check VO/music balance.

### 6. Generate the YouTube title, description & tags  ← always do this
Every Short ships with metadata. Produce a hook-first **title**, a **description** (hook line → funnel
to the episode → hashtags), and **tags**. Full templates + worked EP1/EP2 examples:
`references/metadata-and-publishing.md`. Quick shape:
- **Title:** interactive or wow hook + ` #shorts` (e.g. `Can you spot the hidden octopus? 🐙 #shorts`).
- **Description:** first line is the hook (it's all that shows before "…more"), then "You met <guest> in
  Episode N — find the full adventure on our channel", then 5–7 hashtags. Sanity-check any auto-suggested
  hashtag matches THIS animal (YouTube suggested `#hermitcrab` on the octopus Short — wrong).
- **Tags:** ~15 topic keywords (the animal, the behavior, the smart word, "science for kids", the show).

### 7. Publish & funnel — the Made-for-Kids reality
These are **Made for Kids**, which **disables clickable links, comments, info cards, and end screens.**
So the funnel is **playlists** (put the Short + the episode in one playlist) + the **baked-in end-card**
(that's *why* it's burned into the pixels). Timing: publish the episode first, the Short ~24h later,
then keep a steady cadence. Reasoning + details: `references/metadata-and-publishing.md`.

## Gotchas (each one cost a rebuild)
- **Captions vanish after the 2nd** with `shorts.add_captions` (multi-image overlay framesync). The
  bundled script burns ONE caption per beat instead — keep it that way.
- **Clip overrun**: if a beat's `ss` + its line length exceeds the clip, the video truncates and audio
  drifts. The script *clamps* `ss`; still, prefer in-points with headroom.
- **`→` and emoji render as tofu** in burned text (the font lacks the glyphs) — the end-card draws a gold
  triangle. Keep `→`/emoji out of captions and the end-card (emoji are fine in the YouTube title/desc).
- **No center play button on the end-card** — it implies a tap Made-for-Kids forbids and covers the art.
  The small ▶ next to "EPISODE N" is enough.
- **VO is cached by filename** — change a line's text ⇒ delete its `_short_build/vo/b<i>.mp3`, or it
  keeps the old audio.

## Cost
~$0 per Short: free Pexels footage + reused thumbnail/music + a few **cents** of ElevenLabs VO. **No
Kling/KIE** — generating realistic nature footage is more expensive, drifts/looks uncanny, and violates
the project's cost law. If a needed shot genuinely can't be found free, that's a conversation with the
owner, not a default to AI.

---
*Pairs with `episode-production` (the cartoon) and `cinematic-episode-writer` (the script). This is the
real-footage companion. Memory: `bentley-companion-short-format`.*
