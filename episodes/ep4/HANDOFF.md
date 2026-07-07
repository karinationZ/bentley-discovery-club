# EP4 — "The Butterfly Highway" · PRODUCTION HANDOFF

> **For the next agent picking up EP4.** This is a *map*, not a substitute for the rules. It tells you
> exactly what's done, what's left, what will bite you, and how to finish without burning credits.
> Written 2026-07-06. Source of truth for gates is always **[`episodes/ep4/GATES.md`](GATES.md)** — if
> this doc and the ledger ever disagree, **the ledger wins.**

---

## 0. START HERE — do these first, in order (non-negotiable)

1. **Load the `episode-production` skill BEFORE touching anything** under `episodes/` or `assets/` — even
   a "trivial" JSON edit is production work (project `CLAUDE.md`). Also load: **`cinematic-episode-writer`**
   (only if story/VO changes — but the story is FROZEN, see §1), **`lipsync-pro`** (any talking shot —
   EP4 has one: s6 catchphrase), **`companion-short`** (the companion Short, deferred).
2. **Read [`GATES.md`](GATES.md) end-to-end.** An **unrecorded gate is an UNPASSED gate.** Never mark a
   gate from memory. Record every ✋ owner approval there with date + evidence, in the same session it happens.
3. **Environment quirk (will waste your first render):** `bentley.shared.kie_client` reads `KIE_KEY` from
   the raw env and **nothing auto-loads `.env`**; background shells don't inherit it, and `python` isn't on
   PATH. Always run KIE work as:
   ```bash
   set -a && . ./.env && set +a && PYTHONPATH=. python3 <script>
   ```
4. **This episode is a NEW-WORLD episode** (new guest Mira, new meadow/eucalyptus plates, ~zero reuse
   library). The "reuse covers most non-hero beats" assumption from EP2 does **not** hold — expect a higher
   hero-render count and lean hard on Ken-Burns stills / cards for the non-hero remainder.

---

## 1. What this episode is

- **ep4 · "The Butterfly Highway"** · guest **Mira the Monarch** (scripted as the *silent girl* monarch —
  the **narrator carries her hooks**; her `M_*` VO lines are coach/song beats, confirm against the shotlist
  at assembly). Bentley = fun-loving Boxer, she/her, LauraZ voice.
- **Runtime ≈ 4:58** (298 s), **21 beats**, 47 sub-shots.
- **STORY + CUT ARE FROZEN.** Animatic Lock **REV6 approved by owner 2026-07-04** (`_meta.animatic_lock`).
  **No script or VO changes** — do not rewrite, re-time the story, or re-record lines. Only produce.

---

## 2. Gate snapshot (see [`GATES.md`](GATES.md) for the full evidence lines)

| # | Gate | Status |
|---|------|--------|
| 0 | Talking-prop lock (`Bentley_TALKING_MASTER.png`) | ⬜ pending (only needed for s6 avatar CU) |
| 1 | Premise lock | ✅ locked |
| 2 | VO QC | ✅ **PASSED** (all lines recorded + cleared) |
| 3 | **Animatic Lock** (story+cut) | ✅ **PASSED** → *renders are unlocked with `BENTLEY_EPISODE=ep4`* |
| 3b | Credit estimate | ✅ PASSED (plan v3, EP3 method, no Turbo) |
| 4 | **Keyframe QC** | ✅ **PASSED** (17 locked; 3 legacy frames flagged for redo — see §5) |
| 5 | **Render hand-picks** | 🟡 **IN PROGRESS** — this is where you are |
| 6 | Final QA | ⬜ pending |
| 7 | Release review vs the 11 Rules | ⬜ pending |

**Credit position:** balance ≈ **10,000 cr**. EP4 render spend so far ≈ **1,174 cr**. Remaining hero
renders (≈13 shots, see §4) ≈ **1,050–1,400 cr** at 70cr × 1.15 reroll reserve — comfortable headroom.
**On a 402 (credits out): STOP and tell the owner.** Never hunt for a workaround.

---

## 3. What's DONE ✅

- **VO — complete & QC-passed (gate 2).** All `B_*` / `M_*` / `N_*` lines live in **`scratch/ep4/vo/`** as
  cleaned masters (built by `scratch/ep4/make_vo.py`, best-of by `record_best_of.py`; voices LOCKED:
  Bentley=LauraZ, Mira=eleven.MIRA, Narrator=Bill). No manifest file — the reel is defined in code.
