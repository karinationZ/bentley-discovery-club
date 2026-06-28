# Superseded Notice

This handoff is historical. For the shipped Episode 2 final and the Episode 3-ready pipeline rules, use `docs/series/season_1/ep2/EP2_FINAL_HANDOFF.md`.

Key superseding decisions from the final pass:

- Build from `scratch/ep2/assembly/EP2_v5_FINAL.mp4`, not v6.
- Use `kling-3.0/video` for new motion going forward.
- Do not rely on Kling-Avatar for Bentley/Indi mouth animation unless full-duration QA proves no human teeth or human-style smile.
- Prefer VO-over animated performance shots for non-human dialogue.

---

# Bentley Ep2 — Production Handoff
*For external review (ChatGPT / another tool / another approach). Written 2026-06-23. Honest state, including failures.*

---

## TL;DR — THE ONE UNSOLVED PROBLEM
**The generative AI pipeline cannot reliably hold the LOCKED Bentley character across an episode.** Every per-shot re-render reinterprets him — ears, tail, paws, proportions, and drawing style drift shot-to-shot. Prompt rules ("docked tail, floppy ears, no white paws, match the master") are only weakly obeyed and are routinely violated. This is the root cause of "you changed the master prop" / "you broke all the hard rules," and it has caused repeated buggy cuts (v6 made Bentley *worse* than v5: erect ears, long tail, white paws, wrong style).

**This is a structural limitation, not a prompt-tuning problem.** A real fix needs one of: a trained identity model (LoRA/DreamBooth), a 3D-rigged character, a tool with true character-reference locking, or strict human-in-the-loop keyframe curation. See §7–8.

---

## 1. THE PROJECT
- Kids' YouTube animated series **"Bentley's Big Adventures"** (ages 4–8, soft 3D Pixar style), based on the owner's real Boxer.
- **Ep2 "The Octopus Escape Artist"** (~3:02, 35 shots): Bentley (Boxer puppy) explores a tide pool, spots a hidden eye on a rock, playfully chases what she thinks is prey, accidentally scares a shy octopus (Indi) toward danger (an eel), realizes her mistake, calms down + uses her catchphrase, learns octopus facts (camouflage / boneless squeeze / three hearts), Indi confesses she was scared, they become friends. Ant-trail teaser for Ep3.

## 2. CANON / HARD RULES (these keep getting broken — enforce ruthlessly)
**Bentley** — master = `assets/character_design/Bentley_MASTER_pixar.png`:
- Cartoony-Pixar 3D **PUPPY** EXACTLY like the master. NOT realistic, NOT adult-proportioned.
- Red-fawn coat · black mask · grey chin · white chest blaze.
- **SHORT DOCKED tail** (small stub) — NEVER a long/whippy tail.
- **FLOPPY folded ears** (boxer ears down) — NEVER both ears erect/up (this looks like a different breed; the owner called it "ridiculous").
- **Solid red-fawn paws** — NEVER white socks/toes.
- Brown eyes · teal collar · gold paw-print tag.
- Happiness = tongue out / soft eyes / tail wiggle. **NEVER a human smile or human teeth.**

