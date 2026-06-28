# Bentley's Big Adventures — LOCKED CHARACTER DESIGN (source of truth)

> Locked 2026-06-15. This is the canonical look for the entire series. Every shot + video must inherit it.

## 🔒 HARD RULE — STYLE & CONSISTENCY (locked 2026-06-20, client directive)
For EVERY shot, edit, variation and tweak:
- Keep the existing **approved drawing style**
- Keep the exact same **art direction**
- Keep the exact same **proportions**
- Keep the exact same **character language**
- Keep the exact same **rendering style**

**Do NOT redesign the character. Do NOT reinterpret the style. Do NOT "improve" the style.**

**Use the approved master prop as the SINGLE SOURCE OF TRUTH.** To make any change, **EDIT the approved frame** (FLUX Kontext `flux-kontext-max` for minimal, style-preserving edits) — do **NOT** re-generate the shot from scratch or from the masters, because regenerating drifts the drawing style (it once turned a dimensional-3D two-shot into flat-2D/toony). Make ONLY the one change requested; preserve shape language, proportions, face structure, character appeal, and overall look & feel. If the old and new versions are placed side by side, they must clearly look like **the same character from the same show**.
> Approved references: Indi master `Indi_LOCKED.png` · Bentley charm `Bentley_paw_tag.png` · approved 3D shot style `scratch/ep2/hero_v2/s16_exchange.png`.

## 🔒 HARD RULE — CREATURES EXPRESS LIKE ANIMALS, NOT HUMANS (locked 2026-06-20, client directive)
**This applies to EVERY creature — Bentley, Indi, and any guest.** The ban is specifically on **HUMAN teeth and HUMAN smiles** (a flat human row of teeth; lips pulled back into a human grin) — in keyframes AND motion/avatar. ✅ **Natural animal anatomy is CORRECT and wanted:** Bentley is a **dog and HAS natural dog teeth** (canines, small dog teeth) and a tongue — a natural open dog mouth / tongue-out happy pant is the *right* look (reference: **`Bentley_happy_ref.png`** — tongue out, soft eyes, ears down). ⛔ **Octopuses (Indi) genuinely have NO teeth** — never give her any teeth or a toothy smile; her happiness shows through soft eyes, arm gestures, mantle posture and colour. The i2v/video model keeps adding HUMAN smiles + teeth to both the dog and the octopus — prompt hard against it (lock the mouths) and **reject any frame with a human grin, or ANY teeth on the octopus.**

Bentley specifically must **NEVER smile like a human** — no pulling the lips back, no baring teeth, no human grin, no human-looking teeth. A human-style smile/teeth breaks the illusion (reads as "a human in a dog costume"). **This applies to keyframes AND motion/avatar shots** — Kling i2v and avatar models love to add a human smile; prompt explicitly against it and **REJECT any frame with a human grin or human teeth.**
Bentley shows **happiness through natural DOG behavior** (use real Boxer references):
- tail wiggles / wags
- mouth opens **naturally** and relaxed; **tongue lolls/hangs out**; light happy panting
- **soft, warm, expressive eyes**
- relaxed soft floppy ears; bouncy, wiggly body language

