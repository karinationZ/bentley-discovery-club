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

> **📕 THE PRODUCTION PLAYBOOK** — `references/PRODUCTION_PLAYBOOK.md` (in THIS skill; v1.1, from the EP3
> post-mortem) is the full operating manual: story workflow with owner gates, animation stage order + QC
> gates, composition/consistency/lip-sync/transition procedure, the QA scan suite, the EP3 hall-of-shame,
> and the hard constraints (C1–C10). **Read it at the start of every episode and at every post-mortem.**
> Hierarchy (one normative chain, no parallel sources): 10 Mandatory Rules (owner law, §0.0) → this
> SKILL.md (enforcement) → the playbook (procedure & history). Update them together, from ONE session at
> a time (two parallel sessions editing the chain is how contradictions are born), and bump the playbook
> version line on every owner-law change. **✋ gate passes are RECORDED in `episodes/<ep>/GATES.md`** —
> an unrecorded gate is an unpassed gate.

---

## 0.0 THE 10 MANDATORY PRODUCTION RULES  *(OWNER LAW — 2026-07-03; governs everything below)*

**Requirements, not suggestions.** Every episode is reviewed against all ten before it is approved for
release — this is a HARD GATE in §9. They consolidate and elevate the laws already in this skill; where a
rule points to a section, that section holds the mechanics.

1. **Action over dialogue.** Visuals serve the STORY, not the talking. Under every VO line show
   *meaningful action* — Bentley + guest interacting/exploring/demonstrating, plus environmental life
   (plants, insects, wind, water, birds). The viewer watches an ADVENTURE, not a conversation. Never let
   talking heads carry a beat. → §0, §5.
2. **Approved master talking prop ONLY.** When Bentley speaks, drive the shot from the ONE owner-approved
   **Talking Bentley** master prop/keyframe (locked per series). Do NOT generate alternative talking
   keyframes per shot, experiment with facial styles, or invent new interpretations. Same for Marco and
   every recurring character. → §3, §5.
3. **Never drift from the approved style.** Compare every generated shot against the master prop BEFORE it
   reaches the cut — reject anything too realistic / too cartoonish / off-proportion / off-expression /
   off-render. → §3, §9.
4. **Avoid extreme close-ups.** No parade of oversized single-face CUs. Default to MEDIUM and WIDE with
   both characters + environment in frame; reserve a tight CU only for a genuine emotional beat. → §0, §5.
5. **One cohesive scene per story beat.** Break the script into logical beats; build ONE continuous
   animated sequence per beat and let the whole narration play over it. No sentence-by-sentence stitching,
   no angle change every line. → §0 (Continuous-Section Law).
6. **Invisible transitions.** Every cut has a reason; no abrupt jump in angle/background/style. If the
   audience notices the edit, it failed. Hard cut / match-cut / ≤0.4s crossfade only; never dip to black
   mid-film. → §6.
7. **Absolute character consistency.** Bentley is identical throughout — face, eyes, muzzle, fur,
   proportions, lighting, render, background style. Never "different Bentleys." (Rule 3 is the check.) → §3, §7.
8. **Story before animation.** Finalize script → verify dialogue → confirm logical flow → define beats, and
   pass the zero-credit **Animatic Lock** BEFORE any Kling spend. Generating before the story is validated
   wastes time and credits. → §10 step 1.
9. **Multi-character lip-sync QA (mandatory gate).** When 2+ characters share the frame, ONLY the speaker's
   mouth moves; the listener reacts naturally. Never animate the wrong mouth; never both unless both speak.
   Checked every release via the wrong-speaker motion sweep + EDL trace. → §5, §9.
10. **Think like an animator, not an editor.** Ask "what is the best animated SCENE that tells this part of
   the story?" — not "which clip next?". Scenes must feel alive and cinematic, naturally supporting the
   narration (Bentley, Marco, or narrator). → §0, §8.

**Final standard:** every episode feels like ONE continuous adventure; the viewer remembers the character
bond, the environment, the discovery, and the feeling — and NEVER notices the editing, a character
inconsistency, an abrupt cut, reuse, or a lip-sync mistake.

---

## 0. THE CONTINUOUS-SECTION LAW  *(GOLDEN RULE — the #1 lesson, learned the hard way on EP3, 2026-06-30)*

