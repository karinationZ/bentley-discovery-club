---
name: cinematic-episode-writer
description: >-
  Write or revise a cinematic, production-ready episode script for "Bentley's Big Adventures" (the
  kids' AI-animation series about Bentley the Boxer puppy). Use this WHENEVER the user wants to
  create, fix, tighten, or punch-up an episode's story, screenplay, storyline, dialogue, narration,
  beat sheet, or shotlist — even if they don't say "skill" or "cinematic." Triggers on: "write
  episode N", "fix the story/dialogue", "the script feels disconnected", "make the storyline
  better", "draft the next episode", "the scenes don't connect", "the lines make no sense", or any
  request to turn an episode idea into a script. It produces a beat sheet + line-by-line VO script +
  EDL/cue sheet + shot list, all tuned to the AI-generation pipeline. Prefer this over free-handing a
  script: free-handed scripts are exactly how episodes end up as "a collection of clips, not a story."
---

# Cinematic Episode Writer — Bentley's Big Adventures

A complete episode reads as **one story a grandpa is telling**, with characters who happen to talk —
not a string of pretty shots. A child watching should never wonder *"why are we suddenly here? who's
talking? how do these connect?"* This skill exists because that question is the #1 failure mode, and
it is a **writing** problem solved before a single frame is generated.

The job is to turn an episode premise into a **production-ready script package** that plugs straight
into the build pipeline. You are writing for two readers at once: a 5-year-old (who needs feeling and
clarity) and the AI render+edit pipeline (which needs shots it can actually make and cut together).

## When you start, read the references
- `references/bentley-canon.md` — characters, locked voices, world, tone, the "Stop. Look. Listen."
  device, and how the science is handled. **Read this first, every time** — canon is non-negotiable.
- `references/story-craft.md` — the arc/beat-sheet template and the craft of writing for ages 4–8
  (the emotional + educational weave, causality, dialogue). Read before steps 2–4.
- `references/shot-and-pipeline.md` — the cinematography toolkit and the AI-pipeline hard rules
  (motion>static, no human teeth, real transitions, one-clip-per-beat, consistency, output formats).
  Read before step 5.

The script is *produced* under the companion **`episode-production`** skill (the mandatory production
rulebook + the Kling 3.0 cost gate). So in your EDL, tag each shot's value clearly — **hero /
character-interaction** (warrants Kling 3.0) vs **supporting** (establishing, transition, card, hold,
narration-only → reuse / still+Ken-Burns / card / cheaper tool). That tagging is what keeps premium
credits on the moments viewers notice.

## The workflow (do these in order)

### 1. Lock the premise
Pin down, in a sentence each: the **science subject** (the animal/phenomenon this episode teaches),
the **guest character** (who embodies it), **Bentley's emotional lesson** (what she learns — usually
a flavor of *Stop. Look. Listen.*), and the **cliffhanger** that hands off to the next episode. If the
user gave only a topic, propose these and confirm before writing.

### 2. Find the spine (the most important step — this is what prevents "a collection of clips")
Write down explicitly:
- **One feeling** the episode is about (e.g., "it's safe to be seen").
- **One lesson** for Bentley.
- **3–4 science facts**, and — crucially — **how the biology IS the story.** The guest's real
  adaptations must *be* the plot, not trivia stapled on. (EP2: Indi hides *because* the reef is
  dangerous; her camouflage and boneless escape are *how she survives*; that's *why* she's alone;
  Bentley seeing her is the payoff.) If the facts don't drive the plot, redesign until they do.

A child should be able to answer "what was that about?" with the feeling, and "what did you learn?"
with the lesson. If you can't, the spine is weak — fix it before continuing.

### 3. Build the beat sheet
Use the act template in `story-craft.md`. Every beat must **cause the next one** (chase → fright →
danger → realization → turn). For each beat note its *emotional* purpose and its *educational*
purpose. Open with a 10–15s **cold-open hook** (a "wait, what?!"), end on the **cliffhanger**. Include
at least one **non-plot bonding beat** (the characters just enjoying each other) — episodes feel
hollow without it.

### 4. Write the dialogue, line by line
Each line is a **reaction to the line before it** — never a non-sequitur. Keep each character's voice
distinct (see canon). Deliver facts through *wonder*, not lectures. Read it aloud in your head: it
must sound like natural, warm, funny speech for ages 4–8, with no dark or depressing notes. Then run
the **causality check**: walk the lines in order and confirm a kid would never ask "wait, why?". The
catchphrase "Stop. Look. Listen." is **always Bentley's**, used at the emotional turn.

### 5. Design the shots
For each beat write the shot: type, camera move, staging, the **motion** in it, lighting/mood, and the
**transition in**. Obey the pipeline rules in `shot-and-pipeline.md` — most importantly: **every shot
has motion** (static + zoom reads as broken), dialogue plays over a shot of the **speaking** character
kept alive, transitions are real cuts/match-cuts/crossfades (**never a dip to black**), and **no clip
is reused** (a callback uses a different angle). Flag which shots already exist vs. which must be
generated (the **bridge shots** — keep this list minimal; the pipeline is expensive and drifts).

### 6. Emit the package
Output the four artifacts in the exact formats in `shot-and-pipeline.md`:
1. **Beat sheet** (table: act · beat · action · emotional purpose · science).
2. **VO line list** — `label | speaker (B/I/N) | text`, the format `make_vo.py` consumes.
3. **EDL / cue sheet** — per beat: picture (reuse or BRIDGE), VO, ~duration, shot/camera, transition,
   consistency notes (matches `docs/series/season_1/ep2/EP2_STORY_REPAIR_EDL.md`).
4. **Bridge-shot list** — only the shots that must be generated, with intent + reference assets.

**Hand off an animatic-ready EDL.** Emit the EDL/cue sheet (artifact 3) as a *machine-runnable* JSON
shotlist — each beat `{type: card|vo_over|ffx|motion|talk, src, dur, over, vo, status: todo|reuse}` —
so the production **Animatic Lock** gate (`episode-production` §10 step 4) renders the timed story
scratch with **no re-authoring**, and the *same* JSON later feeds final assemble. This is not new
authoring: the EDL you already write just needs to be in this runnable schema.

## Self-review before you hand it over
Look at the draft twice with fresh eyes:
- **As a 5-year-old:** Does every scene follow from the last? Is it ever unclear who's talking or
  where we are? Is anything scary or sad in the wrong way? Is it *fun*?
- **As the pipeline:** Any static shot, human smile/teeth, dip-to-black, reused clip, or a line over
  the wrong character? Any bridge shot that isn't truly necessary?
Fix what you find inline. A script that passes both reads is the whole point of this skill.

## Output style
Lead with the spine (feeling + lesson + facts) so the user can sanity-check the foundation in five
seconds, then the beat sheet, then the script, then the production artifacts. Keep dialogue tight and
speakable. When revising an existing episode, preserve what works and show what changed and why —
don't rewrite wholesale unless the spine itself is broken.
