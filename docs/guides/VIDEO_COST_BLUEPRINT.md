---
title: Video Cost Blueprint — PROJECT-WIDE LAW
status: MANDATORY — always follow
source: ChatGPT cost analysis (owner-approved 2026-06-26); KIE pricing endpoint POST https://api.kie.ai/client/v1/model-pricing/page (pulled 2026-06-26)
applies_to: ALL video generation in this project (episodes, shorts, tests, everything)
---

# Video Cost Blueprint (PROJECT LAW)

> **THE CORE RULE: never use premium video models for open-ended exploration. Use them only after the
> prompt, shot, duration, aspect ratio, reference frames, and success criteria are LOCKED.**

KIE bills video by credits and video is the expensive class (KIE docs: ~100–500 credits/generation).
This blueprint is the standing law for every video generation decision in the project. The
`episode-production` skill enforces it; this doc is the canonical reference.

## Pricing signals (KIE, 2026-06-26 — re-check periodically)
| Tier | Good candidates | Cost signal | Use for |
|---|---|---|---|
| **Ultra-cheap scouting** | Runway 720p, Grok Imagine 480/720, Hailuo 02, Seedance 1.5 Pro 480/720 | `$0.008–0.035/s` or `$0.06–0.25/video` | prompt testing, camera tests, rough motion |
| **Cheap Kling scouting** | Kling 2.1 Std, Kling 2.5 Turbo | `$0.125–0.42/video` | Kling-style motion without 3.0 spend |
| **Mid production** | Kling 2.6, **Kling 3.0 no-audio 720/1080**, Hailuo 2.3, Seedance 1.5 Pro 1080 | `$0.0375–0.09/s` or `$0.275–0.55/video` | clean cuts, locked ideas |
| **Premium** | Kling 3.0 + audio/4K, Kling 3.0 Motion Control, Seedance 2.0 Std, Veo 3.1 Quality | Kling 3.0 audio 1080 `$0.135/s`; 4K `$0.335/s`; Seedance 2 up to `$1.04/s` | hero shots, final renders, complex continuity |

**Critical nuance: Kling 3.0 is NOT always expensive.** Kling 3.0 **720p, no audio ≈ `$0.07/s`** (~$0.35 / 5s).
What gets expensive: rerolling before the direction is locked, using audio, going 4K, Motion Control.

## Use Kling 3.0 (full/premium) ONLY when
- Final or near-final output, not exploration.
- Multi-shot continuity / cinematic transitions / character continuity.
- Product/logo/text legibility cheaper models distort.
- Human dialogue needing native audio/multilingual.
- Brand/client-facing where one good render beats five mediocre retries.
- Start/end-frame control after references are approved.
- Motion Control only when a reference performance must be preserved.

## NEVER use Kling 3.0 (premium) for
- First-pass prompt exploration.
- Bulk variants where 80–90% are thrown away.
- Background loops, B-roll, mood tests, thumbnails.
- Anything where audio isn't final.
- 4K before 720/1080 is approved.
- **Fixing bad prompting. Rewrite and test CHEAPLY first.**

## The workflow (ordered — do not skip)
1. **Plan without video spend** — script, shot list, aspect ratio, duration, references, negative prompts.
2. **Stills/storyboards first** — lock composition + character/product look before any motion. (Stills are cheap/free.)
3. **Scout cheaply** — 2–4 variants on Seedance 1.5 Pro / Runway / Hailuo / Grok / Kling 2.5 / Kling 2.6.
4. **Mid-tier validation** — once direction works, test **Kling 3.0 no-audio 720/1080** or Seedance/Hailuo.
5. **Premium render gate** — escalate ONLY if the cheap/mid pass proved the shot and the remaining limit is *quality, not prompt ambiguity*.
6. **Final only** — add audio, 1080/4K, Motion Control, premium rerenders AFTER approval.
7. **Post-process** — upscale/edit/color/mix. Don't reroll premium for small fixes post can solve.

## Routing rules
- **Seedance 1.5 Pro** — audio-video sync on a tight budget (cinematic, sync audio, multilingual, first/last frame).
- **Seedance 2 Fast** — scalable iteration (faster/cheaper, core Seedance 2 capability).
- **Seedance 2 Standard** — complex motion, multi-shot, production control.
- **Hailuo 2.3** — expressive human motion/face; Hailuo Fast/Standard for cheap volume.
- **Kling 3.0 Turbo** — Kling-3.0-series quality with better speed/cost for repeated production.
- **Kling 3.0 full / Motion Control** — only locked, high-value shots (continuity, audio, brand, 4K, reference motion).
- *(Project caveat, from prior tests: cheap models DRIFT recognizable characters — fine for SCOUTING a prompt/motion direction, but the FINAL character shot still renders on Kling 3.0. Scout cheap, finalize on Kling 3.0.)*

## Quality gate (all must pass before ANY premium spend)
- [ ] Prompt has passed on a cheap model.
- [ ] Reference image/start frame approved.
- [ ] Duration + aspect ratio final.
- [ ] Audio need known.
- [ ] Shot value is high (hero/key narrative/client deliverable).
- [ ] Failure reason is model quality, **not** unclear direction.

## The policy
**≥80% of generations cheap or mid-tier; ≤20% premium finalization.** Log credits per episode; if premium
share climbs, challenge each premium shot against this blueprint.