**Indi** — master = `assets/character_design/Indi_LOCKED.png`: soft purple · **TEAL eyes (NEVER brown — owner rejected a brown re-lock)** · no nose · no eyebrows · two teal ring spots · small (≈Bentley's-head size) · tiny mouth · toothless.

**Eel** — design ref `assets/pilot_shots/ep2/keyframes/a2_12_eelstir_v4_chosen.png`: shown as a **dark MENACING SILHOUETTE** (open jaw, backlit, Indi recoiling in frame) — NOT cute, NOT gory.

**Other:** "Stop. Look. Listen." = **Bentley's voice** (ElevenLabs LauraZ), paced with pauses — NEVER the narrator. Tone cheerful/funny/kid-safe.

**ABSOLUTE: never redesign or regenerate the master props.** Edit FROM them; never produce a "new" Bentley/Indi/eel.

## 3. HOW THE PIPELINE WORKS
**Backend:** KIE.ai (`.env` → `KIE_KEY`). Models:
- `nano-banana-pro` — image gen/edit (keyframes), ~18 cr.
- `kling-2.6/image-to-video` — i2v animation, ~55 cr / 5 s, 1904×1088.
- `kling/ai-avatar-standard` — talking lip-sync (audio→video), ~40 cr, 720p.

**VO:** ElevenLabs — Bentley = `LauraZ`, Indi = `FcZStbCG9g9QxDlJioSD`, Narrator = Bill. **ffmpeg** for assembly/mix/grade.

**Stages** (`docs/guides/PRODUCTION_PIPELINE.md`):
1. **Script** → `docs/series/season_1/ep2/EPISODE2_SCRIPT.md`.
2. **Shotlist** → `episodes/ep2/shotlists/ep2_master.json` (35 shots; each has `id`, `type` = motion/talk/voover/card, `src`, `voice`, `line`, `dur`).
3. **Keyframes** — derive per-shot by EDITING the locked master with `nano-banana-pro` → `assets/pilot_shots/ep2/keyframes/<id>.png`.
4. **Motion** — Kling i2v from keyframe → `assets/pilot_shots/ep2/motion/<id>.mp4`. **Talking** — Kling-Avatar from a talk-keyframe + VO → `scratch/ep2/talking/talk_*.mp4`.
5. **VO** — ElevenLabs → `scratch/ep2/vo/*.mp3`.
6. **Assemble** — `scratch/ep2/assemble_ep2.py`: per-shot segments (crop / fill-frame / trim-to-speech / **per-shot color normalize toward V57/S32**), then concat → `EP2_v3.mp4`. Contains: `OVR` dict (per-shot overrides: voover/card), `SRCMAP` (de-dup source overrides), `CROP` (caption-killing crops), `title_establish` (live-water title), `normalize_seg` (grade).
7. **Mix** — `scratch/ep2/mix_ep2.py`: per-act music + key SFX + ambient + final 1080p grade → `EP2_FINAL_v3.mp4`.
8. **QA**.

**Reusable framework:** `bentley/character_framework/` — `anatomy.py` (DOG/CEPHALOPOD describe+ban), `characters.py` (BENTLEY/INDI registry + master paths), `prompts.py` (talking/motion prompt builders), `rules.py` (7 rules), `pipeline.py` (talk/batch/derive_keyframe).

**Pipeline gotchas learned the hard way:**
- Source resolution order in the assembler: `OVR` dict → shotlist `src` (CAN pin an OLD path) → `motion/<id>.mp4`. A re-render saved to the wrong path is **silently ignored** (cost a full review round on the rock-eye). Always verify a frame extracted from the FINAL file.
- The viewer caches by filename → always deliver a **fresh filename** (e.g. `EP2_v7…`).
- ffmpeg concat needs uniform audio (48 kHz stereo) or VO garbles.

## 4. CURRENT STATE — WHAT WORKS vs WHAT'S BROKEN
**Best current cut:** `scratch/ep2/assembly/EP2_v5_FINAL.mp4` (owner says better than v6). **`EP2_v6_FINAL.mp4` = the broken-Bentley rebuild — do NOT use.**

**Works:** story structure (after the Act-2 re-stage), Indi (~90% on-model), the catchphrase, the eel-as-menacing-silhouette, the live photoreal opening plate, the uniform color grade, VO, and the assemble/mix/grade ffmpeg pipeline itself.

**Broken (the blocker):** **Bentley off-master** — across shots he varies between a chibi puppy and a realistic Boxer, gets erect ears, a long tail, white paws, and a different render style. v6's "conform" pass made it worse.

## 5. FAILED ATTEMPTS / CHALLENGES (honest, chronological)
1. **Lip-sync teeth** — Kling-Avatar leaks human teeth/hands onto non-humans; Wan 2.2 & Infinitalk gated/broken on the account. → settled on Kling-Avatar + teeth-aware prompt (owner accepts occasional teeth on talking shots).
2. **Photoreal master** (`Bentley_MASTER_hero.jpg`) couldn't be matched by AI animation → re-baselined to the cartoony-Pixar master.
3. **TWO RENDERING PATHWAYS diverge** — Kling-Avatar (talking) renders chibi; Kling i2v (action) drifts realistic → two Bentley models intercut.
4. **CONFORM attempt (v6)** — re-derived all action keyframes from the Pixar master + re-i2v'd to unify the look → **drifted WORSE** (erect ears, long tail, white paws, new style). This is the current failure and the clearest proof the generative step won't hold identity.
5. **Animation reuse** (same clip used twice: settle, reform) → fixed via de-dup.
6. **Color inconsistency** (brightness V23–71) → fixed via per-shot normalization.
7. **Act-2 = narrated not shown** (chase not scary, Indi calm not fleeing, eel smiling, never shares a frame with Indi) → fixed by re-staging, but the re-render introduced the Bentley drift.
8. **Process failure (mine):** I auto-batched re-renders and shipped before the owner approved each on-model frame — amplifying the drift instead of catching it. The owner's standing rule (QC every frame, approve before generating, never auto-batch) was the right call.

## 6. ROOT CAUSE
`nano-banana-pro` "editing from the master" and `kling-2.6 i2v` both **regenerate** the character; they treat the master image + prompt as loose hints, not a hard identity lock. There is no mechanism forcing the exact same model across shots, so anatomy/style vary every render and the hard rules are violated unpredictably. This is a fundamental limitation of prompt-conditioned generative video for **locked-character** animation.

## 7. WHAT WOULD ACTUALLY FIX IT (ranked — the key question for ChatGPT)
1. **Trained identity model** — fine-tune a LoRA / DreamBooth (or equivalent character model) on the locked Bentley master (render/collect multiple clean angles + poses first), then generate ALL keyframes from THAT model so identity is consistent, then i2v. This is the standard industry solution for AI character consistency.
2. **3D-rigged character** — build Bentley once as a rigged 3D model (Blender/Maya, or an AI 3D generator), animate traditionally → 100% consistent; use AI only for backgrounds. How real studios guarantee consistency.
3. **True character-reference tooling** — switch keyframe generation to a tool with real identity locking and test which holds Bentley best: Midjourney `--cref`, IP-Adapter / InstantID, Kling "Elements"/character-consistency, Runway, Higgsfield character refs.
4. **Human-in-the-loop curation** — generate 4–8 candidates per keyframe, hand-pick the on-model one, NEVER auto-batch-and-ship. Slow but works with current tools.
5. **Reduce shot count + reuse a small approved on-model clip library** (carefully, to avoid the repetition problem the owner also flagged).

Recommendation: pursue **#1 or #2** for a real fix; **#3/#4** as stopgaps if staying on the current toolchain.

## 8. WHAT'S LEFT (if continuing this episode)
- **BLOCKER:** Bentley consistency (see §7). Nothing else ships until this is solved.
- **P1 polish** (from the 7-agent review, `EP2_PRODUCTION_REVIEW.md`): re-frame the repeated talking-head close-ups (match-jump on ~5 Bentley + 4 Indi CUs); trim the 14.4 s confess hold + 9.9 s button hold; add an "Indi gets wedged" setup beat (2:00 jump); gentle dissolves on the 0:38–0:53 underwater seams.
- Final QA pass against this canon sheet.

## 9. KEY PATHS
- Masters: `assets/character_design/Bentley_MASTER_pixar.png`, `Indi_LOCKED.png`, eel `assets/pilot_shots/ep2/keyframes/a2_12_eelstir_v4_chosen.png`. Spec: `assets/character_design/LOCKED_ELEMENTS.md`.
- Cuts: `scratch/ep2/assembly/EP2_v5_FINAL.mp4` (best), `EP2_v6_FINAL.mp4` (broken).
- Pipeline scripts: `scratch/ep2/{assemble_ep2,mix_ep2,talk_ep2}.py`; framework `bentley/character_framework/`.
- Shotlist: `episodes/ep2/shotlists/ep2_master.json`. Script: `docs/series/season_1/ep2/EPISODE2_SCRIPT.md`.
- Reviews: `docs/series/season_1/ep2/EP2_PRODUCTION_REVIEW.md`, `EP2_QA_REPORT.md`. Pipeline doc: `docs/guides/PRODUCTION_PIPELINE.md`.
- Repo: private GitHub `karinationZ/bentley-discovery-club`.
