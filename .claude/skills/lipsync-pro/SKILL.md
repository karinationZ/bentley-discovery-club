---
name: lipsync-pro
description: >-
  Use when ANY character must speak on screen in "Bentley's Big Adventures" — planning, generating,
  rendering, fixing, or QA-ing a talking shot, dialogue plate, lip-sync pass, Avatar/OmniHuman call,
  Rhubarb/viseme timing, or the Blender rig. Also use when a mouth flaps out of sync, the WRONG
  character's mouth moves in a two-shot, human teeth appear, a mouth reads as a "hole in the cheek,"
  or anyone proposes a new lip-sync tool, a re-sync model, or "one more reroll." Load this BEFORE
  spending any KIE credit on a shot that contains a spoken line.
---

# Lip-Sync Pro — Bentley's Big Adventures (MANDATORY operating manual)

> **Part of the single normative chain** — the 11 Mandatory Rules (`episode-production` §0.0) →
> `episode-production/SKILL.md` → `references/PRODUCTION_PLAYBOOK.md` → THIS skill (the lip-sync
> authority the others defer to: production §0.3/§5 and playbook Part 6 summarize; this file holds the
> full method). Never contradict the chain; update together, same day.

Every RENTED lip-sync path failed on Bentley: post-hoc re-sync tools barely move a cartoon muzzle,
Avatar caricatures anything but a tight frontal CU, the 2.5D mouth patch was owner-rejected 3× as
anatomically wrong, and OmniHuman re-imagines her identity on every take (prompt guards ignored).
**OWNER DIRECTIVE (final, 2026-07-02): we build and use OUR OWN 3D-rig lip-sync system for Bentley.**
This skill is the single source of truth for making characters talk. It pairs with
`episode-production` (§0.3/§5 defer to this skill for lip-sync) and `cinematic-episode-writer`
(which stages dialogue mouth-visible in the first place).

**The prime directive:** *Lip-sync is deterministic character animation, not a generative slot
machine. Timing is free (Rhubarb). The mouth is an owned asset (the rig). Never pay twice for the
same mouth.*

---

## 0. THE FOUR LAWS *(⚖️ ship-blocking — read before anything else)*

### 0.0 THE SYNC-OR-HIDE LAW  *(⚖️ owner-forced 2026-07-03 — the root of the whole EP3 loop)*
**Every dialogue line whose speaker's mouth is READABLE on screen must trace to a sync tool
(Kling-Avatar CU · OmniHuman mask · the rig), OR be staged mouth-hidden. NEVER play VO-over-alive on
a plate where a talking face is the focus** — a Kling/i2v plate CANNOT hear the audio, so its mouth
flaps to nothing and reads as broken lip-sync episode-wide (EP3 had 15/25 lines like this; the owner
saw "a lot of lip-sync issues" every one). VO-over is legal ONLY when the mouth is genuinely not the
focus: head down (sniffing/scooping), turned away, tiny/distant, or an environment/no-face shot
(§0.4 STAGING). **The gate is deterministic and needs no detector: walk the EDL — every character
line must sit on a sync-tool clip or a mouth-hidden shot. A raw talking-face plate under a line = a
ship-blocking defect.** (Motion-heatmap QA §2b.6 catches WRONG-speaker; it does NOT measure sync
accuracy — automated mouth-vs-audio correlation was tried and is unreliable, so the EDL trace IS the
gate.)

### 0.1 THE WRONG-SPEAKER LAW
**On any multi-character plate, ONLY the speaker's mouth may move. Every non-speaker is generated
MOUTH-CLOSED, calm, still.** Never put "talking / mouths opening and closing / speech rhythm"
prompts on a multi-character plate — that bakes flapping into EVERYONE and the line reads as the
wrong character's, episode-wide (the EP3 v10 systematic defect; root cause was exactly that prompt).
A line that visually reads as the wrong speaker is a **ship-blocking defect** (same rank as §5a
SHOT-FLOW LAW). Full plate rules in §2.

