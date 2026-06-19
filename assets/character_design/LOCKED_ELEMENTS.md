# Bentley's Discovery Club — LOCKED CHARACTER DESIGN (source of truth)

> Locked 2026-06-15. This is the canonical look for the entire series. Every shot + video must inherit it.

## 🎨 Art direction (LOCKED)
**Premium dimensional cartoon — "stylized realism."** Pixar/Bluey-grade appeal with soft tactile fur warmth, soulful curious eyes, and believable Boxer anatomy. **NOT** flat 2D, **NOT** plastic/rubber toy, **NOT** photoreal. Likeness is distilled from the real dog, not discarded.

## 🐶 Bentley — locked features
Young female Boxer based on the real dog Bentley:
- Rich **red-fawn** coat
- Strong **black mask** with a subtle **dark brindle** hint on the forehead
- **Grey-white frosting** on the chin / lower muzzle
- Gentle **brow wrinkles**, **soulful** dark-brown eyes (appealing, not googly)
- Natural **floppy ears** (both folded), small **white chest blaze**, wet little black nose
- **White is ONLY on the chest blaze.** Her legs and **all four paws are solid red-fawn — NO white socks, NO white feet/toes.** (The AI keeps hallucinating Boxer "socks"; every shot prompt must explicitly forbid them.)
- **EARS (locked):** both ears are **ALWAYS soft, floppy, and folded DOWN** — even when alert / curious / excited. **NEVER prompt "ears up / pricked / erect / snapping upright / alert ears"** (real recurring bug — it makes a pointed-ear dog that's off-model). Image-to-video & talking-avatar models faithfully reproduce whatever ears the **keyframe** shows, so the keyframe itself must already have floppy folded ears.
- **TAIL (locked):** **SHORT, docked, stubby Boxer tail — NEVER a long tail** (matches the real Bentley). Every keyframe + edit must show the short docked tail; reject any long-tail render. (The video/avatar models inherit the keyframe's tail, so the source image must be correct.)
- **⛔ MOUTH / TEETH — HARD RULE (locked):** when her mouth opens (talking, gasping, wonder) she has a **natural dog mouth — soft pink tongue + small natural dog teeth**. **NEVER a row of uniform white HUMAN teeth, NEVER a human grin, NEVER human-like front teeth.** This is the #1 recurring failure on wide-open talking close-ups (WHOAA + tag both hit it). Bake into EVERY talking-shot keyframe prompt: *"natural dog mouth, soft pink tongue, small dog teeth, NO human teeth, NO human grin."* **Check every talking close-up frame and REJECT + regenerate anything with human teeth.** Avoid holding the mouth wide-open; favor partial opens + tongue.
- **TALKING-SHOT TIMING:** talking-avatar clips often render **longer than the speech** (e.g., a 5.5s line → a 7s clip = silent mouth-flap at the end). Always **trim the avatar clip to ~speech length + ~0.2s** so the mouth doesn't move after the line ends. Also, when assembling, **pin each line's audio to its shot's exact frame position** (avatar audio is often shorter than its video, which causes cumulative A/V drift if you concat audio+video together).
- **Proportions:** NEVER prompt "big eyes" — it balloons them googly/cross-eyed. Say *"soulful, well-proportioned eyes, balanced head-to-body, correct short muzzle, athletic build, match the master — NOT oversized, NOT googly."* Multi-character shots drift the most; always pull 2–3 takes and reject any off-model proportions.
- Friendly athletic Boxer build, slightly rounded/cute
- **Costume:** teal collar + softly glowing **spiral seashell** charm (the "Listening Shell") — her only accessory
- **She is FEMALE** — always render a smooth, neutral, featureless underside with **NO genitalia** (standard for a wholesome kids' cartoon). State this in any prompt with a rear/underside angle.

## 🔑 Higgsfield Elements (use in every generation)
| Element | ID | Use |
|---|---|---|
| **Bentley-MASTER** ✅ THE LOCKED CANONICAL | `1c82ee5b-8713-4596-80ec-6ce854502a4d` | **The one true Bentley — use for ALL shots + video.** 3D dimensional animated Boxer **with soft fur**, clean face (no white on forehead/nose), both floppy ears. Embed `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>` + restate her features + "same dog, match the model sheet exactly." Model sheet: `Bentley_MODEL_SHEET_turnaround.png` + `Bentley_MODEL_SHEET_expressions.png`. |
| ~~Bentley-v3-LOCKED~~ (superseded) | `779b0db5-96bd-42aa-b3e0-ed9029dc77a6` | Realistic head-tilt — superseded by Bentley-MASTER. |
| ~~Bentley-v2-sniff~~ (superseded) | `cfa3f9cb-6ce6-4ca6-be7b-ce3117efb385` | Earlier re-anchor — superseded by v3. |
| ~~Bentley-hero~~ (SUPERSEDED) | `b6adcf93-5849-44fc-b686-74455b2ea54b` | Older look — drifted across expressions. Do NOT use going forward. |
| Bentley-real (photo identity) | `b35dd3ab-b66d-4a6d-98b4-a9d09f9cd7b4` | Source identity from real photos. Use only to regenerate the hero look, not for shots. |
| **Stella** (mentor, sea star) | `e9016448-5da5-4309-92e6-a3bf3bb78bac` | Embed `<<<e9016448-5da5-4309-92e6-a3bf3bb78bac>>>`. |
| **Pip-clean** ✅ (guest, hermit crab) | `752fec82-e78e-4289-8257-07176fcb82e0` | Embed `<<<752fec82-e78e-4289-8257-07176fcb82e0>>>`. Grumpy-but-soft, big eyes, dull cracked brown spiral shell, **clean face — NO whiskers, NO antennae**. THE Pip for all shots. |
| ~~Pip~~ (superseded — had cat-whiskers) | `d74e14ad-ac10-47a2-8561-856901f6f82b` | Old whiskered Pip. Do NOT use. |
| **Tidepool-cove** (environment) | `d406065e-7b28-4b52-aa02-1e3290032dc1` | Embed `<<<d406065e-7b28-4b52-aa02-1e3290032dc1>>>`. Multiple element placeholders per prompt are supported. |

## 🏭 Winning recipe
- **Model:** `nano_banana_2` → resolves to **Nano Banana 2** (`nano_banana_flash`), ~2.5 cr/image on PLUS (cheap).
- **Approach:** "realism dialed down to stylized cartoon" beat "cartoon pushed up to warmth." Keep her soul; simplify forms; soft fur hint.
- **Video model (LOCKED):** **Minimax Hailuo 2.3** (`minimax_hailuo`) — ~6 cr/6s, big soulful eyes, best for character emotion. **NOT** Seedance 2.0 (17.5 cr, 3× the cost). Veo 3.1 Lite (`veo3_1_lite`) is the backup for wide/cinematic shots. Always negate white socks in the motion prompt. (Cost details in memory: higgsfield-video-cost-optimization.)
- **Aspect:** 3:4 for hero/portrait; 16:9 for scene shots; 9:16 for Shorts.

## 🗂️ Locked image files (this folder)
- `Bentley_HERO_LOCKED.jpg` — the master hero (candidate A). The face of the series.
- `Bentley_closeup_expression.jpg` — bigger-eyed close-up (candidate B). Use for **emotional beats + thumbnails**.
- `Bentley_turnaround.*` — 4-angle model sheet (pending).

## ✅ Standard generation snippet
```
model: nano_banana_2
prompt: "<<<b6adcf93-5849-44fc-b686-74455b2ea54b>>> — [SHOT DESCRIPTION]. Premium dimensional cartoon (Pixar/Bluey), soft fur warmth, soulful eyes, NOT photoreal, NOT flat. [camera] [lighting] [environment]. No text, no watermark."
```

## ⏭️ Still to lock (same recipe + style)
- Stella the Sea Star · Pip the hermit crab · the Crystal Cove tide-pool environment plate · then the 122-shot pilot.
