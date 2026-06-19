# EPISODE 1 — FIX PLAN (APPROVAL-READY)

**Supervising-producer merge of 5 QA audits** (Animation · Character Design · Story/Producer · Audio · Video-Editor/Color)
**Subject cut:** `assets/pilot_shots/hybrid_ep1/Bentley_Ep1_v2_FINAL_1080p.mp4` — 251.7s / 4:11.7 / 1080p / 24fps
**Date:** 2026-06-18 · **Status:** AWAITING APPROVAL — nothing will be rendered, regraded, or re-exported until you say go.

---

## 0. THE ONE-SENTENCE TRUTH (why "fixed" didn't feel fixed)

The fixes were **built but never wired into the cut.** The corrected VO (`a1_02_NEW.mp3`, `a5_04_NEW.mp3`) and the re-render specs (`ep1_rerender_batch.json`) were produced on disk, but `assemble_v2_final.py` still points the flagged shots at their **old source clips** and `mix_v2_final.py` contains **zero** references to the `_NEW` audio. The 15:23 rebuild ran the unmodified scripts, so the shipped mp4 is the old footage with the old lines. **Only one fix actually landed: the a3_02 live-wave re-render.** On top of that, a **brighter graded master already exists** (`Bentley_Ep1_v2_BRIGHT.mp4`) and the **darker** one was shipped as FINAL by mistake.

**Verified by me, not just inherited from the audits:**
- `assemble_v2_final.py` line 24 → `a1_02_bentley_hear.mp4` (old, 3.73s); line 47 → `N6_payoff_armor.mp4` (old, 10.13s); line 48 → `a5_04_tag.mp4` (old, 8.00s). ✓
- `grep NEW` in `mix_v2_final.py` and `assemble_v2_final.py` → **0 hits.** The NEW VO is parked, unused. ✓
- VO durations (ffprobe, exact): `a1_02_NEW.mp3` = **3.920s**, `a5_04_NEW.mp3` = **9.600s** (current a5_04 slot is only 8.00s → must grow). ✓
- Brightness (ffprobe signalstats, YAVG): a5_04@225s **FINAL 69.2 < PREMIX 76.3 < BRIGHT 130.4**; N6@218s **FINAL 81.5 vs BRIGHT 139.8**; a1_02@28s **FINAL 82.4 vs BRIGHT 114.0.** The shipped FINAL is the darkest of three existing masters. ✓
- a3_02 live water: interframe luma diff during Pip's plea runs a continuous ~0.4–1.4/frame (churning), confirming the wave re-render landed. ✓

---

## 1. ISSUE AUDIT TABLE — FIXED vs UNRESOLVED (with evidence)

All five auditors converged. Where they disagreed I resolved it (see notes under the table). Verdicts below are the **merged, final** dispositions.

| # | Issue (shot / timecode) | VERDICT | One-line evidence (this cut) |
|---|---|---|---|
| **1** | Reaction line "…come on!" + missing surprise→curiosity CU (`a1_02_hear`, 26.2–29.9s) | **UNRESOLVED ✗** | Build uses old `a1_02_bentley_hear.mp4` (asm L24); `a1_02_NEW.mp3` not wired; shot is a dark medium ¾-profile that hard-cuts to Pip — no held reaction CU exists. Backlit (face ~25–52). |
| **2** | ~0:53 two Bentley shots feel stitched (`a1_06_twoshot`→`N1_guess`, cut @52.79s) | **UNRESOLVED ✗** | Across-cut SSIM 0.58 (within-shot 0.93); two near-identical CUs, pose/scale/mouth jump; no sound-bridge; `N1_guess` also shows an upper-teeth grin @56.0s. |
| **3** | "STOP. LOOK. LISTEN." not slowed/charming (`a5_04_tag`, 223.7–231.7s) | **UNRESOLVED ✗** | Build uses old 8.0s `a5_04_tag.mp4` (asm L48); slowed `a5_04_NEW.mp3` (9.60s) not wired and can't fit the 8.0s slot; darkest face in the film (~36–61); no head-tilt; old fast line plays. |
| **4** | Lighting/color: too dark, washed, inconsistent (episode-wide) | **PARTIAL / mostly UNRESOLVED ✗** | Two problems: (a) **delivery regression** — shipped FINAL darker than BRIGHT & premix (verified above), FREE to fix; (b) **baked-in backlight** on Bentley CUs (faces 36–61 vs sky 150–194, Pip ref 104–136) — grade cannot add a key that wasn't rendered. Grade spread YAVG 57→124, sat mean ~17. |
| **5** | 03:35 payoff: creepy mouth / human teeth / weak wide comp (`N6_armor`, 213.6–223.7s) | **UNRESOLVED ✗ (LOCKED violation)** | Build uses old `N6_payoff_armor.mp4` (asm L47); wide full-body comp, **upper-teeth human grin** @218/221s; flat/dim; tail reads long, not docked. Brightening does not fix mouth/comp/tail. |
| **6** | ~1:29 frozen wave behind Pip (`a3_02_flip`, 85.3–108.5s) | **FIXED ✓** | Build uses re-rendered `a3_02_pip_flip.mp4` (Jun 18 10:29); interframe churn ~0.4–1.4/frame, visible foam motion; Pip on-model. **Done — drop from batch.** |

