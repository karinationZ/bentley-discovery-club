---
title: Token Efficiency Rules
tags:
  - rules
  - production
  - cost
---

# Token Efficiency Rules

> [!important] Hard rule
> **Use what we already have first.** Generation costs real money and re-rolls are the #1 budget leak. Minimize generation; maximize reuse and consistency.

## The reuse-first workflow
> [!check] Before generating anything, in order:
> 1. **Reuse approved assets** — clips, stills, SFX, music already in `assets/approved/`.
> 2. **Reuse approved props** — the Bentley & Pip masters and the clean shell ([[Bentley Master Prop]], [[Pip the Hermit Crab]]).
> 3. **Reuse approved voices** — the locked cast; never re-roll a line you already have ([[Voice Rules]]).
> 4. **Reuse approved scenes** — environment plates and b-roll where they fit.
> 5. **Only then generate new** — and only what is strictly necessary.
> 6. **Get owner approval before any significant credit spend.**

## Why this matters
> [!note] The real cost driver is re-rolls
> On Episode 1 the expense wasn't the per-image price — it was **re-generating the same shots** repeatedly. A clean **keyframe-QA-first** pass (approve the cheap still *before* the expensive motion/talking render) beats re-rolling a finished clip. See [[Lessons Learned]].

## Cost discipline in practice
- **Keyframe before clip.** A keyframe is a fraction of a motion/talking render's cost — QA it first and re-roll *it*, not the clip.
- **Batch + parallelize** renders, but **gate** them behind keyframe approval.
- **Approval gate.** Present a plan + a credit/$ estimate and get a "yes" **before** firing a batch.
- **Cheapest capable tool.** kie.ai (Kling 2.6 + Avatar + Nano-Banana) is materially cheaper than fal.ai at equal/better quality — see [[Production Workflow]].
- **Track spend** per episode and report it in the validation summary.

## Approval etiquette
- **Small fix** (≤ a couple of renders): proceed, then report.
- **Batch / restructure / new beat:** plan → estimate → **approve** → execute → QA → report.

See also: [[Production Workflow]] · [[Lessons Learned]]
