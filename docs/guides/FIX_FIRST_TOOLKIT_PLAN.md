# FIX-FIRST TOOLKIT — repair programmatically before regenerating (plan + inventory)

**2026-07-05 · owner-directed.** Companion to the FIX-FIRST law in `episode-production` SKILL §1b /
playbook Part 11. Goal: every RECURRING defect gets checked against an internal tool BEFORE any
regeneration spend. Regeneration is the LAST resort, never the default. Inspiration + precedent:
`bentley/fix/magic_wand.py` (the zero-token white-paw recolorer, owner-commissioned, bake-off-proven
in `scratch/ep4/wand_lab/`).

## The ladder (cheapest layer that owns the defect — always walk it top-down)

| Tier | Cost | Layer | Tools |
|---|---|---|---|
| 1 | 0 cr | **Edit layer** — EDL math, trims, conforms, transitions, sharpen/grade in ffmpeg | `bentley/qa/edl_lint.py` · `bentley/fix/tail_trim.py` · `bentley/fix/shot_match.py` (1.5) · assembler/mix/grade |
| 2 | 0 cr | **Local pixel layer** — deterministic recolor/patch/fill, nothing outside the selection | `bentley/fix/magic_wand.py` · `recolor.py` · `tail_dock.py` · `plate_match.py` · `prop_paste.py` |
| 3 | ~2–4 cr | **Surgical AI edit** — minimal-change edit of the otherwise-approved frame | `bentley/fix/kontext_edit.py` (FLUX Kontext) · nano-banana-edit paw pass (playbook §3.2 4b) |
| 4 | 70 cr | **Re-render** — LAST resort; reroll cap ≤2 → restage → downgrade → owner | Kling 3.0 from the clean keyframe + locked elements |

(QA companion: `bentley/qa/scan_suite.py` — the Part 8.1 scans in one command; it finds the
defects the ladder then fixes.)

Discipline at every tier: **preview/measure → fix → re-run the SAME QC gate the asset failed.**
An unverified fix is not a fix. Bulk fix passes obey Rule 11 waves like any other stage.

## BUILT — production tools (tested, `tests/test_*.py`; ✋ owner approved the full set 2026-07-05)

| Tool | Tier | Defect it owns | Notes |
|---|---|---|---|
| `bentley/fix/magic_wand.py` | 2 | **White paws / socks** on stills AND video ROIs | Edge-aware in-shot recolor; preview-first; coat sample validated. Bake-off-proven (`scratch/ep4/wand_lab/`). |
| `bentley/fix/recolor.py` | 2 | **Any other canon-color drift** — collar off teal, tag off gold, eyes off brown, guest palettes | magic_wand's engine generalized; target sampled from the LOCKED master (`--to-ref/--to-xy`) so fixes converge on canon. Smoke-verified on a real 2K EP4 keyframe. |
| `bentley/fix/tail_dock.py` | 2 | **Too-long/hairy tail on a STILL vs clean background** | Edge-aware select + multiscale diffusion inpaint + matched grain; `--keep` protects the stub; WARNs on textured background (→ tier 3). Body-crossing tails are NEVER its job. |
| `bentley/fix/tail_trim.py` | 1 | **Frozen Kling tail** (C7) | `scan` (exit-code QC gate) / `trim` (cut at last moving frame, fresh filename). Refuses fully-static clips (that's a §5 defect). |
| `bentley/fix/shot_match.py` | 1.5 | **Grade inconsistent across shots · Kling-Avatar darkening** | Reinhard LAB stats conform of a clip to a scene ref (`--luma-only` = the Avatar lift). `scan` first: a huge delta means the shot is WRONG, not mis-graded. |
| `bentley/fix/plate_match.py` | 2 | **Background drift between adjacent keyframes of one scene** | Conform keyframe bg stats to the LOCKED scene-anchor plate; `--protect` boxes keep characters byte-identical. |
| `bentley/fix/prop_paste.py` | 2 | **Missing/mangled canon prop** (Listening Tag, shells) | Composite from the prop's locked RGBA cutout; `--match-light`; video only on locked-camera static ROIs. Perspective/occlusion = tier 3. |
| `bentley/qa/edl_lint.py` | 1 | **Freeze-stretch / VO-outlasts-picture / >1.3× retime / same-clip back-to-back / missing media** | The freeze-push math (`wants/clip/push=0.00`) mechanized; run at EDL time AND after every clip swap. Exit-code gate. |
| `bentley/qa/scan_suite.py` | QA | **Part 8.1 scans in one command** — freeze, black (leading=FAIL, trailing=OK), sharpness sweep, jitter, streams | Streaming, native fps; verified on the real EP4 animatic (every card correctly flagged as a freeze). Stops the per-episode rewrite of scratch scan scripts. |
| `bentley/fix/kontext_edit.py` | 3 | **Anatomy-level drift on an approved frame** — too-long tail (cluttered bg), googly eyes, warped prop | SPENDS ~2–4 cr. Productionizes the proven s10a eye-fix pattern; minimal-change prompt; never regenerate from masters. |

Shared core: `bentley/fix/color_transfer.py` (CIELAB Reinhard transfer, clipped gains — used by
shot_match / plate_match / prop_paste's `--match-light`).

**FIRST-USE VALIDATION (wand_lab law, still binding):** the pixel tools shipped with synthetic +
real-asset smoke checks, not a full scored bake-off per defect class. The FIRST production use of
each tool on a NEW defect class runs eyes-on: preview/scan → fix → zoomed side-by-side vs the
master → only then does the fix enter the cut. Any visible seam/miss on a real asset = stop, file
the case in `scratch/<ep>/wand_lab/`-style scoring, tune before second use.

## REGEN-ONLY — do NOT build fixers for these (owner law / proven dead ends)

- **Jitter/shake** → locked-camera re-render; deshake measured WORSE (EP3: 13.3 vs 10.3).
- **Identity drift** ("different Bentleys") → the #1 blocker; masters + elements + hand-pick only.
- **Anatomy/pose in VIDEO**, human teeth, wrong expression → re-render from the clean keyframe.
- **Any mouth-region video compositing** → the lip-sync method table is CLOSED (2.5D patch rejected
  3×); a "freeze the listener's mouth" patch is the same dead end from the other side.
- **Keyframe softness** → REJECT + regenerate (owner law 2026-07-04); the measured sharpen pass is
  a final-cut edit-layer rescue only, never an asset fix.
