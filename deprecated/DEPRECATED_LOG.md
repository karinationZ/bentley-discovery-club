# Deprecated code log

Frozen scripts kept for history and reference. **Nothing here is deleted.** These were
one-off, episode-1-specific, or superseded scripts that already did their job. They are kept
**byte-for-byte as they were** at the time of the 2026-06-19 reorganization.

> ⚠️ These were written against the old flat layout (`from kie_client import ...`,
> relative `tests/...` paths). They are **not maintained** against the new `bentley/` package.
> To actually re-run one, you'd adjust its imports to `from bentley.shared.kie_client import ...`
> and its paths (`tests/` → `scratch/`). In practice none of these need to run again.

## `episode1_scripts/` — one-off / superseded EP1 builders

| File | Why frozen |
|------|-----------|
| `assemble_acts123.py` | superseded by `bentley/episode_builder/assemble.py` (v2 final) |
| `assemble_v2.py` | superseded by `assemble.py` (v2 final) |
| `kie_batch_keys.py` | EP1 Tier-1 batch — keyframes (done) |
| `kie_batch_avatars.py` | EP1 Tier-1 batch — talking avatars (done) |
| `kie_fix_keys.py` | EP1 round-2 fix — keyframes (done) |
| `kie_fix_videos.py` | EP1 round-2 fix — videos (done) |
| `kie_fix_octopus.py` | EP1 one-off — robust octopus render (done) |
| `kie_avatar_run.py` | EP1 one-off — avatar from hosted URLs (proof) |
| `kie_talk_n6.py` | EP1 one-off — prove the kie talking path (proof) |
| `narrator_audition.py` | casting — narrator candidates (Bill won; voices LOCKED) |
| `pip_audition.py` | casting — Pip candidates (Callum won; voices LOCKED) |
| `narration_short.py` | EP1 one-off — shorter narration re-records (done) |

## `smoke_tests/` — kie.ai vs fal experiments

| File | Why frozen |
|------|-----------|
| `test_kie_n6.py` | kie vs fal keyframe cost/quality test (done) |
| `test_kie_n6_bright.py` | bright N6 keyframe variant test (done) |
| `test_kie_video.py` | kie Kling 2.6 i2v cost test (done) |

## Reusable logic that was salvaged

The reusable *patterns* from these scripts already live in the active package: the kie client
(`bentley/shared/kie_client.py`), catbox hosting / TTS / clean-master helpers, and the batch
structure. The frozen copies retain their own inlined helpers — that duplication is harmless
because the files are frozen.

## `docs_guides/` — superseded production docs (moved 2026-07-03)

Superseded by the single normative chain established after the EP3 post-mortem:
**10 Mandatory Rules** (vault) → **`.claude/skills/episode-production/SKILL.md`** →
**`references/PRODUCTION_PLAYBOOK.md`** (inside the skill). Unique content was absorbed into the
playbook before the move (avatar freezes-background/darkens/text-hallucination gotchas; the
full-duration worst-frame-fails QA principle).

| File | Why frozen |
|------|-----------|
| `EPISODE_PRODUCTION_GUIDE.md` | EP1-era how-to; references pre-reorg flat scripts (`assemble_v2_final.py`, `grade_v2_final.py`, …) that no longer exist at those paths |
| `EPISODE_PRODUCTION_SKILL.md` | was a "must-stay-identical" human mirror of the skill; drifted stale (frozen 2026-06-27, missing §0/§0.0/playbook) — a stale mirror misleads |
| `PRODUCTION_PIPELINE.md` | the 9-stage gated flow — superseded by playbook Parts 2–3 + the skill §10; its unique gotchas absorbed into the playbook |
