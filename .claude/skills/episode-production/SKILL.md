---
name: episode-production
description: >-
  The MANDATORY single source of truth for PRODUCING any "Bentley's Big Adventures" episode. Load this
  BEFORE generating, rendering, animating, editing, assembling, or QA-ing any episode footage, shot,
  card, or asset. It holds the hard rules: the Kling 3.0 cost gate (when premium animation is and is
  NOT allowed), Bentley/character/prop canon, animation/transition/voice rules, asset reuse, and the
  pre-delivery QA checklist. Trigger on ANY request to build/produce/render/animate/cut/assemble an
  episode, generate shots, spend Kling/KIE credits, make a shotlist/cue sheet, or run episode QA —
  even if the user doesn't name this skill. Pairs with `cinematic-episode-writer` (the script phase):
  write the script with that, produce it under THESE rules. Every episode-production agent MUST load
  this first.
---

# Episode Production — Bentley's Big Adventures (MANDATORY rulebook)

This is the single source of truth for turning an approved script into a finished episode. It exists
because the same mistakes keep recurring — a "stitched-together montage," off-canon Bentley, wasted
Kling credits, dip-to-black transitions, dialogue over the wrong character. **Read this before you
generate or edit anything.** Pair it with the `cinematic-episode-writer` skill (the script/story
phase). Write the script there; produce it here.

**The prime directive:** *Maximize quality where viewers notice it most; minimize credit usage
everywhere else.* Premium animation for character moments, cheap tools for supporting footage, reuse
approved assets whenever possible — without sliding back into a disconnected montage.

---

## 1. THE KLING 3.0 COST GATE  *(hard rule — Kling is expensive)*

> **⚠️ OPERATES UNDER [VIDEO_COST_BLUEPRINT.md](../../../docs/guides/VIDEO_COST_BLUEPRINT.md) — PROJECT LAW.**
> **Never spend premium video on EXPLORATION.** Scout the prompt/shot CHEAPLY (Seedance 1.5 Pro / Kling 2.5 Turbo /
> Kling 2.6 / Hailuo / Runway), lock prompt+duration+aspect+refs, THEN render Kling 3.0 **once** for the final.
> Kling 3.0 **720p no-audio ≈ $0.07/s is cheap** — the budget killer is *rerolling before lock*, audio, and 4K.
> **Never "fix bad prompting" on Kling 3.0 — rewrite and test cheap first.** Target **≥80% cheap/mid, ≤20% premium.**
> Caveat still holds: cheap models DRIFT recognizable characters — scout the *direction* cheap, render the *final*
> character shot on Kling 3.0.

Before generating **any** shot, ask one question:

> **Is a character emoting or interacting, or is this a signature/hero/action moment a viewer will
> actually remember? **

- **YES → Kling 3.0** (premium i2v + locked element refs).
- **NO → do NOT spend Kling.** Reuse an approved clip, animate a still (Ken-Burns/parallax), build a
  card/graphic in ffmpeg/PIL, or use a cheaper model.

**Use Kling 3.0 ONLY when at least one is true:**
- Bentley and another character are interacting (two-shots, the bond, play)
- A dialogue/emotional close-up where the face carries the moment
- An emotional beat, key story moment, or signature episode image
- A hero shot or a complex action shot (chase, escape, transformation)

**NEVER use Kling 3.0 for:**
- Static scenes · ocean/reef backgrounds · establishing shots · transition shots
- Title cards · fact/"NEXT TIME" cards · simple camera moves · hold/settle shots
- Filler · narration-only scenes where no character is emoting

**Shot-type → tool (use the cheapest that meets the bar):**
| Shot | Tool |
|------|------|
| Bentley + character interaction / emotional CU / hero / complex action / signature | **Kling 3.0** |
| Establishing / ocean bg / location | reuse the plate, or a still + Ken-Burns, or **Kling 2.5 Turbo (test tier)** |
| Transition / wipe / match-cut | the editor (ffmpeg) — **no generation** |
| Title / fact / NEXT-TIME card | PIL/ffmpeg card over a live plate — **no generation** |
| Hold / settle / "static-with-life" insert | reuse a *different sub-range* of an approved clip |
| Prop insert (the tag, a shell) | macro of a still + Ken-Burns, or reuse |
| Narration-only (no character acting) | reuse / b-roll / Ken-Burns over approved footage |

