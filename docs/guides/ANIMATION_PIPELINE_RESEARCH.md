# Reusable-Asset Animation Pipeline — Research & Recommendation
*Deep-research report, 2026-06-24. 21 primary sources, 25 claims verified (25 confirmed / 0 refuted).*

## The question
Can we replace per-shot AI video (Kling i2v) — which is **expensive**, **drifts off-model**, and **can't do mouth/lip-sync without human teeth on the dog** — with the *games model*: build a character RIG once, then reuse and lip-sync it across every shot, consistent and ~free?

**Answer: yes.** A rigged master asset solves all three problems at once:
- **Consistency** → perfect (same rig every shot, zero drift).
- **Lip-sync** → deterministic, free, repeatable, and **the human-teeth problem disappears by design** — you author the mouth/viseme shapes once as a *dog* mouth (tongue + dark openings, no human teeth), so the rig physically *can't* grin.
- **Cost** → ~zero per shot (local render, no AI credits per shot). The cost moves to a **one-time rig build**.

## The two viable tracks

### ⭐ TRACK B — Blender + Rhubarb (free, open-source, Python-automatable) — RECOMMENDED
- **Rhubarb Lip Sync** — MIT-licensed CLI that turns a voice recording into viseme/mouth-shape timing (`rhubarb -o out.txt line.wav`, `--machineReadable` JSON, optional `--dialogFile` transcript for best accuracy). Free for commercial use, trivially called from Python via `subprocess`. The de-facto OSS standard. [github.com/DanielSWolf/rhubarb-lip-sync]
- **`blender_rhubarb_lipsync_ng`** (maintainer Premik) — **MIT, actively maintained** (v1.8.1, Blender 3.3–5.1). Wraps the Rhubarb CLI: runs it on an audio file → Cues → maps each cue to a reusable **bone Action OR shape-key** → **Bake to NLA**. Crucially: **one cue-mapping is reused across all dialogue, at zero per-shot cost.** Works for 3D armature rigs *and* blendshape/shape-key rigs. [github.com/Premik/blender_rhubarb_lipsync_ng]
- **Blender `bpy`** — the whole flow (import master rig → drive Rhubarb cues → bake NLA → render) is scriptable and runs **headless**: `blender --background --python build_shot.py`. Slots straight into our existing Python/ffmpeg pipeline.
- ⚠️ **Do NOT use the older `scaredyfish/blender-rhubarb-lipsync`** — abandoned, broken on Blender 3.2+. Use the Premik `_ng` fork.
- Alt viseme stage: **Papagayo-NG** (free GPL, ~all Python, real `--cli`, exports MOHO/JSON, can call Rhubarb/Allosaurus).
- **Bootstrap shortcut:** **Tripo3D Python SDK** (paid cloud) does one-shot image→rigged-3D with **QUADRUPED** (= Bentley) and **OCTOPOD** (= Indi) rig types — useful to turn an existing Bentley/Indi image into a starting rigged mesh, **but it only applies preset locomotion, not audio lip-sync** (Rhubarb still does the mouth). [pypi.org/project/tripo3d]

### TRACK A — 2D puppet (paid, NOT Python-scriptable) — faster, but a fallback
- **Reallusion Cartoon Animator 5** — turns static images into rigged 2D puppets; **AccuLips** auto-generates mouth animation from a WAV/MP3; visemes are **hand-editable on a timeline** (double-click to swap a viseme). Paid (perpetual). [reallusion.com/cartoon-animator]
- **Adobe Character Animator** — auto-rigs a puppet from a layered, correctly-named PSD/AI file; **Adobe Sensei** auto lip-syncs from audio (phoneme→viseme). Free **Starter** mode; **Pro** is subscription (~$55–70/mo as of Aug 2025).
- ❌ **Neither is Python-scriptable** — Cartoon Animator exposes only an After Effects JavaScript bridge + Motion Link to iClone; Reallusion's Python Open API is **iClone/Character Creator only, never CTA**. And auto-rig targets **flat 2D art**, so a 3D-Pixar Bentley render becomes a flat 2D puppet (no true 3D rotation).