The worst, most-repeated failure is an episode **chopped sentence-by-sentence** — many short clips (and
tight talking-head CU inserts) that interrupt the flow and burn credits on shots that don't serve the
story. **Never build an episode as one-clip-per-VO-line.** Instead:

1. **Group the whole script into ~8–12 LOGICAL SECTIONS**, not per-sentence beats. A section is one
   complete story beat / dialogue exchange — e.g. the crumb-pickup = ONE scene (sniff → try to lift →
   nudge with the nose → roll → carry); the antenna/tickle = Marco climbs onto the nose, stands firmly,
   reads the scent, tickles — all continuous. Do the grouping in `cinematic-episode-writer`; produce it
   here. Keep multi-line exchanges together — **no section is a lone talking head.**

2. **Generate ONE continuous animated shot per section** — the two-shot of the characters *together*,
   alive, the **action supporting the dialogue**, no cutting inside the section. This is **fewer,
   longer, better shots** — which is *cheaper* AND better story, resolving the "too many credits on
   shots that don't help the story" complaint. (Kling's continuous single-shot max is ~5s; if a
   section's VO runs longer, cover it with 2–3 continuous shots of the SAME evolving scene — never
   per-sentence *unrelated* clips — and/or Ken-Burns over relevant stills. Keep any retime ≤ ~1.3×.)

3. **Lip-sync — current status (updated 2026-07-03; the method table is CLOSED):** governed by the
   **Sync-or-Hide law** — every readable talking mouth traces to a sync tool OR is staged mouth-hidden;
   the EDL trace is the gate. Working methods (full detail: `lipsync-pro` skill + playbook Part 6):
   **A. Kling-Avatar** on the locked Talking prop — tight/bright/front-facing CU only; reserved for
   Bentley's signature lines (the catchphrase), brief intercuts, never a whole beat. **B. OmniHuman-1.5
   mask** — in-frame sync for a small/guest speaker in a two-shot (PROVEN on Marco; FAILS when a
   dominant face is in frame); listener stays still. **C. (future) the Blender rig.** **D. VO-over-alive**
   — the default for continuous scenes: speaker's BODY acts the line, every non-speaker prompted
   "mouth closed," readable mouths staged away from camera.
   **Dead ends — do NOT rebuild these:**
   - **2.5D mouth-patch overlay (`bentley/lipsync/` renderer) — FAILED, owner-rejected 3×:** a flat
     patch is ANATOMICALLY WRONG on ¾/down-facing/profile heads (the real mouth is an occluded seam
     under the muzzle; a pasted frontal mouth reads as a hole in the cheek regardless of tracking).
     The module's TIMING layer (Rhubarb adapter, viseme mapping, QA-sweep tooling) is sound and
     reusable; the patch renderer is not.
   - Video re-sync tools (sync.so `sync-2`, latentsync) — human-lip trained, barely move a cartoon
     MUZZLE (tested 2026-06-17, REJECTED).
   - Kling-Avatar on wide/side/small framings — caricatures the face. Do NOT chop scenes into
     talking-head CUs to get sync — that IS the failure the owner rejected.
   **QA lesson (binding):** judge lip-sync against ANATOMY ("is this where the character's mouth
   physically is in this pose?"), not overlay placement. See the deep-research report + owner decision
   before any new lip-sync build.

**Hard sub-rules (owner-set):** no static scenes (every shot has real, meaningful motion); **never pan
or shake a static image**; no scene under ~3 seconds unless truly unavoidable (a brief sanctioned sync
intercut ~1.3s+ INSIDE a continuous scene is a cut-in, not a scene — exempt); **character animation
must always support the dialogue.** This LAW governs §5, §8, §9 and §10 below — wherever they say
"beat," read "**section**."

---

## 1. THE KLING 3.0 COST GATE  *(hard rule — Kling is expensive)*

> **⚠️ OPERATES UNDER [VIDEO_COST_BLUEPRINT.md](../../../docs/guides/VIDEO_COST_BLUEPRINT.md) — PROJECT LAW.**
> **Never spend premium video on EXPLORATION.** Scout the prompt/shot CHEAPLY (Kling 2.5/3.0 Turbo /
> Hailuo / Runway — NEVER a banned/avoid model: Kling 2.6 is BANNED and Seedance drifts characters —
> see the tier table below), lock prompt+duration+aspect+refs, THEN render Kling 3.0 **once** for the final.
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
`kling-2.6`). Confirm the exact KIE slug for the **Kling Turbo cheap tier** before the first
cheaper-tier render (no Seedance slug is needed — that tier is AVOID, and "Seedance 1.5 Pro" doesn't
exist on our backends), and keep the locked element-refs / hand-pick flow for any model.