### 0.2 ANATOMY-FIRST QA
Judge every synced mouth against **anatomy** — *"is this where the character's mouth physically is
in THIS pose?"* — never against overlay placement or "the mouth moved." On a ¾/down-facing muzzle
the real mouth is an occluded seam; a frontal mouth pasted there reads as a hole in the cheek no
matter how good the tracking is. This is the lesson of the 2.5D-patch rejection. Full gates in §5.

### 0.3 NO GENERATIVE ROULETTE ON BENTLEY
**⛔ Bentley dialogue NEVER goes through OmniHuman, and never through "one more reroll" of any
generative sync.** Owner verdict 2026-07-02: 3 OmniHuman takes = 3 different canon violations
(squashed face → invented long tail → plastic white lower lip); the ≤300-char prompt cannot bind
her identity against an audio-driven performance. The vicious circle (each take fixes one drift,
creates another) is **structural**, not bad prompting — same pattern as Kling/Avatar rerolls.
Bentley's word-accurate sync comes from the OWNED rig (§4c) or is not shown (§0.4). The ONE
exception is the owner-locked catchphrase Avatar CU (§4a).

### 0.4 THE STAGING LAW
**Sync is only shown on a mouth the viewer can read.** Dialogue shots are DESIGNED ¾-front minimum
(a `cinematic-episode-writer` duty). When a head faces away, is tiny (< `min_mouth_px` ≈ 24 px), or
the camera leaves the speaker: do NOT sync — hold the listener, cut to reaction, or play
**VO-over-alive** (§1 branch D). Nobody in professional animation adds word-accurate sync to an
unreadable mouth; neither do we.

---

## 1. PER-SHOT DECISION TREE *(run this for EVERY spoken line, before any generation)*

```
Is it the "Stop. Look. Listen." catchphrase moment?
├─ YES → A. Kling-Avatar tight face-CU (owner-locked, §4a). Voice = Bentley/LauraZ, ALWAYS.
└─ NO → Who speaks, and is the mouth readable?
    ├─ Mouth unreadable (< ~24 px, away-facing, camera leaves speaker)
    │     → D. VO-over-alive: closed-mouth plate + speaker-isolation staging (§2). No sync pass.
    ├─ Speaker = Bentley (or any complex-canon character: heavy identity spec, drift history)
    │     → C. RIG ONLY (§4c). If the rig can't serve the shot yet → D (VO-over-alive).
    │       NEVER OmniHuman, NEVER Avatar (except A), NEVER reroll-roulette (§0.3).
    └─ Speaker = simple character (Marco-class: simple silhouette, few canon anchors),
      framed frontal/¾ with a readable mouth
          → B. OmniHuman-1.5 (§4b) under pilot→gate→batch + the 1-reroll rule (§6).
```

| Branch | Method | Cost | Status |
|---|---|---|---|
| A | Kling-Avatar CU (catchphrase only) | ~40 cr/line | PROVEN, owner-locked |
| B | OmniHuman-1.5 (simple characters) | ~26 cr/s @720p (~137 cr/take) | APPROVED for Marco-class (1/1 clean); BANNED for Bentley |
| C | Owned Blender rig (Bentley/complex) | ~$0/line after build | Pipeline proven end-to-end; deformation quality = active build (§4c) |
| D | VO-over-alive (closed-mouth plate) | plate cost only | Production default whenever A–C don't apply |

**A held two-shot beats a synced close-up.** Never chop a continuous section into talking-head CUs
to "get sync" — that is the exact owner-rejected failure (`episode-production` §0, no-giant-heads).
Lip-sync CUs, when they exist at all, are brief (~1.3 s) intercuts inside two-shots.

---

## 2. PLATE GENERATION RULES *(the wrong-speaker law in practice)*

Prompt recipes by plate type — get this right at GENERATION time; paint-out after the fact is
expensive and usually impossible (the EP3 LEAN plate was un-patchable):

