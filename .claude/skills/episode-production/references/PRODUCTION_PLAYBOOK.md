# BENTLEY'S BIG ADVENTURES — PRODUCTION PLAYBOOK

**Version 1.3 · 2026-07-05 · v1.3 = THE FIX-FIRST LAW (owner-directed 2026-07-05): every recurring
defect is checked against an internal fix tool BEFORE any regeneration — regen is the LAST resort.
Ladder + inventory: SKILL §1b + `docs/guides/FIX_FIRST_TOOLKIT_PLAN.md`; FULL toolkit built &
✋-approved 2026-07-05 — zero-token: `bentley/fix/{magic_wand,recolor,tail_dock,tail_trim,
shot_match,plate_match,prop_paste}.py` + `bentley/qa/{edl_lint,scan_suite}.py`; surgical-edit
tier `bentley/fix/kontext_edit.py` (FLUX Kontext, productionized from the s10a eye fix). ·
v1.2 = RULE 11: incremental production, never large batches (owner law
after the EP4 mis-styled 36-image keyframe batch — 720 cr lost to ONE systematic error × batch size);
waves codified in §3.2/§3.3/Part 8.2/Part 11. · v1.1 (2026-07-04) = premortem reconciliation
(no-opening-fade everywhere, paw-law exception cross-linked, scout tiers corrected, candidates =
keyframe-layer + render reroll cap, pre-flight credit estimate, gate ledger, promoted QA tooling).**
**This is the reference manual OF the `episode-production` skill** — it lives in that skill's
`references/` (same pattern as `cinematic-episode-writer`'s references). The SKILL.md is the short
enforcing rulebook that auto-loads on every production task; THIS file is the full operating manual,
read at the **start of each episode** and at post-mortems. **One normative chain, no parallel sources:
11 Mandatory Rules (owner law) → SKILL.md (enforcement) → this playbook (procedure & history).**
When a rule changes, update the chain together — a rule changed in one document only is itself a defect.
**Version discipline:** bump the Version line above on EVERY owner-law change, back-port the change into
SKILL.md the same session, and never edit the chain from two parallel sessions (that is how the
fade-rule contradiction of 2026-07-04 was born). **Gate discipline:** every ✋ gate pass is recorded in
`episodes/ep<N>/GATES.md` — an unrecorded gate is an unpassed gate.

**ALL episode-creation skills align to this chain (owner law 2026-07-03) — they help each other, never
contradict:** `cinematic-episode-writer` (+ its references `shot-and-pipeline.md` / `story-craft.md` /
`bentley-canon.md`) writes FOR these rules; `lipsync-pro` is the lip-sync authority the chain defers to
for method detail (production §0.3 and Part 6 here are its summaries). Each carries a header naming the
chain; a cross-skill alignment check is part of every post-mortem (Part 12).

It exists because EP3 took **~15 revision cycles** to reach releasable quality — and almost every cycle
was a *predictable* failure we had already met in EP1/EP2. The goal: **higher quality on the first pass,
minimal rework, minimal AI credit/token burn.**

---

## PART 0 — EP3 POST-MORTEM (why this playbook exists)

### What WORKED (keep doing)
| Practice | Evidence |
|---|---|
| **Section-based EDL** (`build_sections.py` → assembler): one continuous scene per story beat, VO laid over it | v8 rebuild fixed the "stitched montage"; the owner's cut notes dropped sharply after |
| **Animatic Lock** — validate the WHOLE story as a zero-credit timed animatic before any Kling spend | EP2 proven at 0 credits; story/cut problems caught before they cost anything |
| **Locked masters + `kling_elements` + hand-picked candidates** | Every drift incident traces to a shot that skipped one of these |
| **Kling-Avatar on a tight, bright, FRONT-FACING face CU** for talking shots | The one reliable word-accurate sync method; wide/dim/side framings caricature |
| **OmniHuman mask** for in-frame two-shot sync (speaker masked, listener still) | Proved on Marco-class characters; fails when a dominant face is in frame |
| **Wrong-speaker motion heatmap** (`scratch/ep3/qa_mouthmotion.py`) + **EDL sync trace** as the lip-sync gate | Caught the flapping-listener defects; the *automated audio-correlation detector* was proven unreliable — the EDL trace IS the gate |
| **Locked-camera re-render** instead of post-stabilization | Deshake made the opening WORSE (jitter 13.3 vs 10.3); locked re-render measured 4.8 |
| **Measured QA** — jitter (mean frame-diff), sharpness (edge-var), 24fps freeze scans, frame sheets | Every owner-flagged defect this cycle was reproducible as a number first; "looks fine" isn't evidence |
| **Freeze-push math check** on the EDL before assembling | `wants Xs / clip Ys / push=0.00` — 30 seconds of arithmetic that catches every freeze before rendering the cut |
| **Tail-trim** on Kling clips (they hold the last frame) | The 4:47 micro-freeze was a frozen Kling tail; trim to the last moving frame |
| **Sharpen pass tuned to the pipeline** (unsharp 1.8 measured through 720p→1080p) | Rescued the soft butterfly ending; verify halo-free at final size |
| **Fresh filename + verify a frame from the FINAL file** | Prevents silently-stale delivery (players cache by name; re-renders get pinned to old srcs) |

### What FAILED (never repeat) — each with its root cause
1. **Built the episode per-VO-line first** → stitched montage, angle change every sentence. *Root cause:
   thinking like an editor ("which clip next?") instead of an animator.* → Rule 5/10, §2.
2. **Giant talking-head parade** (v4) → owner rejected the whole cut. *Root cause: chasing lip-sync by
   chopping scenes into CUs.* → Rule 4, §5.
3. **Character drift across shots** — "0:23 and 0:26 are different Bentleys." *Root causes: fresh
   talking keyframes per shot; conform re-renders drifting further; no per-shot master comparison.* →
   Rules 2/3/7, §6.
4. **Lip-sync rabbit holes** — the 2.5D mouth-patch system (rejected 3×), per-frame AI restyle (flickers),
   video re-sync tools (human-lip trained). Weeks of effort, zero shipped output. *Root cause:
   re-exploring a solved/known-dead problem instead of using the proven methods.* → §7 method table is CLOSED;
   new methods require an owner-approved research gate first.
5. **15/25 dialogue lines were VO-over with visible flapping mouths.** *Root cause: no per-line sync trace;
   Kling invents mouth motion it can't hear.* → Sync-or-Hide law, §7.
6. **Freeze-stretch defects** (0:12, 4:47, the 2s end freeze) — VO longer than the clips under it; retime
   caps at 1.5× and the assembler freezes the last frame. *Root cause: EDL authored without the
   freeze-push math.* → §4 step 6, hard constraint C6.
7. **Post-fixing bad renders** (deshake, upscale-stretch) instead of re-rendering right. *Root cause:
   sunk-cost thinking; a 70cr locked-camera re-render beats every filter.* → §3 render laws.
8. **Prompting paw colors** ("red-fawn paws" → literally red paws). *Root cause: color words in prompts
   get painted.* Say "paws same color as her coat, no white socks." → §6 prompt language.
9. **Environment shots generated from the character master alone** → invented wrong worlds (Sahara dunes,
   giant bread loaf). *Root cause: no scene anchor.* ALWAYS nano-banana-EDIT an actual episode frame. → §6.
10. **Credits ran out mid-episode (402)** after thousands spent on revisions. *Root cause: rendering before
    QC-ing keyframes, batch fixes not batched, drift rerolls.* → §11 budget discipline.
11. **Delivered un-QA'd cuts** — owner caught wrong-shot-under-line and loop defects that a per-beat check
    would have found. *Root cause: QA-ing parts, not the FINAL file.* → §10.
12. **Skipped pipeline stages** (EP2 regression, 5-agent RCA) — shotlist/assemble/mix/grade order exists
    for a reason. → §3 stage order is mandatory.

### The one-sentence lesson
> **Every expensive failure was a planning failure.** The cheap phase (script, EDL math, keyframe QC,
> animatic) is where quality is decided; the expensive phase (Kling) must only ever execute an
> already-validated plan.

---

## PART 1 — THE 11 MANDATORY PRODUCTION RULES (owner law, 2026-07-03; Rule 11 added 2026-07-05)

Full text: `youtube_vault/Rules/Production Standards (10 Mandatory Rules).md` (filename kept for link
stability; content covers all 11) and `episode-production` §0.0. Short form — **all eleven are
ship-blocking**:

1. **Action over dialogue** — multi-character action + environmental life under every VO line.
2. **Approved master talking prop ONLY** — one locked Talking prop per character; no alternatives ever.
3. **Never drift from approved style** — every shot compared to the master before it reaches the cut.
4. **No extreme close-up parade** — medium/wide default; CU only for a genuine emotional beat.
5. **One cohesive scene per story beat** — never sentence-by-sentence stitching.
6. **Invisible transitions** — if the audience notices the edit, it failed.
7. **Absolute character consistency** — same Bentley, every frame.
8. **Story before animation** — script + Animatic Lock BEFORE any render spend.
9. **Multi-character lip-sync QA** — only the speaker's mouth moves. Mandatory release gate.
10. **Think like an animator, not an editor** — build scenes, don't stitch clips.
11. **Incremental production — never large batches** (2026-07-05) — keyframes AND renders go out in
    small gated waves: validation wave first → ✋ owner approval per group → only then the next group.
    Every stage has a quality gate before additional tokens are spent.

---

## PART 2 — STORY PLANNING WORKFLOW  *(cheap phase — where quality is decided)*

**Owner gates are marked ✋. Nothing renders until gate 3 passes.**

1. **Premise lock** (`cinematic-episode-writer`): science subject, guest character, Bentley's lesson,
   next-episode hook. ✋ *Owner confirms premise.*
2. **Spine → beat sheet → dialogue**: one feeling, one lesson, 3–4 facts that ARE the plot. Every beat
   causes the next. Mandatory beats: cold-open hook (10–15s), ≥1 non-plot bonding beat, the
   catchphrase at the emotional turn (Bentley only), next-time hook consistent with the LOCKED next
   episode (EP4 = The Butterfly Highway; the girl monarch is silent, narrator carries her hooks).
3. **Section grouping (Rule 5, done in writing)**: group the script into **8–12 logical sections**.
   For each section define: the ONE evolving scene, who is on screen, what they are *doing* during every
   line, which lines are sync-tool lines vs staged mouth-hidden. **No section is a lone talking head.**
4. **EDL as machine-runnable JSON** (`episodes/ep<N>/shotlists/ep<N>_master.json`) with real file paths.
   **Run the freeze-push math on every section now**: VO duration vs clip coverage; every piece must show
   `push=0.00` at retime ≤1.3×. If a section's VO is 17s, plan 3–4 clips — not 2. **Mechanical since
   2026-07-05:** `python -m bentley.qa.edl_lint <shotlist>` does this arithmetic (VO-vs-picture,
   retime ceiling, same-clip back-to-back, missing media) with an exit-code gate — run it here and
   again after every clip swap.
   **Tag every piece with a `scale`** (`solo_cu`/`two_shot`/`wide`/`medium`/`insert`/`card`) and run
   `python -m bentley.qa.shot_ratios <shotlist>` — the Shot-Flow ratios (≤ ~35% solo heads, ≥ ~25%
   two-shots) are free arithmetic here and unmeasurable later by eyeball.
5. **VO recording — with PERFORMANCE direction (owner law 2026-07-04).** A flat, emotionally-neutral
   read is a DEFECT (the "Best. Morning. EVER!" lesson: periods cue a deadpan read). Every emotive line
   carries eleven_v3 audio tags (`[gasps]`, `[thrilled]`, `[whispering]`, `[big yawn]`…) + energetic
   punctuation matched to the moment; excited sounds excited, curious sounds curious. Spot-listen each
   character's takes before the animatic; flat = re-record (cheap here, expensive later). For mlv2
   voices (tags unsupported/stripped) shape emotion via punctuation + word choice.
   **Take-variance law (measured 2026-07-04):** eleven_v3 is NONDETERMINISTIC per take — identical
   settings produced a 15× clarity spread across Bentley's lines (0.23%–3.48%, 4–10 kHz band).
   Production recording is therefore **BEST-OF-3 with a measured pick** (score = clarity − loudness
   penalty; library `bentley/voices/best_of.py`, episode usage pattern `scratch/ep4/record_best_of.py`)
   + **two-pass loudnorm to exactly −16 LUFS** (single-pass undershoots short clips). Run the per-line
   QC table (`python -m bentley.qa.qa_vo <vo_dir>`: LUFS / true-peak / clarity% / centroid, outliers
   flagged per speaker) before the animatic — a flagged line never reaches the cut.
   (locked voices only: Bentley=LauraZ, Narrator=Bill, guest=its locked voice;
   catchphrase = `tts_catchphrase`, three words, deliberate pauses).
6. **✋ ANIMATIC LOCK** (`python -m bentley.episode_builder.animatic <shotlist>`): the full story as a
   timed zero-credit animatic (recorded VO over reuse/stills/cards). Owner watches it END TO END and
   approves STORY + CUT. **Present the pre-flight credit estimate WITH the animatic**
   (`BRIDGE count × 70cr × 1.15 reroll reserve`) — the owner approves the story AND the spend in one
   gate; no approved estimate = no render spend. **Record the sign-off + estimate in
   `episodes/ep<N>/GATES.md`.** **This is the point of no return for the script — no story changes
   after render spend begins.** (Certifies story/cut only, NOT visual drift.)

---

## PART 3 — ANIMATION WORKFLOW  *(expensive phase — executes the validated plan)*

**Stage order is mandatory. Skipping stages caused the EP2 regression.**

### 3.1 Asset gate (before ANY shot)
- All recurring masters LOCKED and frozen: `Bentley_MASTER_pixar.png` (+ turnaround),
  **`assets/character_design/Bentley_TALKING_MASTER.png`** (the ONE Rule-2 talking prop — ✋ owner lock
  = the EP4 asset gate, recorded in `episodes/ep4/GATES.md`; once locked it SUPERSEDES the EP1–EP3
  legacy Avatar keyframe `assets/approved/bentley/N6_kie_key_bright2.png` — never use both in one
  episode), guest master (e.g. `Marco_LOCKED.png` + model sheet), episode environment plate
  (established once, reused as the scene anchor for every keyframe).
- New guest? Design → ✋ owner locks the master → only then write shots that lean on the look.

### 3.2 Keyframes (nano-banana-pro / nano-banana-edit)
- **⚖️ RULE 11 — INCREMENTAL WAVES (owner law 2026-07-05):** NEVER generate the episode's full keyframe
  set in one batch — the EP4 painterly batch burned 720 cr on ONE systematic style error × 36 images.
  Calibrate ONE shot side-by-side vs the master → ✋ owner sign-off on that single image → then waves of
  ~4–6 shots, each hand-picked, QC'd, and ✋ owner-approved before the next wave generates anything.
- **ASSET QUALITY BAR (owner law 2026-07-04 — "every asset sharp, clean, production quality"):**
  masters / props / plates / thumbnail bases generate at **`resolution: "4K"`** (5504×3072, 24cr —
  capital K; lowercase "2k" is a 500 error); keyframes at 2K default (2752×1536). EVERY accepted image
  passes a sharpness check (edge-var through the delivery pipeline, floor ≈100 at 1080p) — soft,
  low-detail, or mushy assets are REJECTED and re-generated, never "fixed in post" or shipped.
- **Character keyframes:** generate FROM the locked master(s) via `nano-banana-pro` (`image_input` list).
  **Never regenerate a master. Never generate from a previous generation.**
- **Scene/environment keyframes:** ALWAYS nano-banana-**EDIT** an actual episode frame (generation from a
  character master alone invents wrong worlds).
- **Known model gotchas:** nano-banana whitens paws/toes by default — a paw region is trusted ONLY
  after the recipe's paw-fix EDIT pass + toe-level zoom QC (steps 4/4b below; a *generation* pass is
  never asked to restyle paws on its own); the docked tail slips to long — run a DEDICATED second edit
  pass to shorten it when it does.
