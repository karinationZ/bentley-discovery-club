# EP2 — Story-Repair EDL / Cue Sheet (v8)
**"The Octopus Escape Artist" · Season 1 Ep 2 · rewrite of the edit, NOT a re-render of the animation.**
Authored 2026-06-23. Supersedes the v7 assembly (`scratch/ep2/final_v7/assemble_v7.py`).
Status: **v9 BUILT & DELIVERED** → `scratch/ep2/final_delivery/EP2_v9_FINAL.mp4` (3:34, 1080p). Total KIE spend: 106 credits (BRIDGE-1 only).

**v9 revision (2026-06-23, after owner review of v8):** Owner found v8 regressed vs v7 in finish quality. Root causes + fixes, all in `scratch/ep2/final_v8/` (`rerecord_v9.py` + `assemble_v9.py` + `mix_v9.py`):
- **Dialogue** rewritten by a story-editor agent (10 lines re-recorded, ElevenLabs): `B_realize` (clearer eel), `I_stopped`→`I_creep`, `B_snackpouch`, `I_confess` (drop "open water gone wrong"), `B_colorgame` (names the colour match), `N_hearts` (cozy closer); NEW `B_eel`, `N_shadow` (eel "awake again" bridges its return), `I_colorturn`; `I_hide` re-recorded upbeat (banned dark line scrubbed). Catchphrase confirmed Bentley-only.
- **Quality**: v8's 6–7 re-encode passes → **2** (one pass per beat: trim+retime+concat+grade+VO; concat by copy; one final encode in mix). Killed the softness.
- **Freezes** (0:10, 0:28): clone-pad holds → gentle ≤1.35× retime.
- **Pale/dark** (#11, #14): dropped the aggressive per-shot auto-grade; small per-beat lift only on genuinely dark beats.
- **Camo** (#4 distorted): the procedural dissolve was a regression → clean real footage. **Hearts** (#19 on black): removed the gfx → warm Bentley+Indi closer + a real point→turn→ants transition.
- **Loop** (#18): de-duped squeeze/reform. **Red paws** (#13): avoided `a3_20_twoshot` (bright-red socks).
Lesson: do NOT substitute procedural PIL/ffmpeg gfx for real rendered footage, and minimize re-encode generations.

## Why this exists
The v7 cut (`scratch/ep2/final_delivery/EP2_FINAL.mp4`, 3:03) has strong animation but reads as "a collection of clips, not a story." Root cause is in the **edit + audio layer**, not the shots:
- Every cut dips to **black** (each segment is faded in/out to black, then concatenated).
- The same source clips are **reused/looped** (rock-eye, lunge, reform).
- **Four recorded lines were dropped** (`B_hook1`, `B_help`, `N_taste`, `N_friends`), so the story loses its connective tissue and the Act-2 danger is *narrated but never shown*.
- Long speeches play over **multi-clip montages of non-talking shots**, so characters never look like they're speaking and scenes seem to interrupt themselves.

**The full story is already recorded** (25 VO lines, see `scratch/ep2/make_vo.py`, canonical `ORDER`) and **the shots already exist**. This EDL re-cuts them into the scripted order with real transitions. Only **1 shot must be generated** (the Act-2 causal connector); 1 more is optional.

## Build principles (the policy this cut obeys)
1. **No black-dip cuts.** Default transition is a hard **CUT**. Crossfades (~0.4s) only for time/place jumps and the emotional settle. Exactly one fade-in (open) and one fade-out (end).
2. **One clip = one beat.** No clip plays twice. Where a callback is wanted (the eel shadow), use a *different sub-range* of the source, never the same frames.
3. **VO-over, character alive.** Every line plays over a shot of the **speaking** character, who is breathing/moving the whole line. No mid-line cut away from a speaker. No AI lip-sync (keeps the no-human-teeth / identity-safe rule).
4. **No frozen stills, no extreme slow-mo.** Prefer the motion clip over a held still; never stretch a clip past ~1.3× (kills the 2:11 lag). If VO outlasts a clip, add a second angle/CU, don't slow it down.
5. **Restore the dropped lines** and follow the recorded `ORDER`.
6. **Keep the v7 grade** (per-shot normalize toward V57/S32 daylight; mood shots — eel lair, underwater bolt — exempt). Owner praised the look; don't regress it.
7. **Catchphrase is always Bentley's voice** (`B_stoplook`), never the narrator (canon).

## Source legend
`V7` = `scratch/ep2/final_v7/motion/` (approved, on-model Bentley) · `OLD` = `assets/pilot_shots/ep2/motion/` · `SCR` = `scratch/ep2/motion/` · `KF` = `scratch/ep2/final_v7/keyframes/` · `BRIDGE` = must generate (see below).
Trans: `C` cut · `X` crossfade · `M` match-cut · `FI` fade-in (open) · `FO` fade-out (end).

## Cue sheet

### COLD OPEN — "The rock had an eyeball"
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|1|Title over live tide pool|`OLD/plate_live` + title|—|4.0|FI|the only opening fade|
|2|Bentley spots & boops the "rock"|`V7/a0_02_boop`|`B_hook1`|5.6|C|**restored** cold-open line|
|3|Rock snaps open one EYE → ink puff|`SCR/s03_rock_eye_motion`|— (sfx)|2.5|M|used **once**; match-cut on the ink|
|4|Bentley blinks in the ink|`SCR/bentley_cu_awe_motion`|`B_hook2`|2.7|C|fresh reaction (not the realize clip)|

### ACT ONE — The Chase
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|5|Narrator sets up Bentley + the Tag|`V7/a1_07_chase` (range A)|`N_intro`|5.6|C|over chase action|
|6|"Gotcha! …Rock. Gotcha—!"|`V7/a1_07_chase` (range B)|`B_chase`|4.9|C|distinct sub-range from #5|
|7|A "rock" squirts water → "rude"|*verify squirt source in chase/boop*|`B_rude`|2.0|C|**VERIFY**; tiny insert if none|
|8|Camo science: color **and** texture change|`BRIDGE-2` *or* improved procedural|`N_camo`|5.4|C|grey→gold, smooth→spiky, melts into rock|
|9|Bentley lunges at a curling arm|`V7/a1_09_lunge`|—|3.0|M||
|10|Indi gone; a neat spiral shell remains|lunge tail / shell insert|— (sfx)|2.0|C|Bentley tilts head|

### ACT TWO — It Gets Worse  *(the causal hinge — the #1 story fix)*
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|11|Bentley corners Indi; eyespots flare|`V7/a2_10_corner_v2`|`B_help`|2.9|C|**restored** — the chase is about *helping*|
|12|Indi panics, bolts toward a lair|`OLD/a2_11_bolt`|— (sfx)|2.5|C||
|13|Indi flees **straight into the eel's path**|**BRIDGE-1**|— (sfx)|3.0|X|**THE causal connector** — Indi + eel in one frame|
|14|The moray eel stirs, jaw open|`OLD/a2_12_eelstir`|— (sfx)|2.0|C|reads as threat, not a smile|
|15|"…I chased her right at it."|`V7/a2_13_realize`|`B_realize`|1.9|C|now lands **with** setup|

### ACT THREE — The Turn
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|16|Bentley stills; Listening Tag GLOWS|`V7/a3_14_stoplook`|`B_stoplook`|3.4|C|catchphrase = Bentley|
|17|Indi creeps out of the dark|`SCR/s14_emergence_motion` (A)|—|2.5|X|water settles|
|18|"…You stopped."|`SCR/s14_emergence_motion` (B)|`I_stopped`|0.9|C|over a clear **Indi** shot (fixes "whose voice")|
|19|"Why do you keep hiding?"|`V7/a3_18_why`|`B_why`|1.6|C||
|20|"I'm the hide-and-seek CHAMPION!"|`SCR/s16a_colorgame_motion` (+slow push)|`I_hide`|11.3|C|Indi alive, **no** mid-line cut to Bentley|
|21|"Well, I'm not leaving… champ."|`V7/a3_21_snackpouch`|`B_snackpouch`|6.9|C|now follows the champion line logically|
|22|A shy tentacle curls around her paw|`V7/a5_30_pawhold` + CU|`N_taste`|13.8|C|**restored** science; paw-hold no longer silent|
|23|"I wasn't running from *you*…"|`SCR/s16_exchange` + reform|`I_confess`|14.3|C|Indi alive & clearly speaking; ≤1 shell cutaway|

### ACT THREE-AND-A-HALF — The Color Game (bonding)
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|24|Indi blushes warm red-fawn|`V7/a3_23_colorchange`|—|3.0|C||
|25|"You did *ME!* You're a tiny ME!"|`V7/a3_24_youdidme`|`B_colorgame`|6.4|C||
|26|They play — giddy bonding two-shot|`V7/a3_20_twoshot`|`N_friends`|6.9|C|**restored**; satisfies the bonding-two-shot rule|

### ACT FOUR — The Escape Artist
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|27|A shadow returns|`OLD/a2_12_eelstir` (range C)|— (sfx)|1.2|X|callback — **different range**, not a loop|
|28|Indi wedges tight in a too-small gap|`V7/a4_25_wedged_v2.mp4`|`I_hurt`|2.5|C|**motion**, not the still|
|29|"You don't have bones… just breathe."|`V7/a4_27_breathe`|`B_breathe`|9.4|C|natural speed; CU insert if VO outlasts|
|30|Indi pours through the coin-sized gap|`SCR/s20_squeeze_motion`|—|3.0|C|**real squeeze** (fixes the loop)|
|31|Boneless science|`SCR/s20_squeeze` → `OLD/a4_29_reform`|`N_boneless`|5.4|C|over squeeze→reform|
|32|She reforms, whole, on the far side|`OLD/a4_29_reform`|—|2.0|C||

### ACT FIVE — The Button
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|33|"I *see* you. You're amazing."|`V7/a5_31_button`|`B_button`|9.8|C||
|34|Three-hearts science|`OLD/a5_32_science` + new motion-graphic|`N_hearts`|4.7|C|replace the cheap drawn hearts|

### TAG / CLIFFHANGER → EP3
| # | Beat | Picture | VO | ~s | T | Notes |
|--|------|---------|----|----|---|-------|
|35|Indi presses a shell: "There's a gathering."|`OLD/a6_34_ants` (A)|`I_gathering`|3.7|C||
|36|A line of ants carries a crumb the size of a car|`OLD/a6_34_ants` (B)|— (sfx)|3.0|C||
|37|"Where are you all *GOING?*"|`V7/a6_35_whereGoing`|`B_ants`|2.5|C||
|38|NEXT TIME card|card|—|3.0|X|"The Ant City Beneath Our Feet"|
|39|Outro / subscribe|card|`N_outro` (+ optional `B_stoplook` reprise)|5.0|FO|closing fade; catchphrase stays Bentley|

## Bridge shots to generate (the only new renders)
**BRIDGE-1 — REQUIRED — "Indi into the eel's path" (beat 13).** One ~3–5s shot: the small purple two-spot octopus (Indi, teal eyespots, per `assets/character_design/Indi_LOCKED.png`) darts low across the sand toward a dark reef crevice where a moray eel's silhouette looms, jaw parting, clearly *aimed at her*. Soft/menacing, ages 4–8, no gore. Tide-pool palette to match shots 12/14. **This is the shot that makes the danger real and fixes issues #3, #9, #10.** Generate per the locked pipeline (Kling 3.0 + element refs), 4–8 candidates, hand-pick, no auto-batch.

**BRIDGE-2 — OPTIONAL — camo color/texture change demo (beat 8).** Indi's skin visibly shifting grey→gold and smooth→bumpy, melting into rock "in the blink of an eye." *Decision:* generate a real transformation shot, **or** keep an improved procedural texture-morph over the locked still (zero KIE). Recommend trying the improved procedural first; generate only if it doesn't read.

Everything else uses existing footage. The "static octopus" (#12/#17), "looping coin/reform" (#21), and "cheap hearts" (#22) issues are fixed by **using the live clips + a better motion-graphic**, not by re-rendering.

## Runtime
Speech = 138s. With action beats + breathing room and the loops/over-stretches removed, the complete-story cut lands **~3:05–3:25** — roughly the v7 length, but with **zero filler**: the restored lines replace the padding rather than adding to it.

## Issue → fix traceability (owner's 23 notes)
- **#1 rock loop / dark dip** → beat 3 plays the eye clip once; no black-dip (principle 1).
- **#2 black-screen transitions** → principle 1 (cuts/crossfades only).
- **#3 eel disconnected** → BRIDGE-1 + beats 11–15 rebuilt as a causal unit.
- **#4, #5, #8 abrupt transitions** → principle 1 + match-cuts (beats 3, 9).
- **#6 weird color change** → BRIDGE-2 / improved camo demo (beat 8).
- **#7 reused water-play / lunge** → principle 2; distinct sub-ranges (beats 5/6), lunge once (9).
- **#9 no narration 0:47–0:54** → `B_help` restored (11) + Act-2 re-scored.
- **#10 "she chased her…" out of blue** → setup beats 11–14 precede `B_realize` (15).
- **#11 line cut off** → trim to speech-end, not to a clip boundary.
- **#12, #17 static octopus** → live Indi clips (17, 20, 23) instead of stills/zoom.
- **#13 octopus in Bentley's voice** → Indi lines over clear Indi shots (18, 20, 23); voice ids already distinct.
- **#14 line read, no lip move** → VO-over-alive (principle 3); Indi visibly moving under every line.
- **#15 talk scene interrupts itself** → no mid-line cutaways (principle 3) for 20 & 23.
- **#16 "Well I'm not leaving" makes no sense** → re-sequenced to follow `I_hide` (20→21).
- **#18, 2:01 / #2:05 VO off / "now you hear me"** → re-mapped `I_hurt`/`B_breathe` (28–29) with setup.
- **#20 2:11 slow-mo lag** → no >1.3× stretch (principle 4); breathe at natural speed (29).
- **#21 2:22 loop / coin** → real `s20_squeeze_motion` (30).
- **#22 2:43 cheap hearts** → new motion-graphic over live Indi shot (34).
- **#23 2:45 scene from nowhere** → `I_gathering` over the ants reveal with the shell hand-off (35).

## Build steps (after approval; detailed plan via writing-plans)
1. `assemble_v8.py` — drive the cut from this table (data-driven cue list; cut/crossfade/match per row; trim each VO to speech-end; sub-ranges to avoid reuse).
2. Generate **BRIDGE-1** (+ BRIDGE-2 if chosen); hand-QC each frame vs canon; insert.
3. New three-hearts motion-graphic (beat 34).
4. `mix_v8.py` — music beds per act, ambience, SFX, ducking under VO.
5. QA the **final export** end-to-end: black-frame/freeze/loop scan, per-line VO-over-correct-character check, transition check, continuity sheet.