- **Multi-character plate, one speaker (VO-over or OmniHuman):** speaker may get gentle natural
  motion; every non-speaker gets **"mouth closed, calm attentive expression, listening"** —
  explicitly, by name, in the prompt. Never a bare "the characters talk."
- **Rig-destined plate (any future rig-composited shot):** EVERYONE mouth closed — the rig owns
  100% of mouth motion and only ADDS openings (closed visemes render no patch; that's what kills
  sticker-flicker). Prompt: "mouth closed, calm" — never "talking / mouth moving."
- **Solo speaker plate, VO-over-alive:** mild natural talking motion is tolerated (it is not
  word-accurate and never will be — don't reroll chasing sync on an i2v plate; i2v cannot hear).
- **Speaker-isolation staging (free, always available):** design the beat so the speaker is the
  clear visual subject on their line — OTS on the speaker, listener in profile/behind, or cut to
  the listener's still reaction. If the edit can't tell who's talking with the sound off, restage.

QA hook: §5 speaker-match check runs on every multi-character beat, sound-off.

### 2b. CONVERSATION GRAMMAR *(two characters talking — THE core problem; owner-framed 2026-07-02)*

Single-head sync is a solved problem (branch A/B, or the hybrid: rig keyframe → nano-banana-pro
**from the locked master** → Avatar). Conversations fail when one continuous multi-character plate
is asked to carry word-sync — generative video cannot aim at ONE mouth. So a conversation is never
one plate; it is a **shot pattern** (film shot/reverse-shot grammar):

1. **The two-shot names the speaker with BODIES, not mouths.** Speaker gestures/leans/steps;
   listener prompted *"mouth closed, calm, still, listening"* by name — or stage OTS/profile so the
   listener's mouth is not visible at all (an invisible mouth cannot flap).
2. **Word-accurate sync lives ONLY in brief single-speaker cut-ins** (~1.3–2 s) intercut inside the
   two-shot — never the whole beat (no-giant-heads law). Bentley cut-ins = the hybrid pipeline
   anchored to `assets/character_design/Bentley_MASTER_pixar.png` (NEVER to a derived/rig frame —
   anchor drift stacks; owner caught "lost her charm" 2026-07-02).
3. **Marco-class characters sync IN-FRAME in the real two-shot**: OmniHuman `mask_url=[white-blob
   over the speaker]` → only that subject performs, listener stays still, plate preserved.
   ✅ PROVEN 2026-07-03 (smellpath_ts + M_checkyou + Marco mask, 27cr/2s): Marco talked, Bentley
   held mouth-closed and on-model, 3.5× more motion inside the mask than outside. Reference:
   `scratch/omni_ep3/masktest/run_mask.py` (mask = black canvas, white ellipse over the speaker,
   generous but clear of the listener). Still pilot-gate one mask per NEW plate + the §5 sound-off
   check; Marco identity over a LONGER line is the remaining watch-item.
4. **Bentley NEVER syncs in-frame on a multi-character plate** (§0.3 ban) — her conversation lines
   are staging + cut-in, always.
5. Sound-off test decides: if you can't tell who's talking with the audio muted, the beat is
   restaged — not rerolled.
6. **⚖️ MOTION-QA GATE (mandatory before every delivery; owner-forced 2026-07-03 after 3 shipped
   flappers):** a single-frame audit CANNOT see a flapping mouth — wrong-speaker is MOTION. Run
   `scratch/ep3/qa_mouthmotion.py` (per-plate |frame-diff| heatmap, p85-floored, red overlay) on
   every plate that carries a character line; the reviewer asks per line: *does the NON-speaker's
   mouth glow?* Glow on a readable non-speaker mouth = ship-blocker. Validated: caught the owner's
   0:27/0:32/0:40 finds + 2 unreported (marco_lost, smellpath_ts) and correctly CLEARED 5 suspects.
7. **Staging law addition:** the SPEAKER is never framed half-out-of-shot (chin-only/mask-only)
   while a readable listener fills the frame — that guarantees a wrong-speaker read (the lean_help
   failure). Old plates generated with "talking" prompts are ALL suspect — sweep them (§2b.6)
   before reuse; the flap is baked into the video but NOT the keyframe still, so a masked
   OmniHuman regeneration from that same keyframe erases it.

---

## 3. PROMPT-PHRASING LAWS *(⚖️ owner-set — violations have burned real credits)*

1. **NEVER name a paw color.** Not "red-fawn paws," not "solid red-fawn paws," not any color word —
   models paint literal crayon-RED paws. Correct text, always: **"paws the same color as her coat,
   no white socks."** The paws are not a feature; the absence of color difference is.
2. **OmniHuman prompts: ≤300 characters, and treat them as a NUDGE, not a contract.** The model
   demonstrably ignores identity guards (§0.3) — so spend the 300 chars on performance (tone,
   energy, who is addressed, camera hold) plus the two cheap guards that sometimes help:
   **"keep the exact character design"** and the mask/expression guard below. Do NOT stuff full
   canon into the prompt and expect it to bind — it doesn't; that's why Bentley is banned.
3. **Expression guards (every talking prompt, every tool):** "soft natural small-dog mouth,
   **NO human teeth, NO human grin, NO human smile, no bulging eyes**." Dog joy = tongue out, soft
   eyes, tail-stub wiggle. For Marco: "insect mandibles, no lips, no dog teeth, no human mouth."
4. **Closed-mouth plate phrasing (§2):** "mouth closed, calm attentive expression" — the words
   "talking," "speaking," "mouth moving," "speech rhythm" are BANNED on multi-character and
   rig-destined plates.
5. **Avatar keyframe law:** Avatar stays on-model ONLY from a **tight, bright, front-facing
   face-CU** keyframe. Wide/dim/small/side keyframe → caricature (bulging eyes, human grin). That
   failure is the keyframe, not the model — regenerate the keyframe, don't reroll the Avatar.
6. Full character canon (mask, grey chin, floppy ears, SHORT DOCKED TAIL STUB, white chest blaze,
   teal collar + gold paw tag, soft puppy eyes) lives in
   `.claude/skills/cinematic-episode-writer/references/bentley-canon.md` — reference it, don't
   re-improvise it per prompt.

---

## 4. TOOL PLAYBOOKS

### 4a. Catchphrase — Kling-Avatar tight face-CU *(owner-locked; the ONLY Avatar use)*
Full method: `docs/guides/TALKING_LIPSYNC_METHOD.md`. Essentials:
```python
kie_client.run("kling/ai-avatar-standard",
    {"image_url": <tight_bright_frontal_face_CU_url>,   # e.g. assets/approved/bentley/N6_kie_key_bright2.png lineage
     "audio_url": <clean_single_speaker_line_url>,      # tts_catchphrase — Bentley/LauraZ, never the narrator
     "prompt": <avatar_prompt_with_expression_guards>}, timeout=1200, poll=10)
```
Then grade (Avatar darkens):
`eq=brightness=0.05:saturation=1.14:contrast=1.05,unsharp=3:3:0.4:3:3:0.0,format=yuv420p`.
The synced audio file IS the played audio file — sync by construction. ~40 cr/line.

### 4b. OmniHuman-1.5 — simple characters ONLY (Marco-class)
KIE slug `omnihuman-1-5`. Inputs: `image_url` + `audio_url` (+ `prompt` ≤300 chars,
`output_resolution` "720"/"1080", `pe_fast_mode` (False for finals), `seed`, optional `mask_url`
×≤5 to select WHICH subject performs — use it on any multi-character keyframe). Audio <60 s,
≤15 s recommended. ~26 cr/s @720p. Reference implementation: `scratch/omni_ep3/gen_line.py`;
QA: `scratch/omni_ep3/qa_line.py`. Proven win in the EP3 cut: `M_together` (1/1 clean).

**Hard operational gotchas (each one cost real credits):**
- **Host inputs on KIE's own upload API** (`https://kieai.redpandaai.co/api/file-stream-upload`,
  Bearer `KIE_KEY` → `data.downloadUrl`; wrapped in `bentley/shared/hosting.py`). The omnihuman
  worker CANNOT fetch catbox/tmpfiles (connection reset). 3-day retention is fine — inputs are
  consumed in minutes; never use KIE-CDN URLs as long-lived references.