- **Keyframes — 17 locked (gate 4), in `assets/pilot_shots/ep4/keyframes_prod/`.** Every one owner-picked
  side-by-side vs the master. ⚠️ **3 caveats** in §5.
- **Renders APPROVED (wave 0):**
  - `s1b` → `scratch/ep4/renders_w0/s1b_nose_taste.mp4`
  - `s7a` → `scratch/ep4/renders_w0/s7a_reframe_q_r1.mp4` (the `_r1` reroll is the pick)
  - `s8` → `scratch/ep4/renders_w0/s8_run.mp4` (restaged glide→slow-mo RUN; camera pinned)
- **Renders clean / not-yet-rejected (need final ✋ sign-off at assembly):**
  - `s4b` → `renders_w1/s4b_copy_sneeze.mp4` (owner "close to Bentley"; a flagged "style drift" was ruled false)
  - `s5a` → `renders_w1/s5a_lead_bound.mp4` (calm bound passed QC) — **but** owes a surgical mask fix (§4).
- **s7b — ✅ OWNER-APPROVED deliverable = `scratch/ep4/renders_w1/s7b_run.mp4`** ("amazing, I like it!", slow-mo
  run). The fix that worked: stage the beat's FEELING as a natural ACTION matched to its VO (B_mindblown = dog JOY
  → a RUN), not a reaction pose Kling melts. **⛔ PROCESS ERROR to NOT repeat:** the producer ran adversarial QC
  AFTER this approval, treated zoom-level tail/gait flags as blockers, and autonomously rerolled + ¾-front-restaged
  — wasting ~3 renders overriding an approval already given. **Once the owner approves a shot at normal speed, it
  is LOCKED; QC is a PRE-approval gate only and must never trigger an autonomous reroll of an approved clip.** An
  alternative `s7b_run2_clean.mp4` (3.46s ¾-front run, tail occluded by staging) sits on disk if the owner ever
  wants it, but was NOT requested. (Useful lesson from the detour, for FUTURE un-approved run shots only: frame
  ¾-front so the body occludes the docked-tail, since a side-profile run drifts a long tail.) Remaining polish on
  the approved clip: the standard 720p→1080p sharpen pass at assembly.

---

## 4. What's NEXT — remaining work, in priority order

**All hero renders go one small wave at a time, each ending in QC + ✋ owner sign-off recorded in GATES.md
before the next wave spends anything (Rule 11).** Do NOT batch-render the remainder.

### A. Finish the blocked / pending renders (the drift-prone dynamic beats — highest risk)
These four are the current high-risk block. Do **not** just reroll them. The old "Ken-Burns fallback" is now
closed for animation because the owner rejected `s7b_kenburns.mp4` as static zoom-only. For each beat, first
decide staging honestly: only attempt Kling if it can be restaged with **real motion** that the model can hold
(wide / small-in-frame body action, or genuinely subtle living motion). Close/medium expressive reactions are
known-fail in Kling, but a static still push is also not acceptable. If no real-motion staging exists, flag for
owner direction rather than filling the cut with a static substitute.
- `s7b_mindblown` — **REOPENED / no approved deliverable.** Original spin/jump failed; contained close restage failed;
  Ken-Burns fallback rejected as static. Out of rerolls for the same design; needs a new owner-approved real-motion
  restage/coverage choice before any further wave progress.
- `s3a_meet_comeon` — dynamic bounce; base + r1 both failed (blurry, morph, back-to-camera end).
- `s3b_plan_gag` — human-teeth grin (~4.3s) in base; r1 drifted from master.
- `s5b_flower_flop` — human teeth + bug-eyes from ~3.5s; r1 still bug-eyed.
- `s5a` mask fix — the render is otherwise clean; it has a **white-muzzle-stripe** on the keyframe. Fix it
  **surgically** (`bentley.fix.kontext_edit` tier-3, or `magic_wand`/`recolor` if it's a pure color patch —
  try the 0-cr local tools FIRST per the fix-first law) → re-render pinned.

