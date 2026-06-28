# Asset Audit & Reorganization — pre-Episode 2

**Audited:** `/assets` (was 3.9 GB / 1071 files across several parallel Episode-1 attempts).
**Date:** 2026-06-19. **Status:** Phase 1 ✅ DONE · Phase 2 ✅ DONE — **aligned to the committed `docs/REPO_ARCHITECTURE.md` §7** (media stays in `assets/{approved,deprecated,work_in_progress}`; only episode *data* lives in `episodes/epN/`). Resolved the 224 MB duplicate film + fixed the `verify_sync` drift. The large "move episode media into `episodes/ep1/working`" relocation is **intentionally NOT pursued** — it would contradict §7 and rewire ~10 scripts for no benefit the architecture wants. Available on request if you decide to extend the architecture.

> ⚠️ **Concurrency:** a separate reorg is mid-flight (49 uncommitted changes) moving **docs + code** (`docs/series` → `season_1/ep1`, scripts → `bentley/` package, the master → `episodes/ep1/`). It has **not** touched `/assets`. Asset media is **gitignored**, so my asset moves don't tangle that git state. But Phase 2 (below) moves files the **build scripts reference**, and those scripts are what the other reorg is restructuring — so Phase 2 must be coordinated.

## Classification

| Group | Path | Size | Class |
|---|---|---|---|
| Final film | `episodes/ep1/Bentley_Ep1_v2_FINAL_1080p.mp4` | 224M | **Ep1 FINAL** |
| Thumbnail | `…/hybrid_ep1/Bentley_Ep1_thumbnail.jpg` | — | **Ep1 FINAL** |
| Shorts (7 + SRT) | `…/hybrid_ep1/shorts/exports/` | — | **Ep1 FINAL** |
| Shorts docs/builder spec | `…/shorts/*.md`, `shorts_specs.json`, `src/`, `clips/` | 356M | **Ep1 WORKING** |
| Acts 1–3 / 4–6 clips | `…/hybrid_ep1/acts123/`, `acts456/` | 594M | **Ep1 WORKING** |
| v2 pipeline | `…/hybrid_ep1/v2/` (work, fixed, audio, sfx, music) | 1.2G | **Ep1 WORKING** + shared (see below) |
| build / opening_redo / hero* / norm / audio | `…/hybrid_ep1/*` | ~860M | **Ep1 WORKING** |
| Curated masters | `assets/approved/` (bentley, crab, shells, voices) | 113M* | **SHARED — source of truth** |
| Channel art | `assets/branding/` | 28M | **SHARED** |
| Character design | `assets/character_design/` | 36M | **SHARED** |
| Real-dog reference | `assets/bentley_real_pictures/` | 29M | **SHARED reference** |
| Music + SFX library | `…/v2/music/`, `…/v2/sfx/` | ~15M | **SHARED** (currently buried in Ep1) |
| Curated rejects | `assets/deprecated/` (raw VO, off-model stills) | 11M | **DEPRECATED** |
| **Experiments (retired Phase 1)** | `assets/deprecated/ep1_experiments/` | 428M | **DEPRECATED** ✅ moved |
| **Test meeting clips (retired)** | `assets/deprecated/meeting_test/` | — | **DEPRECATED** ✅ moved |

\* `approved/` is 337M because it holds a **224M DUPLICATE** of the final film (also in `episodes/ep1/`).

### Duplicates / junk found
- **DUPLICATE — final film** in `episodes/ep1/` *and* `assets/approved/episodes/` (224M redundant). Keep `episodes/ep1/` as canonical; the `approved/episodes/` copy should become a one-line pointer.
- Working shot clips (`a5_01_piphome.mp4`, `a2_02_softbody.mp4`, …) exist 3× each across `acts*/`, `v2/`, `build/`, `norm/` — pipeline copies (low priority; collapse during Phase 2).
- `concat.txt` / `list.txt` (4–5× each) — regenerable ffmpeg scratch. `.DS_Store` ✅ removed (10).

## ✅ Phase 1 — done (safe, no build impact)
Retired 5 superseded experiment folders (`coldopen_ep1`, `coldopen_teaser`, `full_episode`, `model_tests`, `opening_movement`) + 3 dead test clips → `assets/deprecated/`. Removed junk. **Result:** `pilot_shots/` now contains only `hybrid_ep1/` (the real Episode 1).

## 🟡 Phase 2 — staged target structure (needs script-path coordination)
```
episodes/ep1/
  final/      Bentley_Ep1_v2_FINAL_1080p.mp4 · thumbnail.jpg · shorts/ (7 + SRT)
  working/    acts123 · acts456 · v2 · build · opening_redo · hero* · norm · audio · shorts(src,clips)
  shotlists/  (already here)
assets/   ← SHARED, cross-episode ONLY
  masters/        Bentley + Pip masters · CLEAN_shell · locked voice samples   (= today's approved/)
  audio_library/  reusable music + SFX cues                                     (lift out of v2/)
  branding/  ·  character_design/  ·  reference/ (bentley_real_pictures)
  deprecated/     cross-episode rejects + ep1_experiments + meeting_test
```
**Why Phase 2 is gated:** moving `hybrid_ep1/v2`, `acts123/4`, etc. breaks `bentley/episode_builder/*` + `assemble/mix/grade` (they hard-code `assets/pilot_shots/hybrid_ep1/…`). Those scripts are exactly what the concurrent reorg is restructuring. Doing both at once risks an inconsistent tree. **Recommendation:** run Phase 2 as one coordinated change — relocate assets **and** update the script paths together — once the concurrent code reorg has committed (or hand me the whole reorg to keep code + assets consistent).