- **Persist the taskId to disk IMMEDIATELY after createTask** (a shell timeout orphaned a 108 cr
  task before this rule).
- failCode `50430` = platform busy → back off ~90 s and retry the CREATE, don't burn a new prompt.

### 4c. THE RIG — Bentley and every complex-canon character *(the owned system; the endgame)*
**Why:** visemes live ON the 3D head, so the mouth turns WITH the head — the anatomy failure that
killed every patch/re-sync approach is impossible *by construction*, and the rig physically cannot
produce human teeth (toothless v1 policy, owner-locked; puppy-tooth hints = v2 owner-opt-in only).

**Assets & status (2026-07-02):**
- Mesh: `scratch/rig_build/bentley_mv.fbx` — Tripo multiview, quad topology, textured, likeness
  owner-validated. (Regen if ever needed: `scratch/rig_build/gen_mesh.py`, ~35 cr; Tripo pbr output
  is **FBX, not GLB**.)
- Blender: `/opt/homebrew/bin/blender` (5.1.2), headless
  `blender --background --python <script>.py -- <args>`.
- Proven end-to-end at $0/frame: VO → Rhubarb → openness curve → jaw shape-key → EEVEE render →
  mux = `scratch/rig_build/BENTLEY_RIG_TALK.mp4`. Commands:
