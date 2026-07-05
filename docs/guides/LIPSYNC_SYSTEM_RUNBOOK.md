# Lip-Sync System — Production Runbook

> ⛔ **STATUS: ON HOLD — the 2.5D patch renderer was OWNER-REJECTED (2026-07-01, 3×).** A flat mouth
> patch is anatomically wrong on ¾/down-facing/profile heads (the real mouth is an occluded seam; the
> patch reads as a hole in the cheek regardless of tracking). Do NOT use this runbook for production.
> The TIMING layer (Rhubarb adapter, viseme mapping, calibration/QA tooling) remains valid for the
> researched replacement. See the deep-research report + owner decision.

*The reusable rig lip-sync system (built 2026-07-01, plan: `HIGH_QUALITY_LIPSYNC_SYSTEM_PLAN.md`).
Works for ANY character, plate, line, episode. Zero credits per line; a line re-renders in seconds.*

**Module:** `bentley/lipsync/` · **Tests:** `tests/test_lipsync_*.py` (18) ·
**Rhubarb:** vendored `tools/rhubarb/` v1.14.0

```
audio + transcript ──rhubarb_adapter──► viseme timeline ─┐
character.json + angle sheets ───────► mouth shapes ────┼─► render ─► composite ─► QA sweep
plate .json (calibrated once) ───────► cached track ────┘
```

---

## Daily use: sync ONE line (after character + plate are onboarded)

```bash
python -m bentley.lipsync.pipeline \
  --plate episodes/ep3/lipsync/plates/ep3_strong_ts.json \
  --audio episodes/ep3/vo/B_strong.mp3 --label B_strong \
  --offset -0.28 --out out/B_strong_synced.mp4
```

- `--label` pulls the REAL transcript from the episode script (`label | speaker | text`);
  `--transcript "..."` overrides. Never retype transcripts — a wrong `--dialogFile` degrades cues.
- `--offset` = line start relative to the plate clip start (negative = line already running).
- The plate's mouth track is **cached** (`<plate_id>.track.json`) — every further line on that
  plate skips tracking. Delete the cache to re-track.

**⚖️ QA GATE (ship-blocking):** every run emits `<out>.qa.png` — a dense 0.15s frame sweep.
**Inspect EVERY frame** for: mouth in place, opens inside the muzzle, closed moments = clean
plate, no patch outside visibility windows, no artifacts. Spot-checking a few stills WILL miss
bad frames (proven twice on EP3). A line ships only after its sweep passes.

---

## Onboard a NEW PLATE (once per plate, ~5 min)

1. `python -m bentley.lipsync.calibrate <plate.mp4> --skeleton episodes/<ep>/lipsync/plates/<id>.json`
   → grid-overlaid frame; read coordinates off it.
2. Fill the skeleton:
   - `template_box` — **the MOUTH REGION itself** (closed on the plate). NEVER nose/eye + offset:
     head rotation changes any fixed offset and the mouth drifts onto the cheek (EP3 lesson).
   - `mouth_offset` — mouth anchor relative to the template's top-left (usually its center).
   - `mouth_width` — patch width in plate px (match the muzzle's mouth-zone width).
   - `angle` — which character sheet this framing uses (`front` / `three_quarter` / `side`).
   - `visibility` — windows where the mouth is readable. Exclude spans where the camera leaves
     the speaker or the mouth is an edge-sliver — film grammar: don't sync a mouth the viewer
     can't read. If the speaker's mouth is under `min_mouth_px` the whole shot: skip the rig
     entirely (VO-over-alive), same waiver as Marco's tiny shots.
   - Keep `search_radius_px` ≈ 60 — stops the tracker teleporting to look-alike dark blobs
     (paw, tag — both happened).

## Onboard a NEW CHARACTER (once per character, ~1 hour)

1. **Generate 3×3 viseme grids per angle** with the image models: reference = the locked master
   + a REAL PLATE FRAME CROP for that angle (matches angle+lighting exactly). Prompt the 9 cells
   (`REST_CLOSED MBP CONS AI E O U FV L`), labels UNDER the cells, and the species mouth rules
   (Bentley: toothless dark interior + tongue; Marco: insect mandibles, no lips, no dog teeth —
   design rules in the plan doc). 3–4 candidates → **owner picks** (standing rule).
2. **Cut the sheet:** `python -m bentley.lipsync.sheet_cutter grid.png assets/lipsync/<char>/mouth_shapes/<ver>/ \
   --ref-box <cell-1 stable-feature box> --mouth <cell-1 mouth center> [--mirror]`
   (fractions of a cell; the cutter NCC-registers every cell — grids drift, fixed boxes fail).
   Cut TIGHT: a generous crop duplicates the nose on composite. White tooth-hints are
   auto-darkened. Build a proof montage; **owner approves the sheet** before production.
3. **Write `assets/lipsync/<char>/character.json`** — sheets per angle, `plate_provides`
   (visemes the plate itself covers: on closed-mouth plates `REST_CLOSED MBP CONS FV` → no patch,
   the rig only ADDS openings), optional `rhubarb_map_overrides` (insect mouths etc.),
   `min_mouth_px` waiver.
4. Run `python -m pytest tests/test_lipsync_*.py` — the suite guards the hard rules (no speech
   cue may map to a closed shape, configs must resolve).

## New-EPISODE rules (from `episode-production` + the plan)

- **CLOSED-MOUTH PLATE RULE:** dialogue plates destined for the rig are generated with the
  speaking character's mouth CLOSED/calm. Never prompt "talking/mouth moving" for rig plates —
  baked-in flapping forces paint-out (the EP3 LEAN plate was un-patchable because of this).
- The owner-locked **"Stop. Look. Listen."** moment stays Kling-Avatar. The rig never touches it.
- Mouth tracks are per-PLATE assets: reuse plates → reuse tracks → the per-line cost is minutes.

## Known limits (honest)

- 2.5D patches: no 3D relight; big fast head turns need per-segment calibration or a visibility
  waiver. The long-term fix is the Blender rig (plan Phase 6).
- Comp polish (grain/motion-blur match) is minimal; fine at 1080p playback, visible in freeze-frames.
- Rhubarb is blocking, not acting: emphasis/holds go in the Phase-5 override files when needed.
