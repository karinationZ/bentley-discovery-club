# ep4 · The Butterfly Highway — PRODUCTION BOARD

> **DERIVED VIEW — do not hand-edit.** Rendered from `board.json` by `python -m bentley.board render`. The board is the single source of truth; `GATES.md`/`HANDOFF.md` are also derived. Mutate state only through the `bentley.board` CLI.

**Stage:** `renders` · **Next action (in order):** s1a — keyframe → owner pick → render  [section 1: Cold open — spark & meet] · **Credits:** 9800 balance

**Stages:** premise → vo → animatic → keyframes → **[renders]** → assemble → mix_grade → qa → release

**Shot states:** todo 6 · keyframe 3 · kf_approved 6 · qc 2 · locked 4

## Locked asset manifest (the canon — one reference for every shot)

- **Style anchor:** `assets/character_design/Bentley_MASTER_pixar.png`
- **bentley:** master: `assets/character_design/Bentley_MASTER_pixar.png` · turnaround: `assets/character_design/Bentley_MODEL_SHEET_turnaround.png` · talking: `assets/character_design/Bentley_TALKING_MASTER.png` · voice: `LauraZ`
- **mira:** master: `assets/character_design/Mira_LOCKED.png` · voice: `eleven.MIRA`
- **narrator:** voice: `Bill (eleven.NARRATOR)`
- **Environments:** meadow `assets/character_design/Meadow_plate.png` · grove `assets/character_design/Grove_plate.png`
- **Props:** collar: teal + gold paw-print tag
- **Models LOCKED:** keyframe=`nano-banana-pro` · motion=`kling-3.0/video` · talk=`kling/ai-avatar-standard` — never change the model

## Story spine (keep visible — never 'lose the track')

- **Feeling:** the wonder of the journey / trust the family
- **Lesson:** you don't have to know the whole way — just fly to the next flower
- **Facts:** monarchs migrate over generations · they taste with their feet · metamorphosis

## Shot board

### Section 1 · Cold open — spark & meet — … in progress  ◀ current portion

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s1a | todo |  | B_hook1, B_hook2 |  | — | 0 |
| s2 | todo |  | — |  | — | 0 |
| s1b | **LOCKED** |  | B_hooknose, M_hello, B_iam |  | `scratch/ep4/renders_w0/s1b_nose_taste.mp4` | 0 |

### Section 2 · New friend — copy & play — … in progress

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s3a | keyframe ⚠️RESTAGE | invite / come-on | N_intro, M_comeon | TBD — stage the FEELING as a natural ACTION per its VO (¾-front if a run) | — | 2 |
| s3b | keyframe ⚠️RESTAGE | planning gag | B_plan, M_nomap, B_nomap2 | TBD — stage the FEELING as a natural ACTION per its VO (¾-front if a run) | — | 2 |
| s4a | todo |  | N_feet, M_trythis |  | — | 0 |
| s4b | qc | playful copy | B_copyfeet, M_giggle1, B_questions |  | `scratch/ep4/renders_w1/s4b_copy_sneeze.mp4` | 0 |

### Section 3 · The race & the turn — … in progress

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s5a | qc cosmetic→assembly | lead-the-way | B_lead, N_race | calm bound | `scratch/ep4/renders_w1/s5a_lead_bound.mp4` | 0 |
| s5b | keyframe ⚠️RESTAGE | flower flop | M_floptease, B_flop | TBD — stage the FEELING as a natural ACTION per its VO (¾-front if a run) | — | 2 |
| s6 | kf-approved | catchphrase | B_stoplook, N_turn, B_river | avatar CU: 'Stop. Look. Listen.' | — | 0 |

### Section 4 · The butterfly highway — 🎬 renders done → ASSEMBLE + VO-review

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s7a | **LOCKED** |  | B_wheredoesit, M_dontknow, M_generations |  | `scratch/ep4/renders_w0/s7a_reframe_q_r1.mp4` | 0 |
| s7b | **LOCKED** | JOY | B_mindblown, N_generations | slow-mo run, ¾-front, ears flying | `scratch/ep4/renders_w1/s7b_run.mp4` | 0 |
| s8 | **LOCKED** | hero/thumbnail | M_ridewithme, M_glidecoach, B_glide, N_updraft | slow-mo run→glide | `scratch/ep4/renders_w0/s8_run.mp4` | 0 |

### Section 5 · The secret grove — … in progress

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s9a | todo |  | N_grove |  | — | 0 |
| s9b | kf-approved |  | B_grove, M_home |  | — | 0 |
| s10a | kf-approved |  | B_worm, M_caterpillar |  | — | 0 |
| s10b | kf-approved |  | B_fancyworm, N_button |  | — | 0 |

### Section 6 · Dusk & goodnight — … in progress

| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |
|------|-------|---------|----|------------------|-------------|---------|
| s11a | kf-approved |  | N_dusk, M_goodnight, B_reflect |  | — | 0 |
| s11b | todo |  | M_grovesong, B_dreamy |  | — | 0 |
| s11c | kf-approved |  | B_mantra, N_close |  | — | 0 |
| s11d | todo |  | — |  | — | 0 |

## Decisions log (structured — supersedes prose)

| Date | Scope | Decision | Cost | Status |
|------|-------|----------|------|--------|
| 2026-07-05 | style | style anchor = the LITERAL master (Bentley_MASTER_pixar); painterly is VOID | 720 | active |
| 2026-07-06 | models | models LOCKED: nano-banana-pro / kling-3.0/video / ai-avatar-standard; rig path DEAD | — | active |
| 2026-07-06 | s7b | stage a beat's FEELING as a natural ACTION per its VO (JOY→run), never a reaction pose; run shots ¾-front to occlude the docked tail | 810 | active |
| 2026-07-07 | policy | owner-APPROVED = LOCKED; adversarial QC is a PRE-approval gate only, never reopens an approval | 210 | active |

## Agent protocol (the rails)

1. Read the board FIRST, every session — it is the single source of truth (not chat, not prose).
2. Act only on `next_action` — one shot / one wave at a time (Rule 11).
3. Update the board after every step (state + a decision row + the asset path).
4. NEVER touch a LOCKED shot — owner-approval is terminal; QC is a PRE-approval gate only.
5. A shot advances state only by passing its gate; record the gate.
6. Reroll ≤2 → RESTAGE → trim/downgrade → flag (the counter lives on the shot).
7. Cosmetic ≠ ship-blocking — never gate an approval on a cosmetic defect; defer it to assembly.