## Comparison
| | Blender + Rhubarb (B) | Cartoon Animator / Char Animator (A) |
|---|---|---|
| Consistency / reuse | ✅ perfect, build-once | ✅ perfect, build-once |
| Lip-sync automation | ✅ free, audio→viseme, **scriptable** | ✅ built-in auto lip-sync, GUI-bound |
| Cost | ✅ **$0** (MIT/GPL) | ❌ paid |
| Python scriptability | ✅ **full** (`bpy` headless + Rhubarb CLI) | ❌ none for the puppet tools |
| Matches our 3D-Pixar look | ✅ true 3D rig | ⚠️ flat 2D only |
| Learning curve / upfront effort | ❌ **high** (model + rig + viseme set) | ✅ lower (image → puppet) |

## Honest caveats (verified)
- **Every** auto lip-sync (Rhubarb, AccuLips, Sensei) is "never perfect" — expect occasional manual viseme cleanup. Clean, isolated voice audio (our ElevenLabs VO, no music) + the transcript (`--dialogFile`, which we already have) materially improve it.
- The **human-teeth-on-a-dog** fix is *not* automatic from any tool — it comes from **how we author the mouth rig** (a toothless dog-viseme set). Both Blender and the puppet tools give full control here; no source benchmarks dog faces specifically.
- The real cost is **upfront**: building a good, on-model rig is genuine work, front-loaded once, then ~free forever — the inverse of AI (cheap to start, expensive per shot).
- **Not covered by verified evidence:** Toon Boom Harmony, Moho, OpenToonz, Synfig, Live2D (unassessed here).

## Recommendation for Bentley's Big Adventures
**Build Bentley and Indi as Blender 3D rigs in the locked cartoony-Pixar look, with a toothless dog/cephalopod viseme set, and drive lip-sync with Rhubarb via `blender_rhubarb_lipsync_ng`** — fully Python-automatable into our existing cue-sheet → ffmpeg flow. Optionally bootstrap the starting meshes with Tripo3D from the existing master images. This is the games model the owner intuited: it permanently fixes consistency, gives real (toothless) talking mouths, and drops per-shot AI cost to ~zero — at the price of a one-time rig build.

**Pragmatic rollout:** a **hybrid** first — rigged characters for the talking/hero shots, keep AI/reuse for backgrounds & establishing — then expand rig coverage as the assets mature. Validate with a small **proof-of-concept** (one rough Bentley rig + Rhubarb on a single line) before committing to the full build.

## Open questions (next research, if needed)
- Which viseme-set design most reliably enforces a no-human-teeth dog mouth (shape-key vs sprite-swap)?
- Real per-episode effort-hours: Blender+Rhubarb vs Cartoon Animator AccuLips on the same dialogue (no head-to-head benchmark survived verification).
- Best migration of the existing AI Bentley/Indi look into an on-model rig: Tripo3D one-shot vs hand-modeling vs 2D-trace.

---

## Addendum (2026-07-01) — teeth policy superseded by the lip-sync system plan

This report's "toothless dog-viseme set" recommendation was an *enforcement mechanism* (a rig that
physically can't grin), not an anatomy claim. Owner canon (`assets/character_design/LOCKED_ELEMENTS.md`)
allows natural dog/puppy teeth and bans only HUMAN teeth/smiles. The adopted policy now lives in
`docs/guides/HIGH_QUALITY_LIPSYNC_SYSTEM_PLAN.md`: **v1 rig ships toothless** (same enforcement
guarantee); puppy-tooth hints are a v2 owner-opt-in for `AI`/`OPEN_JAW` after a still-sheet approval.
The report body above is preserved as originally verified on 2026-06-24.