### B. Render the not-yet-rendered heroes (keyframes already locked)
`s6_turn_river` (⚠️ this is the **only talking shot** — `kling/ai-avatar-standard` catchphrase CU on the
locked Talking prop; **load `lipsync-pro`**, and lock gate 0 first), `s9b_grove_cluster`, `s10a_worm`,
`s10b_fancyworm`, `s11a_dusk_reflect`, `s11c_mantra_sleep` (whisper CU, mouth barely moving, VO-over).

### C. Regenerate the 3 legacy-glossy keyframes, THEN render them
`s1a_sky_ignites`, `s4a_taste_flower`, `s11c_mantra_sleep` were made in the **legacy glossy-Pixar** style
(pre-master-anchor). Regenerate them **master-anchored** (`nano-banana-pro`, master-first refs, the exact
gate-4 recipe) → owner keyframe sign-off → render. Otherwise they'll clash with the locked set.
*(Note: `s11c` appears in both this list and §4B — regenerate the keyframe first, then render.)*

### D. Free pieces — $0, no generation (do these via `bentley.episode_builder`)
All `kenburns` sub-shots + the cards: `s2_title`, `s9a_grove_wide`, `s11b_grove_sings`, `s11d_nexttime`, and
every Ken-Burns sub-shot inside the hero beats. Use stills + `placeholders.ken_burns` / `labeled_card`. Zero credit.

### E. Assemble → mix → grade → QA → deliver
There is **no EP4-specific assemble script yet** — use the `bentley.episode_builder` package (the EP1
`assemble.py`/`mix.py`/`grade.py` are hardcoded to EP1; generalize or write an EP4 driver). Then the QA
gate (§9 of the skill): `scan_suite`, `shot_ratios`, `mouthmotion`, `edl_lint`, plus the manual per-beat
VO-vs-picture pass. **QA the FINAL file, not the parts.**

### F. Deferred (not EP4 render work)
Companion Short (`companion-short` skill — pure real-documentary, Pexels footage, ~$0), and the EP3 publish kit.

---

## 5. WATCH-OUTS — the things that have burned credits / been rejected (READ THIS)

1. **Kling drifts Bentley on ANY head/body motion** — grows a long tail, whitens the mask, adds **human teeth**,
   googly/bug eyes, and **melts the face mid-clip** (muzzle → dark blob). This is **the #1 token sink** (the EP3
   402 and every s7b failure). **⚖️ SHARPENED by the s7b restage 2026-07-06:** even a *"contained reaction"* on a
   **close/medium** framing is TOO MUCH motion — the last-frame pin holds the START+END but the MIDDLE still
   collapsed (facial melt at the head-down beat + bug-eyes at the wonder peak). **OWNER UPDATE:** the static
   `s7b_kenburns.mp4` fallback also failed because it is only a zoom on a still. **So:** the only acceptable
   dynamic Bentley path is **real motion** that stays on-model: WIDE / small-in-frame body action, a genuinely
   subtle living idle, or another owner-approved animated coverage choice. **Do not use static Ken-Burns as a
   hero-animation deliverable.** Motion-risk triage still applies, but "contained reaction close-up" and
   "still push-in fallback" are both known-fail staging for s7b.
2. **NEVER derive a 2nd/END keyframe from the master** — that's a fresh identity synthesis and it *will*
   drift (this is why every early s7b END lost the Boxer face). **Derive the END from the APPROVED first
   frame** (put it FIRST in the refs, change ONE thing, small delta). *Lever 1a — the fix that finally worked.*
3. **FLUX Kontext (`kontext_edit`) = surgical repair ONLY** (recolor, one eye, dock a still tail). **Never
   use it to re-pose or change an expression** — it warps the muzzle. *Lever 1b.*
4. **NEVER change the model.** Locked toolchain (§6 table). No swaps, no downgrades, no "let me smoke-test a
   new model," ever, without an explicit owner order. (Owner: *"NEVER NEVER change the model! never!"*)
5. **Style anchor = the LITERAL master images** (`Bentley_MASTER_pixar.png` / `Bentley_TALKING_MASTER.png` —
   the cartoony-Pixar render EP1–3 shipped in). **It is NOT "painterly."** The painterly detour was a
   producer error, **VOID**, and cost **720 cr**. Never re-choose a style per episode; anchor every keyframe
   to the master *image itself*.
