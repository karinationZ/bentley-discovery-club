# Ep2 Bentley Identity-Lock Test
*2026-06-23. Scratch-only gate test; no episode assets were overwritten.*

## Decision
For the Ep2 rescue, use a KIE-only stopgap:

1. **Bentley keyframes:** `gpt-image-2-image-to-image`
2. **Bentley motion:** `kling-3.0/video` with `kling_elements`
3. **Process:** generate 4-8 candidates per keyframe, approve the still, then animate only approved stills. Do not auto-batch.

Keep trained LoRA/DreamBooth or a true 3D rig as the long-term Ep3+ solution.

## Why
The earlier "conform" pass used prompt/reference conditioning, but the current keyframes already contain the failures before animation: long/upright tail, white paws, variable proportions, and style drift. A different video model alone will not fix bad stills.

## Tests Run
All outputs are in `scratch/ep2/identity_lock_test/`.

| Test | Result |
| --- | --- |
| `ideogram/character` | Failed 3 times with KIE internal 500s. Do not depend on it for this rescue pass. |
| `nano-banana-pro` multi-reference | Completed, but still produced a long/upright tail. Fails Bentley canon. |
| `gpt-image-2-image-to-image` boop still | Passed the main Bentley canon gate: floppy ears, docked stub, solid red-fawn paws, no human smile. Slightly more realistic than master. |
| `gpt-image-2-image-to-image` chase still | Passed the main Bentley canon gate. |
| `gpt-image-2-image-to-image` Bentley+Indi two-shot | Bentley mostly passes; Indi drifts softer/more humanoid. Mixed shots need stricter Indi handling or curation. |
| `kling-3.0/video` from GPT Image 2 boop still with Bentley element refs | Passed the main motion gate in a 3-second standard-mode test: docked stub survived, ears stayed down, no white socks. End frame has motion blur, so use short clips and frame-strip QA. |

Credit spend: 78 KIE credits total for this gate (`5152 -> 5074`).

## Review Files
- Still/video review sheet: `scratch/ep2/identity_lock_test/identity_lock_review_sheet.png`
- Full current-drift sheet: `scratch/ep2/identity_lock_test/bentley_identity_sheet.png`
- Promising stills:
  - `scratch/ep2/identity_lock_test/gpt_image_2_i2i_1.png`
  - `scratch/ep2/identity_lock_test/gpt_image_2_chase_1.png`
  - `scratch/ep2/identity_lock_test/gpt_image_2_twoshot_1.png`
- Motion smoke test:
  - `scratch/ep2/identity_lock_test/kling3_boop_from_gpt2.mp4`
  - frame checks: `kling3_boop_0.2.png`, `kling3_boop_1.5.png`, `kling3_boop_2.8.png`

## Production Rule For Step 2
For each target shot:

1. Generate 4-8 `gpt-image-2-image-to-image` still candidates.
2. Reject anything with long/upright tail, white socks/toes, pricked ears, adult/realistic body, wrong tag, human smile/teeth, or mismatched style.
3. For two-character shots, reject if Indi gets a nose, eyebrows, brown eyes, teeth, or a humanoid face.
4. Animate only the approved still with `kling-3.0/video`, using Bentley element refs from `Bentley_MASTER_pixar.png` and `Bentley_MODEL_SHEET_turnaround.png`.
5. Extract a frame strip from the final clip before replacing any episode asset.

Do not build on `EP2_v6_FINAL.mp4`. Baseline remains `scratch/ep2/assembly/EP2_v5_FINAL.mp4`.