**Model tiers — which generator for which shot (owner policy, 2026-06-24; updated with test results):**
| Tier | Model | Use for |
|------|-------|---------|
| **Free — ALWAYS TRY FIRST** | reuse approved clip · still + Ken-Burns · card/graphic · editor transition | Establishing, ocean bg, transitions, title/fact cards, holds, narration-only, inserts. We have a large approved EP2 footage library — reuse covers most non-hero beats at **zero** credits. |
| **Premium** | **Kling 3.0** | **ALL hero character shots** — Bentley+Indi close-ups, dialogue reactions, the camo/transformation reveal, emotional beats, any face-visible moment. ~70 cr / 5s on KIE. Worth it where viewers look; use only when reuse can't serve. |
| **Cheaper — TEST (for must-generate non-hero)** | **Kling 3.0 Turbo** (Higgsfield ~7.5 cr/5s; confirm the KIE slug) | If a non-hero shot truly must be generated (no reuse fits) — small-face wides, simple environment motion. Same Kling family → far more likely to hold our style than Seedance. Evaluate before episode-wide use. |
| **Banned** | ~~Kling 2.6~~ | Not cheap enough to justify the risk; already fails on mouths/teeth. |
| **TESTED → AVOID for characters** | ~~Seedance 2.0 / 2.0 Mini~~ | **Tested 2026-06-24** (eel insert, Seedance 2.0 Mini, 10 cr): it **drifts creatures/characters** — our menacing moray became a cute, big-eyed, smiling cartoon fish; off-model, menace lost. **Do not use for any shot with a recognizable character/creature.** ("Seedance 1.5 Pro" does not exist on our backends — only 2.0 / 2.0 Mini.) Even for pure-environment inserts, reuse/stills beat it. |

**Free / near-free toolbox (prefer these for supporting footage before *any* paid model):** reuse
approved clips · Ken-Burns / parallax on a still (ffmpeg `zoompan`) · procedural motion-graphics (PIL)
· title/fact cards (PIL) · editor transitions.

Caveat learned the hard way: a *procedural or cheaper-model substitute for a hero shot* is a
regression (the v8 camo dissolve / black-hearts) — cheap tools **and** the cheaper models are for
**supporting** footage, never the character moment itself.

*Implementation note:* `bentley.shared.kie_client` currently wires `kling-3.0/video` (and legacy
`kling-2.6`). Confirm the exact KIE model slugs for **kling-2.5-turbo** and **seedance-1.5-pro** before
the first cheaper-tier render, and keep the locked element-refs / hand-pick flow for any model.

**Budget discipline:** aim for a small set of Kling hero shots per episode (target ~12–18), and cover
everything else by reuse/stills/cards. Log credits spent per episode. If the Kling count climbs,
challenge each shot against the gate above.

---

## 2. ASSET REUSE RULES
- **Reuse before you generate.** Map every beat to an existing approved clip first; only mark a shot
  `BRIDGE` (generate) when no existing footage can serve it. Keep the bridge list as short as the
  story allows.
- A reused clip may appear in more than one beat **only** as a *different sub-range* — never the same
  frames twice (byte-identical reuse and loops are instantly visible; this was a top EP2 complaint).
- **Masters are frozen.** Edit *from* the locked masters (`Bentley_MASTER_pixar.png`, `Indi_LOCKED.png`,
  the eel keyframe); never regenerate a master.
- **Deliver under a fresh filename** every time (viewers/players cache by name) and **verify a frame
  extracted from the FINAL file** before calling it delivered.
- Always include the absolute file path when handing the user any asset (they work from the filesystem).

---

## 3. BENTLEY RULES (canon — non-negotiable)
Full canon: `.claude/skills/cinematic-episode-writer/references/bentley-canon.md`. The hard ones:
- Red-fawn Boxer puppy, **black face mask**, grey chin, brown eyes, **floppy folded-down ears**, white
  chest blaze, **solid red-fawn paws — NO white socks/toes**, **short docked tail stub only**, teal
  collar + gold paw-print Listening Tag. Cartoony-Pixar style (not photoreal).
