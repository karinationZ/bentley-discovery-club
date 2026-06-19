# Bentley's Discovery Club — SESSION HANDOFF
> Last updated 2026-06-16. Read this first to resume. Pairs with the alternatives research in `VIDEO_TOOL_ALTERNATIVES.md`.

## 1. What this is
**"Bentley's Discovery Club"** — a scalable, profitable kids' (3-12) + parents YouTube animated nature/science franchise. **Bentley** is a female red-fawn Boxer (based on the user's real dog) who helps a creature each episode and learns nature *through her eyes*. Blends Bluey heart + Pixar story + Nat-Geo facts. Built with **Higgsfield AI** (MCP) + ffmpeg post.

## 2. Where we are RIGHT NOW (the important part)
- **Episode 1 "The Voice in the Shell"** is fully written + produced in a first pass, and the **complete ~81s opening movement (Acts 1–3) has been re-produced to the new "everything alive" standard** (live motion + real lip-sync + living water + consistent Bentley/Pip + populated pools + no jitter, no stills). Then 1080p/60 upscaled.
- **Remaining: Acts 4–6** (the vacancy-chain reveal, Pip home + discovery tag, octopus cliffhanger ≈ the back ~2/3 of the episode) still need the same redo.
- **Budget essentially spent** finishing the opening movement (~$0–20 cr left). The Acts 4–6 redo needs a **top-up (~400–450 cr)** at the proven ~120 cr/40s rate.

### Deliverable videos (clickable)
| File | What it is |
|---|---|
| `assets/pilot_shots/hybrid_ep1/opening_redo/work/FULL_OPENING_MOVEMENT_v1.mp4` | ⭐⭐ **THE FLAGSHIP** — the complete ~81s opening movement (Acts 1–3: voice → meet Pip → soft-body science → wrong rescue → not-a-swimmer flip → realization), fully to the new standard. 12 shots, 8 lip-synced. + 1080p/60 upscaled version alongside. THIS is the look + length to match. |
| `assets/pilot_shots/hybrid_ep1/opening_redo/work/OPENING_REDO_v1.mp4` | The first 39s proof (Act 1 only) — superseded by the full movement above. |
| `assets/pilot_shots/hybrid_ep1/work/Bentley_Ep1_HYBRID_720_v1.mp4` | Full 3:35 episode v1 (narrator + dialogue). **Superseded look** — too many Ken-Burns stills ("slideshow"), needs the redo. Story/structure is good. |
| `assets/pilot_shots/pilot/A_cinemastudio_UPSCALED_1080p60.mp4` | The 1080p/60 upscale pilot (the "looks pro" finish proof). |

## 3. The HARD RULES (the quality bar — user's review, non-negotiable)
1. **No static shots >1–2s** — Ken-Burns stills read as a "slideshow." Every beat must be live motion.
2. **Water always moves** when visible (foam, ripples, reflections).
3. **Mouths move during dialogue** (lip-sync — see §4).
4. Characters **blink/breathe/shift** even when silent.
5. **No camera jitter** — never Hailuo auto-pans; use locked-camera models; `deshake` in post if needed.
6. **Bentley visually consistent** every shot (locked element).
7. **Pip visually consistent** every shot (locked element — generic-crab stills broke continuity).
8. **Tide pools populated/alive**, never empty.
9. **Cuts motivated by motion**, not cutting between stills.
10. Premium **1080p/60fps finish** on the locked cut.

## 4. THE WORKING PIPELINE (the recipe that hits the bar — proven on OPENING_REDO_v1)
**Per shot:**
1. **Keyframe** → `generate_image` model `nano_banana_2` (~2.5cr), embed locked elements + restate guards:
   - Bentley `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>` · Pip `<<<752fec82-e78e-4289-8257-07176fcb82e0>>>` · Tidepool `<<<d406065e-7b28-4b52-aa02-1e3290032dc1>>>`
   - ALWAYS: "solid red-fawn legs and all four paws — NO white socks"; "soulful well-proportioned eyes, balanced head — NOT googly"; bake in living-water context.
2. **Animate:**
   - **Non-talking shots → `cinematic_studio_3_0`** (30cr/6s) — living water, smooth, prompt "locked static camera, no shake." This is the jitter-free, alive look.
   - **Talking shots → `wan2_7` lip-sync** (~9cr) — see the audio-upload trick below. Mouth syncs + character stays alive.
