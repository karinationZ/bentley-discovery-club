---
title: Production Workflow
tags:
  - production
  - pipeline
  - tools
---

# Production Workflow

> [!abstract]
> The end-to-end pipeline for an episode: **tools → folders → asset/voice/episode pipelines → QA**. Reuse-first throughout ([[Token Efficiency Rules]]).

## Tools & infrastructure
| Layer | Tool | Use |
|---|---|---|
| **Images** | kie.ai **Google Nano-Banana** (`google/nano-banana`, `…-edit`) | keyframes, edit-from-master |
| **Motion video** | kie.ai **Kling 2.6** (`kling-2.6/image-to-video`) | living motion shots (water, action) |
| **Talking video** | **[[Lip-Sync Rig System]]** (local, 0 cr) — Kling Avatar only for the catchphrase CU | lip-synced dialogue shots |
| **Voice / SFX / music** | **ElevenLabs** `eleven_v3` + text-to-SFX + music | VO, sound design |
| **Edit / mix / grade** | **ffmpeg** | assemble, mix, grade, finish |
| **Audio hosting** | **catbox.moe** | public URLs for the Kling Avatar's audio input |

> [!note] Why kie.ai
> Same models as fal.ai (Kling, Nano-Banana, Kling Avatar) at **~⅓ less cost** and a newer Kling (2.6 vs 2.5). Task-based API: `createTask` → poll `recordInfo`, wrapped in `kie_client.py`. (fal.ai's account is exhausted; kie is the active provider.)

## Folder structure (`assets/`)
```
assets/
├── approved/           # canonical source-of-truth — reuse these FIRST
│   ├── bentley/ crab/ shells/ voices/ scenes/ episodes/
├── work_in_progress/   # in-flight assets for the current episode
└── deprecated/         # REJECTED — kept, never deleted (see DEPRECATED_LOG.md)
    ├── bentley/ crab/ shells/ voices/ scenes/
```
Repo guides for in-codebase agents: `docs/guides/ASSET_GUIDE.md`, `docs/rules/MASTER_PROP_RULES.md`, `docs/rules/QA_CHECKLIST.md`; production rules = the `episode-production` skill (+ its `references/PRODUCTION_PLAYBOOK.md`).

## Asset pipeline (per shot)
1. **Keyframe** — `nano-banana-edit` from the approved master → still.
2. **Keyframe QA** — check against [[Bentley Master Prop]] / [[Pip the Hermit Crab]] **before** spending on the clip.
3. **Render** — *motion* (Kling 2.6 i2v) **or** *talking* (Kling Avatar). Never put live water in a talking shot ([[Animation Rules]]).
4. **Stage** the download into `work_in_progress/`.

## Voice pipeline
1. Write the line with `eleven_v3` audio tags.
2. Generate with the locked voice helper (`tts_bentley` / `tts_pip` / narrator) in `pipeline.py`.
3. Auto-clean/master (EQ + loudnorm); keep `_raw` only as archive.
4. For a talking shot, host the mp3 on **catbox.moe** and feed its URL to the Kling Avatar. See [[Voice Rules]].

## Episode pipeline (scripts, in order)
| Stage | Script | Output |
|---|---|---|
| Generate shots | `pipeline.py` / `kie_*.py` | clips + VO |
| **Assemble** | `assemble_v2_final.py` | picture + `timeline.json` (dialogue embedded) |
| **Mix** | `mix_v2_final.py` | premix — narration / SFX / music layered, zero-overlap |
| **Grade** | `grade_v2_final.py` | graded 1080p FINAL |
| **Verify** | `verify_sync.py` | proves **0 voice overlaps** |

## QA process
After the FINAL renders, run the full [[Episode QA Checklist]] — Audio · Voice · Story · Animation · Character · Fact. Nothing publishes until every gate passes and `verify_sync.py` is clean.

See also: [[Token Efficiency Rules]] · [[Lessons Learned]] · [[Episode QA Checklist]]
