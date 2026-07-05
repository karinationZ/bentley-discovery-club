# FIX-FIRST TOOLKIT — repair programmatically before regenerating (plan + inventory)

**2026-07-05 · owner-directed.** Companion to the FIX-FIRST law in `episode-production` SKILL §1b /
playbook Part 11. Goal: every RECURRING defect gets checked against an internal tool BEFORE any
regeneration spend. Regeneration is the LAST resort, never the default. Inspiration + precedent:
`bentley/fix/magic_wand.py` (the zero-token white-paw recolorer, owner-commissioned, bake-off-proven
in `scratch/ep4/wand_lab/`).

## The ladder (cheapest layer that owns the defect — always walk it top-down)

| Tier | Cost | Layer | Tools |
|---|---|---|---|
| 1 | 0 cr | **Edit layer** — EDL math, trims, retimes, transitions, sharpen/grade in ffmpeg | `bentley/qa/edl_lint.py` · `bentley/fix/tail_trim.py` · assembler/mix/grade |
| 2 | 0 cr | **Local pixel layer** — deterministic recolor/patch, nothing outside the selection | `bentley/fix/magic_wand.py` (+ proposed tools below) |
| 3 | ~2–4 cr | **Surgical AI edit** — minimal-change edit of the otherwise-approved frame | `bentley/fix/kontext_edit.py` (FLUX Kontext) · nano-banana-edit paw pass (playbook §3.2 4b) |
| 4 | 70 cr | **Re-render** — LAST resort; reroll cap ≤2 → restage → downgrade → owner | Kling 3.0 from the clean keyframe + locked elements |

Discipline at every tier: **preview/measure → fix → re-run the SAME QC gate the asset failed.**
An unverified fix is not a fix. Bulk fix passes obey Rule 11 waves like any other stage.

## BUILT — production tools (tested, `tests/test_*.py`)

| Tool | Defect it owns | Notes |
|---|---|---|
| `bentley/fix/magic_wand.py` | **White paws / white socks / color drift** on stills AND video ROIs | Edge-aware in-shot recolor; preview-first; coat sample validated. The template for all tier-2 tools. |
| `bentley/fix/tail_trim.py` | **Frozen Kling tail** (C7) — every render holds its last frame | `scan` (QC gate, exit-code) / `trim` (cut at last moving frame, fresh filename). Refuses fully-static clips (that's a §5 defect). |
| `bentley/qa/edl_lint.py` | **Freeze-stretch / VO-outlasts-picture / >1.3× retime / same-clip back-to-back / missing media** | The freeze-push math (`wants/clip/push=0.00`) mechanized; run at EDL time AND after every clip swap. Exit-code gate. |
| `bentley/fix/kontext_edit.py` | **Anatomy-level drift on an approved frame** — too-long tail, googly eyes, mangled prop | Tier 3 (SPENDS ~2–4 cr). Productionizes the proven s10a eye-fix pattern; minimal-change prompt; never regenerate from masters. |

## PROPOSED — need ✋ owner approval + a wand_lab-style bake-off before build

Each of these must be scored on REAL drifted assets (the magic_wand precedent: 3 algorithms,
scored collateral, winner promoted) — never trusted from a synthetic demo.

1. **`magic_wand` recolor generalization** (tier 2, high value): arbitrary canon-color targets, not
   just white→fawn — drifted collar→**teal**, tag→**gold**, eyes→**brown**, Marco's golden-amber,
   Indi's purple. Target sampled from the LOCKED master (`--ref Master.png --ref-xy`) instead of
   in-shot. Owns most "minor character consistency" color defects at 0 cr.
2. **`tail_dock`** (tier 2): too-long/hairy tail on a STILL where the tail sits against clean
   background — box + background inpaint + stub. Honest limit: body-crossing/cluttered tails stay
   tier 3 (`kontext_edit`, today's sanctioned route) or regen.
3. **`shot_match`** (tier 1½): conform a drifted clip's color/luma to a scene reference clip (LAB
   transfer → ffmpeg LUT). Owns "grade inconsistent across shots" QA fails and the known
   **Kling-Avatar darkening** (measure the luma delta vs the source keyframe, auto-lift).
4. **`plate_match`** (tier 2): background consistency — conform a keyframe's background to the
   episode's scene-anchor plate (masked histogram/LAB transfer), for adjacent keyframes of the same
   scene that drifted in sky/light color.
5. **`prop_paste`** (tier 2): composite a LOCKED prop master (Listening Tag, collar, shells) onto a
   still where the prop is missing/mangled; video only on locked-camera static ROIs.
6. **`bentley/qa/scan_suite.py`** (QA, big token saver): ONE command for the playbook Part 8.1
   scans — freeze scan (full runtime), black-frame scan, sharpness sweep (edge-var per scene),
   jitter check, stream checks — instead of re-writing scratch scan scripts every episode.

## REGEN-ONLY — do NOT build fixers for these (owner law / proven dead ends)

- **Jitter/shake** → locked-camera re-render; deshake measured WORSE (EP3: 13.3 vs 10.3).
- **Identity drift** ("different Bentleys") → the #1 blocker; masters + elements + hand-pick only.
- **Anatomy/pose in VIDEO**, human teeth, wrong expression → re-render from the clean keyframe.
- **Any mouth-region video compositing** → the lip-sync method table is CLOSED (2.5D patch rejected
  3×); a "freeze the listener's mouth" patch is the same dead end from the other side.
- **Keyframe softness** → REJECT + regenerate (owner law 2026-07-04); the measured sharpen pass is
  a final-cut edit-layer rescue only, never an asset fix.
