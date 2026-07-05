# Bentley 3D Rig Pipeline — Handoff Brief

*Audience: an engineer/agent picking up the build-once rigged-character pipeline. High-level what/why/how
+ current state + the gap to production. Written 2026-07-05. Repo: `bentley-discovery-club`.*

---

## 1. WHAT this is (one paragraph)

Build **one canonical 3D model of Bentley** (the red-fawn Boxer puppy star of the series), rig it once,
and **animate + render every shot from that single rig** — the way a game or a Pixar film reuses one
character asset across thousands of shots. This replaces the current approach of *generating* Bentley
fresh with AI (nano-banana-pro keyframes → Kling video) for every single shot. The rig becomes the new
"master": pose it, drive its mouth from the recorded voice track, render, composite over a background.

## 2. WHY we need it (the problem it solves)

The AI generative pipeline has three structural problems the rig fixes **all at once**:

| Problem | AI pipeline today | Rig |
|---|---|---|
| **Consistency** (THE #1 blocker) | Every shot's Bentley is generated separately → she drifts shot-to-shot (white paws, white muzzle stripe, mask changes, proportions). We hand-QC every frame and *still* miss drift. | **Zero drift** — it's literally the same mesh + textures every shot. |
| **Lip-sync** | No reliable way to sync a free-posed cartoon dog mouth; AI invents human teeth on wide-open mouths (a recurring owner rejection). | **Deterministic + free**: drive a hand-authored viseme mouth set from the audio. The **human-teeth problem disappears by design** — you sculpt a toothless dog-mouth once and it can never grow human teeth. |
| **Cost** | ~70 cr per 5s Kling render, plus rerolls; a single episode is thousands of credits and dozens of drift-rerolls. | **~$0 per shot** after the build. Cost moves *upfront* (building the rig) then is ~free forever — the inverse of AI. |

Net: the rig is the documented **long-term fix** for the consistency/lip-sync/cost triad. Trade-off: real
upfront modeling/rigging work before it pays off.

## 3. HOW it works (the recommended stack — all free, open-source, Python-automatable)

Verified by deep research (2026-06-24, 21 sources; full cited report: `docs/guides/ANIMATION_PIPELINE_RESEARCH.md`):

- **Blender** — the 3D rig + toon/painterly look-dev + render, driven **headless**:
  `blender --background --python build_shot.py`.
- **Rhubarb Lip Sync** (MIT CLI, audio→viseme timings) via the **`blender_rhubarb_lipsync_ng`** addon
  (the **Premik** fork — MIT, maintained, Blender 3.3–5.1). ⚠️ The old `scaredyfish/blender-rhubarb-lipsync`
  is ABANDONED/broken — do not use. Feed it our ElevenLabs VO mp3s + the episode transcript
  (`--dialogFile`) for accurate visemes.
- **Toothless dog-viseme mouth set** — author ~6–9 mouth shapes ONCE (closed, slightly-open, wide-A, O,
  F/V, etc.) with NO human teeth; Rhubarb picks which shape per audio frame.
- **Tripo3D** (paid Python SDK, optional) — one-shot image→rigged-3D with a QUADRUPED preset to *bootstrap*
  the mesh from the locked 2D master. Bootstrap only; Rhubarb still does the mouth.
- **Integration**: each rendered rig clip slots into the **existing cue-sheet → ffmpeg assemble/mix
  pipeline** (`episodes/ep<N>/*.py`) exactly where a Kling clip goes today. The EDL/animatic/QA layers
  don't change.

**Rollout = HYBRID, not big-bang:** rigged Bentley for **talking + hero character** shots (where drift and
lip-sync hurt most); keep AI/reuse/Ken-Burns for backgrounds and non-character coverage. Composite the
rigged character over AI/painted background plates. Validate with a small proof-of-concept shot that passes
owner QC **before** committing to the full build.

## 4. CURRENT STATE — what's already built (don't redo this)

Prior "RIG STUDIO" work exists (`scratch/rig_build/`, the `lipsync-pro` skill, and completed tasks):
- **Mesh**: image→3D Bentley generated (Tripo) from the locked master → `scratch/rig_build/bentley_mv.fbx`,
  `bentley_pbr.fbx`, `bentley_norm.blend`; turntable `bentley_turntable.mp4`.
- **Rig v1**: `scratch/rig_build/bentley_rig_v1.blend` — jaw bone, weights, mouth interior, tongue.
- **Visemes + driver**: viseme shapes + Rhubarb driver wired (our JSON / the NG addon).
- **Look-dev v1**: toon shading pass toward canon; "alive" idle (head-bone) + a desert staging test
  (`bentley_rig_desert.blend`, `B_strong_alive.mp4`, `BENTLEY_RIG_TALK*.mp4`).
- **Hybrid proof clips**: rig→restyle experiments (`scratch/rig_build/HYBRID_*.mp4`) exploring rig-motion +
  AI-restyle for photoreal talking.
- **Skill**: `lipsync-pro` skill documents the method and is the lip-sync authority in the normative chain.
- **Reference**: `docs/guides/ANIMATION_PIPELINE_RESEARCH.md` (the full cited research);
  memory `bentley-rigged-pipeline-research`.

## 5. THE GAP — what's needed to reach production (the actual work)

The rig exists but is **not production-ready or wired into the episode pipeline**. Milestones:

1. **Look-dev to the LOCKED EP4 style.** The series style is now **matte painterly storybook** (owner
   decision 2026-07-05), NOT glossy 3D — the rig's toon shading must match the approved keyframes
   (`assets/pilot_shots/ep4/keyframes_prod/`) and the master (`assets/character_design/Bentley_MASTER_pixar.png`).
   **✋ owner sign-off on a single rendered still vs the master before anything else.**
2. **Full canon pass on the mesh/textures**: red-fawn coat, black face mask (no white muzzle stripe), grey
   chin, floppy folded-down ears, white chest blaze, **paws same color as coat (no white socks)**, **short
   docked tail stub**, teal collar + gold paw-print Listening Tag. Lock a turnaround that matches the 2D master.
3. **Viseme set finalize + QC**: complete the toothless dog-mouth shapes; verify Rhubarb output on 3–4 real
   EP4 VO lines; confirm the mouth "turns with the head" on ¾/profile poses (the failure mode that killed the
   2.5D patch approach — see `bentley-lipsync-rig-system`).
4. **Headless per-shot build script** (`build_shot.py`): inputs = pose/action + VO mp3 + camera preset +
   background plate; output = a rendered clip (matching our 1080p pipeline) that drops into the EDL. Must run
   `blender --background`.
5. **Pose/action + camera preset library**: run, bound, sit, head-tilt, sniff, flop, catchphrase-still, etc.,
   with locked-camera + simple track presets (mirrors the render prompts we use today).
6. **Background compositing**: rigged Bentley over AI/painted plates (meadow/grove), matched lighting/grade.
7. **PROOF-OF-CONCEPT**: reproduce ONE already-approved EP4 shot (e.g. the s6 catchphrase CU or a two-shot)
   with the rig, side-by-side vs the AI render, and pass owner QC (identity + style + lip-sync + no teeth).
   **This POC is the go/no-go gate for the full build.**

## 6. DEFINITION OF DONE

A rigged Bentley shot that: (a) is **indistinguishable in identity** from the master across repeated
renders (zero drift), (b) **lip-syncs** an ElevenLabs line with **no human teeth**, (c) matches the
**painterly EP4 look**, (d) renders **headless** and slots into the existing cue-sheet→ffmpeg pipeline at
**~$0/shot**, and (e) passes the owner's side-by-side QC vs an AI render on the same beat.

## 7. HARD CONSTRAINTS / GOTCHAS (read before starting)

- **Owner laws** (see `episode-production` skill + memory): never drift the approved style; NEVER name a paw
  color in prompts; short docked tail only; NO human teeth ever; the style anchor is the **literal master
  image**, not a style word.
- **Lip-sync dead ends — do NOT rebuild**: the 2.5D flat mouth-patch (owner-rejected 3× — anatomically wrong
  on ¾/down-facing heads), and human-lip re-sync tools (barely move a cartoon muzzle). The rig's whole point
  is to do it *right*; the Rhubarb *timing* layer from those attempts is reusable, the patch renderer is not.
- **Hybrid first, POC-gated** — do not attempt a full-episode rig build before the single-shot POC passes.
- **Stay in the chain**: the rig plugs into the existing gates (Animatic Lock, keyframe/render QC, 11-rule
  release) — it changes HOW a character shot is made, not the pipeline around it.
- Keep everything **headless + scriptable** (the research's core requirement); the paid 2D-puppet fallbacks
  (Cartoon Animator 5 / Adobe Character Animator) are flat-2D and non-scriptable — only if the 3D route stalls.

---

*Related in-repo: `docs/guides/ANIMATION_PIPELINE_RESEARCH.md` (full research), the `lipsync-pro` skill,
`scratch/rig_build/` (all prior assets), memories `bentley-rigged-pipeline-research`,
`bentley-consistency-blocker`, `bentley-lipsync-rig-system`.*