```bash
# normalize a new mesh (feet z=0, centered, faces -Y, canonical views):
/opt/homebrew/bin/blender -b -P scratch/rig_build/step1_normalize.py -- <mesh.fbx> <outdir>
# talking render from an openness curve:
/opt/homebrew/bin/blender -b -P scratch/rig_build/step2_talk.py -- \
    scratch/rig_build/bentley_mv.fbx <outdir> scratch/rig_build/openness.json
```
- **Honest quality gap (the active build):** a single jaw-open shape key made by raw vertex
  rotation BALLOONS the muzzle like a sock. Broadcast-clean needs a real **jaw BONE with smooth
  weight falloff + modeled tongue + mouth cavity + the ~9 viseme lip shapes**. That is the work;
  the plumbing around it is done.

**⚖️ Rig-work hard rules (each encodes a proven failure):**
1. **NEVER sculpt or weight-paint blind through headless scripts.** That failure mode is why the
   deformation is crude. Do mesh/deformation work with VISUAL feedback: the blender-mcp live
   session (ahujasid/blender-mcp — viewport screenshots per step) or, minimum, a render-and-inspect
   loop after EVERY change. One change → one look. No batch-sculpt-then-render.
2. **Reuse the proven camera** (parent cam to a pivot at head-center, orbit the pivot — the
   `head_inspect` rig). Rewriting camera math from scratch gave black/blown frames repeatedly.
3. Forward axis = **long body axis toward the head centroid**, never "farthest vertex" (that grabs
   a floppy ear). `base_yaw = atan2(fwd.y, fwd.x) - atan2(-1, 0)`.
4. Viseme targets = the LOCKED taxonomy in §4d — sculpt shapes to those names; the timing layer
   then drives them unchanged (`blender_rhubarb_lipsync_ng` is the wiring target, free/MIT).
5. Look-dev (marrying EEVEE renders to the AI-footage look) is a named risk — A/B against real
   plate frames before any rig shot enters a cut.

### 4d. The Rhubarb timing layer *(built, tested, valid — feeds the rig)*
Module `bentley/lipsync/` (18 tests: `python -m pytest tests/test_lipsync_*.py`). The 2.5D patch
RENDERER in this module is retired (owner-rejected); the TIMING layer is production.

