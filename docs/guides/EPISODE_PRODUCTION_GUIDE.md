# EPISODE_PRODUCTION_GUIDE — How an episode is made

> ⛔ **MANDATORY:** load the **Episode Production Skill** first — `.claude/skills/episode-production/SKILL.md`
> (canonical doc: `EPISODE_PRODUCTION_SKILL.md`). It governs the **Kling 3.0 cost gate**, canon, transitions,
> voice, asset reuse, and QA, and is the single source of truth for Ep3+.

End-to-end pipeline for *Bentley's Big Adventures*, the tools behind each stage,
and the hard-won lessons. Run everything with the project venv: `.venv/bin/python …`.

---

## The stack

| Tool | Used for | Notes |
|------|----------|-------|
| **kie.ai** | Images (Google **Nano-Banana** + edit / KIE image edit), video (**Kling 3.0** image-to-video), talking (**Kling Avatar** only when it passes teeth/smile QA) | Cheaper than fal.ai; the current primary. Client: `kie_client.py`. Kling 2.6 is retired for forward production. |
| **ElevenLabs** | Voices, SFX, music | `eleven_v3`. Voice IDs live in `pipeline.py` — refer to voices by **name** only. |
| **ffmpeg** | Assemble, mix, grade, normalize | All cutting/mixing/grading is ffmpeg. |
| **catbox.moe** | Public audio hosting | **Kling Avatar needs a PUBLIC audio URL** — host the voice line on catbox.moe and pass that URL to the avatar job. |

**Voices (LOCKED):** Bentley = **"Laura Z"** · Pip = **"Callum" pitched +10%** ·
Narrator = **"Bill"**. Cleaned samples in `assets/approved/voices/`.

---

## Pipeline stages (and the script that runs each)

1. **Keyframe** — generate the shot's still with Nano-Banana, **edited from the
   approved master** (`REFS["bentley"]` / `REFS["pip"]`) so identity stays consistent.
   → `pipeline.py` (`keyframe()`), batched via `kie_batch_keys.py` / `kie_fix_keys.py`.
   Full-body Bentley stills get a `paw_fix()` pass (see white-paws note in `MASTER_PROP_RULES.md`).

2. **Motion vs. Talk** — each shot is one of two types:
   - **motion** (image-to-video, Kling 3.0): living water, waves, camera moves, body motion.
     → `pipeline.py` (`video()`), `kie_fix_videos.py`.
   - **talk** (Kling Avatar lip-sync): a character delivering a line; only the mouth/face animates. For Bentley/Indi, prefer `vo_over` unless the full clip proves no human teeth or human-style smile.
     → `pipeline.py` (`avatar()`), `kie_batch_avatars.py`, `kie_avatar_run.py`.

3. **Voice** — TTS the line in ElevenLabs, then clean it (ffmpeg chain in `pipeline.py`:
   `tts_bentley()`, `tts_pip()`; narrator via `narration_bill.py` / `narration_short.py`).
   Pip is pitched **+10%**. Raw export is `…_raw.mp3` (deprecated); the cleaned sibling is the keeper.

4. **SFX & music** — `sfx_gen.py`, `music_gen.py` (ElevenLabs) → `v2/sfx/`, `v2/music/`.

5. **Assemble (picture)** — concat all shots into the picture cut with embedded
   lip-synced dialogue. → **`assemble_v2_final.py`** → `EP1_v2_picture.mp4` + `timeline2.json`.
   (Talk shots keep their OWN embedded Kling audio, trimmed to mouth length, so
   mouth == voice by construction.)

6. **Verify sync** — prove ZERO voice overlaps **before** rendering the mix.
   → **`verify_sync.py`** (same scheduler as the mixer; checks every dialogue/narration/cry pair).

7. **Mix** — layer narration / cry / SFX / music / ambient over the picture's
   embedded dialogue; narration is dynamically capped (from `timeline2.json`) so no
   two voices overlap. → **`mix_v2_final.py`** → `EP1_v2_premix.mp4`.

8. **Grade & deliver** — committed, versioned final grade (lift shadows/mids, vibrant,
   warm balance). → **`grade_v2_final.py`** → `Bentley_Ep1_v2_FINAL_1080p.mp4` (the deliverable).

9. **Thumbnail** — `kie_thumb.py` / `kie_thumb_text.py`.

Other helpers: `kie_client.py` (kie API: createTask + poll), `assemble_v2.py` /
`assemble_acts123.py` (earlier assembly variants — still referenced, keep live).

---

## ⚠️ KEY LESSON — Avatar shots FREEZE the background

A **Kling Avatar (talking) shot animates only the mouth/face — the background is
frozen.** So for any shot that needs **live water, waves, or motion behind the
character**, use a **MOTION (image-to-video) shot, NEVER a talking shot.**

This cost **5 failed "frozen wave" attempts** before the fix: the talking shot
`a3_02_pip_flip` (Pip on a static, dead wave) was split into a **motion** wave shot
(`a3_02a_wave_NEW.mp4`, live water) **plus** a separate Pip close-up
(`a3_02b_pipcu_NEW.mp4`). If a beat needs both a line AND live motion, **split it**:
motion shot for the environment, talk shot for the line.

---

## 💰 TOKEN RULE — reuse first

1. **Reuse** approved assets / props / voices / scenes from `assets/approved/`
   **before** generating anything new.
2. Only generate new when the needed asset genuinely doesn't exist.
3. **Get owner approval before any significant credit spend.**

Image keyframes are cheap; video and avatar renders are not. Resume, don't restart —
`pipeline.py` skips any shot whose `.mp4` already exists.