- **NEVER a human smile or human teeth**, and she never stands/acts like a person. Dog joy = tongue
  out, soft eyes, tail-stub wiggle.
- Generate Bentley only from `Bentley_MASTER_pixar.png` (+ turnaround); **4–8 candidates per keyframe,
  hand-pick the on-model one, NEVER auto-batch-and-ship** — the generator drifts.
- Two-characters-in-one-frame is the **highest drift risk**; prefer already-approved footage for those.

---

## 4. MASTER PROP RULES
- **The Listening Tag** (gold paw-print on the teal collar) glows when Bentley is still — the visual
  anchor of "Stop. Look. Listen." Keep it present and consistent on every Bentley shot; feature it at
  the emotional turn.
- **The shells** — the guest leaves small spiral shells as the "someone, please notice me" motif and
  the episode hand-off. Keep the shell design consistent.
- Any recurring prop is referenced from its locked master and kept continuous shot-to-shot and
  episode-to-episode. New props get a locked reference before they're animated.

---

## 5. CHARACTER ANIMATION RULES
- **Motion in every shot.** A static frame with a slow zoom reads as a bug. If a beat is a held
  emotion, make it *static-with-life* (breathing, blink, ripple) — never frozen, and never a
  clone-pad freeze. If a line outlasts a clip, cover it with a second angle, not a >1.3× slow-mo.
