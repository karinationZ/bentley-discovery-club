---
title: EP2 v3 Production Run Log
date: 2026-06-24
tags:
  - bentley/episode-2
  - production/run-log
  - kling-3
aliases:
  - EP2 v3 Run Log
---

# EP2 v3 Production Run Log

## Current State

Episode 2 was restarted as a character-driven rebuild. The v3 script, locked production cue sheet, retimed shotlist, VO, and Pod 1 test renders now exist.

This is not a final episode yet. Paid generation should pause until the credit/cost decision below is resolved.

## Files Created Or Updated

- `docs/series/season_1/ep2/EPISODE2_SCRIPT_v3_CHARACTER_DRIVEN.md`
- `docs/series/season_1/ep2/EP2_v3_PRODUCTION_CUE_SHEET.md`
- `episodes/ep2/shotlists/ep2_v3_character_driven.json`
- `scratch/ep2/restart_v3/make_v3_vo.py`
- `scratch/ep2/restart_v3/generate_v3_assets.py`
- `scratch/ep2/restart_v3/assemble_v3.py`
- `scratch/ep2/restart_v3/check_v3_assets.py`

## Agents Used

The production review used three sidecar QA roles before paid Kling generation:

- Story Editor + Continuity QA
- Animation Director + Animation QA
- VO / Lip Sync QA + Video Editor

Their shared blockers were correct:

- The original 25-shot plan was too short for the locked VO.
- Several shots were too dialogue-dense.
- Kling duration assumptions were inconsistent.
- Mouth safety needed to be in every prompt, not only in the general rules.
- The title card must be deterministic editorial graphics, not generated in Kling.

## What Was Fixed Before Generation

- Retimed the shotlist from 25 shots / 138s to 41 shots / 243.4s.
- Split dense exchanges into smaller visible speaker/listener beats.
- Restored the moray eel educational line.
- Restored the no-bones cue before Indi squeezes through the gap.
- Clarified the shell as a trail clue.
- Split the final character catchphrase and title card into separate beats.
- Added per-shot render durations: 5s or 10s only, then editorial trim.
- Added character-aware prompt safety so Bentley-only shots do not accidentally summon Indi.
- Added single-frame keyframe prompt logic to prevent storyboard/triptych stills.

## Models And Tools Used

- ElevenLabs: locked Bentley, Indi, and narrator voices.
- KIE `gpt-image-2-image-to-image`: v3 keyframes/stills.
- KIE `kling-3.0/video`: v3 Pod 1 motion.
- ffmpeg: VO concatenation, shot audio assembly, frame extraction, QA sheets.
- Local Python/PIL: deterministic title card and QA sheet helpers.

## Generated Assets

VO:

- `scratch/ep2/restart_v3/vo/labels/`
- `scratch/ep2/restart_v3/vo/shots/`
- `scratch/ep2/restart_v3/vo/EP2_v3_VO_READTHROUGH.mp3`
- `scratch/ep2/restart_v3/vo/vo_timing.json`

Timing result:

- 88 VO labels generated.
- Readthrough duration: 247.0s.
- 41 shot-audio files generated.
- Timing extensions flagged after retime: 0.

Pod 1 keyframes:

- `scratch/ep2/restart_v3/keyframes/p01_s01_boop.png`
- `scratch/ep2/restart_v3/keyframes/p01_s02_eye.png`
- `scratch/ep2/restart_v3/keyframes/p01_s03_winkers.png`
- `scratch/ep2/restart_v3/keyframes/p01_s04_names.png`
- `scratch/ep2/restart_v3/keyframes/p01_s05_found_rules.png`
- `scratch/ep2/restart_v3/keyframes/p01_s06_no_boop.png`

Pod 1 motion:

- `scratch/ep2/restart_v3/motion/p01_s01_boop.mp4`
- `scratch/ep2/restart_v3/motion/p01_s02_eye.mp4`
- `scratch/ep2/restart_v3/motion/p01_s03_winkers.mp4`
- `scratch/ep2/restart_v3/motion/p01_s04_names.mp4`
- `scratch/ep2/restart_v3/motion/p01_s05_found_rules.mp4`
- `scratch/ep2/restart_v3/motion/p01_s06_no_boop.mp4`

QA:

- `scratch/ep2/restart_v3/qa/EP2_v3_p01_motion_QA_sheet.jpg`

## Pod 1 QA

Passes:

- Overall style is strong and cohesive.
- Bentley generally looks excellent.
- Interaction staging is much closer to the desired 1:12 / 2:54 feeling.
- No subtitles or text were generated.
- Shot durations are technically usable; no short motion clips.

Failures / risks:

- `p01_s01_boop`: Bentley's tail appears longer than the locked docked-tail prop in motion frames. This can likely be fixed with a crop/zoom or a re-render.
- `p01_s02_eye`: motion reveals more of Indi's body by the midpoint, earlier than the intended eye-only reveal. Editorial trim can reduce this.
- `p01_s04_names` and `p01_s06_no_boop`: Indi still trends toward a cute humanoid smile in some frames. Not teeth, but still risky against the no-human-style-smile rule.
- Several Indi tentacle suckers can read as tooth-like if the frame is cropped poorly. Keep wide enough framing that they read as suckers.

## Credit Reality

Starting KIE balance before v3 paid rendering: 2390 credits.

Observed costs:

- `gpt-image-2-image-to-image` keyframe: 6 credits each.
- Kling 3.0 no-audio 5s motion: 70 credits each.
- Kling 3.0 no-audio 10s motion: 140 credits each.

Spent so far:

- Pod 1 stills and still re-renders: 72 credits.
- Pod 1 motion: 700 credits.
- Remaining KIE balance after Pod 1: 1618 credits.

Projected full all-new v3 Kling 3.0 cost from current 41-shot plan:

- 18 total 5s render units x 70 = 1260 credits.
- 22 total 10s render units x 140 = 3080 credits.
- 1 editorial card = 0 Kling credits.
- Motion subtotal: about 4340 credits.
- Keyframe subtotal: about 240-300 credits depending on re-renders.
- Total expected from scratch: about 4600+ credits.

Because 772 credits have already been spent and 1618 remain, there are not enough credits to finish a fully new Kling 3.0 render of the current v3 plan.

## Recommended Decision

Do not continue rendering all pods blindly.

Choose one:

1. **Top up credits and continue Kling 3.0 v3 rebuild.** This best preserves the owner's stated forward rule: use Kling 3.0 going forward.
2. **Shorten the episode to fewer Kling shots.** This saves credits but risks returning to the rushed montage problem.
3. **Use Kling 3.0 only for hero two-character shots and create procedural/editorial motion for inserts.** This is cheaper, but must be QA'd hard so it does not feel like static scenes pretending to be animation.
4. **Approve a cheaper secondary model for non-character inserts only.** This violates the pure Kling 3.0 rule unless explicitly approved.

Current recommendation: top up before continuing. The v3 structure is correct; the remaining blocker is production budget plus per-shot mouth QA.
