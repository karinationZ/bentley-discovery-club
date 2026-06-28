# EPISODE 1 — "THE VOICE IN THE SHELL"
## MASTER PRODUCTION PLAN (Story Editor's merge — Head Writer + Animation Director + Producer)

> Story Editor's note: This is the single locked production document. It merges the Head Writer's expanded script, the Animation Director's frame-verified visual plan, and the Producer's budget/retention review into one source of truth. Where the three roles disagreed, the Producer's frame-grounded rulings win on **runtime (4:45, not 5:00)**, on the **killed re-gens** (recoil ears, Bentley teeth → verify-only), and on **sound-first sequencing**. The Head Writer's script content and the Animation Director's per-shot visual direction are preserved in full. All element IDs are corrected to the **locked** values in `LOCKED_ELEMENTS.md`: Bentley-MASTER `1c82ee5b-8713-4596-80ec-6ce854502a4d`, Pip-clean `752fec82-e78e-4289-8257-07176fcb82e0`, Tidepool-cove `d406065e-7b28-4b52-aa02-1e3290032dc1`.

---

## EXECUTIVE SUMMARY

Episode 1 expands the existing **2:00 cut into a complete 4:45 episode** that fully lands its emotional spine (Pip's growing-up loneliness + Bentley's "you don't find your home alone" reframe) and its science spine (the **vacancy chain** — when a hermit crab outgrows its shell, the whole tide-pool trades homes up the line), built **reuse-first on all 21 existing rendered shots in order** plus only **6 new shots (~75 cr)** and a near-free narration + sound-design + grade pass. The cheapest, highest-ROI work is **sound** (the current cut opens on 5 s of true silence and goes mute on the 60 s action beat — both fatal retention bugs that cost $0 to fix), so the punch-list runs **sound-first, then the 6 new renders, then the Pip-model keyframe fixes**. The single biggest *visual* problem is that **Pip is currently 3–4 different crabs** (eye-stalks, an angry jagged mouth, a white-nautilus "hero" shell, even human teeth in one frame) — re-keyed to the locked clean Pip on the held close-ups. The new continuity bridge `N3_bridge_safe` (Bentley's wet→dry shake) repairs the one brutal frame-slam, and the resolved Bentley tag is re-ordered to land **before** the octopus so the last face out is the star, not the cliffhanger. Net: tighter, denser, emotionally complete, inside the ~400–450 cr Acts 4–6 top-up already budgeted.

---

## REUSE MAP — all 21 existing shots reused, in order

**Legend:** ✅ reuse-ready · ⚠️ reuse + keyframe fix (no new render; re-key + re-run cheap motion/lip-sync). Shot IDs map to `ep1_acts123.json` / `ep1_acts456.json`.

| # | Existing shot-id | Status | Use in the 4:45 cut |
|---|---|---|---|
| 1 | `a1_01_shell` | ✅ | Cold-open establisher; glow-pulse seeds the Listening-Shell motif |
| 2 | `a1_02_bentley_hear` | ✅ | Bentley hears the cry — Head-Tilt (Bentley-ism #1) |
| 3 | `a1_03_tracking` | ✅ | Bentley tracks the voice (trim 2 s); tail repurposable for the Turn |
| 4 | `a1_04_reveal` | ⚠️ Pip model | Reveal tiny Pip in his cracked shell |
| 5 | `a1_05_pip_meet` | ⚠️ Pip model (worst: stalks+antenna+angry mouth) | Pip's panicked "don't squish me" |
| 6 | `a1_06_twoshot` | ✅ (verify Pip half) | Two-shot — THE scale-lock; Soft-Eyes Lean |
| 7 | `a2_01_pip_correct` | ⚠️ Pip model | Pip: "it's my shell — cracked, too small" |
| 8 | `a2_02_softbody` | ⚠️ Pip model | Soft-body reveal (science + trust beat) |
| 9 | `a3_01_bentley_fix` | ✅ | Bentley's helps-WRONG idea ("back in the sea!") |
| 10 | `a3_02_pip_flip` | ⚠️ Pip model | Pip terror + wave; the teaching-gesture beat |
| 11 | `a3_03_recoil` | ⚠️ verify only (ears OK per frames) | Bentley recoils from the surf crash (soaked) |
| 12 | `a3_04_bentley_stunned` | ✅ (clean once N3 dries her) | Dawning realization |
| 13 | `a4_01_crowd` | ✅ (plate); 🟡 crab family at wide scale | The hermit crabs emerge |
| 14 | `a4_02_lineup` | ✅; 🟡 crab family | Crabs line up biggest→smallest |
| 15 | `a4_03_cascade` | ⚠️ white-nautilus "new shell" → warm spiral | THE vacancy-chain set piece |
| 16 | `a4_04_whoaa` | ✅ verify teeth only | Bentley's WHOAA jaw-drop (Bentley-ism #4) |
| 17 | `a5_01_piphome` | ⚠️ Pip model + human-teeth fix + spiral shell | Pip snug in his new home |
| 18 | `a5_02_pipthanks` | ⚠️ Pip model | Pip's grateful thanks |
| 19 | `a5_03_disco` | ✅ | "That's what the Big Adventures is for" |
| 20 | `a5_04_tag` | ✅ verify teeth only | Franchise tag + Wiggle-Butt rally (Bentley-ism #5) |
| 21 | `a6_01_octopus` | ✅ | Octopus button (cliffhanger, turned into a gag) |

### TOTAL NEW-SHOT COUNT — the budget number

**6 new shots = ~75 cr of new render.**

| Type | Count | Shots | Model | Render |
|---|---|---|---|---|
| **MOTION** | **2** | `N3_bridge_safe`, `N2_shell_science` | Cinema Studio 3.0 (`cinematic_studio_3_0`) + Ken-Burns/Hailuo | ~30 cr + ~3–6 cr |
| **TALKING** | **4** | `N1_bentley_guess`, `N4_pip_lonely`, `N5_bentley_empathy`, `N6_payoff_armor` | Wan 2.7 lip-sync (`wan2_7`) | ~9 cr ea = ~36 cr |
| **TOTAL** | **6** | — | — | **~69–75 cr** + keyframes (~2.5 cr ea, pull 2–3 on hero/risk) |

**Reuse keyframe fixes (re-gen only, NOT new shots — the real hidden cost):** Pip model on **7 shots** (`a1_04, a1_05, a2_01, a2_02, a3_02, a5_01, a5_02`) → triage to the 3 worst held CUs first (`a1_05`/`a2_01` stalks+angry mouth, `a5_01` human-teeth); cascade white-nautilus → warm spiral (`a4_03`). **Killed:** recoil ear re-key (`a3_03`, frames show floppy/acceptable) and Bentley WHOAA/tag teeth re-gen (`a4_04`/`a5_04`, borderline → verify-only, regen ONLY on confirmed human-teeth failure).

---

# 9 NUMBERED DELIVERABLES

## 1. NEW TARGET RUNTIME

**4:45** (285 s). *Producer override of the Head Writer's 5:00.* The episode has ~4:30 of story + ~0:15 breathing room; every 15 s past ~4:30 is measurable drop-off for the 3–5 cohort, and the script's own justification ("hold a 3-year-old to the end") argues for the tighter, denser cut. Banked as a muscular 4:45 with **zero dead air end-to-end** after the sound pass. Built on the proven ~120 cr / 40 s standard set by `FULL_OPENING_MOVEMENT_v1.mp4`.

---

## 2. SCENE-BY-SCENE RUNTIME BREAKDOWN

| Scene / beat | Reused shot-ids / [NEW] | Runtime | Story purpose |
|---|---|---|---|
| **COLD OPEN** — the voice | `a1_01_shell` → `a1_02_bentley_hear` → `a1_03_tracking` (trim 2 s) | **0:00–0:20** (20s) | Hook: a scared voice cries for help by 0:03 over black; Bentley is on the case by 0:12 |
| **ACT 1** — meeting Pip | `a1_04_reveal` → `a1_05_pip_meet` → `a1_06_twoshot` → **[NEW N1_bentley_guess]** | **0:20–0:50** (30s) | Meet Pip (fussy, scared); seed the mis-guess running gag ("snail? tiny knight in armor?") |
| **ACT 2** — secret of the shell 🔬 | `a2_01_pip_correct` → `a2_02_softbody` → **[NEW N2_shell_science]** (≤10 s) | **0:50–1:25** (35s) | Science: hermit crab is soft, borrows a shell, and **the shell doesn't grow with him** — the setup the chain pays off |
| **ACT 3** — wrong rescue + the wave | `a3_01_bentley_fix` → `a3_02_pip_flip` → `a3_03_recoil` → **[NEW N3_bridge_safe]** → `a3_04_bentley_stunned` | **1:25–2:20** (55s) | Bentley helps WRONG (the sea!); Pip explains kid-logic (can't swim, shell floats away); wet→dry bridge; realization |
| **ACT 4** — the heart + the turn ❤️ | **[NEW N4_pip_lonely]** → **[NEW N5_bentley_empathy]** → Turn on `a1_03` tail / held `N5` face | **2:20–2:52** (32s) | Pip's real fear ("I'm scared 'cause I'm growing"); Bentley's "you're just *between shells*… not alone"; Stop·Look·Listen |
| **ACT 5** — ⭐ the vacancy chain 🔬 | `a4_01_crowd` → `a4_02_lineup` → `a4_03_cascade` → `a4_04_whoaa` | **2:52–3:42** (50s) | The wonder/climax: crabs trade homes up the line, click by click; the last shell fits Pip |
| **ACT 6** — home + heart + resolved end | `a5_01_piphome` → `a5_02_pipthanks` → `a5_03_disco` → **[NEW N6_payoff_armor]** → `a5_04_tag` → `a6_01_octopus` | **3:42–4:45** (63s) | Pip home; thanks pays the emotional beat; gag payoff; **Bentley tag last face**; octopus button + next-ep promise |

**Drag-watch flags (both fixed by trims, not new shots):** Act 2 double-science (cap `N2` ≤10 s; ride Bentley's O.S. awe over it) and Act 6 four-part resolution (drop `N6` first if it sags). Act 4 is the #1 under-5 drop-off zone — cap at 32 s, let the collar-glow give kids a moving thing to watch, and let "between shells" lift sad→hope within ~6 s (don't wallow).

---

## 3. ADDITIONAL DIALOGUE RECOMMENDATIONS

New/expanded lines beyond the current 2:00 cut, by scene (speaker · emotion). Voice key: **THEODORE** = warm Nat-Geo grandpa (Inworld "Theodore (en)"); **BENTLEY** = "Abby (en)", bright eager young, +12% tempo; **PIP** = fussy/anxious-sweet, fast nervous patter, self-interrupting.

**COLD OPEN**
- PIP (O.S., from inside the shell, *frightened/trembling*): "…H-help? Is — is anybody out there? Please?" — lands at 0:03 over black.
- PIP (O.S., *anxious*): "It's getting hot out here… and I am NOT okay with that." (plants the heat-stakes)
- BENTLEY (*curious → rallying*): "A voice? Somebody needs help — come on!"
- BENTLEY (*murmuring, sniffing*): "Okay okay okay — this way… little voice, where ARE you…"
- THEODORE **[NEW N02b record]**: "Wherever there's a creature in trouble… that's exactly where Bentley wants to be."

**ACT 1**
- PIP (*panicked/fast*): "Gah! A — a GIANT! Don't squish me, don't eat me, I'm very stringy and I would NOT taste good—!"
- PIP (*indignant, deflating*): "…Lost? I am not *lost.* I know EXACTLY where I am. That is the whole problem." (running gag #1 seed)
- **[NEW N1] BENTLEY** (*playful, rapid-fire*): "Ooh — are you a snail? A teeny tiny knight in shiny armor? A rock that talks?!"
- **[NEW N1] PIP** (*flat, exhausted*): "I'm a *hermit crab.* And the armor is *borrowed.*"
- **[NEW N1] BENTLEY** (*whisper, to camera, thrilled*): "…A talking crab. Best morning EVER."

**ACT 2**
- PIP (*urgent, correcting*): "It's not *me* that's the trouble — it's my *shell.* It's cracked, and it's gotten much too small, and — and ANOTHER thing—" (running gag #2)
- PIP (*shy, vulnerable*): "See? Down here I'm all… soft. No bones, no armor of my own. Without a shell, I'm just a — a snack with feelings."
- BENTLEY (*tender, Soft-Eyes Lean*): "Aww. I would never let you be a snack, Pip."
- THEODORE **[NEW N06 record]**: "When a hermit crab grows, its house does *not.* So it must find a bigger empty shell… and move. A new home, every single time it grows."
- BENTLEY (O.S., over N2, *quiet awe*): "Whoa… a whole new *house* just for getting bigger?" — must ride OVER the diagram so it reads as her wonder, not a lecture.

**ACT 3**
- BENTLEY (*cheerful, certain — dramatic irony*): "Oh! I know! You're a sea creature — so you belong in the SEA! Don't worry, Pip — I'll pop you back in the water!"
- PIP (*immediate dread*): "Wait — no — which water — not the BIG water—?!"
- PIP (*full panic, but EXPLAINING — the teaching moment*): "NO no no — look at it! That's the OPEN surf! I can't *swim* — crabs like me walk, we don't swim! Those waves would smash me on the rocks and tumble me right OUT of my shell — and you SAID it: my shell isn't part of me! It'd float away and I'd be soft and bare and — gone!"
- BENTLEY (*yelping, scrambling back*): "Whoa — okay! Bad idea, bad idea, back we go!"
- THEODORE **[NEW N10a record]**: "Soaked, and a little shaken, Bentley carried Pip back from the edge — up onto the warm, dry rock — and shook the whole ocean right off."
- **[NEW N3] BENTLEY** (*sheepish, shaking off*): "Pblblbh — okay! Note to self: the ocean is NOT a bathtub."
- **[NEW N3] PIP** (*breathless, relieved, fussy callback*): "Thank you. Thank you. We do NOT do the big water. We've discussed this."
- PIP (*small*): "…and I can't fix it myself. I've *tried.* Nothing fits anymore."

**ACT 4**
- **[NEW N4] PIP** (*quiet, the real fear under the fussing*): "I'm not scared of being stuck, Bentley. I'm scared 'cause I'm *growing.* Every day I get a little bigger… and nothing fits anymore… and there's nobody to help me move. So I just… got smaller and smaller inside, and called for help, and hoped."
- **[NEW N5] BENTLEY** (*gentle, sincere*): "Hey. Hey — you're not too small, Pip. You're just *between shells.* …And you don't have to find your home alone. That's the whole point of a friend."
- **[NEW N5] BENTLEY** (*brightening, the reframe*): "Complicated's just a wonder we haven't figured out yet. So let's figure it out — together."
- THEODORE (N11): "…So Bentley did the bravest thing of all… she stopped. She looked. And she *listened.*"
- BENTLEY (*settling, calm*): "Stop… look… listen."

**ACT 5**
- PIP (*realizing, hope flickering*): "Wait… it's — it's a SHELL day. They only come out for a shell day…" — best curiosity gap; plants 10 s before the cascade pays it off.
- BENTLEY (O.S., *building*): "One moves… and they ALL move… ohh—!"
- THEODORE (N16): "Scientists call it a *vacancy chain* — a whole neighborhood, trading homes all at once. And it's *real.* The very last shell… fit Pip perfectly."
- BENTLEY (*exploding, to camera*): "Whoa! Did you just SEE that?! The whole pool helped! Nobody got left out — they just all… moved up *together!*"

**ACT 6**
- PIP (*soft, moved + last fussy callback*): "It fits. It actually… *fits.* Thank you, Bentley. You were the first one who really *listened.* …And ANOTHER thing — you can come back any time. I mean it." (running gag #2 pays off warm)
- BENTLEY (*warm*): "That's what the Big Adventures is for."
- **[NEW N6] BENTLEY** (*teasing, fond*): "And hey — turns out I was a *little* bit right. You ARE a tiny knight… in brand-new shiny armor."
- **[NEW N6] PIP** (*gruff-but-pleased*): "…It's a *shell.* …But I'll allow it." (gag also pays partially on this line alone if N6 is cut)
- THEODORE **[NEW N19 revised record]**: "Today, Bentley learned you don't help by *grabbing.* You help by *listening.* Stop… look… listen…"
- BENTLEY (*to camera → rally*): "Stop. Look. Listen… and you'll find the wonder, *everywhere.* Let's go find the WONDER!"
- BENTLEY (O.S., over octopus, *delighted, NOT scared*): "…Wait. Did that octopus just *wave* at me?! Ooh — new friend!"
- THEODORE **[NEW outro tag record]**: "Next time, on Bentley's Big Adventures… *'The Octopus Escape Artist.'* Tap to dive in — and don't forget to follow, so Bentley can find *you* for the next adventure."

**Theodore lines to record (rest of N-set exists):** N02b, N06, N10a, revised N19, outro tag. Lip-sync every Wan talking shot to the **RAW (un-tempo'd) VO** and reuse that same raw audio in the mix (per HANDOFF §4).

---

## 4. NEW SCENES TO ADD (itemized — the cost driver, kept minimal)

6 new shots only. All 21 existing shots carry the rest; the +2:45 over the current cut is bought mostly with narration + sound + Ken-Burns + reaction-trims of existing shots.

| # | ID | Motion / Talk · Model | One-line description |
|---|---|---|---|
| 1 | `N1_bentley_guess` | **Talk** · Wan ~9 cr | Bentley CU, delighted head-tilt the *other* way; rapid-fire mis-guesses ("snail? tiny knight in armor?") + 4th-wall "best morning ever" — seeds running gag #1 |
| 2 | `N2_shell_science` | **Motion** (no character) · Ken-Burns on a `nano_banana_2` still OR Hailuo, ~3–6 cr, **≤10 s** | Illustrative insert: empty dull spiral shell → a bigger empty spiral beside it, soft glow-thread linking small→big, one water lap — teaches "the shell doesn't grow with you" before the wave |
| 3 | `N3_bridge_safe` | **Motion** (Bentley+Pip) · **Cinema Studio 3.0 ~30 cr** | Dripping Bentley sets Pip on a high dry sun-warm rock and does a full-body water-shake (droplet arc, fur slicked→fluffy) — the **wet→dry continuity bridge** that fixes the frame-slam; lands a laugh |
| 4 | `N4_pip_lonely` | **Talk** · Wan ~9 cr | Pip CU, the genuine emotional beat — frightened/lonely, not angry: "I'm scared 'cause I'm growing… nothing fits… nobody to help me move." The emotional floor |
| 5 | `N5_bentley_empathy` | **Talk** · Wan ~9 cr | Bentley CU, Soft-Eyes Lean, eyes welling — "you're not too small, you're just *between shells*… you don't do it alone." The heart-line / parent-retention shot |
| 6 | `N6_payoff_armor` | **Talk** · Wan ~9 cr | Bentley CU, playful callback grin — "you ARE a tiny knight… in brand-new shiny armor" — pays off the Act-1 gag. **First to cut if Act 6 drags or budget tightens** |

**Itemized cost:** 4× Wan talking (~36 cr) + 1× Cinema Studio bridge (~30 cr) + 1× Ken-Burns/Hailuo insert (~3–6 cr) = **~69–75 cr** + keyframes. Comfortably inside the ~400–450 cr Acts 4–6 top-up.

---

## 5. TRANSITION IMPROVEMENTS

Every cut motivated by motion, eyeline, or a sound bridge — no hard cut between two static frames (HANDOFF hard rule #9). This is what turns 27 disconnected clips into one continuous golden-dawn film.

1. **Black → match-cut on the GLOW** — the shell's glow-pulse motivates the cut to Bentley's eye catching the same warm light. Pip's voice continues O.S. across the cut.
2. **Bentley hears → whip / motion-match on her head-pivot** toward the sound (screen-left, where she'll travel). Theodore N02 bridges the cut.
3. **Tracking → push-in on her downward eyeline** — she lowers her nose toward a rock → cut into the Pip reveal (we see what she sees).
4. **Reveal → reaction cut** — her looming approach triggers Pip's panic → hard cut to his scared CU.
5. **Pip scared → widen to the two-shot** as Bentley leans in (warmth answers fear).
6. **Two-shot → push to her guess CU** (N1) on her delighted "ooh!"
7. **N1 → reaction cut** to Pip's deadpan "I'm a hermit crab." Sound bridge: her whispered "best morning ever" tails under his correction.
8. **Pip correct → match-cut on the cracked shell** (claw-tap → soft-body lift; we go closer/inside).
9. **Soft-body → cut to Bentley's reaction** ("I would never let you be a snack") → Theodore bridges into the science.
10. **N2 science insert → her O.S. awe carries us back** to live action / Act 3.
11. **Bentley fix → hard cut to the looming wave** (the rush collides with reality).
12. **Pip flip → wave CRASH cut** to Bentley's recoil.
13. **Recoil → DIRECT continuous into N3** — **no cut to dry.** She's soaked at the end of the recoil and soaked at the start of N3. (This is the fix for the slam.)
14. **N3 shake = the wet→dry bridge** → settles into stillness → cut to `a3_04` (now dry-to-dry, continuity-clean).
15. **a3_04 stunned → cross-dissolve, music thins** → into the intimate Act 4.
16. **N4 Pip lonely → reaction cut to N5** — the piano carries both faces; no music change across the cut (so the two CUs read as one shared moment in the same light).
17. **N5 empathy → the collar glow blooms** → into the Stop·Look·Listen turn.
18. **Turn → on Bentley's eyes OPENING, cut wide to the crowd** (she opens her eyes → SEES the wonder). Sound bridge: the first faint shell-clicks rise under the cut.
19. **Crowd → cut tighter to the lineup** (chaos organizes).
20. **Lineup → the new shell appears** → into the cascade.
21. **Cascade → move/cut on each CLICK** so the chain reads as a satisfying rhythm; on the final click, **SMASH to the WHOAA**.
22. **WHOAA → cross-dissolve to Pip home** (the wonder pays off in Pip's safety).
23. **Pip home → he looks up → cut to** Pip's thanks.
24. **Thanks → cut to disco** → grin tips into the N6 gag.
25. **N6 → she turns to camera → into the TAG** (the real ending; last face = Bentley).
26. **TAG → whip on the peak of her rally → octopus button** → end card (2-note motif → theme bed). The octopus is now a button AFTER the resolved tag, not the finale.

---

## 6. MUSIC & SOUND DESIGN RECOMMENDATIONS

The cheapest, highest-impact work in the episode. A strong **−13.7 LUFS** bed already exists — the problem is **three silence holes** (0–5 s true digital silence; gaps at ~9–12 s and ~60 s) and **no emotional state-changes scored to the story**. Fix the holes + score the turns + lay the collar-glow leitmotif. Ducking per HANDOFF: narration at 0 dB, music **−8 dB under Theodore and all dialogue**, **−16 dB** bed when nobody speaks, full swell at the cascade (3:30) and the tag (4:40). Generate VO/SFX/music via ElevenLabs/Inworld; assemble in ffmpeg (this build lacks `drawtext`/`vidstab`, has `deshake`).

### Score state-changes (where the music turns)

| Timecode | State | Cue |
|---|---|---|
| **0:00** | CALM / MYSTERY | Sparse — ocean wash, lone gull, the **2-note "wonder" motif** as a lonely sting under Pip's "Help?" Music almost absent; let the cry land. **(Fills the 0–5 s silence — the #1 fix.)** |
| **0:16** | ADVENTURE (lift) | 2-note motif blooms into a light curious adventure bed as Bentley tracks. First real musical energy. |
| **0:55** | DISCOVERY (curious) | Warm inquisitive woodwind under the shell science — "learning a secret" color, NOT lecture-flat. |
| **1:35** | RISING TENSION | Low surf rumble creeps in under "I'll pop you back in the water" (foreshadow). Collar glow DIMS → motif drops out (she's stopped listening). |
| **1:44–2:08** | SUSPENSE / DANGER (peak) | The wave beat — big, percussive, the only scary moment — resolves with the N3 shake (comedy release). **This is where the current ~60 s SILENCE is — the action beat is mute. The worst dead-air hole; must be scored + SFX'd.** |
| **2:20** | THINNING / INTROSPECTIVE | Music pulls back as realization dawns. |
| **2:35** | EMOTIONAL (the heart) | **Drop to intimate solo piano + held strings.** World goes quiet — just gentle water. The emotional floor. |
| **3:05** | THE TURN (held breath) | Music *holds* — a suspended chord under "Stop. Look. Listen." Collar shell blooms to full glow + soft "listening" chime. |
| **3:10–3:48** | DISCOVERY → BUILDING WONDER | The chain builds; music swells with each click; **the clicks are scored as rhythmic percussion** (signature sound moment). |
| **3:48** | TRIUMPHANT (the WHOAA) | Full wonder-theme hit on the jaw-drop. The peak. |
| **4:05–4:40** | WARM RESOLUTION | Theme settles into a warm satisfied major bed under home/thanks/tag. |
| **4:40** | TRIUMPHANT BUTTON | Full warm theme SWELL on the rally ("Let's go find the WONDER!") — the earned ending on Bentley's face. |
| **4:50** | MYSTERY STING → THEME BED | 2-note motif returns on the octopus, then warm theme bed under the end card. Loop closes. |

### Immersive SFX (per beat — the "alive" layer)
- **Continuous bed (entire episode):** ocean wash + gentle dawn ambience under everything — **this alone fills the 9–12 s and 60 s gaps.** Lonely gull punctuation in wides.
- **0:00:** shell-chime (the glow); Pip's voice echoing *out of the shell* (small, reverby).
- **0:16:** Bentley's nails/pads on wet rock, ear-flaps, sniffing.
- **0:30:** tiny nervous Pip skitter; the looming-shadow "whoosh."
- **1:44:** wave RISE (building roar).
- **1:56–2:08:** **big wave CRASH, spray hiss, foam surge, claws skittering on wet rock** (the action SFX currently MISSING) → then the **comedy shake SFX** ("pblblbh" + droplet patter) at 2:08.
- **3:30:** **rhythmic shell CLICKS as scored percussion** — let them land like music. The key SFX moment.
- **3:48:** sparkle/shimmer on the WHOAA catch-lights.
- **4:40:** collar-glow chime at full bloom on "Stop. Look. Listen."
- **4:50:** soft water-curl + subtle "mysterious" sub-bass on the octopus.
- **Collar-shell chime = recurring leitmotif** — the *same* chime every time it glows (cold open, soft-body, the turn, Pip's thanks). Ties the episode together for ~$0.

---

## 7. ANIMATION RECOMMENDATIONS

### Continuity bible (one-world rules — every shot)
- **Time of day: locked golden dawn, never advancing** — the whole episode is ONE continuous morning. New shots inherit the same low warm raking sun.
- **One grade:** warm teal-orange, low contrast, soft (warm golden rim on wet rock + fur; cool teal in shadow/water). Apply identical `eq` + `colorbalance` across all 27 shots as the final pass.
- **Sun direction constant: low at frame-RIGHT.** Bentley's key from screen-right, cool fill on her screen-left. Never flip the light between cuts.
- **Scale lock:** Pip ≈ the size of Bentley's eye (golf-ball-in-shell). Bentley DWARFS Pip; Pip sits on a rock that brings him toward her muzzle. Established once in `a1_06`, honored everywhere — especially `N3` where she carries him.
- **Geography lock:** open SURF (crashing white water) always screen-LEFT/background = danger; safe tide pool (glassy, shells on the bottom) always screen-RIGHT/foreground = safe. The high dry rock in `N3` is camera-RIGHT. Left=danger / right=safe lets a 3-year-old read geography subconsciously.
- **The Listening Shell motif:** Bentley's collar shell glows softly ONLY when someone truly listens. Faint glow in the cold open → dims through the rushing/helps-wrong beats → blooms at "Stop. Look. Listen." (Act 4) and again on Pip's "you really listened" (Act 6).

### Global "alive" layer (kill the dead-world feel — every shot)
- **Water always moves:** rolling foam in surf, glassy ripples + sky reflection in the pool, a slow lap every ~3 s. Never a frozen surface (hard rule #2).
- **Air:** thin dawn mist drifting screen-right→left in wides; tiny floating sparkle in light shafts.
- **Background life:** 2–3 distant scuttling crabs, a swaying anemone, a sea star, a far gull in wides (the crowd plate already has this — match it elsewhere).
- **Micro-life on characters even when silent (hard rule #4):** Bentley always blinks/breathes, ear-flicks, micro weight-shifts, tail-stub wags; Pip's legs/eyes never fully freeze. NO frozen talking heads, NO mannequin pauses.

### Character acting & expressions (where to spend the attention)
1. **`N5_bentley_empathy` (the heart-line)** — THE shot a co-viewing parent stays for. Soft-Eyes Lean, eyes welling, sad→hope re-light on "between shells." If one new shot gets 3 takes, it's this one.
2. **`N4_pip_lonely` (the confession)** — Pip's real voice under the fussing: small, contained, wet eyes, slow (not the fast patter). Must read frightened-not-angry — the opposite of the current `f_31s` angry-jagged-mouth Pip.
3. **`a4_04` WHOAA (the franchise reaction)** — jaw-drop is the money shot; revere it, hold it, let the wow land. **Verify teeth frame-by-frame.**
4. **`N3_bridge_safe` (the shake)** — the single most important *motion* in the episode: load-bearing for continuity AND the biggest laugh. Cinema Studio 3.0, the hero motion model.
5. **`a3_02` Pip flip (the teaching gesture)** — Pip must physically act out the kid-logic: gesture to wave (danger) → gesture to soft body (vulnerable) → mime the shell floating away. This is what finally makes the muddy wave-beat clear.

### Camera
Locked, jitter-free cameras only (never Hailuo auto-pan; `deshake` in post if needed — hard rule #5). Let HER move, not the camera, on the CUs. Push-ins are slow and motivated by eyeline. The cascade is the one place to let a lateral move down the line breathe on each click. The WHOAA holds. The tag holds on Bentley's face for the full catchphrase before the rally.

### Bentley screen-time (Performance Bible rules — target ~70%)
- **She opens and closes every scene** (rule #1: first-face-in / last-face-out — confirm on every act, and the episode's last face is Bentley on the tag, not the octopus).
- **After EVERY reveal/fact, cut to Bentley reacting** (rule #2 — her face discovering the fact IS the shot): the soft-body reveal, the N2 diagram, the crowd, the cascade. These reaction inserts trim from existing `a1_06` / `a5_03` / `a4_04` — **no new render.**
- **Bentley O.S. awe over the no-character beats** (N2 diagram, the crowd wide) so she's present even off-screen.
- **Bentley-isms hit (need ≥3, we have 5):** Head-Tilt (0:10) · Soft-Eyes Lean (0:36 + 2:52) · Stop·Look·Listen + collar glow (3:05) · WHOAA jaw-drop (3:48) · Wiggle-Butt + Paw-Stamp rally (4:40).

### Locked guards on every keyframe (the model-faithful chain: the avatar/motion model reproduces whatever the keyframe shows)
- **Bentley** `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>`: floppy folded ears ALWAYS DOWN (never up/pricked/erect); white ONLY on chest blaze (NO white socks/feet — negate explicitly in the motion prompt); short docked stubby tail; **natural dog mouth + soft pink tongue + small dog teeth — NO human teeth, NO human grin** (the #1 failure on wide-open CUs — pull 2–3 takes, favor partial opens, REJECT any human teeth); soulful well-proportioned eyes (never "big eyes"); female neutral underside on any low angle.
- **Pip** `<<<752fec82-e78e-4289-8257-07176fcb82e0>>>`: big soulful eyes set in the face (**NO eye-stalks**), dull cracked brown **SPIRAL** shell (NOT a dome/headphone or white nautilus), reddish-orange body, clean face (**NO antennae, NO whiskers**). Reject the variant-B stalk-eye/angry-jagged-mouth drift and the variant-A dome shell.
- **Trim** every talking clip to speech length +~0.2 s (avatar clips render long → silent mouth-flap); pin each line's audio to its shot's exact frame position to avoid A/V drift.

---

## 8. PRODUCER FEEDBACK ON RETENTION & ENGAGEMENT

**Hook (first 5 s):** guaranteed once the silence is filled. Pip's "Help?" at 0:03 over black + ocean + gull + 2-note sting; Bentley on the case by 0:12. **The current cut is SILENT for 5 s — a silent open on a kids' channel = instant swipe. Filling the cold-open audio is the highest-ROI change in the entire review and costs $0 in render. Do it first.**

**Predicted drop-off points (in order of risk) + fixes:**
1. **0:00–0:05 the silent open** — *the killer.* Fix: cold-open audio (above). Free.
2. **2:20–2:52 the emotional beat (N4→N5)** — two quiet talking heads + piano is where 3–5s wander. Make the **collar-glow visible and building** during N5 so even a 3-year-old has a moving thing to watch; **cap the beat at 32 s**; let "between shells" lift sad→hope within ~6 s — don't wallow.
3. **0:50–1:25 double science** — soft-body fact + N2 diagram risks "school." Bentley's O.S. awe must ride OVER N2 so it's *her wonder*, not a lecture; keep N2 ≤10 s.
4. **3:42–4:45 the long resolution** — four payoff beats risk an anticlimactic tail. The cascade WHOAA is the real climax; protect the descent — if it sags, **cut `N6_payoff_armor` first** (the gag also pays partly via Pip's "I'll allow it" alone).

**Curiosity gaps / micro-hooks (the retention engine):**
- **0:03 "who's calling for help?"** — answered at the Pip reveal (0:30).
- **The mis-guess running gag** (snail? knight in armor?) — open loop 0:48 → pays at 4:32. Keeps older kids leaning in.
- **The collar-glow motif** — a *visual* question ("why does it light up?") that rewards re-watch. Cheap, keep it.
- **"It's a SHELL day"** (Pip, 3:20) — plants a mystery 10 s before the cascade pays it off. Best curiosity gap in the script — protect it.

**How the ending earns watch-to-end + click-next:**
- **Last face MUST be Bentley, not the octopus** (current cut ends on the tentacle — confirmed bug). The resolved tag + Wiggle-Butt rally lands on Bentley FIRST (rule #1), *then* the octopus is an 8 s button.
- **The octopus button must delight, not scare** — "Did that octopus just *wave* at me?! New friend!" is exactly right. For 3–5s an ominous final note depresses the next-click; a fun mystery invites it.
- **Explicit forward-promise:** Theodore's "Next time… *The Octopus Escape Artist*… tap to dive in" + the named next episode is the click-driver that converts retention into the auto-roll. Keep verbatim.

**Verified myself (so the budget is grounded, not inherited):** integrated loudness is a healthy −13.7 LUFS (a full mix exists) — the issue is the **three silence holes + unscored emotion**, not "no audio," so the fixes are far cheaper than a re-score. The ending music tail exists (last 3 s ≈ −19 dB) — it's **mis-ordered, not silent.** The recoil ears read floppy/acceptable (killed that re-key). Bentley WHOAA/tag teeth are borderline-not-failed (verify-only). Pip is genuinely 3–4 crabs and `f_96s` shows human teeth on Pip — the largest line-item, confirmed.

---

## 9. SPECIFIC CHANGES TO REACH A HIGH-QUALITY 4–6 MINUTE EPISODE (prioritized punch-list)

Do in this order — cheapest / highest-impact first.

**TIER 1 — FREE / NEAR-FREE, HIGHEST RETENTION ROI (do first):**
1. **Fill the cold-open silence (0:00–0:05):** Pip "Help?" over black + ocean + gull + 2-note sting. *The #1 fix in the whole plan.*
2. **Fill the two dead-air gaps (9–12 s and ~60 s):** continuous ocean bed + the missing **wave-crash / spray / claw-skitter SFX** on the surf beat. The action beat must not be mute.
3. **Score the 11 state-changes** (§6 table) — calm / adventure / discovery / suspense / emotional / triumphant. Duck −8 dB under VO.
4. **Re-order the ending:** Bentley tag = last face; octopus = button after it. Free edit; fixes the cut-off feel.
5. **Lay the collar-glow chime leitmotif** across the 4 glow beats (cold open, soft-body, the turn, Pip's thanks).

**TIER 2 — THE 6 NEW SHOTS (the only render spend, ~75 cr):**
6. **`N3_bridge_safe`** (Cinema Studio 3.0) — fixes the verified wet→dry slam. **Render first of the six.**
7. **`N4` + `N5`** (Wan) — the emotional core; 2–3 takes on N5 (the heart-line).
8. **`N1` + `N2`** (Wan + Ken-Burns) — the gag setup + the science plant (N2 ≤10 s, Bentley O.S. awe over it).
9. **`N6`** (Wan) — the gag payoff; **render last, drop first** if Act 6 drags.

**TIER 3 — REUSE KEYFRAME FIXES (re-gen + re-run cheap motion/lip-sync; triage by budget):**
10. **Pip's 3 worst held CUs first:** `a1_05` + `a2_01` (eye-stalks + angry jagged mouth, `f_31s`) and `a5_01` (the **human-teeth Pip**, `f_96s`) → re-key to locked Pip `752fec82`. Then the other 4 (`a1_04, a2_02, a3_02, a5_02`) if budget. Background-scale Pip drift in motion shots is tolerable; the held CUs are not.
11. **Cascade shell:** white-nautilus "new shell" → warm spiral matching Pip's shell family (`a4_03`) — continuity payoff with N2's diagram + Pip's eventual home.
12. **Verify-only (regen ONLY on confirmed failure):** Bentley WHOAA/tag teeth (`a4_04`/`a5_04`); recoil ears (`a3_03`) — both likely pass.
13. **Judgment call (budget-permitting):** upgrade hero-adjacent crowd/lineup crabs (stalked-eye family) to the clean-faced locked family; background crabs may stay.

**TIER 4 — GLOBAL POLISH (the "one world" pass):**
14. One warm teal-orange grade across all 27 shots; lock dawn / sun-right / scale / geography (left=danger, right=safe).
15. Bake the "alive" layer (moving water everywhere, background life, blink/breathe) per HANDOFF hard rules.
16. Motivated cuts + sound bridges (§5 Transition map); **1080p / 60 fps finish** on the locked cut (`upscale_video` bytedance, fps=60).

---

## APPENDIX — SOURCE FILES (absolute)

- Current cut: `/home/user/src/youtube/assets/pilot_shots/hybrid_ep1/Bentley_Ep1_FULL_1080p_v1.mp4`
- Flagship standard to match: `/home/user/src/youtube/assets/pilot_shots/hybrid_ep1/opening_redo/work/FULL_OPENING_MOVEMENT_v1.mp4`
- Shot specs: `/home/user/src/youtube/ep1_acts123.json` · `/home/user/src/youtube/ep1_acts456.json`
- Locked design: `/home/user/src/youtube/assets/character_design/LOCKED_ELEMENTS.md`
- Pipeline: `/home/user/src/youtube/HANDOFF.md`
- Performance bible: `/home/user/src/youtube/Bentley_Season1_MD_Files/Bentley_PERFORMANCE_BIBLE.md`
- Narration script: `/home/user/src/youtube/Bentley_Season1_MD_Files/Episode_1_GRANDPA_NARRATED_FULL.md`
- Assembly timeline: `/home/user/src/youtube/Bentley_Season1_MD_Files/Episode_1_HYBRID_ASSEMBLY_TIMELINE.md`
- Review frames (FREE): `/tmp/ep1_frames/` (incl. `seam_63s.jpg`→`seam_64s.jpg` wet→dry slam; `f_31s.jpg` stalk-eyed angry Pip; `f_96s.jpg` human-teeth Pip)