At all times keep a **natural dog mouth** (soft pink tongue, only small natural dog teeth, NEVER a row of human teeth, NEVER lips pulled into a human smile). Goal: a lovable, realistic Boxer with animated personality — never a human face on a dog.
> **Real reference:** based on real photos of the actual dog Bentley — when happy, her big pink **tongue lolls out** the side and the mouth is open naturally (relaxed jowls, soft eyes); she NEVER shows a human upper-teeth grin. Match the real dog. When an open mouth is needed, default to **tongue-out**, not bared teeth. **Ears** fold softly **DOWN against the sides of the head** (relaxed floppy Boxer ears) — never flying out or sticking up/out. Real Boxers have **pronounced forehead/brow wrinkles** — keep them visible (folds on the brow + a little on the muzzle), don't smooth them away.

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
- **Costume:** teal collar + a softly glowing gold **paw-print name tag** engraved **"Bentley"** (the "**Listening Tag**" — supersedes the old spiral-shell "Listening Shell" charm; ref `Bentley_paw_tag.png`, finalized 2026-06-20 via Nano Banana Pro). The glow is still the Stop-Look-Listen device. Her only accessory. *(Ep1 shipped with the shell; the paw tag is the Ep2-onward look.)* **Tag-name legibility:** the engraved "Bentley" reads only in **stills/close-ups** (Nano Banana Pro); **AI video garbles small text**, so in wide/motion shots the tag reads as a plain gold paw (name not legible at scale — fine). For any shot where the name must be readable, **stamp the clean "Bentley" in post** (Pillow); don't expect the video model to hold it.
- **She is FEMALE** — always render a smooth, neutral, featureless underside with **NO genitalia** (standard for a wholesome kids' cartoon). State this in any prompt with a rear/underside angle.

## 🐙 Indi — Ep2 guest octopus (LOCKED 2026-06-20)
Young California two-spot octopus; the season's shy "messenger." **Designed OCTOPUS-FIRST** — a real octopus gently stylized for animation, **NEVER a human face on a ball** (six early attempts failed by starting from a cute human face; a reset fixed it).
- **Locked master:** `Indi_LOCKED.png` = the **s14 look + defined iridescent ocelli** (FINAL, client-approved 2026-06-20; built with **Nano Banana Pro**). Edit-anchor catbox URL in `.indi_locked_url.txt`. **Model — edit Indi with `nano-banana-pro`** (KIE slug = `nano-banana-pro`, NOT `google/...`; input params `image_input:[url]`, `aspect_ratio`, `resolution:"2K"`, `output_format`): best consistency + instruction-following (~18–24 cr/edit). Generate ALL Indi shots by **EDITING FROM this one frame**; do NOT re-describe her face (let the reference do the work). *To do:* regenerate the model sheet + hero shots from this final master so the whole episode matches (earlier ones used superseded looks).
- **Body:** soft rounded domed mantle + 8 long tapering suckered arms (the arms are the dominant mass); iridescent **grape-purple** jewel skin (matches the Ep1 teaser octopus — purple is canon), glossy/wet, subtle papillae, lighter pinkish-lavender highlights.
- **Eyes (HARD RULES):** **TEAL / aqua-cyan** iris — unnatural, magical, NON-human (**NEVER brown / amber / gold**); soft simple pupil, ONE catchlight, **NO white sclera**, **NO line or seam across the eye**; set fairly lateral on the head with a soft eyelid "hood" (a skin fold, **NOT an eyebrow**).
- **⛔ NEVER on Indi:** human eyes, white sclera, **a nose / nostrils / muzzle**, **eyebrows / brow ridge**, human face-plane / cheeks / chin, human teeth or lips. Her ONLY face features = two teal eyes + one tiny soft lipless mouth.
- **Mouth:** tiny, soft, low, **lipless** seam that opens to a soft "o" (she talks). No teeth.
- **Two-spot ocelli:** exactly TWO soft iridescent peacock-blue **RING markings** (a smooth circle with a slightly darker center + subtle pearlescent shimmer), placed **LOW, just below/in front of each eye** (real bimac anatomy), small and organic. ⛔ **NEVER use the words "chain-link" / "chain"** in a prompt — they make the model draw literal metal chains. ⛔ **NEVER glowing / emissive / neon** — the eyes AND ocelli are NOT light sources. ⛔ Not flat dull painted stains. NOT high "headphones," NOT the blue-ringed-octopus many-rings look.
- **Color = emotion ("Mood-Light"):** purple is her true/resting self; skin **brightens/blooms when happy, pales when scared**; **mottled red-brown ONLY when actively camouflaging**. Emote via color/glow + arm gesture + posture + pupil — **not** the face.
- **Render:** clean, sharp, **colorful** (avoid monochrome-purple washes — stage her in colorful settings so the purple pops); NO film grain / noise.
- **Scale (keep CONSISTENT across every shot):** Indi is a **SMALL** octopus — about the size of **Bentley's HEAD**, NEVER as big as the dog. Bentley is a Boxer puppy; Indi is a little tide-pool octopus she **leans down to**. In any two-shot, keep this proportion AND keep Bentley's full head/face in frame (don't crop her face).
- **Voice (LOCKED 2026-06-20):** ElevenLabs `FcZStbCG9g9QxDlJioSD` — shy / intelligent / guarded-but-warm; `eleven_v3`; settings stability 0.4 / similarity 0.75 / style 0.45 / speed 0.95 → call via `tts_indi()` (`bentley/voices/dialogue.py`).

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
