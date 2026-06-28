# Production Pipeline — the one flow every episode follows

> ⛔ **MANDATORY FIRST STEP (Ep3+):** load the **Episode Production Skill** before any generation or
> edit — `.claude/skills/episode-production/SKILL.md` (canonical doc: `EPISODE_PRODUCTION_SKILL.md`).
> It is the single source of truth for the **Kling 3.0 cost gate** (premium animation only for hero /
> character-interaction shots), Bentley/prop canon, transition/voice/animation rules, asset reuse, and
> the pre-delivery QA checklist. Script first with `cinematic-episode-writer`; produce under these rules.

**Status:** authoritative. Ep1 shipped on this flow. Ep2 regressed because it **skipped stages 1 and 5–9**
(no shotlist, no assemble/mix/grade — only a talking-head reel). We are re-running Ep2 *on this flow* to
prove it restores Ep1 quality; once proven, **every episode follows it in order, with no stage skipped.**

> **Iron rule:** you do not advance to the next stage until the current stage's GATE passes.
> **Iron rule:** QA the **FINAL**, never the parts. A folder of clips — or a concat reel — is **not** an episode.
> **Iron rule:** work in the episode layout (`episodes/<ep>/`, `assets/pilot_shots/<ep>/`), **never loose in `scratch/`** — the assembler reads those paths.
> **Model rule:** use **Kling 3.0 i2v** for new motion. Kling 2.6 is retired for forward production unless an owner-approved regression test proves it is required for a specific shot.

---

## The flow

| # | Stage | Tool / code | GATE (must pass to advance) |
|---|-------|-------------|------------------------------|
| 0 | **Script** | `docs/series/.../EPISODEn_SCRIPT.md` (play format) | Owner approves the read-through script. |
| 1 | **Shotlist** (storyboard) | `episodes/<ep>/shotlists/*.json` (schema below) | Every script beat is a shot; motion + talk + **establishing + B-roll + reaction** interleaved; ≥1 non-plot bonding two-shot; owner approves the shot plan. |
| 2 | **Keyframes** | Nano-Banana **edited FROM the approved master** (`bentley.character_framework.derive_keyframe`) | Each keyframe QA'd full-frame vs the master (on-model; MUST-HAVE/MUST-NEVER). Cheap stills approved **before** any motion. |
| 3 | **Shots** (motion / talk) | **Kling 3.0 i2v** + tightly limited Kling-Avatar via the shotlist (`pipeline.py <shotlist>`, resumable); talking prompts from `bentley.character_framework` | **Every clip QA'd full-duration** (≥1 frame/sec, **worst-frame fails**, weight emotional peaks). On-model + anatomy-clean or it's re-done FROM the master. |
| 4 | **Voice / SFX / music** | `bentley.voices` (ElevenLabs) — locked voices; catchphrase paced; kid-appropriate tone | All lines recorded; catchphrase = Bentley, paced. (Runs parallel to 2–3.) |
| 5 | **Assemble** | clone `bentley/episode_builder/assemble.py` → ordered EDL → `timeline.json` | One end-to-end **picture cut** exists; motion at native speed; talk trimmed to mouth length; **no match-jump** cuts; VO-over-action composited (reaction/exclamation lines). |
| 6 | **Sync verify** | `bentley/episode_builder/timeline.py` + `bentley/qa/verify_sync.py` | One-voice-at-a-time; mouth == voice; no overlap. |
| 7 | **Mix** | `bentley/episode_builder/mix.py` | **Continuous ambient + music bed across every seam** (no re-anchor mid-beat); narration sequenced; SFX in. |
| 8 | **Grade** | `bentley/episode_builder/grade.py` | One consistent grade over the whole episode; avatar darkening lifted. |
| 9 | **QA the FINAL** | watch the master end-to-end + `docs/rules/QA_CHECKLIST.md` | Owner approves the **finished episode** (story flow + tone curve + character + sync), not the parts. |

> **Ordering override — the Animatic Lock gate (Ep3+).** Before any Stage-3 Kling spend, the **VO reel
> (Stage 4) must be COMPLETE**, then a **timed Animatic / Story Lock** — the whole episode on the EDL
> from reuse clips / stills / labeled cards + the recorded VO, at **zero** Kling/KIE/ElevenLabs credits
> — must pass owner sign-off. So for episodes under the gate the order is **VO → Animatic → Kling** (VO
> is no longer parallel to Stage 3). Sync-verify (6) and Grade (8) are unchanged. Full rule + checklist:
> `.claude/skills/episode-production/SKILL.md` §10 step 4 and §9 "Animatic Lock". *(Tool — built
> 2026-06-27: `bentley/episode_builder/animatic.py`; run
> `PYTHONPATH=. python -m bentley.episode_builder.animatic episodes/<ep>/shotlists/<list>.json`;
> proven zero-credit on EP2.)*

## Shotlist schema (`episodes/<ep>/shotlists/*.json`)
```jsonc
{ "work": "assets/pilot_shots/<ep>/<act>",
  "shots": [
    { "id": "a1_03_chase", "type": "motion", "dur": "5",
      "keyframe": "<NB prompt, edited from master>", "motion": "<i2v motion>",
      "ref": "bentley", "src": "scratch/ep2/motion/s..._motion.mp4", "status": "ready|redo|todo" },
    { "id": "a3_16_why", "type": "talk", "voice": "bentley", "ref": "bentley",
      "line": "Why do you keep hiding?", "emotion": "tender",
      "src": "scratch/ep2/talking/talk_B_why.mp4", "status": "ready" },
    { "id": "a4_19_breathe", "type": "vo_over", "vo": "scratch/ep2/vo/B_breathe.mp3",
      "over": "<motion shot id>", "note": "exclamation/reaction → VO over action, not a talking CU" }
  ] }
```
`type`: `motion` (Kling 3.0 i2v) · `talk` (Kling-Avatar, mouth==voice, only after teeth/smile QA) · `vo_over` (VO laid over a motion/established shot) · `card` (title/tease) · `ffx` (Ken-Burns/glow plate). `status`: `ready` (clip exists + passed QA) · `redo` (exists, failed QA) · `todo` (not built).

## Why this exists — failures this flow prevents (don't repeat)
- **"Built but never wired in."** Ep2 generated good clips but never built a shotlist or assembled them → no story order, orphaned setup shots (e.g. the color-change that sets up *"You did ME!"* existed but was never cut in). → Stages 1 + 5.
- **QA'd the parts, not the whole.** A talking-head reel got mistaken for the episode. → Stage 9.
- **Frame-0 QA.** Bentley's human-smile drift appeared mid-clip (clean at 0s) and slipped. → Stage 3 full-duration QA.
- **Off-model from drifted CUs.** A non-master close-up produced an off-model Bentley. → Stage 2 always-from-master.
- **Working loose in `scratch/`.** The assembler can't find inputs. → episode layout.
- **Avatar gotchas:** it **darkens** (grade lifts) and **freezes** backgrounds (split the beat: i2v motion + VO over it, plus a dry talking CU); it hallucinates **text** on short exclamations (→ those are `vo_over`, not talking CUs).

Character/anatomy/lip-sync/transition rules are codified in **`bentley/character_framework/`** (see its README) and the vault (`youtube_vault/Rules/`, `Lessons Learned.md`).