- **Dialogue = Kling-Avatar lip-sync, driven from a TIGHT BRIGHT FRONT-FACING FACE-CU keyframe (the
  proven Ep1 method).** → **Full standard + exact prompts/workflow: [TALKING_LIPSYNC_METHOD.md](../../../docs/guides/TALKING_LIPSYNC_METHOD.md). Follow it every episode; do not re-explore.**
  `kling/ai-avatar-standard` (~40 cr, image+audio+prompt) syncs the mouth to the
  VO and stays on-model **only if the keyframe is a tight, bright, front-facing face close-up** (cf.
  `assets/approved/bentley/N6_kie_key_bright2.png`). A **wide / dim / small / side-angle face keyframe
  CARICATURES her** (bulging eyes, human grin) — that failure is the keyframe, NOT the model. So: for
  every talking beat, generate a tight face-CU keyframe first, then Avatar; intercut the talking CUs as
  dialogue. Occasional small puppy teeth accepted; no human grin. (VO-over-alive is the fallback only
  when a face-CU genuinely can't be staged.)
- Never lay a long speech over a montage that cuts away from the speaker.
- No octopus/animal human faces; keep the guest on-model (e.g. Indi: teal eyes, two ring eyespots,
  toothless).

### 5a. SHOT-FLOW LAW *(HARD RULE — owner-mandated 2026-06-27; ship-blocking)*
1. **Talking-head ratio + multi-character lip-sync.** Solo talking-head CUs must not dominate — target
   **≤ ~35% runtime solo heads, ≥ ~25% two-shots/interaction**. **When ≥2 characters are on screen,
   the SPEAKER must visibly animate/lip-sync their own line and the LISTENER stays still.** A line
   lip-synced by the wrong character (octopus mouthing Bentley's words) is a **ship-blocking defect**.
   To get interaction *without* the wrong-speaker bug, build fresh **"speaker-talks, listener-still"
   two-shots**: keyframe = speaker mouth-open / listener mouth-closed; Kling i2v animates only the
   speaker. (Caveat: the two-shot mouth moves but isn't frame-synced like a CU — right character +
   interaction, not exact lip-sync. Use CUs for hero lip-sync lines, two-shots for conversational beats.)
2. **Longer continuous scenes, NOT many short stitched clips.** Prefer fewer, longer shots that hold the
   whole beat. **Never cover one VO by stitching two sub-ranges of the SAME clip, and never reuse a clip
   @0 across back-to-back beats** — both read as a cheap loop. A line that outlasts its clip gets ONE
   continuous generated/retimed shot, not a splice.
3. **Cohesive scene-to-scene flow.** Every cut flows from the last (hard cut / match-cut on continuing
   motion); it must feel like a story, not a montage. **Show the cause before the reaction** (e.g. show
   the octopus turned Bentley-colored *before* Bentley says "you did me!").

---

## 6. TRANSITION RULES
- **No dip-to-black between shots, ever** (the v7 disaster: every cut faded through black). The only
  black is one fade-in at the very open and one fade-out at the very end.
- Default transition is a **hard cut**. **Match-cut** on a continuing motion/shape for momentum.
  **Crossfade (~0.4s)** only for a real time/place jump or an emotional settle.
- One clip per beat; no loops. Transitions are an **edit** operation — never a Kling render.

---

## 7. VOICE RULES
- **Locked voices:** Bentley = LauraZ (`tts_bentley`); the guest = its locked voice (e.g. Indi =
  `eleven.INDI`, `tts_indi`); Narrator = Bill (`tts_bill`/`eleven.NARRATOR`, grandpa settings); Pip =
  Callum +10% pitch.
- **The catchphrase "Stop. Look. Listen." is ALWAYS Bentley's**, never the narrator's, in every
  episode including outros — three words with a deliberate pause between each (`tts_catchphrase`).
- Every line is assigned to the correct speaker and plays over a shot of **that** character (a guest
  line that reads as Bentley is a known defect). Re-record only the lines whose text changed.
- Keep all dialogue cheerful/funny/age-4–8; **no dark or depressing lines.**

---

## 8. STORYTELLING RULES  *(produced from the script — full craft in `cinematic-episode-writer`)*
- The cut must obey the script's **spine** (one feeling + one lesson + 3–4 facts that *drive the
  plot*) and its **causal chain** (every beat causes the next). If the edit breaks causality (a beat
  lands "out of nowhere"), restore the connective shot/line — don't ship the seam.
- Keep the cold-open hook, the **bonding beat** (non-plot joy), and the cliffharger intact.
- Deliver facts as wonder, never as a data-dump.

---

## 9. PRE-DELIVERY QA CHECKLIST  *(run against the FINAL exported file — all must pass)*
**Technical**
- [ ] Black-frame scan: **no** interior black (only the open/close fades).
- [ ] No reused/looped frames; callbacks use distinct sub-ranges.
- [ ] No static-with-zoom-only shots; no clone-pad freezes; no >1.3× slow-mo.
- [ ] Grade consistent across shots (mood shots intentionally darker, not flat/pale).
- [ ] Streams OK (1080p, audio present); delivered under a **fresh filename**; a frame from the FINAL
      file visually verified.

**Canon / character**
- [ ] Every Bentley shot: docked tail, floppy ears, red-fawn paws (no white socks), tag, black mask.
- [ ] No human smile / human teeth (Bentley or guest).
- [ ] Guest on-model (eyes/eyespots/no human face).

**Story / audio**
- [ ] Every line over the correct, *alive* speaker; catchphrase is Bentley.
- [ ] Causality holds (no "why are we here?" beat); bonding beat present; cliffhanger lands.
- [ ] No dark/depressing lines; it's *fun*.

**Cost**
- [ ] Every Kling shot passes the §1 gate; supporting footage used reuse/stills/cards; credit spend
      logged. Anything that didn't need Kling and used it → flag for next time.

**Animatic Lock** *(pre-render gate — run on the step-10.4 scratch BEFORE any Kling spend)*
- [ ] Every recorded VO line present and **in script order**, none dropped (audio-only pass; full new + reused reel).
- [ ] Every line over its **correct speaker** — reliable on real footage; **label-only/weak on gray cards** → flag for §10 step 5.
- [ ] Watched **muted**: every cut answers the previous beat; no dip-to-black; no same-clip back-to-back.
- [ ] The causal hinge is **shown** by a real bridge placeholder, not narrated over a gap.
- [ ] Measured runtime on target; no VO outlasts its beat; no >1.3× stretch.
- [ ] Catchphrase is Bentley at the turn; no dark lines; bonding beat + cliffhanger **present and placed** (not whether they "land").
- [ ] Reads as **one story, not a montage**.
- [ ] **Scope disclaimer signed:** certifies STORY + CUT only — NOT on-model character, identity hold
      across shots (the #1 blocker), lip-sync, grade, or that placeholder timing survives generation.
      Those stay with §10 step 5 hand-pick + this §9 on the FINAL file.
- [ ] Overlap note: **§5a SHOT-FLOW LAW is authoritative** for wrong-speaker / same-clip / cause-before-reaction on the FINAL cut.

---

## 10. THE PRODUCTION WORKFLOW (ordered; don't skip)
1. **Script** — produce/approve the script package with `cinematic-episode-writer` (spine → beats →
   VO list → EDL/cue sheet → bridge-shot list). The EDL tags each beat REUSE vs BRIDGE, in the
   machine-runnable JSON schema the step-4 animatic consumes.
2. **Tag every shot against the §1 cost gate** — confirm each BRIDGE truly needs Kling; downgrade the
   rest to reuse / still+Ken-Burns / card / cheaper model. Get owner sign-off on the Kling list
   *before* spending (approve-direction-first).
3. **VO — assemble the COMPLETE reel** — record changed/new lines (locked voices) AND concatenate the
   full VO set (new + reused mp3s) **in script order** into the reel the step-4 animatic consumes.
   (The dropped-line check in step 4 has no input without the full reel.)
4. **Story Scratch / Animatic Lock** *(owner-mandated; ship-blocking; ZERO Kling/KIE/ElevenLabs
   credits)* — before **any** Kling spend, build a TIMED animatic of the WHOLE episode on the cue-sheet
   EDL: the complete recorded VO in canonical order over placeholder picture, where every beat is a
   reused clip, a Ken-Burns still of a locked master/plate, or a **labeled card naming the speaking
   character + beat** (un-shot BRIDGEs auto-render a card — never silently skipped). Watch it twice
   (audio-only, then muted) and clear the **Animatic Lock** sub-checklist in §9. **No Kling render runs
   until the owner signs off the animatic.** On PASS the animatic shotlist is the **STARTING EDL** for
   assembly; placeholder durations are estimates, so re-check/re-time the cut rhythm at step 6/§9 after
   the real shots land (this is "start from the locked story EDL," NOT "zero rework"). Overlaps §5a
   (wrong-speaker, same-clip-back-to-back, cause-before-reaction): the animatic is the *pre-render*
   pass; **§5a stays authoritative on the FINAL cut.**
   > **PRECONDITION (build before Ep3 renders):** this gate needs a productionized JSON-shotlist
   > animatic in `bentley/episode_builder/` — extract `ken_burns()` into the package; add a
   > missing-asset → labeled-card fallback; JSON-drive `assemble.py`; add a zero-cost VO concat from
   > existing mp3s (a TTS re-synthesis path spends ElevenLabs — do **not** use it here); reuse the
   > `shorts.py` caption track for card labels. Build the scratch through that path ONLY — **never**
   > `pipeline.py <shotlist>` / `produce()`, and never the `bentley.animation.*` or
   > `bentley.asset_generation.*` generation modules (they spend KIE/fal). The artifact is one
   > zero-credit `*_ANIMATIC.mp4` checked into the episode dir; until the tool exists the gate is
   > "planned," not satisfiable.
5. **Generate the approved Kling bridge shots** — 4–8 candidates each, **owner/hand pick**, QC every
   frame vs canon; never auto-batch. *(A green animatic certifies STORY + CUT, **not** on-model render —
   character drift is caught ONLY here and at §9. For new-character episodes — e.g. EP3: Mari, no locked
   master, Bentley+Mari scale two-shots — keep this hand-pick LOUDER than the animatic sign-off, never
   quieter.)*
6. **Assemble** — data-driven from the animatic shotlist (its EDL graduates in place: each `todo`
   placeholder is replaced by its rendered Kling clip); hard cuts + match/cross per the EDL; one clip
   per beat; minimal re-encodes (build each beat in one pass, concat by copy, one final encode in the mix).
7. **Sync-verify** — `bentley/qa/verify_sync.py`: one voice at a time, mouth == voice, no overlap.
8. **Mix** — music beds by mood, ambience, SFX, ducked under VO; the one open/close fade.
9. **Grade** — one consistent grade over the whole episode; avatar darkening lifted.
10. **QA §9 against the FINAL file**, then deliver under a fresh filename with its absolute path.