### New / cross-cutting findings surfaced by the audits (folded into the plan)

| Tag | Finding | VERDICT | Disposition |
|---|---|---|---|
| **N-A** | **Recurring LOCKED upper-teeth / human-grin** in 3 talking CUs: `a1_02` (28s), `N1_guess` (56s), `N6` (221s) | **UNRESOLVED ✗** | Killed by the #1, #2(N1), #5 re-renders; every re-render keyframe must bake "natural dog mouth, no upper teeth." QA gate on every accepted take. |
| **N-B** | **Long-clip mouth-flap risk:** N6 (10.13s) and a5_04 (8.0s) run longer than their lines | **UNRESOLVED ✗** | New renders trimmed to speech +~0.2s; VO pinned to frame per LOCKED timing rule. |
| **N-C** | **Wrong (darker) master shipped** — `Bentley_Ep1_v2_BRIGHT.mp4` exists, is +25–60 luma brighter, never clips | **UNRESOLVED ✗** | FREE: rebuild grade from BRIGHT levels; do not ship the dark FINAL. |
| **N-D** | **Grade is an un-versioned one-off** — not in any committed script (only per-shot dim/crop is) | **UNRESOLVED ✗** | FREE: commit `grade_v2_final.py` so brightness stops regressing between cuts. |
| **N-E** | **Bentley & Pip never share a frame** in the meet-cute (`a1_06_twoshot` is a misnomer — Bentley solo); bond reads thin | **UNRESOLVED ✗** | Deferred (TIER 2 / future) — not blocking; noted for honesty. Helped indirectly by the #1 reaction CU + #2 fix. |
| **N-F** | **Extra backlit Bentley faces** beyond the hero set: `N5_empathy` (43), `a3_01_fix` (49), `a3_04_stunned` (51), `a1_06_twoshot` (50) | **PARTIAL** | TIER 2 relights (approval-gated). Grade-lift if budget held; see §3. |

