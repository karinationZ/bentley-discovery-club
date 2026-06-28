---
title: EP2 Final Handoff
date: 2026-06-23
tags:
  - bentley/episode-2
  - production/handoff
  - pipeline/kling-3
aliases:
  - Episode 2 Final Handoff
  - EP2 v7 Handoff
---

# EP2 Final Handoff

## Status

Episode 2 is delivered.

- Final deliverable: `scratch/ep2/final_delivery/EP2_FINAL.mp4`
- Working master: `scratch/ep2/final_v7/assembly/EP2_v7_FINAL.mp4`
- Runtime: `183.461s`
- Format: `1920x1080`, H.264, `24 fps`, AAC stereo `48 kHz`
- SHA-256: `55c5c1f116b589577be72018414bf2dd497630b827cc83675731215865122e19`
- Baseline used: `scratch/ep2/assembly/EP2_v5_FINAL.mp4`
- Baseline explicitly not used: `EP2_v6_FINAL.mp4` because it was the broken-Bentley rebuild

## What Changed

The final pass was a rescue build focused on the one real blocker: character identity, especially Bentley's face/body consistency and the no-human-teeth/no-human-smile rule.

The story spine from v5 was preserved because it already worked: tidepool setup, Indi reveal, eel threat, Bentley learning to stop/chase less, rescue, science payoff, and ant-city tease. The work was to rebuild the weak visual links around that spine.

Main changes:

- Replaced risky/off-model Bentley action beats with v7 assets.
- Avoided risky Kling-Avatar mouth animation in final dialogue-heavy moments.
- Converted many lines to VO-over animated performance/cutaway shots so Bentley and Indi do not need model-imposed human mouth shapes.
- Restored the `B_chase + B_rude` audio beat.
- Moved `N_outro` to the outro card instead of the ants shot.
- Added/kept the eel danger bridge and the wedged/rescue setup.
- Replaced the camo beat with a safe macro animated skin-camouflage shot.
- Replaced the risky squeeze shot with a safer wedge/breathe/reform composite.
- Added a non-text animated science payoff overlay for the three-hearts/blue-blood fact.
- Kept final cards only; no subtitles were added.

## Models And Tools Used

### KIE.ai `gpt-image-2-image-to-image`

Used for Bentley rescue keyframes because it held the core Bentley canon better than Nano-Banana Pro in the identity-lock test.

Observed result:

- Better docked tail/stub retention.
- Better red-fawn paws with fewer white-sock failures.
- Better floppy ear retention.
- Less human-smile drift on Bentley stills.

Settings used in `scratch/ep2/final_v7/generate_v7_assets.py`:

```python
payload = {
    "prompt": shot.still_prompt,
    "input_urls": shot_ref_urls(shot, refs),
    "aspect_ratio": "16:9",
}
kie_client.run("gpt-image-2-image-to-image", payload)
```

Reference inputs:

- `Bentley_MASTER_pixar.png`
- `Bentley_MODEL_SHEET_turnaround.png`
- `Indi_LOCKED.png` when Indi was in the shot

### KIE.ai `kling-3.0/video`

Used for v7 motion. This is the forward-production winner and should replace Kling 2.6 going forward.

Why:

- Kling 3.0 held Bentley's silhouette and prop identity better than Kling 2.6.
- `kling_elements` gave materially better character anchoring than prompt-only i2v.
- The 3-second identity smoke test preserved docked tail, floppy ears, and red-fawn paws where prior attempts drifted.

Settings used:

```python
payload = {
    "prompt": shot.motion_prompt,
    "image_urls": [approved_still_url],
    "sound": False,
    "duration": "5",
    "aspect_ratio": "16:9",
    "mode": "std",
    "multi_shots": False,
    "kling_elements": elements,
}
kie_client.run("kling-3.0/video", payload)
```

Bentley element:

```python
{
    "name": "bentley",
    "description": "Bentley locked red-fawn Boxer puppy with short docked tail stub, floppy folded ears, red-fawn paws, black mask, teal collar, gold paw tag",
    "element_input_urls": [bentley_master_url, bentley_turnaround_url],
}
```

Indi element:

