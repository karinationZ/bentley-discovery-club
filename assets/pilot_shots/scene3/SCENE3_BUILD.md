# Episode 1 — Scene 3 "The Flaw" · Build Record
### 12 shots (S013–S024) · ~41s · first full Bentley + Pip scene · cheap pipeline

> **Why this scene:** to de-risk **two-character consistency**. Result: Bentley + Pip both hold on-model across the whole scene, in stills AND motion. The episode is a green light.

## Pipeline used
- **Keyframes:** `nano_banana_2`, embedding `<<<Bentley-MASTER>>>` + `<<<Pip>>>` + `<<<Tidepool-cove>>>`, restating features + "NO white socks." Reviewed via ffmpeg contact sheet.
- **Motion:** **Minimax Hailuo 2.3** (`minimax_hailuo`, 768, 6s, ~6 cr) for the 9 character beats. **Free Ken Burns** (ffmpeg zoompan) for S013 establish, S018 determined-grin, S024 sun-insert.
- **VO:** Inworld TTS — Narrator **Evelyn** (placeholder, swappable), Bentley **Abby** (+12% atempo), Pip **Snik**. Placed per-shot via adelay.
- **Music:** `sonilo_music` warm playful bed (34s, looped under dialogue at 0.18).

## Concurrency gotcha
PLUS = **max 6 concurrent jobs** (video+audio+music all count). Fire in batches of ≤6; excess errors with no credit loss.

## Cost (this scene)
~**104 cr** all-in (9 Hailuo ×6 = 54, + ~17 keyframes, 11 VO lines, 1 music bed). Balance 815 → 711.

## Honest episode estimate (revised)
Scene 3 is **animation-dense** (9 of 12 shots needed motion). Talkier / insert-heavy scenes (the science explainer, discovery tag) lean more on free Ken Burns. Realistic full episode ≈ **400–500 cr** (not the earlier optimistic 250–300) — still ~2 episodes/month, still ~3× cheaper than all-Seedance (~1200 cr).

## Open polish items
- Narrator voice (Evelyn) — audition alternatives if desired.
- No SFX layer yet (wave crash on S020, anemone gulp etc. come in later scenes). Music + VO carry v1.
- Pip-in-mouth gallop (S019) reads, but could be re-rendered tighter if wanted.

## Files
`keyframes/` selected stills · `clips/` raw Hailuo mp4s · `seg/` trimmed+normalized segments · `audio/` VO + music · `work/Bentley_Ep1_Scene3_v1.mp4` (deliverable) + `scene3_vo.m4a` + `scene3_contact_sheet.png`.