**Tally: 1 FIXED ✓ · 5 UNRESOLVED ✗ (one of them, #4, is "PARTIAL" — half free / half render).** Plus 6 cross-cutting items, all addressed below.

### Disagreements I resolved (honesty notes)
- **a3_02 (#6):** Animation + Story + Editor say **FIXED**; Character-Design said UNRESOLVED (it measured the **old** `v2/a3_02_pip_flip.mp4.bak`/720p source, not the cut). The **cut** uses the new 23.2s 10:29 clip and my interframe test shows live water → **FIXED.** The batch entry for a3_02 is **stale; drop it** (don't spend a render).
- **N1 / a3_01 / a3_04 / N5 / a1_06 relights:** CD + Editor want re-renders; Animation + Audio call them edit-first/optional. Resolution: **TIER 1 (must-do)** carries only what's strictly required to clear the 6 issues + the LOCKED teeth violation. The extra backlit faces are **TIER 2 (optional, approval-gated)** — the episode is shippable without them once the grade lifts midtones, but they're the difference between "good" and "polished." You decide at approval.
- **#2 N1 teeth:** because `N1_guess` has a LOCKED upper-teeth frame at 56s, the clean fix is to **re-render N1** (kills the teeth AND lets us re-frame so it stops match-jumping a1_06). A pure free edit (dissolve) hides the jump but **cannot remove the teeth** if N1 stays on screen at 56s. N1 is therefore in **TIER 1**.

---

## 2. IMPLEMENTATION PLAN (per unresolved issue: exact fix · asset · how)

> Legend — **REUSE** = existing asset, no render. **NEW** = fal render required. **FREE** = ffmpeg/edit/wire only.

### Issue #1 — Reaction line + surprise CU
- **Exact fix:** Render a tight, bright, wide-eyed Bentley CU (surprise→curiosity→excitement) lip-synced to the corrected line *"A voice? Somebody needs help?"*; insert it as a held ~1.5–2.0s reaction **before** the Pip reveal; wire `a1_02_NEW.mp3`.
- **Asset:** **NEW render** — `a1_02_react` (spec already in `ep1_rerender_batch.json`, sound, ship as-is). VO `a1_02_NEW.mp3` (3.92s) = **REUSE** (just wire it).
- **How:** keyframe from batch (warm front-left key, eyes wide+sparkling, ears soft-down, **natural dog mouth, NO upper teeth**) → talk clip timed to 3.92s → repoint `assemble_v2_final.py` L24 to the new clip and **lengthen the slot to ~3.9s** → reference `a1_02_NEW.mp3` in `mix_v2_final.py` (replace the old embedded line) → re-export.

### Issue #2 — Stitched 0:53 transition (+ N1 teeth)
- **Exact fix:** Re-render `N1_guess` as a deliberately different framing (slightly tighter/lower, gentle push-in) with matched key light and a clean **natural dog mouth**, so it no longer match-jumps `a1_06_twoshot` and the teeth frame is gone. In the edit, add a short cross-dissolve / continuous ambient+music bed across the seam (don't hard re-pin `theme_wonder` at the cut).
- **Asset:** **NEW render** — `N1_guess` (relit + re-framed + teeth-clean). a1_06 stays **REUSE** (grade-match only).
- **How:** new keyframe (push-in, key light, no upper teeth) → talk clip → repoint N1 in EDL → in `mix_v2_final.py` add `acrossfade`/ambient bridge and remove the music re-anchor at 52.79s → re-export. (If budget is held, the **free fallback** is dissolve-only, but it leaves the teeth — not recommended.)

### Issue #3 — "STOP. LOOK. LISTEN." charm beat
- **Exact fix:** Render a warm, charming tight CU with a **gentle head-tilt + direct eye contact + key light**, paced to the slowed VO; **grow the timeline slot from 8.0s → ~9.6s**; wire `a5_04_NEW.mp3` (which carries the Stop…/Look…/Listen… pauses).
- **Asset:** **NEW render** — `a5_04_tag` (hero; batch spec good, add explicit head-tilt + key). VO `a5_04_NEW.mp3` (9.60s) = **REUSE**.
- **How:** keyframe (warm key, head-tilt, soulful eyes-to-lens, soft natural mouth) → talk clip rendered/trimmed to ~9.6s → change `assemble_v2_final.py` L48 slot `8.00 → 9.60` and repoint to new clip → reference `a5_04_NEW.mp3` in the mix → re-export. **Budget a 2nd take** (this is the love-at-first-sight shot).

### Issue #4 — Lighting/color (split fix)
- **(a) FREE — global lift & consistency:** Rebuild the grade from `Bentley_Ep1_v2_BRIGHT.mp4` levels (or re-grade premix to match), then apply the single committed recipe in §5. Target every shot YAVG ~95–110, YHIGH ~205–215, sat ~22–26, no clipped blacks/highlights. **Commit it as `grade_v2_final.py`** (N-D).
- **(b) NEW — backlit faces:** The key light is carried by the #1/#3/#5 (and #2's N1) re-renders, whose keyframes already specify *"warm golden-dawn key raking across her face from camera-left ~30° above eye-line."* Optional extra backlit faces (N5/a3_01/a3_04/a1_06) → **TIER 2** relights or grade-lift.
- **How:** colorist pass (free) + the relight keyframes (already in scope under #1/#3/#5/#2).

### Issue #5 — N6 payoff (LOCKED teeth / weak comp)
- **Exact fix:** Execute the `N6_payoff_armor` spec already written in the batch: tight 85mm warm CU, soulful eyes into lens, **soft closed/barely-open mouth, lower teeth only, NO upper-teeth grin**, warm golden key, **short docked tail**; trim to speech (~6s).
- **Asset:** **NEW render** — `N6_payoff_armor` (hero; spec excellent, ship as-is).
- **How:** keyframe (QA for upper-teeth + long-tail **before** spending the clip render) → talk clip trimmed to ~6s → repoint `assemble_v2_final.py` L47 and shorten slot from 10.13s to ~6s → re-export. **Budget a 2nd take.**

### Issue #6 — Frozen wave
- **No action.** Already fixed and verified. **Drop the stale `a3_02_pip_flip` entry from `ep1_rerender_batch.json`** so it doesn't waste a render.

### Cross-cutting wiring (FREE, applies to all of the above)
1. Repoint `assemble_v2_final.py` EDL lines 24 (a1_02), 47 (N6), 48 (a5_04), and the N1 entry → new clips; fix the three slot durations.
2. Add `a1_02_NEW.mp3` + `a5_04_NEW.mp3` references to `mix_v2_final.py` (replace the old embedded lines).
3. Add the #2 sound-bridge; stop the music re-pin at 52.79s.
4. Re-run `assemble_v2_final.py` → `mix_v2_final.py` → grade → export. Then **re-run `verify_sync.py`** (must stay 0 overlaps).

---

## 3. RE-RENDER LIST + FAL BUDGET

**Model:** fal. **Unit costs:** keyframe ≈ **$0.04**; talk/video clip ≈ **$0.20–0.40**. Hero/hard shots (teeth, head-tilt, live motion) budget **2 takes**; standard shots **1 take (+1 spare allowance)**. **fal balance is currently EXHAUSTED → a top-up is required before any render** (top-up is the only spend this plan asks you to approve).

### TIER 1 — MUST-DO to clear the 6 issues + LOCKED violation (4 shots)

| Shot | Serves | Takes | Keyframe | Clips | Subtotal |
|---|---|---|---|---|---|
| `a1_02_react` | #1 reaction CU + new line + relight | 2 | $0.04 | 2 × $0.30 | **$0.64** |
| `a5_04_tag` (hero) | #3 charm CU + slowed VO + relight | 2 | $0.04 | 2 × $0.35 | **$0.74** |
| `N6_payoff_armor` (hero) | #5 teeth/comp/tail + relight | 2 | $0.04 | 2 × $0.35 | **$0.74** |
| `N1_guess` | #2 re-frame + #N-A teeth + relight | 2 | $0.04 | 2 × $0.30 | **$0.64** |
| | | | | **TIER 1 TOTAL** | **≈ $2.76** |

*(Floor, if every shot lands on take 1: keyframes 4×$0.04 + clips 4×~$0.32 ≈ **$1.44**. Plan to the 2-take ceiling.)*

### TIER 2 — OPTIONAL polish relights (approval-gated; episode ships without these once graded)

| Shot | Why | Takes | Keyframe | Clip | Subtotal |
|---|---|---|---|---|---|
| `N5_empathy` | face 43, black-void mask | 1 (+spare) | $0.04 | $0.30 | **$0.34** |
| `a3_01_fix` | face 49, no fill | 1 (+spare) | $0.04 | $0.30 | **$0.34** |
| `a3_04_stunned` | face 51 | 1 (+spare) | $0.04 | $0.30 | **$0.34** |
| `a1_06_twoshot` | face 50; other half of #2 | 1 (+spare) | $0.04 | $0.30 | **$0.34** |
| | | | | **TIER 2 TOTAL** | **≈ $1.36** |

### BUDGET BOTTOM LINE
- **TIER 1 only (recommended minimum): ≈ $2.76** → with retry headroom **top up ~$3.50.**
- **TIER 1 + TIER 2 (full polish): ≈ $4.12** → with retry headroom **top up ~$5.00.**
- **# shots to re-render:** **4** (Tier 1) — or **8** if Tier 2 approved.
- **a3_02 (#6): $0** (already fixed; remove stale batch entry).

### FREE work (do regardless of funding — no fal spend)
- Wire `a1_02_NEW.mp3` + `a5_04_NEW.mp3` into the mix; repoint EDL; fix 3 slot durations.
- Re-grade from BRIGHT levels + apply the §5 recipe; **commit `grade_v2_final.py`.**
- #2 sound-bridge + kill the music re-pin.
- Re-export; re-run `verify_sync.py`.
- **VO is already recorded** — $0 to use it.

---

## 4. REUSABLE ASSETS — already good, KEEP (do not re-do)

- **`a3_02_pip_flip.mp4` (23.2s, Jun 18 10:29)** — live churning water, Pip on-model. **Keep as-is.** (#6 done.)
- **`a1_02_NEW.mp3` (3.92s)** and **`a5_04_NEW.mp3` (9.60s, with the Stop/Look/Listen pauses)** — recorded, correct; **just wire them.**
- **`Bentley_Ep1_v2_BRIGHT.mp4`** — proves a brighter, non-clipping grade exists; **use as the grade base** (don't re-render to fix brightness).
- **`ep1_rerender_batch.json` specs** — `a1_02_react`, `a5_04_tag`, `N6_payoff_armor` are sound; **ship as written** (drop the stale `a3_02` entry; tweak `N1_guess` framing).
- **Audio bed (verified GOOD, no work):** −14.12 LUFS, −1.32 dBTP, no clipping, no dead air; **0 voice overlaps** (`verify_sync.py` PASS); cry-before-Bentley placement correct (~0.8s then 0.5s gap); recoil music + wave SFX scored; even dialogue levels (~−17 to −18.5 mean).
- **On-model compliance (CURRENT cut):** tail (docked), ears (floppy-down), paws (NO white socks — recurring bug is clean), chest blaze, soulful eyes — **all COMPLIANT.** Only LOCKED defect is the upper-teeth grin in a1_02/N1/N6, fixed by the Tier 1 re-renders.
- **All non-flagged shots / Pip shots** (front-lit, face ~104–136) — **grade-only**, no re-render.

---

## 5. GRADE PLAN — single consistent recipe for the whole episode (FREE)

**Goal:** bright, vibrant, natural-contrast, warm, inviting, daytime-leaning, consistent. **Base = BRIGHT-master levels** (do NOT start from the dark FINAL). Two steps, committed as `grade_v2_final.py`:

**Step 1 — Per-shot exposure normalize** (because shots arrive 57→124):
- Lift each shot's whole-frame **YAVG → ~95–110** and **YHIGH → ~205–215**; anchor already-bright title cards, lift the darkest most (a4_01 +35; a5_04 / N5 / BR1 +25). Use per-shot `eq=brightness/gamma` (the assemble script already has per-shot hooks).

**Step 2 — One global creative grade** (identical chain on every shot):
- **S-curve (`curves`):** lift shadows ~+8, hold mids, roll highlights to YHIGH ≈ 210 (kill crushed blacks YMIN 3–14 and dull caps YHIGH 149–165).
- **Saturation/vibrance:** `eq=saturation=1.18` (mean SAT ~17 → ~22–26; title's 27–32 is the "alive" reference); mild vibrance so fur/skin pop without blowing the sky.
- **Warmth:** `colorbalance` +0.04–0.06 mids-red / −0.03 mids-blue + a touch warm in highlights — golden-dawn, not orange cast.
- **De-haze foggy BGs** (a1_04, a2_01, a5_02, a6_01): local contrast / mild `unsharp` + black-point lift on rocks to cut the milky look (keep a little as intentional dawn mist).
- **Finish:** `format=yuv420p`, broadcast-safe levels, no true-peak/level clip.
- **Targets after grade:** every shot **YAVG 95–110, YHIGH ~205–215, SATAVG 22–26.**

**Honesty note:** the grade fixes the *global* dark/washed/inconsistent problem and the front-lit shots completely. It **cannot** create a key on the backlit Bentley faces — lifting them just greys the shadow (BRIGHT only reaches face ~77–83, still ~40% under target). Those faces are cured by the **re-render key light** (Tier 1 covers the hero ones; Tier 2 the rest).

---

## 6. EXECUTION ORDER + QA CHECKLIST (mapped to your acceptance)

> **No step runs until you approve.** Order is sequenced so the free work and keyframe-QA gates happen *before* any clip-render spend.

**Phase A — FREE prep (no fal):**
1. Drop stale `a3_02` from `ep1_rerender_batch.json`.
2. Write the wiring edits: EDL repoint (L24/47/48 + N1) and slot durations (a1_02→3.9s, a5_04→9.6s, N6→~6s); add `_NEW` VO + sound-bridge to `mix_v2_final.py`.
3. Draft `grade_v2_final.py` from BRIGHT levels (§5).

**Phase B — fal top-up + keyframe gate:**
4. **Top up fal (~$3.50 Tier 1, or ~$5.00 Tier 1+2).**
5. Render the 4 (or 8) keyframes. **GATE:** reject any with upper teeth / human grin / long tail / no key light **before** rendering clips.

**Phase C — clip renders:**
6. Render talk clips (2 takes on a5_04/N6/a1_02/N1). **GATE:** pick the take with clean natural mouth, head-tilt (a5_04), live read; trim to speech +~0.2s.

**Phase D — assemble / grade / export:**
7. Re-run `assemble_v2_final.py` → `mix_v2_final.py` → `grade_v2_final.py` → export new FINAL.

**Phase E — QA re-test (acceptance gate):**
8. Re-run `verify_sync.py` (**must = 0 overlaps**). Re-measure brightness + face-luma.

### Re-test / QA checklist (each maps to your stated acceptance)

| Your acceptance | Pass condition |
|---|---|
| #1 reaction fixed | New line "A voice? Somebody needs help?" plays (no "…come on!"); a held bright reaction CU sits before the Pip reveal; **no upper teeth.** |
| #2 transition flows | a1_06→N1 no longer match-jumps (re-framed N1 + dissolve + continuous bed); **N1 teeth gone @56s.** |
| #3 STOP·LOOK·LISTEN | Slowed VO with audible Stop…/Look…/Listen… pauses; head-tilt + eye contact; warm key; slot ≥9.6s. |
| #4 lighting/color | Every shot YAVG 95–110, YHIGH ~205–215, SAT 22–26; no clipped blacks; backlit hero faces now key-lit ≥ ~110; grade committed to script. |
| #5 N6 payoff | Tight warm CU, eye contact, **soft mouth / lower teeth only**, short docked tail, trimmed to speech. |
| #6 wave | Still alive (re-confirm interframe motion). |
| Audio integrity | −14 LUFS / ≤−1 dBTP / no clipping / no dead air / **0 voice overlaps** retained. |
| "Make us love Bentley" (0:25–0:53) | Curious/warm/playful/charming reads on the new CUs; she's lit, sparkly, clean-mouthed — not anxious/dark. |

---

### APPROVAL DECISIONS REQUESTED
1. **Approve the re-render scope:** TIER 1 only (4 shots, ~$2.76) **or** TIER 1 + TIER 2 (8 shots, ~$4.12)?
2. **Approve the fal top-up:** ~$3.50 (Tier 1) **or** ~$5.00 (Tier 1+2).
3. Confirm the FREE work (VO wiring + regrade from BRIGHT + commit grade script) proceeds in all cases.

*Nothing is rendered, regraded, or re-exported until you approve. On your go, execution follows Phase A→E above.*
