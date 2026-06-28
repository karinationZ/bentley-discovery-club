# Episode 1 — "The Voice in the Shell" · HYBRID BUILD SHEET (production)
> Smart-hybrid build, 2026-06-16. Narrator (Theodore) **+** character dialogue (Bentley/Pip). Cinema Studio 3.0 on Bentley's 6 hero beats; reuse paid Hailuo clips + free 60fps upscale for the rest. Inherits `Bentley_PERFORMANCE_BIBLE.md` + `LOCKED_ELEMENTS.md`. Target ≤200 cr.

## THE 6 BENTLEY HERO BEATS → Cinema Studio 3.0 (30cr each, except #6 reused)
| # | Beat | Bentley-ism | Keyframe | Camera (Cinema Studio) |
|---|------|-------------|----------|------------------------|
| H1 | **Cold-open WONDER** — ears snap up, she hears the voice | head-turn / ears-up | NEW `HK1` | slow push-in as ears snap up |
| H2 | **WHOAA reveal of Pip** — jaw-drop discovering him | WHOAA jaw-drop | NEW `HK2` | push-in + slight tilt-down |
| H3 | **NOT-A-SWIMMER flip** — recoil from the surf | startled recoil | NEW `HK3` | quick handheld recoil, spray |
| H4 | **STOP·LOOK·LISTEN turn** — collar glows, she listens | collar-glow sit | NEW `HK4` | calm slow push-in, glow blooms |
| H5 | **Vacancy-chain WHOAA** — awe at the wonder | WHOAA jaw-drop | NEW `HK5` | push-in on her wonder face |
| H6 | **The TAG to camera** — "find the wonder" | grin + paw-stamp | ♻️ **pilot upscaled grin** | (already done — reuse) |

## NON-HERO SHOTS → reuse paid Hailuo clips (+ free 60fps upscale)
`reuse_followvoice` · `reuse_twoshot` · `reuse_pipscared` · `reuse_nudge` · `reuse_softbody` · `reuse_setdown` · `new_crowd` · `new_lineup` · `new_cascade` · `new_piphome` · `new_rescue` · `new_octopus` (all in `pilot_shots/full_episode/clips/`).

## AUDIO — HYBRID MIX (narrator spine + dialogue)
- **Narrator (Theodore):** `full_episode/audio/proc/N01–N20.wav` — ALL EXIST ✅
- **Bentley/Pip dialogue (front half):** `opening_movement/audio/proc/B_*.wav`, `P_*.wav` — EXIST ✅
- **NEW back-half dialogue to generate (cheap):**
  - BENTLEY (Abby +12%): "Whoa… did you SEE that?! The whole pool helped!" (vacancy WHOAA)
  - PIP (Snik): "It… fits. Thank you, Bentley." (home)
  - BENTLEY: "That's what the Big Adventures is for." (Soft-Eyes home)
  - BENTLEY (tag): "Stop. Look. Listen… and you'll find the wonder, everywhere. Let's go find the WONDER!"
- **Mix rule:** narrator carries transitions/science; dialogue carries reaction/heart. Narrator ducks under dialogue. One warm music bed; swell at the vacancy-chain reveal.

## LIP-SYNC (talking close-ups)
MCP audio path erroring → route H2/H4/H6 talking close-ups through **web Lip-Sync Studio** (I'll hand over keyframe + VO + steps), OR retry MCP. Wide/action beats: cut away (no lip-sync needed).

## BUILD ORDER
1. Generate 5 hero keyframes `HK1–HK5` (Nano-Banana, ~13cr).
2. Animate H1–H5 on Cinema Studio 3.0 (~150cr). H6 reused.
3. Generate 4 new back-half dialogue lines (~8cr).
4. Upscale all final clips → 1080p/60fps (free).
5. Assemble: hero beats + reuse clips on the narrator+dialogue mix, one grade, music.
6. Deliver `Bentley_Ep1_HYBRID_v1.mp4` + lip-sync handoff.

## BUDGET TRACKER  (start: 402.81 cr)
| Step | Est | Actual |
|---|---|---|
| 5 hero keyframes | ~13 | — |
| 5 Cinema Studio hero shots | ~150 | — |
| 4 dialogue lines | ~8 | — |
| upscales | ~0 | — |
| **Total** | **~171** | — |