3. **Finish:** `upscale_video` (bytedance, fps=60, target 1080p) — the single biggest "looks pro" step. ~free–cheap.
4. **Post (ffmpeg):** normalize all to 1280x720@24 → concat → layer narration + dialogue + music → warm grade (`eq` + `colorbalance`) → loudnorm. NO freeze-pad, NO Ken-Burns-as-primary.

**⚠️ LIP-SYNC — the unlock (Wan 2.7 / Seedance 2.0):** audio MUST be an **uploaded media_id, not an audio-gen job id** (job-id → "Something went wrong" every time). Flow: generate VO → `media_upload(filename,"audio/wav")` → `curl -X PUT --data-binary @file '<upload_url>'` → `media_confirm(type:audio, media_id)` → pass media_id as the **`audio` role** (shows `type:"audio_input"`). Lip-sync to the **RAW** (un-tempo'd) VO and use that same raw audio in the mix. Wan returns video with dialogue baked in.

**Other gotchas:** Inworld voices need the **" (en)" suffix** ("Abby (en)", "Snik (en)", "Theodore (en)"). `select_workspace` first or false "out of credits." **Max 6 concurrent** gen jobs (video+audio+music all count) — batch ≤6. This ffmpeg build LACKS `drawtext` + `vidstab` (has `deshake`).

## 5. The OPENING REDO recipe (exact template to replicate for every scene)
6 shots, ~120cr, 39s: (1) Cinema Studio shell+foam establisher · (2) **Wan** Bentley reacts "A voice? Somebody needs help!" · (3) Cinema Studio Bentley tracking · (4) Cinema Studio reveal Pip · (5) **Wan** Pip "Don't squish me!" · (6) **Wan** two-shot Bentley reassures. Narration N01-N03 (Theodore) fitted over the Cinema Studio shots; Wan shots carry synced dialogue; faint O.S. "hello?"; music bed; warm grade.
- Keyframes used: `assets/pilot_shots/hybrid_ep1/opening_redo/keyframes/` (KA_shell, KB_tracking, KC_pipcrack, KD_pipcu, KE_twoshot).
- Uploaded audio media_ids (lip-sync): B_hear `ba79f93f...`, P_meet `2081830f...`, B_rush `deb1ce13...`.

## 6. THE OPEN DECISION (what to do next)
The opening proves the standard at **~120 cr / 40s**. Full 3:35 episode to this bar ≈ **~650 cr**. Balance ~113 cr → **needs a top-up.** Options the user was weighing:
- **(A) Top up (~550+ cr) → full-episode redo** on the §4 pipeline (the goal). ~28 shots: ~8-10 Cinema Studio hero/water + ~10 Wan talking + reuse where still good, then 1080p/60 finish.
- **(B) Redo worst scenes within ~113 cr** — the frozen-ocean/jitter scenes + the 1:52 "older Bentley" collar shot; rest stays v1.
- **(C) Pause** (current state) — bank the new opening, resume later. ← we are here.

## 7. Key reference docs (already written)
- `Bentley_Season1_MD_Files/Bentley_PERFORMANCE_BIBLE.md` — Bentley's 6 signature moves, voice, catchphrases, star rules.
- `Bentley_Season1_MD_Files/PRODUCTION_UPGRADE_PLAN.md` — the full strategy (Bentley=star, hybrid format, tiered pipeline).
- `Bentley_Season1_MD_Files/Episode_1_HYBRID_ASSEMBLY_TIMELINE.md` — the 30-utterance Ep1 cut spec (narrator + dialogue).
- `Bentley_Season1_MD_Files/Episode_1_GRANDPA_NARRATED_FULL.md` — the 20-line narrator script + science spine (vacancy chain).
- `assets/character_design/LOCKED_ELEMENTS.md` — canonical look + element IDs + all guards.
- Memory: `~/.claude/.../memory/` — higgsfield-quality-pipeline, -cost-optimization, seedance-gotchas, bentley-discovery-club.

## 8. To resume in one line
Decide §6 budget → if full redo, replicate the §5 recipe across the Ep1 scenes using §4 pipeline (Cinema Studio + Wan lip-sync + locked elements), then assemble per the ASSEMBLY_TIMELINE and 1080p/60 finish.