- **⚖️ THE ON-MODEL KEYFRAME RECIPE (owner-forced 2026-07-04 after white-paw/cartoonish rejection).**
  nano-banana-pro DRIFTS Bentley by default — **whitens her paws** and **renders her more cartoonish**
  than the master, *regardless of the prompt*. Non-negotiable recipe:
  1. **Master-fidelity prompt**: lead with "keep Bentley EXACTLY identical to the reference master —
     same face, fur, eye size/shape, refined proportions and realistic render style; do NOT make her
     more cartoonish or enlarge her eyes." Pass BOTH the body master AND the turnaround as refs.
  2. **EMPHATIC paw block** (the prompt "no white socks" alone FAILS): "CRITICAL: her paws, feet and
     lower legs are SOLID RED-FAWN, the exact same color as her coat — NO white paws, NO white socks,
     NO white toes." **This exact coat-bound construction is the ONE sanctioned exception to the
     prompt-phrasing law (SKILL §3 / §3.3 below):** the color word is permitted ONLY bound to "the
     exact same color as her coat" in the same sentence — never *name* a paw color in isolation
     ("red-fawn paws" → literal red paws).
  3. **Generate ≥4 candidates, HAND-PICK** — never ship one roll (that was the failure).
  4. **PAW-ZOOM QC (mandatory):** crop the lower-body/paw region of EVERY candidate and view it
     enlarged next to the master — do NOT trust the wide shot or the prompt. White paws = REJECT.
     If all candidates drift, run the step-4b paw-fix pass, then **re-run this PAW-ZOOM QC on the
     fixed frame** before the shot may enter the cut — a paw-fix that hasn't re-passed QC is
     unverified, not fixed.
  4b. **PAW-FIX — MAGIC WAND FIRST (0 cr), AI edit second (owner-commissioned tool, 2026-07-05):**
     white paws/toes are fixed with `bentley/fix/magic_wand.py` — a LOCAL zero-token recolor
     (`PYTHONPATH=. python -m bentley.fix.magic_wand preview|fix IMG --box x,y,w,h --coat x,y`):
     it samples the coat IN-SHOT (matches that shot's light by construction — no red over-correct)
     and touches nothing outside the boxes. DISCIPLINE: preview the mask overlay BEFORE fixing;
     boxes hug the paws (blaze/white flowers in a box will recolor — same pixel signature); the
     coat sample must be true fawn (tool rejects collar/teal). Escalate to `google/nano-banana-edit`
     (~4cr, "repaint her paws/toes/feet SOLID red-fawn to match her coat…") only when the wand can't
     (extreme cream gradients, anatomy-level drift). Either way, finish with **toe-level zoom** QC
     (crop ~0.5×0.5 on the paws, enlarge) — do not rely on the pick sheet.
  5. Guest scale: state the guest's real size ("Mira is a SMALL butterfly, ~the size of the puppy's
     eye") — the model over-sizes small guests.
- **✋ KEYFRAME QC GATE (cheap, mandatory):** before any Kling render, compare each keyframe against the
  master side-by-side — identity, proportions, style tier, paws (coat-colored, no socks), docked tail,
  tag/collar, no human teeth. Rejecting a keyframe costs ~2cr; rejecting a render costs 70cr.

### 3.3 Renders (Kling 3.0 — hero shots only)
- **Cost gate first** (`episode-production` §1): character emoting/interacting/hero moment → Kling 3.0.
  Everything else → reuse / Ken-Burns still / card / editor. Target **12–18 Kling shots/episode**.
- **Render defaults:** `kling-3.0/video` i2v · `multi_shots: False` · `kling_elements` with the locked
  master + turnaround (**2–4 images required** — 1 image is a 400 error) · prompt ≤ **300 chars** ·
  **"LOCKED STATIC TRIPOD CAMERA"** unless the beat truly needs a move (locked camera measured 3×
  stabler and sharper than deshaked handheld) · 5s duration (plan sections around it). **Build the payload
  with `bentley.shared.render.render_shot(prompt, candidates=[...], ref=MASTER, last_frame=…, out=…)`** —
  the sanctioned path that bakes in best-of (#4) + last-frame pin (#3) + the Bentley element. Last-frame
  pinning is now **mechanically enforced** (`bentley/shared/drift_guard.py` in `kie_client.run`): a
  character video render that isn't pinned is REFUSED unless `BENTLEY_PIN_OVERRIDE="<reason>"` is set for a
  deliberate big-motion beat. Keyframe candidates are ranked measured, not by eye (`bentley.qa.image_bestof`
  — no seed exists on this stack).
- **Prompt language laws:** never name a paw color ("paws same color as her coat, no white socks");
  "SHORT DOCKED TAIL STUB"; "mouth closed" for every non-speaking character in frame; motion verbs for
  the speaker's *body* (not mouth) on VO-over shots.
- **Ops:** failCode 50430 = concurrency → 30–90s backoff-retry; 400/422 = deterministic → fix payload,
  don't retry; on **402 (credits out): STOP and tell the owner** — never hunt for workarounds.
  Video renders run with `BENTLEY_EPISODE=ep<N>` set — `kie_client` mechanically refuses video models
  until that episode's GATES.md records the Animatic Lock PASSED (`bentley/shared/gates.py`); a
  PermissionError here means a gate is missing, not a bug to work around.
- **Candidates live at the KEYFRAME layer (~2cr), not the render layer:** 4–8 keyframe candidates per
  shot, hand-picked. A hero shot then gets **ONE Kling render** from the picked keyframe + a **hard
  reroll cap of ≤2**. Past the cap the shot is REDESIGNED, never rerolled again — the escalation
  ladder is: reroll (≤2) → restage the beat (angle/distance/staging, mouth hidden) → downgrade to
  reuse/still/card → flag to the owner. Two-shots may take the most *keyframe* candidates (highest
  drift risk). **NEVER auto-batch-and-ship.**
- **⚖️ RULE 11 — WAVED RENDERS (owner law 2026-07-05):** never render a whole episode in one batch.
  A **VALIDATION WAVE** first (~3 clips spanning the risk classes: highest-drift two-shot · solo action
  hero · environment/butterfly) → ✋ owner reviews all three → then ~6–8 clips per wave, each wave ending
  in the Render QC gate + ✋ owner hand-picks (recorded in GATES.md) before the next wave runs. Same law
  for animation passes: animate a small section, verify lip-sync / consistency / transitions / story
  flow, then continue. Worst-case loss = one wave, never the episode.
- **✋ RENDER QC GATE (per clip, before it may enter the EDL):**
  - Identity vs master (Rule 3/7) — same Bentley, same style tier.
  - **Sharpness:** edge-var at 3 timestamps through the full pipeline (source→720p→1080p); reject < ~100
    or any mid-clip dip (soft push-ins).
  - **Stability:** mean frame-diff; unintended shake → re-render locked, do NOT deshake.
  - **Tail check:** Kling holds its last frame — find the last *moving* frame and trim the clip there.
    Mechanical: `python -m bentley.fix.tail_trim scan <clips>` (exit-code gate) / `trim` (cuts at the
    last moving frame, fresh filename; refuses fully-static clips — those are §5 defects, not tails).
  - **Motion truth:** the action matches the beat ("smelling" = actively sniffing, not lying still).
  - **Full-duration, worst-frame-fails:** QC ≥1 frame/sec across the WHOLE clip and judge by the worst
    frame, not frame 0 — EP2's human-smile drift appeared mid-clip while frame 0 was clean.

### 3.4 Assemble → Mix → Deliver
- Assemble data-driven from the EDL (`build_sections.py` → `assemble_v2.py` pattern). One final encode
  in the mix; no generational re-encodes.
- Re-run the **freeze-push math against the real clip durations** after any clip swap
  (`python -m bentley.qa.edl_lint <shotlist>` — planned durations lint clean does NOT mean real
  clips do).
- Mix: mood-mapped music beds, sidechain-ducked under VO; ambience low; **no opening fade-from-black**
  (owner rule); one long warm fade-out at the very end only.
- Deliver: **fresh filename every time**, verify frames extracted from the FINAL file, always give the
  absolute path.

---

## PART 4 — SCENE COMPOSITION GUIDELINES

- **The two-shot is the backbone.** Both characters in frame, in the environment, *doing* something.
  Solo talking-head ratio ≤ ~35%; two-shots ≥ ~25% (Shot-Flow Law) — **measured, not eyeballed:**
  every EDL piece carries a `scale` tag; `python -m bentley.qa.shot_ratios <shotlist>` does the
  arithmetic at animatic time.
- **Shot-scale variety is mandatory:** wide (establish/geography) → medium two-shot (dialogue/action) →
  insert (paws, crumb, trail, tag) → CU (reserved: the emotional turn, the catchphrase, one per act).
- **Every shot has real motion** — character action + environmental life (grass, sand, insects, light).
  A static frame with a zoom reads as a bug; **never pan/shake a static image.**
- **No scene under ~3s** (a sanctioned sync intercut ~1.3s+ INSIDE a continuous scene — e.g. the
  catchphrase CU — is a cut-in, not a scene: exempt); longer continuous scenes are never
  stitched/looped sub-ranges.
- **Show cause before reaction** — the thing happens on screen, THEN the character reacts.
- **Screen geography:** keep characters on consistent sides across a scene; eyelines match (Bentley looks
  down-left at Marco → Marco looks up-right at Bentley).
- **Environmental storytelling:** the world carries exposition (the shimmering trail, the burrow, the
  crumb) so the camera doesn't have to sit on faces while facts are narrated.

---

## PART 5 — CHARACTER CONSISTENCY RULES

- **Masters are frozen.** Edits happen FROM masters, never TO them. To change an approved shot,
  nano-banana-EDIT the approved frame (minimal change) — never regenerate from scratch (style drifts).
- **One Talking prop per character** (Rule 2): every talking CU drives from
  `assets/character_design/Bentley_TALKING_MASTER.png` (see §3.1 for its lock status and the legacy
  keyframe it supersedes) — never a per-shot face keyframe.
- **Canon (hard):** red-fawn Boxer pup, black face mask, grey chin, floppy folded ears, white chest
  blaze, **short docked tail stub**, paws same color as coat (no white socks, never a named color),
  teal collar + gold paw-print Listening Tag. Cartoony-Pixar tier — not photoreal, not flat-cartoon.
- **Dog, not human:** never a human smile / human teeth; joy = tongue out, soft eyes, tail-stub wiggle.
- **Two-characters-in-frame is the highest drift risk** → these shots get the most *keyframe*
  candidates and the hardest hand-pick (renders stay capped per §3.3).
- **Per-shot drift check is mandatory** (Rule 3): master beside every candidate at QC. If a shot drifts,
  re-render from the clean keyframe + locked elements — conform/fix-up re-renders drift WORSE.

## PART 6 — LIP-SYNC RULES  *(the method table is CLOSED — do not re-explore)*

**THE SYNC-OR-HIDE LAW:** every readable talking mouth in the cut must trace to a sync tool, OR the
line is staged so the mouth isn't readable (behind, above, silhouette, distance, object). A raw talking
face under a VO line is a **ship-blocker**. The **EDL trace is the gate** — for every dialogue line,
name the tool or the hide. (The audio-correlation auto-detector is proven unreliable; don't trust it.)

| Situation | Method |
|---|---|
| Bentley signature line (catchphrase, hero CU) | **Kling-Avatar** on the locked Talking prop — tight, bright, front-facing. 1–2 per episode, brief (~1.3s+) intercuts inside scenes, never a whole beat. **Avatar gotchas (EP1-proven):** it FREEZES the background (never use where live water/wind/motion must play behind the face — split the beat: i2v motion shot + the CU), it DARKENS the image (lift in the grade), and it hallucinates on-screen TEXT for short exclamations (those are VO-over, not Avatar) |
| Guest speaks in a two-shot, guest is small / no dominant face | **OmniHuman-1.5 mask** (white ellipse over the speaker); listener stays still. FAILS with a dominant face in frame — check first |
| Any line in a continuous scene | **VO-over-alive with the mouth managed**: speaker's *body* acts the line; every non-speaker prompted "mouth closed"; readable mouths staged away from camera |
| Listener in any two-shot | STILL mouth, natural body reactions only (Rule 9) |

**Dead ends — banned:** 2.5D mouth patches (owner rejected 3×, anatomically wrong on free poses) ·
per-frame AI restyle (flickers) · human-lip re-sync tools (sync.so, latentsync) · Kling-Avatar on
wide/side/small faces · chopping scenes into CUs to get sync. New method proposals require an
owner-approved research gate BEFORE any build.

**QA:** wrong-speaker motion heatmap sweep (`python -m bentley.qa.mouthmotion` — productionized from
the ep3 pattern) on every multi-character beat + the per-line EDL trace. Judge any synced element
against ANATOMY (is the mouth where the mouth IS in this pose?), not overlay placement.

## PART 7 — TRANSITION RULES

- Default = **hard cut** on action. **Match-cut** on continuing motion/shape. **Crossfade ≤0.4s**
  (owner law, §0.0 rule 6) only for a real time/place jump or emotional settle (~3–5 per episode).
- **No dip-to-black mid-film, ever.** No opening fade-from-black. One warm fade-out at the very end.
- Cut INTO movement, not out of a settle; never cut two near-identical framings together (reads as a jump).
- Transitions are an *edit* operation — never a render.
- If a transition is noticeable, it has failed (Rule 6) — fix the shots on either side, don't decorate it.

---

## PART 8 — QA CHECKLIST  *(run against the FINAL exported file; ALL must pass before the owner sees it)*

**Never present an un-QA'd cut. The owner is not the QA department.**
*(SKILL §9 is the CANONICAL release checklist; this Part 8 is its procedure manual — scan thresholds
and how-to. If they ever diverge, §9 wins and the divergence is a chain defect to fix the same day.)*

### 8.1 Automated scans (scripted, objective)
> **ONE command since 2026-07-05:** `python -m bentley.qa.scan_suite <final.mp4>` runs the
> freeze / black-frame / sharpness / jitter / stream scans below with pass-fail exit codes and
> timestamps (leading black = FAIL per the no-opening-fade rule; trailing black = the one closing
> fade, OK). Stop rewriting per-episode scratch scan scripts.
- [ ] **Freeze scan** — 24fps frame-diff over the FULL runtime; any <0.35-diff run ≥0.2s = investigate/fix.
- [ ] **Black-frame scan** — no interior black (only the closing fade).
- [ ] **Sharpness sweep** — edge-var per scene; flag any scene ≪ its neighbors (soft render / over-stretch).
- [ ] **Jitter check** on new renders — mean frame-diff; no shaky camera shipped.
- [ ] **Wrong-speaker heatmap** on every multi-character dialogue beat — does the NON-speaker's mouth glow?
- [ ] **Freeze-push math** re-verified against final clip durations (`push=0.00` everywhere) —
  `python -m bentley.qa.edl_lint <shotlist>` exits 0.
- [ ] Streams: 1080p, audio present, expected duration.

### 8.2 The Eleven-Rule Gate (owner law — §0.0; any fail = not releasable)
- [ ] Action carries every beat · [ ] Talking prop only · [ ] No drift vs master · [ ] No CU parade ·
  [ ] One scene per beat · [ ] Invisible transitions · [ ] Same Bentley throughout · [ ] Story was
  locked pre-render · [ ] Speaker-only mouths · [ ] Feels animated, not stitched · [ ] Produced in
  incremental gated waves (Rule 11 — validation wave + ✋ owner checkpoint per group in GATES.md).

### 8.3 Manual per-beat pass (contact sheets + watch-through)
- [ ] Every VO line over the correct, ALIVE speaker (per-beat VO-vs-picture check — the EP3 wrong-shot
  defects were caught only this way).
- [ ] Sync-or-Hide EDL trace complete for every dialogue line.
- [ ] Canon frame-check: docked tail, coat-colored paws, tag, mask, no human teeth, guest on-model.
- [ ] No reused frames/loops; callbacks are distinct sub-ranges.
- [ ] Causality holds; bonding beat present; catchphrase = Bentley; next-time hook matches the locked
  next episode; kid-tone (no dark lines).
- [ ] Grade consistent; music moods match story beats; no VO clipped or overlapped.

### 8.4 Delivery
- [ ] Fresh filename · [ ] Frames verified FROM the delivered file · [ ] Absolute path in the handoff ·
  [ ] Credits spent logged · [ ] `episodes/ep<N>/GATES.md` complete — every ✋ gate has a recorded pass
  (an unrecorded gate is an unpassed gate).

---

## PART 9 — COMMON MISTAKES TO AVOID  *(the EP3 hall of shame — memorize)*

1. Building the cut per-VO-line ("editor brain"). → Sections first, always.
2. Chasing sync with talking-head CU inserts. → Sync-or-Hide instead.
3. Fresh talking faces per shot. → The locked Talking prop.
4. Prompting a paw color. → "Same color as her coat, no white socks."
5. Generating an environment from a character master. → Edit a real episode frame.
6. Post-fixing a bad render (deshake/stretch/upscale). → Re-render locked-camera from the clean keyframe.
7. Stretching a clip past 1.3× or past its length. → Plan enough clips; freeze-push math.
8. Shipping a Kling clip without trimming its frozen tail.
9. Auto-batching renders and shipping unseen. → Hand-pick, always.
10. Trusting "it looks synced" / "it looks stable." → Measure it (heatmap, edge-var, frame-diff).
11. Re-exploring solved problems (lip-sync methods, thumbnail style, voice settings). → The table is closed.
12. Re-rendering a shot but not re-pointing the EDL. → Verify a frame from the FINAL file.
13. Spending on renders before the keyframe passed QC. → Cheap gate before expensive step, every time.
14. Presenting a cut the team hasn't QA'd end-to-end. → §8, no exceptions.

---

## PART 10 — HARD PRODUCTION CONSTRAINTS  *(physics of the pipeline — plan around, never fight)*

- **C1. Kling 3.0 max ~5s continuous** → sections longer than 5s of VO need 2–4 planned clips of the
  SAME evolving scene.
- **C2. Retime ceiling 1.3×** (assembler caps at 1.5 but ≥1.4 reads as slow-mo blur) → freeze-push math
  at EDL time.
- **C3. Kling can't hear** → mouths flap to nothing on VO-over; manage every mouth (Part 6).
- **C4. Generative identity drifts by default** → locked masters + elements + hand-pick are the only
  countermeasures; two-shots drift most.
- **C5. Prompt ≤300 chars · elements need 2–4 images · `multi_shots: False` · 50430 = backoff ·
  402 = STOP and tell the owner.**
- **C6. Pipeline resolution is 720p → 1080p upscale** → sharpness must be verified THROUGH the pipeline,
  not on the source.
- **C7. Kling holds its final frame** → tail-trim every clip.
- **C8. Credits are finite** → budget ~12–18 hero renders/episode + ~10–15% reroll reserve; candidates
  live at the keyframe layer, ONE render + ≤2 rerolls per shot (§3.3); the pre-flight estimate
  (`BRIDGE × 70cr × 1.15`) is approved at the Animatic gate; QC gates before every spend; log
  per-episode totals. New-world episodes (thin reuse library) have a structurally higher BRIDGE count —
  estimate honestly, never assume EP2-level reuse.
- **C9. Locked voices only** (Bentley=LauraZ, Narrator=Bill, guests locked at design time);
  catchphrase is ALWAYS Bentley's.
- **C10. Owner gates are sequential and real:** premise ✋ → animatic ✋ → keyframe QC ✋ → hand-picks ✋ →
  final QA → release review vs the 10 Rules. Nothing skips a gate, and **every gate pass is RECORDED
  in `episodes/ep<N>/GATES.md`** (gate, date, what exactly was approved) — sessions change, chat
  memory doesn't survive; the ledger is the only proof a gate passed.

---

## PART 11 — COST & TOKEN DISCIPLINE

- **The 80/20 law:** exploration/scouting on cheap or free tools (reuse, stills, animatic, nano-banana
  keyframes); Kling 3.0 renders ONCE from a validated keyframe (plus the capped ≤2 reroll reserve,
  §3.3 — "candidates" NEVER means multiple renders), per the cost gate.
- **No large batches (Rule 11, 2026-07-05):** all generation/animation spend goes out in small gated
  waves with an ✋ owner checkpoint between waves (§3.2/§3.3). Batching has no price discount — it only
  multiplies a systematic error by the batch size. Worst-case loss = one wave, never the episode.
- **Fix at the cheapest layer that owns the defect — now OWNER LAW as the FIX-FIRST ladder (SKILL
  §1b, 2026-07-05; inventory + roadmap in `docs/guides/FIX_FIRST_TOOLKIT_PLAN.md`):**
  tier 1 edit layer (free: `edl_lint` math, `tail_trim`, `shot_match` conform/Avatar-lift,
  assembler/mix/grade) → tier 2 local pixel (free, preview-first: `magic_wand` paws, `recolor`
  any canon color, `tail_dock` still-tail inpaint, `plate_match` background conform, `prop_paste`
  locked-prop composite) → tier 3 surgical AI edit (~2–4cr: `kontext_edit` FLUX Kontext minimal
  change / nano-banana-edit paw pass) → tier 4 re-render (70cr, LAST resort, reroll cap
  unchanged). Detection: `bentley/qa/scan_suite.py` (Part 8.1 in one command). Regen-only classes
  skip straight to tier 4: jitter, identity drift, video anatomy/teeth, mouth compositing (closed
  table), keyframe softness. Every fix re-passes the QC gate it failed; first use on a NEW defect
  class = eyes-on zoomed vs the master (wand_lab law); NEVER re-render to fix an edit problem.
- **Batch your fixes:** collect a full defect list, fix in one rebuild cycle, one QA pass — not one
  rebuild per note.
- **Token discipline:** don't re-research settled decisions (they're in the skills/memory/vault); don't
  rebuild dead ends (Part 6 banned list); reuse the proven scripts instead of writing new ones per
  episode. **Canonical paths** — productionized (episode-agnostic): `bentley/qa/mouthmotion.py`,
  `bentley/qa/qa_vo.py`, `bentley/qa/shot_ratios.py`, `bentley/qa/edl_lint.py`,
  `bentley/qa/scan_suite.py`, `bentley/qa/image_bestof.py` (drift lever #4 — measured keyframe pick),
  `bentley/voices/best_of.py`, `bentley/qa/verify_sync.py`, `bentley/episode_builder/animatic.py`,
  `bentley/shared/kling.py` (drift lever #3 — first+last frame i2v payload), and the fix package:
  `bentley/fix/{magic_wand,recolor,tail_dock,tail_trim,shot_match,plate_match,prop_paste,kontext_edit,color_transfer}.py`. Per-episode patterns to copy
  and adapt: `episodes/ep3/build_sections.py`, `episodes/ep3/assemble_v2.py`, `episodes/ep3/mix_ep3.py`.
  ⚠️ The `assemble_v2.py` in `deprecated/episode1_scripts/` is STALE — never grab it by filename search.

---

## PART 12 — CONTINUOUS IMPROVEMENT

After every episode: a short post-mortem against this playbook — what worked, what failed, which rule
was missing. **Update the playbook + skills the same day.** A lesson that isn't codified will be
re-learned at full price on the next episode (EP3 proved it).

**Cross-skill alignment check (part of every post-mortem):** re-read `cinematic-episode-writer` (+ its
three references) and `lipsync-pro` against this chain — any statement that contradicts a chain rule is
a defect to fix that day. (Found 2026-07-03: "one clip per beat" and "not AI lip-sync" in
`shot-and-pipeline.md`, and a stale "no working sync method" in production §0.3 — all reconciled.)
