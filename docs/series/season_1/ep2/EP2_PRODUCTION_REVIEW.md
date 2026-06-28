# EP2 "The Octopus Escape Artist" — Full Production Review
**EP2_v5_FINAL.mp4 · 35 shots / 182s · 7-agent review (Exec Producer, Story Editor, Animation Director, Animation QA, Video Editor, VO/Lip-Sync QA, Continuity QA), 2026-06-22.**
Full specialist reports: workflow output `tasks/wvqb4y8e2.output`. Review material: `/tmp/review/` (contact sheets + per-shot metrics).

## TOP-LINE VERDICT: DO NOT SHIP — reads as stitched clips, not one story
All six specialists independently reached FAIL. Lines/character attribution are correct and the catchphrase ships, but the episode fails on all of the owner's hard-NO axes at once:
1. **Two byte-identical animation reuses** (settle clip @0:17 & 0:53; reform clip @2:19 & 2:39).
2. **Color grade plays as 4+ different films** (brightness V23–71, saturation S15–73, hue swing ~160°).
3. **The Act-2 causal engine does not exist on screen** — the danger is narrated, never shown.
4. **Bentley is TWO different models** intercut (realistic-Boxer in wides/action vs Pixar-chibi in close-ups) + broken docked-tail/red-fawn-paw canon nearly everywhere.
Indi is the bright spot — ~90% on-model and shippable (teal eyes approved — do NOT change).

## PRIORITIZED FIX LIST

### P0 — owner hard-NO + cohesion-breaking (fix first)
- **P0-A [RE-RENDER]** Kill REUSE #1: re-render shot 12 `a3_15_settle` (0:53) as a real self-calming beat with Indi still in danger visible. Keep 0:17 as intro.
- **P0-B [RE-RENDER]** Kill REUSE #2: re-render shot 29 `a5_32_science` (2:39) as a dedicated "three hearts" visual (triple-pulse). Keep 2:19 reform.
- **P0-C [FREE EDIT]** ONE color grade, anchored to the Bentley-CU look (**target V57 / S32, neutral daylight**). +20V lift on all 4 Indi talk shots; rescue eelstir (0:48, V23); re-temp the 5 WB offenders (establish, breathe, ants, bolt, eelstir); pull 4 over-bright down; lift 3 pale shots. Re-measure: every story shot V52–63 / S29–36.
- **P0-D [RE-RENDER]** Rebuild the Act-2 hinge (shots 09–12) as a connected unit: (a) chase visibly frightens Indi; (b) Indi flees in fear toward open water; (c) ONE shot with BOTH Indi + eel; (d) Bentley-eyeline sees the danger → "I chased her right at it." Re-sequence the confession (1:33) earlier.
- **P0-E [RE-RENDER+GRADE]** Re-design the eel (shot 10) to read as a threat (open jaw toward Indi, reptilian silhouette) + lift exposure. It currently SMILES.
- **P0-F [RE-RENDER]** Lock ONE Bentley model — conform the realistic-Boxer wide/action shots (boop, chase, lunge, corner, twoshot, colorchange, pawhold) to the cartoony-Pixar master. (Forced by the avatar limit: talking shots can only render Pixar.)

### P1 — visibly rough
- **P1-A** Docked tail on every Bentley shot with a visible tail (long tails everywhere now).
- **P1-B** Remove white paws/toes (boop, chase, lunge, pawhold).
- **P1-C** Add the missing "Indi gets wedged" beat before shot 23.
- **P1-D** Re-render shot 04 reintro to keep the hidden-eye mystery alive.
- **P1-E** Re-grade/re-gen shot 23 wedged (Indi's shader pops matte-grey).
- **P1-F** Break the Bentley talking-head match-jump — re-frame ≥3 of shots 16/22/28/32.
- **P1-G** Break the Indi talking-head match-jump + the 11.6s hide hold (intercut).
- **P1-H** Trim over-long static holds: confess 14.4s (~8s too long), button 9.9s, breathe 9.3s.
- **P1-I** Add real motion to twoshot (SSIM 0.785) + squeeze (0.724).
- **P1-J** Smooth the 0:38–0:53 underwater seams with timing-safe in-place overlaps (after P0-C/D).

### P2 — polish
- Verify shot 17 source `_indi_talk2.mp4` is final; confirm chase carries 2 VO lines OK; rendered title establisher; punch-in on the hidden eye; dip-to-card at 32→33; collar-tag + scale continuity spot-checks.

### Do NOT touch
Indi's teal eyes; Indi's intentional color-change beats (camo, colorchange, youdidme); the ants teaser + end cards; catchphrase shot 13 (ship as-is).

## COHESION VERDICT — the 5 changes that most improve cohesion (impact order)
1. Build the Act-2 hinge so the danger is SHOWN, not narrated (P0-D + P0-E).
2. Lock one Bentley model + docked tail + red-fawn paws (P0-F + P1-A + P1-B).
3. Apply the single Bentley-CU grade across the film (P0-C) — mostly free, kills the per-cut brightness "pumping."
4. Eliminate both byte-identical reuses with purpose-built replacements (P0-A + P0-B).
5. Break the talking-head monotony + dead air (P1-F/G/H).

## SEQUENCING (per Exec Producer)
Re-renders FIRST (P0-A/B/D/E/F + P1 character/framing) → then the grade pass (P0-C, free) → then transitions/trims (P1-J, P2, mixer-coordinated via one EDL). Grading or cutting before re-rendering just re-times footage that's about to be replaced.
