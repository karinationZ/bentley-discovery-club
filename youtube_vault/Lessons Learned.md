---
title: Lessons Learned
tags:
  - foundation
  - lessons
  - postmortem
---

# Lessons Learned

> [!important] Read this before producing anything
> These are the mistakes Episode 1 already paid for. Re-reading this note is the cheapest QA you'll ever do.

## 🎬 Animation & rendering
> [!danger] Talking shots freeze the background (the 5× wave)
> The Kling Avatar animates **only** the mouth/face — water/waves behind it **freeze**, and no prompt fixes it. We "fixed" the frozen wave **five times** before realizing the model itself was the cause. **Fix:** put live motion in a *motion (i2v)* shot and the talking on a *dry close-up* — never both in one shot. See [[Animation Rules]].

- **Nano-Banana reads "golden dawn" as moody dusk.** Push **bright / high-key / daylight / NOT dusk** explicitly, or faces come out dark.
- **The Kling Avatar darkens its output.** Feed a **bright** keyframe and **lift in the grade**.
- **A grade can't re-light a backlit face** — it only greys the shadow. Backlit faces must be **re-rendered**, not graded.
- **Match-jump cuts.** Cutting between two near-identical close-ups of the same character looks like a glitch — vary framing/pose.
- **Title cards need `-loop 1`**, or the PNG only exists at frame 0.

## 🐶 Character consistency
- **Long tail** is the #1 recurring Bentley error — hammer "short docked tail" in every prompt.
- **Human teeth / grins** kept appearing in close-ups — bake in "natural dog mouth, small lower teeth only, no human teeth" and give the Avatar a near-closed-mouth keyframe.
- **Furry shell.** A "Pixar soft-fur style" prompt suffix bled **fur onto the shell**. Keep style suffixes off props; QA props for fur.
- **Pip drifted into "3–4 different crabs"** (eye-stalks, white nautilus, antennae). Always edit from the **master**.

## 🔌 Process
> [!warning] "Built but never wired in" — the worst bug
> We once generated all the fixes but **never integrated them** into the build — the assemble still pointed at the old clips, the new VO sat unused, and a dark master shipped. The lesson: **a fix isn't done until it's wired into the build *and re-verified on screen*.** QA the FINAL, not the parts.

- **Re-rolls are the real cost driver**, not the per-image price → **keyframe-QA-first** ([[Token Efficiency Rules]]).
- **Keyframe before clip** — approve the cheap still before the expensive motion/talking render.
- **Diagnose before you spend.** When something fails repeatedly, find the *root cause* (e.g. the model freezing backgrounds) instead of re-trying the same approach.

## 🛠️ Infra gotchas
- **fal.ai `subscribe` hangs silently on an exhausted balance** (no error thrown) — once cost ~2 hours. Wrap renders in a hard timeout; we migrated to **kie.ai**.
- **catbox.moe can transiently 422** server-side on a specific file even when others work — **re-host fresh** (new URL) and retry; fallback: regenerate the keyframe via Nano-Banana (kie-internal URL, always fetchable).
- **Kling Avatar needs a *public* audio URL** — host the VO on catbox.moe.
- **Never print or expose `.env`** — it holds the API keys.

## Resolved decisions
> [!success] Paws — resolved (owner-confirmed)
> Bentley's paws are **solid red-fawn, NO white socks**. A draft spec briefly said "white paws" — that was a slip; **Episode 1's look is canon**. Keep `fix_paws.py` / `paw_fix()` removing any white socks. See [[Bentley Master Prop]].

See also: [[Episode QA Checklist]] · [[Animation Rules]] · [[Bentley Master Prop]]
