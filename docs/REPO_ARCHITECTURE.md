# Repository Architecture & Migration

*Reorganization performed 2026-06-19. This document is the audit, the new architecture, the
migration map, the cleanup plan, and the conventions — in one place.*

---

## 1. Current architecture review (before)

The repo had grown organically into a **flat root**: 32 `.py` files, 12 `.md` docs, and 7
`.json` configs all sitting at the top level, alongside the media tree. Concretely, the smells:

| Smell | Evidence |
|-------|----------|
| **No package / flat namespace** | 32 scripts at root; imports via `from pipeline import ...` + a `sys.path.insert` hack in `overlay_vo`/`supp_vo`. |
| **Version-in-filename** | `assemble_acts123` → `assemble_v2` → `assemble_v2_final`; `mix_v2_final`; `grade_v2_final`. |
| **Duplicated helpers** | ffprobe `dur()` copy-pasted in 4 forward files; catbox `host()` in ~5; ElevenLabs `tts()` boilerplate in 6; `clean_master()` in 3. |
| **Behavior-critical duplication** | The voice-overlap scheduler was hand-copied between `mix` and `verify_sync` ("MUST match … exactly"). They had already **drifted** (see §8). |
| **Mixed responsibilities** | `pipeline.py` was both a CLI *and* an imported library (hence the `sys.path` hack). |
| **Scattered config** | Voice IDs hardcoded in 4 different files; absolute `/Users/...` paths in 7 files. |
| **`tests/` was not tests** | It held 289 MB of generated media + URL pointers, not a test suite. |
| **Doc sprawl** | Root docs overlapped the `youtube_vault` bible (e.g. `MASTER_PROP_RULES.md` vs vault's *Bentley Master Prop*). |
| **Dead directory** | `NARRATOR_AUDITIONS/` was empty. |
| **Not under version control** | No git → no history, no safety net for a large move. |

**Guiding principle for the fix:** of the 32 scripts, ~15 were already-run, one-off, EP1-specific
work; ~17 are the forward path that runs again for future episodes. *Invest refactoring only in
code with a future; freeze the rest unchanged.*

---

## 2. New architecture (after)

A proper Python package (`bentley/`) for active code, a thin entrypoint at root, per-episode
**data** separated from **code**, consolidated docs, and a frozen `deprecated/` archive.

```
youtube/
├── pipeline.py              # thin orchestrator — python pipeline.py <shotlist.json>
├── bentley/                 # importable package (pip install -e .)
│   ├── shared/              #   ffio · paths · eleven · audio · fal · kie_client
│   ├── asset_generation/    #   keyframes · thumbnail · thumbnail_text · title_card · shells
│   ├── animation/           #   video · avatar
│   ├── voices/              #   dialogue · narration · music · sfx
│   ├── episode_builder/     #   assemble · mix · grade · overlay_vo · supp_vo · shorts · timeline
│   └── qa/                  #   verify_sync
├── scripts/                 # runnable utilities (fix_paws.py)
├── prompts/                 # prompt library as data, per episode (convention; see §7)
├── episodes/ep1/shotlists/  # per-episode DATA: the *.json fed to pipeline.py
├── assets/                  # media (git-ignored): approved/ deprecated/ work_in_progress/ ...
├── docs/                    # guides/ decisions/ episodes/ rules/ series/ launch/ + this file
├── youtube_vault/           # canonical Obsidian production bible
├── scratch/                 # generated media from smoke tests (was tests/)
├── tests/                   # real unit tests (import-safe)
└── deprecated/              # frozen one-off / superseded scripts (never deleted)
```

### Module ownership

| Package | Responsibility | Public surface |
|---------|----------------|----------------|
| `shared/ffio` | ffprobe/ffmpeg helpers | `dur(path)` |
| `shared/paths` | repo-root-relative paths (portable) | `ROOT`, `ASSETS`, `SCRATCH`, `episode_assets()` |
| `shared/eleven` | ElevenLabs key + **LOCKED voice IDs** + low-level TTS | `KEY`, `BENTLEY/PIP/NARRATOR/THEO_GEORGE`, `speak()` |
| `shared/audio` | dialogue clean-master chain | `clean_master()` |
| `shared/fal` | fal model IDs, approved refs, timeout-guarded subscribe | `M_*`, `REFS`, `fsub()` |
| `shared/kie_client` | kie.ai jobs client | `run()`, `credits()`, `download()` |
| `voices/dialogue` | Bentley / Pip / Theodore character TTS | `tts_bentley/pip/theo()` |
| `voices/{narration,music,sfx}` | Bill narration · music cues · SFX palette | entrypoints |
| `asset_generation/*` | keyframes, thumbnail, title card, shells | mix of helpers + entrypoints |
| `animation/{video,avatar}` | Kling i2v · Kling lip-sync | `video()`, `avatar()` |
| `episode_builder/timeline` | **single source** voice scheduler | `make_next_talk_start()`, `place_sequential()` |
| `episode_builder/{assemble,mix,grade,overlay_vo,supp_vo,shorts}` | the editor | entrypoints |
| `qa/verify_sync` | zero-voice-overlap check | entrypoint |

---

## 3. Migration map (old → new)

**Forward code** (relocated + cleaned; behavior preserved by verbatim relocation):

| Old (root) | New | Change | Risk |
|------------|-----|--------|------|
| `kie_client.py` | `bentley/shared/kie_client.py` | move | none |
| `pipeline.py` | `pipeline.py` (root) | thinned; stages extracted to package | low — import-smoke verified |
| `music_gen.py` | `bentley/voices/music.py` | key←`eleven`; `__main__` guard | low |
| `sfx_gen.py` | `bentley/voices/sfx.py` | key←`eleven`; guard | low |
| `narration_bill.py` | `bentley/voices/narration.py` | key/voice←`eleven`; guard | low |
| `overlay_vo.py` | `bentley/episode_builder/overlay_vo.py` | import `dialogue`; drop `sys.path` + dup `tts_theo`; guard | low |
| `supp_vo.py` | `bentley/episode_builder/supp_vo.py` | same as overlay_vo | low |
| `assemble_v2_final.py` | `bentley/episode_builder/assemble.py` | `ffio.dur`; portable `ROOT` | low |
| `mix_v2_final.py` | `bentley/episode_builder/mix.py` | `ffio.dur`; `timeline` scheduler; `ROOT` | **medium** — see §8, unit-tested |
| `grade_v2_final.py` | `bentley/episode_builder/grade.py` | guard | low |
| `shorts_lib.py` | `bentley/episode_builder/shorts.py` | `ffio.dur` | low |
| `verify_sync.py` | `bentley/qa/verify_sync.py` | `ffio.dur`; `timeline` scheduler; `ROOT` | **medium** — unit-tested |
| `make_title.py` | `bentley/asset_generation/title_card.py` | portable path | low |
| `kie_thumb.py` | `bentley/asset_generation/thumbnail.py` | import path; `tests/`→`scratch/`; guard | low |
| `kie_thumb_text.py` | `bentley/asset_generation/thumbnail_text.py` | `tests/`→`scratch/` | low |
| `shell_gen.py` | `bentley/asset_generation/shells.py` | move | none |
| `fix_paws.py` | `scripts/fix_paws.py` | move | none |

**New modules** extracted from duplication: `shared/{ffio,paths,eleven,audio,fal}`,
`voices/dialogue`, `asset_generation/keyframes`, `animation/{video,avatar}`,
`episode_builder/timeline`.

**Data & docs:** `ep1_*.json` → `episodes/ep1/shotlists/`; root `*.md` →
`docs/{guides,decisions,episodes/ep1,rules}/`; `Bentley_Season1_MD_Files/` → `docs/series/`;
`Channel_Launch/` → `docs/launch/`. **Rename:** `tests/` → `scratch/`.

All moves used `git mv` (history preserved). **Backward compatibility:** the one public
invocation people rely on — `python pipeline.py <shotlist>` — is unchanged. Other scripts moved
to `python -m bentley.<pkg>.<module>` (see README table).

---

## 4. Cleanup plan (deprecated/)

15 frozen scripts moved to `deprecated/` (12 EP1 one-offs + 3 smoke tests) — see
[`deprecated/DEPRECATED_LOG.md`](../deprecated/DEPRECATED_LOG.md). **Nothing was deleted.** They
are kept byte-for-byte; the reusable patterns already live in the active package.
`NARRATOR_AUDITIONS/` is empty and can be removed at will (left in place to honor "delete nothing").

---

## 5. Safety / git

- Baseline commit captured the original flat layout before any change (revertible).
- Reorg done on branch `chore/repo-reorg` as reviewable commits.
- `.gitignore` excludes secrets (`.env`), `.venv`, caches, and **all binary media** (the repo is
  4.7 GB of renders — code/docs/configs only, a few MB, are tracked). `.env.example` documents
  the required keys without values.

---

## 6. Verification performed

- `py_compile` on every `.py` — all parse.
- Import-smoke: 21/21 library + guarded-script modules import cleanly (with `.env` loaded).
- `tests/test_timeline.py`: the extracted scheduler matches hand-computed placements — **passes**.
- `ffio.dur` exercised on real media.
- `pipeline.py` imports and reaches its main logic unchanged.

> Not run: the full paid media pipeline (fal/kie/ElevenLabs cost + keys). Behavior is preserved by
> **verbatim relocation** (identical ffmpeg strings, prompts, EQ chains), not logic rewrites.

---

## 7. Standards & conventions

- **Naming:** `verb_noun.py`, lowercase, no version/`_final` suffixes on active code. Frozen files
  keep their historical names.
- **Folders:** one responsibility per package. Helpers are defined **once**, in `shared/`.
- **Imports:** active code uses absolute package imports (`from bentley.shared.ffio import dur`).
  No `sys.path` hacks. Library modules are import-safe; entrypoints guard execution with
  `if __name__ == "__main__":` (work in progress — see §8).
- **Secrets & config:** API keys and **LOCKED voice IDs** live only in `bentley/shared/eleven.py`
  / `.env`. Never hardcode a voice ID or absolute path in a script.
- **Prompts:** large prompt strings should migrate to `prompts/<episode>/` as data (seeded; done
  incrementally — currently still inline in the generators).
- **Episodes:** all per-episode *data* goes under `episodes/epN/`; code stays episode-agnostic.
  Today the builders are still EP1-baked (the EDL/narration tables are inline) — generalizing them
  to read `episodes/epN/` config is the main scaling follow-up.
- **Assets:** keep the existing `assets/{approved,deprecated,work_in_progress}/` convention.
- **Docs:** the `youtube_vault` Obsidian bible is canonical for creative rules; `docs/` holds
  engineering/production docs. Avoid duplicating the vault.

---

## 8. Known follow-ups & discovered issues

1. **`verify_sync` drift (discovered):** its narration list is **missing the `PIPOS_wave1`
   entry** that `mix` has. The scheduler is now shared, but each still owns its own event *data*,
   so the drift is preserved, not fixed — `verify_sync` won't catch a `wave1` overlap. Reconcile
   the two lists (decide whether `wave1` should be checked) — left to you since it's content canon.
2. **Generalize the builders for ep2+:** lift the inline EDL / narration / SFX tables out of
   `assemble`/`mix` into `episodes/epN/` config so the builders become episode-agnostic.
3. **Prompt extraction:** move inline prompt strings into `prompts/` as data.
4. **`__main__` guards:** the data-heavy entrypoints (`assemble`, `mix`, `verify_sync`,
   `title_card`, `thumbnail_text`) still execute on import; wrap them in `main()` when convenient.
5. **Doc reconciliation:** root rules docs (now in `docs/rules/`) overlap the `youtube_vault`
   versions — pick one canonical home.