6. **NEVER large batches (Rule 11).** Batching has no price discount — it only multiplies a systematic error
   by its size. Validation wave (1–3 spanning risk classes) → ✋ owner → then ~4–8 per wave with a QC gate.
7. **Reroll cap ≤2, then RESTAGE, then downgrade, then flag.** Drift surviving 2 rerolls is a *design*
   problem, not a dice problem. **Never reroll #3.** Candidates live at the ~18cr KEYFRAME layer, not the
   70cr render layer.
8. **s7b specifically is OUT of rerolls on the failed design.** The authorized restage render drifted, and the
   Ken-Burns fallback was rejected as static animation. Do not reroll #3; restart only with a new owner-approved
   real-motion restage/coverage decision.
9. **Adversarial QC is mandatory and it works.** Independent skeptic agents (one per failure class: teeth /
   eyes / tail / mask / paws / identity) catch what a single reviewer's eye misses — it caught the wave-1
   human teeth that were shipped past me. Zero credits (read-only). Run it on every rendered clip's frames.
10. **Paws:** NEVER prompt a paw *color* — "red-fawn paws" is what produced RED paws. Say **"paws the same
    color as her coat, no white socks."** White-paw drift is fixed 0-cr locally by `bentley.fix.magic_wand`.
11. **The 3D RIG PATH IS DEAD** (owner killed it 2026-07-06 — too slow, 3D living backgrounds impossible, no
    artist). **Never propose a rig / meshing / LoRA-off-KIE.** We stay on KIE + the drift-reduction stack.
12. **Don't reach for the Ken-Burns downgrade by default** (owner: *"it will get you into a vicious circle"*)
    — it's the *last* rung of the ladder, after restage.
13. **Two mechanical guards protect spend — do NOT route around either.** `gates.py` refuses video renders
    without `BENTLEY_EPISODE=ep4` + a PASSED Animatic Lock; `drift_guard.py` refuses a character render
    that isn't **last-frame-pinned**. A `PermissionError` from them = a missing gate, not a bug.
14. **Bentley is a dog, not a human.** No human smile / human teeth. Joy = **tongue out, soft eyes, tail
    wiggle.** Docked tail = **short stub, no white tip.** She/her. Catchphrase **"Stop. Look. Listen."** is
    **always Bentley's voice**, never the narrator.
15. **Always include the absolute file path** when you deliver any generated asset (the owner works from the
    filesystem).

---

## 6. Must-follow rules (the binding chain)

> **Before touching EP4, LOAD the `episode-production` skill.** This is a pointer map, NOT a substitute. The
> normative chain is: **11 Mandatory Rules (owner law, §0.0) → `SKILL.md` (enforcement) →
> `references/PRODUCTION_PLAYBOOK.md` (procedure & history).** Load `lipsync-pro` for the s6 talking shot.

### (a) The 11 Mandatory Production Rules — `SKILL.md §0.0` (all ship-blocking)
1. **Action over dialogue** — meaningful action + environmental life under every VO line; never a talking head carrying a beat.
2. **Approved master talking prop ONLY** — drive Bentley speech from the one locked Talking master; no per-shot talking keyframes.
3. **Never drift from approved style** — compare every shot to the master before the cut.
4. **Avoid extreme close-ups** — medium/wide default; tight CU only for a real emotional beat.
5. **One cohesive scene per story beat** — one continuous sequence per beat; no sentence-by-sentence stitching.
6. **Invisible transitions** — hard cut / match-cut / ≤0.4s crossfade only; never dip to black mid-film.
7. **Absolute character consistency** — same Bentley every frame (Rule 3 is the check).
8. **Story before animation** — done here (Animatic Lock passed).
9. **Multi-character lip-sync QA** — only the speaker's mouth moves; wrong mouth = ship-blocker.
10. **Think like an animator, not an editor** — build the best animated SCENE, not "which clip next."
11. **Incremental production — NEVER large batches** — small gated waves, ✋ owner approval per group.