**Invocation contract (all pinned — do not "rediscover"):** vendored binary
`tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-macOS/rhubarb` (v1.14.0, NOT on PATH) · MP3 → 16 kHz mono
WAV transcode first (Rhubarb accepts WAV/OGG only) · **always** `--dialogFile` with the line's REAL
transcript (never retype — `transcript_for(label)` reads the episode script's `label | speaker |
text` table) · `-r pocketSphinx` · `--extendedShapes GHX` · unknown output cue = hard error.
```python
from bentley.lipsync.rhubarb_adapter import run_rhubarb, transcript_for
cues = run_rhubarb("episodes/ep3/vo/B_strong.mp3", transcript_for("B_strong"))
```

**Viseme taxonomy (LOCKED) + Rhubarb map** (`bentley/lipsync/visemes.py`):

| Rhubarb | Project viseme | Note |
|---|---|---|
| `A` | `MBP` | M/B/P lip closure |
| `B` | `CONS` | slightly-open consonants + EE, ~half of voiced time — **NEVER closed** (closed = ventriloquist; verified blocker) |
| `C` | `AI` | open vowel |
| `D` | `AI` (→`OPEN_JAW` if the set has it) | deterministic, no "or" in the adapter |
| `E` | `O` | rounded mid-open vowel |
| `F` | `U` | puckered/rounded |
| `G` | `FV` | dog-safe F/V contact (never literal human teeth-on-lip) |
| `H` | `L` | tongue-forward L |
| `X` | `REST_CLOSED` | silence — with `A`, the ONLY cues allowed to close the mouth (unit-tested) |

Shape set v1 (all toothless): `REST_CLOSED MBP CONS AI E O U FV L`. Characters onboard as DATA
(`assets/lipsync/<char>/character.json`: per-angle sheets, `plate_provides`,
`rhubarb_map_overrides` for insect mouths, `min_mouth_px` waiver). Guests never reuse Bentley's
mouth anatomy — same timing, own artwork (Marco = mandibles).

---

## 5. QA GATES *(⚖️ ship-blocking — a talking shot is not done until ALL pass)*

1. **Anatomy first (§0.2):** the mouth opens WHERE the mouth physically is in this pose, inside the
   muzzle, following snout angle and volume. A perfectly-timed mouth in the wrong place is a FAIL.
2. **Dense sweep — inspect EVERY frame.** Build a ~0.15 s contact sheet per synced clip
   (`bentley.lipsync.qa_sweep.sweep(video, out_png, step=0.15, crop=<mouth box>)`; for generative
   takes `scratch/omni_ep3/qa_line.py <LABEL>` adds a drift metric — mean abs RGB vs keyframe,
   **<25 good, >40 investigate**). Spot-checking a few stills missed bad frames TWICE on EP3.
3. **Speaker match (ship-blocker, §0.1):** play each multi-character beat sound-off — you must be
   able to say who is talking. Then sound-on: the moving mouth is the voice's owner; every
   non-speaker is still. One wrong-speaker beat blocks the episode.
4. **Sync:** closures land on M/B/P; open vowels on audible open vowels; mouth closed in pauses and
   whenever the character isn't speaking.
5. **Canon:** no human teeth/grin/smile arc; on-model (mask, ears, docked tail stub, coat-colored
   paws, collar+tag); no identity drift across the take (OmniHuman's signature failure — check the
   WHOLE body, not just the face: the invented-long-tail take passed a face-only check).
6. **Continuity:** the plate outside the mouth is untouched; no shimmer/float at patch edges; no
   patch outside visibility windows; the continuous shot stays continuous.
7. **Cost:** no full-video reroll was spent to fix ONLY a mouth (that's a rig/staging problem —
   §6). Judge lip-sync defects separately from plate defects in QA notes.

---

## 6. COST DISCIPLINE *(KIE credits are FINITE — the account has hit 402 mid-episode)*

- **Pilot → gate → batch.** ONE line first on any new tool/keyframe/character → full §5 QA →
  **owner verdict** → only then batch the rest. Never auto-batch-and-ship. (This is how OmniHuman
  was safely scoped to Marco and safely banned for Bentley at 3 takes instead of 26.)
- **The 1-REROLL RULE (generative sync):** one reroll, maximum, per shot — and only with a changed
  input (new keyframe, new mask, new seed WITH a diagnosis). If take 2 introduces a NEW canon
  violation, you are in the vicious circle (§0.3): **STOP. Fall back. Do not take spin 3.**
- **Fallback ladder (always available, in order):** rig render (§4c) → restage the beat
  speaker-isolated + VO-over-alive (§2, free) → hold the listener/reaction (free). "No sync shown"
  is a professional answer; a third reroll is not.
- **Reference prices:** rig ≈ $0/line · Avatar ≈ 40 cr/line · OmniHuman ≈ 26 cr/s @720p
  (~137 cr/take observed) · Kling 3.0 no-audio ≈ $0.07/s. Rhubarb timing: free, minutes,
  transcripts already exist.
- **On a 402 (out of credits): stop everything and tell the owner.** Never quietly switch tools or
  queue retries.
- Log every credit spent on talking shots per episode; anything that bought sync a cheaper branch
  could have delivered → flag in the episode retro.

## 7. DEAD ENDS — tested, rejected, DO NOT REBUILD

| Approach | Verdict |
|---|---|
| 2.5D mouth-patch overlay on free-posed video (`bentley/lipsync/` renderer) | Owner-rejected 3× — anatomically wrong on ¾/down/profile heads. Timing layer stays; renderer stays dead. |
| Post-hoc video re-sync (sync.so `sync-2`, latentsync, etc.) | Human-lip trained; barely moves a cartoon muzzle; sync.so's own docs exclude animals. |
| OmniHuman-1.5 on Bentley | 3 takes / 3 canon violations; prompt guards ignored; BANNED (§0.3). Simple characters only. |
| Kling-Avatar on wide/dim/small/side framings | Caricature (bulging eyes, human grin). Tight bright frontal CU only — and only branch A. |
| Kling/Seedance i2v "prompted hard for talking" as a sync method | i2v cannot hear; mouths flap out of time; on multi-char plates it CAUSES the wrong-speaker defect. |
| Chopping scenes into per-line talking-head CUs to get sync | THE owner-rejected failure. Two-shots are the backbone. |
| Blind headless sculpting/deformation scripts | Ballooned muzzle; the reason for rig rule §4c.1. Visual feedback or don't touch the mesh. |
| Flat mouth patches on video, any flavor | Same anatomy failure as row 1, by construction. |

## 8. RED FLAGS — STOP and re-read §0

- "Just one more OmniHuman/Avatar take on Bentley — the last one almost passed."
- "I'll prompt the two-shot with both characters talking; we'll fix the extra mouth later."
- "The overlay is perfectly placed" (placement is not anatomy).
- "The sweep is huge — I spot-checked a few frames."
- "I'll write 'red-fawn paws' just this once."
- "The mouth is only 15 px, but sync would be nice" (waiver exists for a reason).
- "I'll sculpt all nine visemes headless tonight and render in the morning."
- "The catchphrase would sound great in the narrator's voice here."

**Any of these = stop, pick the branch §1 actually prescribes, and if in doubt ask the owner
(approve-direction-first is the standing workflow).**

---
*Cross-refs: `episode-production` (production rulebook; its §0.3/§5 defer here for lip-sync) ·
`cinematic-episode-writer` (stages dialogue mouth-visible) ·
`docs/guides/LIPSYNC_PRO_RESEARCH_2026-07.md` (why) ·
`docs/guides/HIGH_QUALITY_LIPSYNC_SYSTEM_PLAN.md` (rig plan + amendments) ·
`docs/guides/LIPSYNC_SYSTEM_RUNBOOK.md` (retired patch renderer — timing sections still valid) ·
`docs/guides/TALKING_LIPSYNC_METHOD.md` (Avatar CU method) ·
`youtube_vault/Production/Lip-Sync Rig System.md` (vault record).*