```python
{
    "name": "indi",
    "description": "Indi locked small soft purple California two-spot octopus with teal eyes, two teal ring spots, no nose, no eyebrows, tiny toothless mouth",
    "element_input_urls": [indi_url, indi_url],
}
```

Important KIE gotcha: each `kling_elements[*].element_input_urls` list needs 2-4 images. For Indi, the single locked image was duplicated to satisfy the API.

### Nano-Banana Pro / FLUX.1 Kontext

Not used as the final rescue generator for Bentley v7. Nano-Banana Pro was tested for Bentley identity, but the multi-reference result still produced long/upright-tail drift. It remains useful for low-risk style edits and locked Indi/prop adjustments, but do not use it as the primary Bentley identity-lock tool unless it passes a fresh canon gate.

FLUX.1 Kontext was part of the broader available stack but was not the deciding tool in the final v7 rescue.

### Kling-Avatar / AI-Avatar

Not relied on for final risky talking shots. The production choice was to avoid mouth-sync where it created human teeth, human smiles, or model-drifted faces.

Forward rule:

- Use Kling-Avatar only for shots where a full-duration QA pass proves mouth == voice and no human teeth/smile appear.
- For Bentley and especially Indi, prefer `vo_over` plus body/eye/tentacle acting.
- For octopus dialogue, treat mouth-sync as optional, not required.

### ElevenLabs

Existing VO files in `scratch/ep2/vo` were reused. Final assembly placed them over motion/performance shots in ffmpeg instead of forcing new AI-avatar lip-sync.

### ffmpeg / Python

Final picture assembly and mix were local:

- `scratch/ep2/final_v7/assemble_v7.py`
- `scratch/ep2/final_v7/mix_v7.py`

The v7 assembly is 37 real segments. The mixer filters out intermediate `_silent` and `_bg` files so the timeline does not accidentally include temp renders.

## Process

1. Reviewed existing handoff, action items, v5/v6 status, and QA reports.
2. Treated `EP2_v5_FINAL.mp4` as the baseline because v6 had broken Bentley.
3. Ran an identity-lock gate:
   - `ideogram/character`: rejected due repeated KIE internal errors.
   - `nano-banana-pro` multi-reference: rejected for Bentley long/upright tail drift.
   - `gpt-image-2-image-to-image`: accepted for Bentley stills.
   - `kling-3.0/video` with `kling_elements`: accepted for motion.
4. Generated v7 replacement stills and motion clips under `scratch/ep2/final_v7`.
5. Curated outputs manually; rejected outputs that failed canon.
6. Rebuilt the episode with safer routing:
   - kept working v5 story beats;
   - inserted better Bentley motion;
   - converted risky mouth/lip-sync beats to VO-over;
   - used safe still/composite/VFX when generation failed.
7. Mixed the final episode with act music, ocean ambient, SFX, final grade, and 1080p export.
8. QA'd the final MP4, not just the segments.
9. Copied the final master to `scratch/ep2/final_delivery/EP2_FINAL.mp4` and verified the copy byte-matches the v7 master.

## Rejected Or Routed-Around Assets

- `EP2_v6_FINAL.mp4`: rejected as broken-Bentley baseline.
- `a3_20_twoshot.mp4`: rejected because Bentley paws drifted bright red/off-model.
- `a4_25_wedged_v2.mp4`: rejected because the octopus mouth became toothy/risky; final uses the safe still instead.
- `a1_08_camo_v2` motion: KIE safety blocked generation; final uses an animated macro camouflage pass from the approved still.
- Original `a4_28_squeeze`: replaced because the octopus read too much like a human-style smile in mouth-risk QA.

## QA Evidence

Final file inspected: `scratch/ep2/final_delivery/EP2_FINAL.mp4`

Technical QA:

- `ffprobe`: `183.461s`, `1920x1080`, H.264, `24/1`, AAC stereo `48000 Hz`
- Full decode: `ffmpeg -v error -i EP2_FINAL.mp4 -f null -` passed with no error output
- Subtitle stream count: `0`
- Silence check: no `silence_start` / `silence_end` hits at `-45 dB` for `1.2s`
- Black-frame check: no sustained black hits at `d=0.5`
- Freeze/static scan: `freeze_issue_count=0`
- Volume: mean `-17.5 dB`, max `-0.5 dB`
- Copy verification: `cmp` passed; delivery and master share the same SHA-256