### (b) Hard credit / spend guardrails — `SKILL.md §1, §1b`
- **Kling 3.0 cost gate:** Kling ONLY when a character emotes/interacts or a hero/signature/complex-action
  moment. Everything else → reuse / Ken-Burns still / card. Never scout on premium; never "fix bad prompting"
  on Kling — rewrite and test cheap first. Banned: Kling 2.6. AVOID for characters: Seedance (drifts). Turbo
  is a *premium speed* tier on KIE (~90cr) — **rejected for this series** (cost + stiff butterflies).
- **Rule-11 waves** (above) · **Reroll ladder** (≤2 → restage → downgrade → flag) · **Fix-first law** (walk
  the ladder from the top: 0cr edit → 0cr local pixel → ~2–4cr surgical AI → 70cr re-render LAST) · **Two
  mechanical gates** (watch-out #13) · **Pre-flight estimate** = `renders × 70 × 1.15`, approved with the animatic.

### (c) Drift-reduction stack — `SKILL.md §3a` (stack ALL, cheapest-first — no single lever is enough)
Edit-from-master (1) · **derive-END-from-approved-frame (1a)** · **Kontext = surgical-only (1b)** · measured
best-of (2, `image_bestof`) · i2v + `@Bentley` element (3) · **pin last frame (4, mechanically enforced)** ·
chain from prev QC'd frame re-anchored to master (5) · stage around weak spots (6) · free color patch (7) ·
reuse (8) · **motion-risk triage** (restage high-motion before first render). Honest ceiling ~85–95% on-model.

### (d) Ranked token sinks to avoid
1. Render rerolls on high-motion shots → motion-triage + ≤2 cap. 2. Keyframe re-gen churn from batch errors →
Rule-11 waves + calibrate one shot vs master before any batch. 3. QC round-trips → cheap gate before every
expensive step; route a defect to the right tool (size ≠ color). **One-line default:** *edit from the approved
frame, never generate blind; measure-rank every candidate; render calm-and-pinned only; restage any big-motion
beat BEFORE it costs a render; reroll ≤2 then restage.*

### (e) CLOSED lip-sync method table — do NOT re-explore (`SKILL.md §0`, `lipsync-pro`)
**WORKS:** A. Kling-Avatar CU (`kling/ai-avatar-standard`) on the locked Talking prop — tight/bright/front CU,
hero line only (EP4: s6 catchphrase). B. OmniHuman-1.5 mask — guest in-frame sync (Marco/Mira-class), **banned
on Bentley**. C. (future) Blender rig. D. **VO-over-alive** — the production default; speaker's BODY acts the
line, non-speakers "mouth closed," readable mouths staged away. Judge sync by ANATOMY, not overlay placement.
**DEAD ENDS (never rebuild):** 2.5D mouth-patch overlay (rejected 3×), human-lip re-sync tools (sync-2,
latentsync), per-frame AI restyle, Avatar on wide/side/small framings, chopping scenes into talking-head CUs.

### (f) LOCKED toolchain models — **NEVER change the model**
| Purpose | Model slug |
|---|---|
| Keyframes | **`nano-banana-pro`** (`nano-banana-edit` for edits; never base `google/nano-banana`) |
| Motion / hero video | **`kling-3.0/video`** (i2v + `kling_elements`, `multi_shots: False`) |
| Talking CU | **`kling/ai-avatar-standard`** |
| Guest in-frame sync | **`omnihuman-1-5`** (guest only; never Bentley) |

---

## 7. The EDL / shot plan (from `episodes/ep4/shotlists/ep4_master.json`)

Two-level structure: **21 beats**, each split into continuous sub-shots (`seq`). The Kling cost gate applies
at the sub-shot level — a beat is a HERO render only where a sub-shot is `plan: "kling"`; every `kenburns` /
`card` sub-shot is FREE. `_meta.animatic_lock` = **APPROVED REV6 2026-07-04, story+cut FROZEN.**

| # | Beat id | type | HERO vs FREE (sub-shots) | dur (s) | VO labels | status |
|---|---------|------|--------------------------|---------|-----------|--------|
| 1 | s1a_sky_ignites | motion | **HERO** 1 kling + 2 kenburns | 15.28 | B_hook1, B_hook2 | todo |
| 2 | s2_title | card | FREE 1 card (reuses s1a still) | 3.5 | — | todo |
| 3 | s1b_nose_taste | motion | **HERO** 2 kling + 1 kenburns | 16.53 | B_hooknose, M_hello, B_iam | todo |
| 4 | s3a_meet_comeon | motion | **HERO** 1 kling + 1 kenburns | 13.74 | N_intro, M_comeon | todo |
| 5 | s3b_plan_gag | motion | **HERO** 1 kling + 2 kenburns | 18.64 | B_plan, M_nomap, B_nomap2 | todo |
| 6 | s4a_taste_flower | motion | **HERO** 1 kling + 1 kenburns | 12.13 | N_feet, M_trythis | todo |
| 7 | s4b_copy_sneeze | motion | **HERO** 1 kling + 2 kenburns | 20.43 | B_copyfeet, M_giggle1, B_questions | todo |
| 8 | s5a_lead_bound | motion | **HERO** 1 kling + 1 kenburns | 13.36 | B_lead, N_race | todo |
| 9 | s5b_flower_flop | motion | **HERO** 1 kling + 1 kenburns | 11.91 | M_floptease, B_flop | todo |
| 10 | s6_turn_river | **talk** | **HERO** 1 kling avatar + 3 kenburns | 19.52 | B_stoplook, N_turn, B_river · "Stop. Look. Listen." | todo |
| 11 | s7a_reframe_q | motion | **HERO** 1 kling + 1 kenburns | 13.92 | B_wheredoesit, M_dontknow, M_generations | todo |
| 12 | s7b_mindblown | motion | **HERO** 1 kling + 2 kenburns | 18.72 | B_mindblown, N_generations | todo |
| 13 | s8_glide | motion | **HERO** 2 kling (2nd = THUMBNAIL money shot) + 1 kenburns | 18.41 | M_ridewithme, M_glidecoach, B_glide, N_updraft | todo |
| 14 | s9a_grove_wide | ffx | FREE 1 kenburns | 8.08 | N_grove | todo |
| 15 | s9b_grove_cluster | motion | **HERO** 1 kling + 1 kenburns | 7.43 | B_grove, M_home | todo |
| 16 | s10a_worm | motion | **HERO** 1 kling + 1 kenburns | 15.04 | B_worm, M_caterpillar | todo |
| 17 | s10b_fancyworm | motion | **HERO** 1 kling + 2 kenburns | 18.88 | B_fancyworm, N_button | todo |
| 18 | s11a_dusk_reflect | motion | **HERO** 1 kling + 2 kenburns | 22.98 | N_dusk, M_goodnight, B_reflect | todo |
| 19 | s11b_grove_sings | motion | FREE 1 kenburns | 9.99 | M_grovesong, B_dreamy | todo |
| 20 | s11c_mantra_sleep | motion | **HERO** 1 kling (whisper CU, VO-over) + 2 kenburns | 16.08 | B_mantra, N_close | todo |
| 21 | s11d_nexttime | card | FREE 1 card (reuses s9a still) | 3.5 | — | todo |

**Tally:** 21 beats · 47 sub-shots = **21 kling (HERO)** + 24 kenburns + 2 card. **18 hero beats**
(s1b & s8 carry 2 kling sub-shots each). `_meta.counts.reuse = 0` (no prior-episode clip reuse; s2/s11d
reuse *stills* only). Timeline runtime = 298.08 s.

*Note: the animatic timeline flattens every beat to a Ken-Burns still proxy — the per-seq kling renders are
not yet reflected in the animatic. The animatic is the zero-credit story proxy; the master JSON drives final assemble.*

---

## 8. Render state (as built)

All clips are 5.04 s Kling outputs (24 fps). `renders_w0/` = wave 0, `renders_w1/` = wave 1. Owner pick noted.

| Shot | Clip (if any) | Status | Notes |
|------|---------------|--------|-------|
| s1b | `renders_w0/s1b_nose_taste.mp4` | ✅ **APPROVED** | wave 0; hard push-in noted |
| s7a | `renders_w0/s7a_reframe_q_r1.mp4` | ✅ **APPROVED** (reroll #1) | pick = `_r1` |
| s8 | `renders_w0/s8_run.mp4` | ✅ **APPROVED** | restaged glide→slow-mo RUN, camera pinned; `s8_glide.mp4` superseded |
| s5a | `renders_w1/s5a_lead_bound.mp4` | 🟡 clean, **owes mask fix** | white-muzzle-stripe surgical fix + re-render pending |
| s4b | `renders_w1/s4b_copy_sneeze.mp4` | 🟡 clean, not rejected | "close to Bentley"; VO-sync at assembly |
| s3a | `renders_w1/s3a_meet_comeon(_r1).mp4` | ❌ **REJECTED** (Kling drift) | blurry, morph, back-to-camera; dynamic bounce → restage |
| s3b | `renders_w1/s3b_plan_gag(_r1).mp4` | ❌ **REJECTED** (Kling drift) | human-teeth grin ~4.3s; r1 drifted → restage |
| s5b | `renders_w1/s5b_flower_flop(_r1).mp4` | ❌ **REJECTED** (Kling drift) | teeth + bug-eyes ~3.5s; dynamic flop → restage |
| s7b | ✅ `renders_w1/s7b_run.mp4` (slow-mo run) | ✅ **OWNER-APPROVED** ("amazing, I like it!") | LOCKED by owner. (A later autonomous reroll+¾-front restage over this approval was a PROCESS ERROR — see gate-5 note; `s7b_run2_clean.mp4` is an unrequested alt on disk.) Needs sharpen pass at assembly |
| s6, s9b, s10a, s10b, s11a, s11c | — | ⬜ **NOT YET RENDERED** | keyframes locked; render per §4B |
| s1a, s4a, s11c | — | ⬜ **NOT YET RENDERED** | keyframes are **legacy-glossy** → regen master-anchored first (§4C) |

`scratch/ep4/design/turbo_smoke_out.mp4` is the rejected Turbo smoke-test artifact, not a shot.

---

## 9. Keyframe state

**Style anchor (LOCKED):** the literal master images `assets/character_design/Bentley_MASTER_pixar.png` +
`Bentley_TALKING_MASTER.png`. Every keyframe is generated and QC'd side-by-side against these. **Not painterly.**

**17 LOCKED keyframes in `assets/pilot_shots/ep4/keyframes_prod/`** (owner-picked, gate 4 PASSED):
`s1a_sky_ignites`, `s1b_nose_taste`, `s3a_meet_comeon`, `s3b_plan_gag`, `s4a_taste_flower`, `s4b_copy_sneeze`,
`s5a_lead_bound`, `s5b_flower_flop`, `s6_turn_river`, `s7a_reframe_q`, `s7b_mindblown`, `s8_glide`,
`s9b_grove_cluster`, `s10a_worm`, `s10b_fancyworm`, `s11a_dusk_reflect`, `s11c_mantra_sleep`.

**⚠️ Keyframes needing work before their render:**
- **`s1a`, `s4a`, `s11c` — legacy glossy-Pixar** (pre-master-anchor). Regenerate master-anchored → owner sign-off.
- **`s7b_mindblown.png` in `keyframes_prod/` is the OLD rejected keyframe.** The later restage pair is in
  `scratch/ep4/kf_s7b_restage/` (`s7b_start_c1.png` + `s7b_endc1_c1.png`), but the render and static fallback
  both failed. Treat those frames as references only until a new real-motion s7b direction is approved.
- **`s5a`** keyframe has the white-muzzle stripe to fix surgically (§4A).

`assets/pilot_shots/ep4/keyframes/` holds the **animatic placeholders** (superset incl. dead `s11a_dusk_creak`,
`s11b_promise`) — not the production set. Use `keyframes_prod/`.

---

## 10. Assembly inputs, VO & tooling

### VO — `scratch/ep4/vo/` (gate 2 PASSED)
All lines exist as cleaned masters + `_raw` captures. Bentley `B_*` (21 lines), Mira `M_*` (14), Narrator
`N_*` (10). Auditions in `scratch/ep4/vo/audition/` (not final). Reel is code-defined (`make_vo.py` /
`record_best_of.py`), no manifest file.

### Pipeline tools (run from repo root, `PYTHONPATH=. python3 -m ...`)
**`bentley.episode_builder`** — `animatic` (zero-credit story cut from a shotlist), `assemble`/`mix`/`grade`
(final picture/sound/color — currently EP1-hardcoded, generalize for EP4), `placeholders` (Ken-Burns / cards
+ the ffmpeg-only guardrail), `shorts` (9:16 builder), `timeline` (one-voice-at-a-time scheduler).
**`bentley.qa`** — `edl_lint` (freeze-push math on a shotlist), `image_bestof` (rank keyframe candidates vs
master), `mouthmotion` (wrong-speaker detector), `qa_vo` (per-line VO table), `scan_suite` (freeze/black/
sharpness/jitter/stream scans on the FINAL file), `shot_ratios` (solo-CU ≤35% / two-shot ≥25%).
**`bentley.fix`** (fix-first ladder; all 0-cr local except `kontext_edit`) — `magic_wand` (white→coat paws),
`recolor` (any canon-color drift), `plate_match` (bg conform), `prop_paste` (missing prop), `tail_dock`
(over-long tail on a still), `tail_trim` (frozen clip tails), `shot_match` (color/luma conform of a clip),
`kontext_edit` (⚖️ ~2–4cr surgical FLUX edit — the ONLY sanctioned way to change an approved frame).
**`bentley.shared`** — `render.render_shot` (**the ONE sanctioned character-render entry**, bakes in best-of
+ last-frame pin + `@Bentley` element), `kling.i2v_payload`/`bentley_element`, `kie_client` (+ the two spend
guards), `gates`, `drift_guard`, `hosting`, `eleven`.

---

## 11. The exact recipe to render a shot correctly (copy this)

```
1. KEYFRAME(S):
   - START frame: EDIT from the master (nano-banana-pro, master-first refs) — never blind text-to-image.
   - END frame (for the pin): DERIVE FROM the approved START frame (START first in refs, ONE small delta).
     Never from the master. (Lever 1a — this is what fixed s7b.)
   - Rank candidates:  PYTHONPATH=. python3 -m bentley.qa.image_bestof --ref <MASTER> <cands...>
   - ✋ owner keyframe sign-off (record in GATES.md) BEFORE rendering.
2. MOTION-RISK TRIAGE: is the beat high-motion (jump/flop/spin/big-travel)? If yes → RESTAGE to contained
   motion (locked camera, centered, small pop) BEFORE the first render. Do not render raw-then-reroll.
3. RENDER (the sanctioned path bakes in pin + element + best-of):
     set -a && . ./.env && set +a
     export BENTLEY_EPISODE=ep4
     PYTHONPATH=. python3 -c 'from bentley.shared.render import render_shot; render_shot(<prompt>,
        first_frame=<start.png>, last_frame=<end.png>, out=<out.mp4>)'
   (drift_guard refuses this if it isn't last-frame-pinned; gates.py refuses without ep4 + Animatic Lock.)
4. QC: extract frames + run the ADVERSARIAL QC sweep (skeptic agents per failure class: teeth/eyes/tail/
   mask/paws/identity). Fix drift with the fix-first ladder (0-cr tools first).
5. ✋ owner sign-off → record in GATES.md gate 5.
6. If drift: reroll (≤2) → RESTAGE → animated coverage/owner direction → flag. NEVER reroll #3,
   and do not use static Ken-Burns as a hero-animation deliverable.
```

---

## 12. One-paragraph TL;DR for the next agent

Load the `episode-production` skill and read `GATES.md`. Story + VO + keyframes are locked; you're on **gate 5,
the hero renders.** Approved: s1b, s7a, s8, **s7b** (`renders_w1/s7b_run.mp4` — slow-mo run, OWNER-APPROVED;
the fix was re-staging the FEELING as a natural ACTION per its VO. Do NOT re-QC or reroll an owner-approved shot).
Continue the drift-rejected dynamic beats **s3a/s3b/s5b** (apply the s7b action-lesson) (+ s5a mask fix),
render the locked-keyframe heroes **s6/s9b/s10a/s10b/s11a/s11c**, and regen+render the legacy-glossy **s1a/s4a/s11c**.
Then Ken-Burns/cards for the free pieces, then assemble→mix→grade→QA→deliver. **Render one small wave at a time,
QC each (adversarial sweep), get ✋ owner sign-off in GATES.md before the next wave.** Never change the model,
never batch, never reroll a dynamic shot past #2 (restage instead), derive END keyframes from the approved START,
keep the LITERAL-master style, and on a 402 stop and tell the owner. Balance ≈ 10k cr; remaining ≈ 1–1.4k cr.
```
```
