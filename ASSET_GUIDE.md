# ASSET_GUIDE — Where everything lives

This is the map of the `assets/` folder for *Bentley's Big Adventures*. Read this
first when you need to find a prop, a voice, a scene, or the finished episode.

> **Golden rule:** reach for an **approved** asset before you generate anything new.
> See the reuse-first token rule in `EPISODE_PRODUCTION_GUIDE.md`.

---

## Top-level layout

```
assets/
├── approved/            ← SOURCE OF TRUTH. Owner-approved, copied here. Use these first.
│   ├── episodes/        ← finished Episode 1 master + thumbnail
│   ├── scenes/          ← approved kie.ai re-render shots (*_NEW.mp4) in the final cut
│   ├── bentley/         ← best on-model Bentley stills (QA refs + edit bases)
│   ├── crab/            ← clean canonical Pip (hermit crab) keyframe
│   ├── shells/          ← clean smooth glowing seashell (still + clip)
│   ├── voices/          ← 1–2 cleaned samples of each LOCKED voice (no _raw)
│   └── README.md        ← per-folder detail + remote master image URLs
│
├── work_in_progress/    ← scratch / in-flight assets not yet approved or rejected
│
├── deprecated/          ← rejected or superseded assets (MOVED here, never deleted)
│   ├── bentley/ crab/ shells/ voices/ scenes/
│   └── DEPRECATED_LOG.md ← one line per retired file, with the reason
│
├── pilot_shots/         ← the live BUILD tree (scripts read/write here). Do not reorganize.
│   └── hybrid_ep1/      ← Episode 1 working dir: keyframes, clips, audio, v2/, build/…
├── branding/  character_design/  bentley_real_pictures/   ← brand + reference inputs
```

> `approved/` and `deprecated/` hold **copies / moved rejects**. The **originals
> that the pipeline actually consumes still live under `pilot_shots/`** (and a few
> under `tests/`). Never assume an approved copy is the build input — the scripts
> point at the original paths.

---

## How to find each prop's canonical master

| Asset | Canonical approved copy | Live original / master |
|-------|-------------------------|------------------------|
| **Finished Episode 1** | `assets/approved/episodes/Bentley_Ep1_v2_FINAL_1080p.mp4` | `assets/pilot_shots/hybrid_ep1/` |
| **Thumbnail** | `assets/approved/episodes/Bentley_Ep1_thumbnail.jpg` | same dir |
| **Approved scene shots** | `assets/approved/scenes/*_NEW.mp4` | `assets/pilot_shots/hybrid_ep1/v2/fixed/` (wired into `assemble_v2_final.py`) |
| **Bentley (image identity)** | `assets/approved/bentley/N6_kie_key_bright2.png`, `BR3_explore_key.png` | **remote master URL** in `pipeline.py` → `REFS["bentley"]` (see `approved/README.md`) |
| **Pip (image identity)** | `assets/approved/crab/a3_02b_pipcu_key.png` | **remote master URL** in `pipeline.py` → `REFS["pip"]` |
| **Shell** | `assets/approved/shells/CLEAN_shell_key.png` / `.mp4` | `assets/pilot_shots/hybrid_ep1/v2/`; regen via `shell_gen.py` |
| **Voices** | `assets/approved/voices/{BENTOS,PIPOS,THEO}_*.mp3` | `assets/pilot_shots/hybrid_ep1/v2/audio/`; voice IDs in `pipeline.py` |

The two **remote master images** (Bentley + Pip) are the identity source every
keyframe is edited from. Their URLs are recorded in `assets/approved/README.md`
and in `pipeline.py`. Do not download or fork them — always edit *from* them.

---

## Naming conventions (so you can read the tree at a glance)

- **Shot ids**: `a<act>_<beat>_<name>` (e.g. `a3_02b_pipcu`) or narration beats `N1..N6`,
  bridge/intro beats `I1..I4`, b-roll `BR1..BR3`, hero beats `H1..H6`.
- **Per shot in the build dir**: `…_key.png` = keyframe, `<id>.mp4` = rendered clip,
  `…_vo.mp3` = the shot's voice line, `…_seg.mp4` = a trimmed/segmented cut.
- **`*_NEW.mp4`** = an approved kie.ai **re-render** that replaced a broken/superseded shot.
- **Voice file prefixes**: `BENTOS_*` = Bentley (Laura Z), `PIPOS_*` = Pip (Callum +10%),
  `THEO_*` = Narrator (Bill). A trailing **`_raw`** = the un-cleaned export (deprecated;
  the cleaned sibling without `_raw` is the keeper).
- **`.preFIX` / `.bak` / `.pretext`** suffixes = pre-edit snapshots kept beside a file.
- **`CLEAN_*`** = the de-furred / corrected regeneration of a prop.

---

## Deprecated assets

Anything rejected or superseded is **moved** (never deleted) into
`assets/deprecated/<category>/`, and every retired file is logged with a one-line
reason in **`assets/deprecated/DEPRECATED_LOG.md`**. Because this is not a git
repo, a file is only moved after a `grep -rl "<stem>" --include='*.py'` confirms
**zero** script references; anything still referenced is left live and noted in the
log's "Skipped" section.