Visual QA sheets generated from the final MP4:

- Scene midpoints: `scratch/ep2/final_v7/EP2_v7_FINAL_scene_qa_sheet.png`
- Every 4 seconds: `scratch/ep2/final_v7/EP2_v7_FINAL_every4s_qa_sheet.png`
- Transitions: `scratch/ep2/final_v7/EP2_v7_FINAL_transition_qa_sheet.png`
- Mouth/identity risk frames: `scratch/ep2/final_v7/EP2_v7_FINAL_mouth_risk_qa_sheet.png`

Visual QA decisions:

- Bentley sampled close-ups: no human teeth and no human-style grin.
- Camo beat: macro texture shot, no face/mouth.
- Wedged beat: safe still, no toothy octopus mouth.
- Squeeze beat: safer wedge/breathe/reform composite.
- End cards contain title/outro text only; there are no subtitles.

## Agents Used

The user requested a full production team. These were the specialist roles used:

- Executive Producer: `019ef5aa-0cf0-78f3-9f86-3cca6e8d5ab7`
- Story Editor: `019ef5aa-7196-7941-b43a-411a96470768`
- Animation Director: `019ef5aa-c0e7-7fe1-92cf-c5ca4f50a1b7`
- Animation QA: `019ef5ab-0ce1-7963-be71-e293c4a7ebc6`
- VO / Lip Sync QA: `019ef5ab-663d-7331-aaeb-074a5bb3a322`
- Video Editor: `019ef5ab-aeb8-74b3-ae11-e55a836c8bd0`
- Continuity QA: `019ef5b2-2af5-7871-b37a-06f41d2670d4`

Their findings shaped the final:

- Do not build on v6.
- Replace off-model Bentley action shots.
- Avoid risky AI-avatar talking-mouth shots.
- Restore the missing `B_rude` cue.
- Move `N_outro` to the outro card.
- Add the eel/wedged danger bridge.
- Remove static/frozen padding.
- Verify final export frames, not only source clips.

## Episode 3 Pipeline Rules

Use this as the starting point for Episode 3.

1. Use **Kling 3.0 i2v** for all new motion by default.
2. Use `kling_elements` for character shots.
3. Generate/approve stills before animating. Never auto-batch and ship.
4. For Bentley, start with `gpt-image-2-image-to-image` or a better trained identity model; do not rely on Nano-Banana Pro alone unless it passes the canon gate.
5. For Indi, avoid literal mouth-sync unless there is an approved toothless viseme/rig solution.
6. Use VO-over body/eye/tentacle acting for non-human dialogue.
7. Keep every line tied to a visual action; do not park dialogue on long talking-head holds.
8. QA the full duration of every clip. Worst frame fails.
9. QA the final export, not just the parts.
10. Build in the episode layout for Ep3 instead of scratch once the pipeline scripts are promoted.

Recommended Ep3 preflight:

1. Pick 3 representative shots: Bentley action, Bentley+Indi two-shot, creature/ant sequence.
2. Generate 4-8 still candidates per shot.
3. Animate only the best stills with `kling-3.0/video`, `mode=std`, `duration=5`, `sound=False`, `kling_elements`.
4. Make a frame strip at start/mid/end plus one every second.
5. Run the same final QA suite before approving the model path.

## What's Left

For Episode 2:

- Nothing blocks delivery. The final file is exported and QA'd.
- Optional archival cleanup: promote the v7 scratch scripts into the main episode builder only if we want this exact workflow reusable as code.

For Episode 3:

- Build a real reusable Kling 3.0 KIE runner in the main pipeline, not only in `scratch/ep2/final_v7`.
- Update old historical docs that still mention Kling 2.6 when they are copied forward.
- Decide whether to train a Bentley LoRA/DreamBooth or build a simple 3D/2.5D rig for long-term identity lock.
- Create an approved toothless Indi mouth/viseme policy before any future lip-sync attempt.
- Keep a budget buffer for manual curation; the winning process is cheap per attempt but depends on rejecting bad frames early.