**Budget discipline:** aim for a small set of Kling hero shots per episode (target ~12–18), and cover
everything else by reuse/stills/cards. Log credits spent per episode. If the Kling count climbs,
challenge each shot against the gate above.
- **Candidates live at the KEYFRAME layer (~2cr each), NOT the render layer.** "4–8 candidates" means
  4–8 *keyframe* candidates hand-picked before any render. A hero shot then gets **ONE Kling render**
  from the picked keyframe plus a **hard reroll cap of ≤2** — it never means 4–8 × 70cr renders
  (that reading is a 4–8× budget blowout; the EP3 402 was reroll spirals).
- **Reroll escalation ladder** (drift that survives 2 rerolls is a DESIGN problem, not a dice problem):
  reroll (≤2) → **RESTAGE** the beat (different angle/distance/staging, mouth hidden) → **downgrade**
  to reuse/still/card → **flag to the owner**. Never keep rerolling the same shot.
- **Pre-flight credit estimate (part of the Animatic Lock sign-off):** compute
  `BRIDGE count × 70cr × 1.15 (reroll reserve)` and put the number in front of the owner WITH the
  animatic. **No approved estimate = no render spend.**
- **New-world episodes** (new location/guest, thin reuse library — e.g. EP4): the "reuse covers most
  non-hero beats" assumption is calibrated on EP2's library and does NOT hold by default. Expect a
  higher BRIDGE count, compute the estimate honestly, and lean harder on stills/Ken-Burns/cards for
  the non-hero remainder.

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
  chest blaze, **paws the SAME COLOR as her coat — NO white socks/toes**, **short docked tail stub only**,
  teal collar + gold paw-print Listening Tag. Cartoony-Pixar style (not photoreal).
