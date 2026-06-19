---
title: Animation Rules
tags:
  - rules
  - animation
  - motion
---

# Animation Rules

> [!important] Everything is alive
> The world must **breathe**. A static frame reads as cheap and breaks the spell. Every outdoor shot needs continuous environmental motion.

## Environmental motion — required
> [!danger] Never static
> In every outdoor scene, these must **always** be moving:
> - 🌊 **Ocean / water** — must move; **waves must crash and churn naturally**, foam surging and receding
> - 🌿 **Trees & grass** — sway
> - ☁️ **Clouds & sky** — drift
> - 💧 **Tide-pool water** — ripple
>
> A frozen wave or glassy-still water is an automatic **QA fail**.

## The frozen-background law
> [!warning] Talking shots FREEZE the background
> The **Kling Avatar** (lip-sync) model animates **only** the mouth/face — it freezes water, waves, and everything behind the character, **no matter the prompt**. This cost **5 failed attempts** to "fix" a frozen wave.
>
> **The fix is structural, not a prompt** — when live motion is needed behind a speaking character, **split the beat**:
> 1. a **motion (i2v) shot** for the live water/action, with the voice laid over it in the mix, **and**
> 2. a separate **dry talking close-up** (Avatar) on a plain background where nothing needs to move.
>
> Never expect a talking shot to have a moving background.

## Character motion standards
- **Native speed only** — no slow-motion as a substitute for animation (only the 2 title cards get a gentle 1.2×).
- Motion must be **purposeful**: a sniff that leads to a head-lift, a recoil that sells fear — not idle drift.
- Hold the character **on-model through the whole clip** — check mid-frames, not just frame 0. See [[Bentley Master Prop]].

## Lip-sync standards
- Talking shots use the **Kling Avatar** driven by the character's locked VO → mouth matches voice by construction.
- The Avatar keyframe should have a **clean, near-closed mouth (no teeth)** so the lip-sync opens it naturally.
- The Avatar **darkens** its output → use a **bright keyframe** and lift in the grade.

## Scene-transition standards
- Prefer **hard cuts** on the action/dialogue rhythm; keep a **continuous ambient + music bed** across seams so cuts don't feel "stitched."
- Don't cut between two **near-identical** shots of the same character (reads as a glitch) — vary the framing/pose. *(Ep 1's `a1_06 → N1` jump was fixed by re-framing N1 the other way.)*
- Don't **re-anchor** (restart) the same music cue at a cut inside a continuous beat — let it ride.

## Grade — one world
- One **consistent grade** across the whole episode (`grade_v2_final.py`): an S-curve lifting shadows/midtones without washing highlights, plus vibrant saturation and a warm balance.
- A grade can lift a **front-lit** face; it **cannot** re-light a **backlit** one — fix those at the **render** stage, not in the grade.

See also: [[Lessons Learned]] · [[Production Workflow]] · [[Episode QA Checklist]]
