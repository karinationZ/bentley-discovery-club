# Episode 1 — Cold Open (Scenes 1–2) · Build Record
### Produced on the **LOCKED Bentley-MASTER** (`1c82ee5b`) + Tidepool-cove (`d406065e`)

> This is the first footage built on the locked character design. **Result: zero drift** — Bentley held on-model across macro, sniff, sit-back surprise, head-tilt, and rally-leap, in stills AND through motion. The drift problem is solved; this pipeline is repeatable for the full episode.

## Timeline (≈21.0s, cut to `Teaser_music`)
| # | Beat | Clip (Seedance job) | Keyframe | Seg dur | VO |
|---|------|---------------------|----------|---------|----|
| A | Glowing shell macro (hook) | `f1f72eac` | `ecef4758` | 4.0s | Pip whisper "…Help? Somebody?" @0.5s |
| B | Nose pushes in & sniffs | `ba01e277` | `594e13b0` | 3.5s | — |
| C | Pulls back, surprised | `0b6a0b74` | `0b663882` | 2.5s | — |
| D | Endearing head-tilt | `21a02691` | `424609cc` | 3.0s | Bentley "Did the beach just… talk to me?" @10.4s |
| E | Rally pop "let's go!" | `3e930108` | `a4b94142` | 4.0s | Bentley "Let's go find the WONDER!" @13.7s |
| F | Wonder flash (tide-pool life) | `ac8cd0b9` | `0209d9ea` | 4.0s | — (music swell) |

## Audio bed → `work/coldopen_audiomix.m4a`
- Music `Teaser_music.m4a` @0.40, fade in 0.6s / out from 19.8s.
- `Pip_whisper_Snik.wav` @0.5s, ×1.9.
- `Bentley_line1_Abby_fast.wav` @10.4s, ×1.45.
- `Catchphrase_FindTheWonder.wav` @13.7s, ×1.55.
- amix normalize=0 → alimiter 0.95.

## Source / model
- Image keyframes: `nano_banana_flash`, 16:9, each embedding `<<<1c82ee5b…>>>` + restated 5 signature features + "match the model sheet."
- Video: `seedance_2_0`, mode **fast**, 720p, 16:9, 4s, role `start_image` = keyframe job-id. Decline preset `IN THE DARK` (`24bae836…`) to generate literally.
- **Gotcha:** the first wonder-flash render came back `nsfw` (false positive on "anemone blooms/sways") — fixed by rewording to "starfish / green sea plants shimmer."

## v2 update (current deliverable) → `work/Bentley_Ep1_ColdOpen_v2.mp4`
Two fixes after review:
1. **Style** — the sniff (S003) had rendered photoreal while the rest were stylized cartoon. Re-rendered in-style (cause: "macro / real fur / cinematic" tips nano-banana to photoreal — now banned from prompts).
2. **White paws** — every Bentley shot had hallucinated Boxer "socks." Locked the rule (white ONLY on chest) and paw-fixed each keyframe via nano-banana edit (free).
3. **Cheaper model** — re-animated the 3 character beats on **Minimax Hailuo 2.3** (`minimax_hailuo`, ~6 cr/6s) instead of Seedance 2.0 Fast (17.5 cr). Kept the Seedance shell/tilt/wonder (no paws / no Bentley). New jobs: sniff `66e05085`, reaction `68f9d63f`, rally `53dce88b`. Clean-paw keyframes: sniff `2be516b4`, reaction `a18c3f1b`, rally `fbde0a25`. Whole re-render ≈ 24 cr.

## Files
- `keyframes/` — locked stills (incl. alt takes S003_nose_b, S005_tilt_b).
- `clips/` — raw Seedance mp4s (have their own auto-audio; discarded in favor of our mix).
- `seg/` — trimmed + normalized 1280×720/24fps segments for concat.
- `work/` — audio mix + final assembly.