- **⚖️ PROMPT-PHRASING LAW (owner, 2026-07-02 — root cause of the crayon-RED-paw drift):** NEVER write
  a color word for the paws in any generation prompt ("red-fawn paws"/"solid red-fawn paws" makes
  models paint literal RED paws). Correct prompt text: **"paws the same color as her coat, no white
  socks."** The paws are not a feature — the absence of color difference is. **The ONE sanctioned
  exception** (owner-forced 2026-07-04): the EMPHATIC paw block inside the ON-MODEL KEYFRAME RECIPE
  (playbook §3.2), where the color word is bound to the coat in the same breath ("…SOLID RED-FAWN,
  the exact same color as her coat — NO white paws/socks/toes"). Only that exact coat-bound
  construction; never a standalone color phrase.
- **⚖️ ON-MODEL KEYFRAME RECIPE + ASSET QUALITY BAR (owner, 2026-07-04):** nano-banana-pro drifts
  Bentley by default (whiter paws, more cartoonish) — every character keyframe follows the recipe in
  playbook §3.2: master-fidelity prompt + emphatic coat-bound paw block + ≥4 keyframe candidates
  hand-picked + mandatory **PAW-ZOOM QC**. Masters/props/plates generate at `resolution: "4K"`,
  keyframes at 2K; every accepted image passes the sharpness floor (edge-var ≈100 through the 1080p
  pipeline) — soft assets are re-generated, never shipped or "fixed in post."
- **NEVER a human smile or human teeth**, and she never stands/acts like a person. Dog joy = tongue
  out, soft eyes, tail-stub wiggle.
- Generate Bentley only from `Bentley_MASTER_pixar.png` (+ turnaround); **4–8 candidates per keyframe,
  hand-pick the on-model one, NEVER auto-batch-and-ship** — the generator drifts. (Keyframe
  candidates are cheap; renders are not — see §1 budget discipline for the render-side cap.)
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
- **Dialogue = the CONTINUOUS-SECTION LAW (§0), NOT a talking-CU per line.** ⚠️ **This supersedes the
  old "Avatar face-CU on every talking beat" method** — intercutting a tight talking-CU for each line is
  exactly the sentence-by-sentence chopping the owner rejected on EP3. Build each dialogue **section** as
  ONE continuous **VO-over-alive** two-shot (i2v prompted hard for natural talking mouths). Reserve
  **Kling-Avatar** (`kling/ai-avatar-standard`, ~40 cr, image+audio) for the **signature "Stop. Look.
  Listen." moment ONLY** — plus a rare true-hero line *only if* no video-to-video sync tool is available
  (see §0.3). When you DO use Avatar, it stays on-model only from the **ONE locked Talking prop
  (Rule 2): `assets/character_design/Bentley_TALKING_MASTER.png`** — ✋ owner lock of this file IS the
  EP4 asset gate (playbook §3.1); until it is locked, the EP1–EP3 legacy keyframe
  `assets/approved/bentley/N6_kie_key_bright2.png` remains the working reference. **Never use both in
  one episode** — two "approved" talking faces is a Rule 2/7 violation by construction. A
  wide/dim/small/side keyframe CARICATURES her (bulging eyes, human grin) — that failure is the
  keyframe, not the model. Small puppy teeth ok; no human grin. Full Avatar method:
  [TALKING_LIPSYNC_METHOD.md](../../../docs/guides/TALKING_LIPSYNC_METHOD.md).
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
   **Measure the ratios, don't eyeball them:** tag every EDL piece with a `scale`
   (`solo_cu`/`two_shot`/`wide`/`medium`/`insert`/`card`) and run
   `python -m bentley.qa.shot_ratios <shotlist.json>` at animatic time — the check is free arithmetic
   there; an untagged or over-ratio EDL doesn't pass the Animatic Lock.
2. **Longer continuous scenes, NOT many short stitched clips.** Prefer fewer, longer shots that hold the
   whole beat. **Never cover one VO by stitching two sub-ranges of the SAME clip, and never reuse a clip
   @0 across back-to-back beats** — both read as a cheap loop. A line that outlasts its clip gets ONE
   continuous generated/retimed shot, not a splice.
3. **Cohesive scene-to-scene flow.** Every cut flows from the last (hard cut / match-cut on continuing
   motion); it must feel like a story, not a montage. **Show the cause before the reaction** (e.g. show
   the octopus turned Bentley-colored *before* Bentley says "you did me!").

---

## 6. TRANSITION RULES
- **No dip-to-black between shots, ever** (the v7 disaster: every cut faded through black), and **no
  opening fade-from-black either (owner rule, 2026-07-04 — supersedes the old "open/close fades")**.
  The ONLY black is one long warm fade-out at the very end.
- Default transition is a **hard cut**. **Match-cut** on a continuing motion/shape for momentum.
  **Crossfade (~0.4s)** only for a real time/place jump or an emotional settle.
- No clip ever repeats (callbacks = different sub-range); no loops. One continuous scene per section
  (§0) — "one clip per beat" means *no reuse*, never one-clip-per-VO-line. Transitions are an **edit**
  operation — never a Kling render.

---

## 7. VOICE RULES
- **Locked voices:** Bentley = LauraZ (`tts_bentley`); the guest = its locked voice (e.g. Indi =
  `eleven.INDI`, `tts_indi`); Narrator = Bill (`tts_bill`/`eleven.NARRATOR`, grandpa settings); Pip =
  Callum +10% pitch.
- **The catchphrase "Stop. Look. Listen." is ALWAYS Bentley's**, never the narrator's, in every
  episode including outros — three words with a deliberate pause between each (`tts_catchphrase`).
- Every line is assigned to the correct speaker and plays over a shot of **that** character (a guest
  line that reads as Bentley is a known defect). Re-record only the lines whose text changed — **or
  whose read is flat** (see next bullet).
- **⚖️ PERFORMANCE + TAKE-VARIANCE LAW (owner, 2026-07-04):** a flat, emotionally-neutral read is a
  DEFECT — every emotive line carries eleven_v3 audio tags (`[gasps]`, `[thrilled]`…) + energetic
  punctuation. eleven_v3 is NONDETERMINISTIC per take → production recording is **BEST-OF-3 with a
  measured pick** + two-pass loudnorm to −16 LUFS, then the per-line VO QC table BEFORE the animatic
  (tools: `bentley/voices/best_of.py`, `bentley/qa/qa_vo.py`; full law: playbook Part 2 step 5).
  A flagged line never reaches the cut.
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
> **This §9 is the CANONICAL release checklist.** Playbook Part 8 is its procedure manual (scan
> thresholds + how-to); if they ever diverge, §9 wins and the divergence is a chain defect to fix the
> same day. **Gate ledger:** before trusting any "already approved" claim, check
> `episodes/<ep>/GATES.md` — every ✋ gate pass is recorded there; an unrecorded gate is an UNPASSED gate.

**§0.0 TEN-RULE GATE (owner law — CHECK FIRST, ship-blocking).** Walk the finished cut against ALL TEN
mandatory rules in §0.0 and confirm each passes: (1) action carries every beat, not talking heads · (2)
Bentley talking shots from the approved master prop only · (3) every shot compared to the master, no
drift · (4) no CU parade — medium/wide default · (5) one continuous scene per beat · (6) invisible
transitions · (7) Bentley identical throughout · (8) story + Animatic Lock done before any render · (9)
only the speaker's mouth moves in a two-shot · (10) scenes feel animated, not clip-stitched. Any rule
failing = **not approved for release.**

**Continuity / sections (§0 — CHECK FIRST, ship-blocking)**
- [ ] Cut sentence-by-sentence? **FAIL.** Each logical section is ONE continuous scene, not 3–5 stitched
      clips. Count shots per section — a dialogue exchange chopped into per-line clips is the #1 defect.
- [ ] Any **giant single talking-head CU** as a whole beat? Only the "Stop. Look. Listen." moment may be
      a tight synced CU; everywhere else is two-shots / wides / action.
- [ ] Every scene has real motion; **no static shot, no pan/shake over a static image**; no scene < ~3s
      (a sanctioned sync intercut ~1.3s+ inside a continuous scene is a cut-in, not a scene — exempt).
- [ ] Character animation supports the dialogue (e.g. "I'm smelling" = actively sniffing, not lying still).

**Technical**
- [ ] Black-frame scan: **no** interior black (only the closing fade — NO opening fade, owner rule 2026-07-04).
- [ ] No reused/looped frames; callbacks use distinct sub-ranges.
- [ ] No static-with-zoom-only shots; no clone-pad freezes; no >1.3× slow-mo.
- [ ] Grade consistent across shots (mood shots intentionally darker, not flat/pale).
- [ ] Streams OK (1080p, audio present); delivered under a **fresh filename**; a frame from the FINAL
      file visually verified.

**Canon / character**
- [ ] Every Bentley shot: docked tail, floppy ears, paws same color as coat (no white socks, not red), tag, black mask.
- [ ] No human smile / human teeth (Bentley or guest).
- [ ] Guest on-model (eyes/eyespots/no human face).

**Story / audio**
- [ ] Every line over the correct, *alive* speaker; catchphrase is Bentley.
- [ ] Any lip-synced element judged against ANATOMY (mouth where the character's mouth physically is
      in that pose), not overlay placement (§0.3 — the 2.5D patch failure).
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
- [ ] **Shot-scale ratios measured** (§5a): every EDL piece carries a `scale` tag and
      `python -m bentley.qa.shot_ratios` passes (≤ ~35% solo heads, ≥ ~25% two-shots).
- [ ] **Credit estimate presented and approved:** `BRIDGE count × 70cr × 1.15` computed and put in
      front of the owner WITH the animatic (§1). No approved estimate = no render spend.
- [ ] **Scope disclaimer signed in the gate ledger** (`episodes/<ep>/GATES.md`): certifies STORY + CUT
      only — NOT on-model character, identity hold across shots (the #1 blocker), lip-sync, grade, or
      that placeholder timing survives generation. Those stay with §10 step 5 hand-pick + this §9 on
      the FINAL file.
- [ ] Overlap note: **§5a SHOT-FLOW LAW is authoritative** for wrong-speaker / same-clip / cause-before-reaction on the FINAL cut.

---

## 10. THE PRODUCTION WORKFLOW (ordered; don't skip)
1. **Script → SECTIONS (§0)** — produce/approve the script with `cinematic-episode-writer`, then **group
   it into ~8–12 LOGICAL SECTIONS** (spine → sections → VO list → EDL/cue sheet → bridge-shot list). The
   EDL is **section-based, one continuous scene per section — NOT one clip per VO line** (§0). Tag each
   section REUSE vs BRIDGE, in the machine-runnable JSON schema the step-4 animatic consumes.
2. **Tag every SHOT against the §1 cost gate** — confirm each BRIDGE section truly needs Kling; cover
   over-long sections with 2–3 continuous shots of the SAME evolving scene (never per-sentence clips) +
   stills/Ken-Burns. Downgrade the rest to reuse / still / card / cheaper model. Get owner sign-off on
   the Kling list *before* spending (approve-direction-first).
3. **VO — assemble the COMPLETE reel** — record changed/new lines (locked voices) AND concatenate the
   full VO set (new + reused mp3s) **in script order** into the reel the step-4 animatic consumes.
   (The dropped-line check in step 4 has no input without the full reel.)
4. **Story Scratch / Animatic Lock** *(owner-mandated; ship-blocking; ZERO Kling/KIE/ElevenLabs
   credits)* — before **any** Kling spend, build a TIMED animatic of the WHOLE episode on the cue-sheet
   EDL: the complete recorded VO in canonical order over placeholder picture, where every beat is a
   reused clip, a Ken-Burns still of a locked master/plate, or a **labeled card naming the speaking
   character + beat** (un-shot BRIDGEs auto-render a card — never silently skipped). Watch it twice
   (audio-only, then muted) and clear the **Animatic Lock** sub-checklist in §9. **No Kling render runs
   until the owner signs off the animatic — record the sign-off + the §1 credit estimate in
   `episodes/<ep>/GATES.md`.** On PASS the animatic shotlist is the **STARTING EDL** for
   assembly; placeholder durations are estimates, so re-check/re-time the cut rhythm at step 6/§9 after
   the real shots land (this is "start from the locked story EDL," NOT "zero rework"). Overlaps §5a
   (wrong-speaker, same-clip-back-to-back, cause-before-reaction): the animatic is the *pre-render*
   pass; **§5a stays authoritative on the FINAL cut.**
   > **TOOL (built 2026-06-27 — gate now SATISFIABLE):** the productionized JSON-shotlist animatic is
   > `bentley/episode_builder/animatic.py` (+ `placeholders.py`: the extracted `ken_burns()` and the
   > `shorts.py`-caption labeled card). Run:
   > `PYTHONPATH=. python -m bentley.episode_builder.animatic episodes/<ep>/shotlists/<list>.json`
   > → one `episodes/<ep>/<EP>_ANIMATIC.mp4` + `_timeline.json` (the STARTING EDL). It reads the
   > `{id,type,dur,src,vo,over,status}` schema; picture = reuse clip → Ken-Burns still → labeled card
   > (un-shot beats auto-card, **never** silently skipped); audio = the existing per-line mp3s
   > concatenated in script order (**no TTS** — that spends ElevenLabs). A hard credit guard allows only
   > `ffmpeg`/`ffprobe`; it imports nothing from `bentley.animation.*` / `bentley.asset_generation.*`
   > and never calls `pipeline.py <shotlist>` / `produce()`. Proven on EP2 (36 beats, 0 credits);
   > regression-tested in `tests/test_animatic.py`.
5. **Generate the approved Kling bridge shots** — 4–8 **keyframe** candidates each (~2cr, hand-picked),
   then **ONE render per shot + the §1 reroll cap (≤2, then restage/downgrade — never keep rolling)**,
   **owner/hand pick**, QC every frame vs canon; never auto-batch. *(A green animatic certifies STORY + CUT, **not** on-model render — character drift is
   caught ONLY here and at §9. For new-character episodes — e.g. EP3: Mari, no locked master,
   Bentley+Mari scale two-shots — keep this hand-pick LOUDER than the animatic sign-off, never quieter.)*
6. **LIP-SYNC PASS — ON HOLD (§0.3):** the 2.5D patch renderer was owner-rejected (anatomically wrong
   on free-posed heads). Until the researched replacement is adopted: dialogue = VO-over-alive per
   §0.3, catchphrase = Kling-Avatar tight-CU. Any lip-sync QA judges ANATOMY, not overlay placement.
7. **Assemble** — data-driven from the animatic shotlist (its EDL graduates in place: each `todo`
   placeholder is replaced by its rendered — and rig-synced — clip); hard cuts + match/cross per the
   EDL; one clip per beat; minimal re-encodes (build each beat in one pass, concat by copy, one final
   encode in the mix).
8. **Sync-verify** — `bentley/qa/verify_sync.py`: one voice at a time, mouth == voice, no overlap.
9. **Mix** — music beds by mood, ambience, SFX, ducked under VO; ONE closing fade-out only (no
   opening fade-from-black — owner rule 2026-07-04).
10. **Grade** — one consistent grade over the whole episode; avatar darkening lifted.
11. **QA §9 against the FINAL file**, then deliver under a fresh filename with its absolute path.
