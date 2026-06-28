# Bentley's Big Adventures — production repo

Kids' YouTube animation franchise (channel: *Bentley's Big Adventures*), built on a
fal / kie.ai / ElevenLabs / ffmpeg pipeline. This repo holds the **code, configs, and docs**.
The rendered media (~4.7 GB) lives on disk but is **git-ignored** on purpose (see `.gitignore`).

> Private repo — do not push to a public remote. Secrets live in `.env` (git-ignored); see `.env.example`.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # if not already set up
cp .env.example .env                                # then fill in your real API keys
pip install -e .                                    # exposes `import bentley.*` everywhere
python tests/test_timeline.py                       # sanity check (no API calls)
```

## Layout

```
pipeline.py            # thin orchestrator entrypoint:  python pipeline.py <shotlist.json>
bentley/               # the importable package — all reusable production code
  shared/              #   ffio, paths, eleven (voice IDs+key), audio, fal, kie_client
  asset_generation/    #   keyframes, thumbnail(+_text), title_card, shells
  animation/           #   video (Kling i2v), avatar (lip-sync)
  voices/              #   dialogue, narration, music, sfx
  episode_builder/     #   assemble, mix, grade, overlay_vo, supp_vo, shorts, timeline
  qa/                  #   verify_sync
scripts/               # runnable utilities (fix_paws.py)
prompts/               # prompt library as data, per episode (convention — see docs)
episodes/ep1/          # per-episode DATA: shotlists/ (the *.json fed to pipeline.py)
assets/                # all media (git-ignored): approved/ deprecated/ work_in_progress/ ...
docs/                  # guides/ decisions/ episodes/ rules/ series/ launch/ + REPO_ARCHITECTURE.md
youtube_vault/         # canonical Obsidian production bible (characters, rules, lessons)
scratch/               # generated media from smoke tests / experiments (was tests/)
tests/                 # real unit tests (import-safe, no API calls)
deprecated/            # frozen one-off / superseded scripts — kept for history, never deleted
```

Full audit, migration map, and conventions: **[docs/REPO_ARCHITECTURE.md](docs/REPO_ARCHITECTURE.md)**.

## Running the pipeline

| Task | Command |
|------|---------|
| Produce shots from a shotlist | `python pipeline.py episodes/ep1/shotlists/ep1_v2keys.json` |
| Narration (Bill) / music / SFX | `python -m bentley.voices.narration` · `.music` · `.sfx` |
| Overlay & supplemental VO | `python -m bentley.episode_builder.overlay_vo` · `.supp_vo` |
| Assemble picture | `python -m bentley.episode_builder.assemble` |
| Sound mix | `python -m bentley.episode_builder.mix` |
| Color grade (final) | `python -m bentley.episode_builder.grade` |
| Verify zero voice overlaps | `python -m bentley.qa.verify_sync` |
| Build 9:16 Shorts | `python -m bentley.episode_builder.shorts` |
| Title card / thumbnail | `python -m bentley.asset_generation.title_card` · `.thumbnail` · `.thumbnail_text` |
| Fix paws on a keyframe | `python scripts/fix_paws.py <img.png>` |

All commands run from the repo root. Library modules under `bentley/{shared,voices/dialogue,
animation,...}` are import-safe; the builder/generator modules above are entrypoints (run them).
