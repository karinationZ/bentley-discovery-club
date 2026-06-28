# Episode 2 — Full QA Report
**Master reviewed:** `scratch/ep2/assembly/EP2_FINAL_master.mp4` (3:49, 1080p). End-to-end pass by 5 QA specialists (Animation, Video Editor, VO/Lip-Sync, Storytelling, Character). Timestamps are master times.

## Executive summary — the ONE root cause
**~70% of the complaints trace to a single assembler bug: narration shots LOOP a 5s clip 2.7–3.5× to fill long VO.** Every "frozen / static / buggy / repeating / VO drifts after 1:30" note is this: the picture hard-resets (pose/eyes snap) mid-sentence while the voice runs. Fix this one thing (de-loop) and the reintro, camo, squeeze, science, and the post-1:30 drift all resolve at once. The rest is a focused list of re-renders + edit fixes. The **story spine is sound** — the breaks are execution (a de-fanged threat, a missing panic beat, two wrong-source clips, smile-drift, the teal eye).

---

## 1. Transition Issues Report
| Time | From → To | Issue | Sev | Fix |
|---|---|---|---|---|
| 0:04 | establish → boop | painterly flat plate → glossy 3D; style+scale pop ("0:05 jumpy") | MAJOR | short dissolve; regrade establish; live-water plate |
| 0:17 | ink → **title card** | title interrupts the cold open mid-action | MAJOR | move title to 0:00 |
| 0:19 | title → reintro | bland teal card → leaping squirt-gag puppy as "narrator b-roll"; tonal whiplash | MAJOR | calm Bentley beat under N_intro |
| 1:03 | corner → bolt | sunny surface pool → fully underwater cave; environment/light discontinuity | **CRIT** | ink-puff bridge + regrade bolt to surface light |
| 1:14 | realize → stoplook | two near-identical worried CUs back-to-back; catchphrase fires before "settle" | MAJOR | re-order settle→stoplook; insert cutaway |
| 1:18→end | all back-half Bentley CUs | match-jump fatigue — every talk CU reuses the SAME sunset-tidepool framing | MAJOR | vary scale/angle; intercut two-shots/macros |
| global | all cuts | hard cuts only; **letterbox "breathing"** (segs vary 720/712/626px active) | MAJOR | normalize all segs to one frame size; add cold-open dissolves |

## 2. VO Sync Report
*(Lengths match — this is intra-shot drift, not a global offset.)*
| Time | Line/shot | Issue | Sev | Fix |
|---|---|---|---|---|
| 1:15 | "Stop. Look. Listen." | 1.4s dead-mouth tail + garbled caption; mouth onset off | **CRIT** | trim seg to VO; re-crop/re-render caption |
| 0:19/0:38/2:38/3:13 | N_intro/N_camo/N_boneless/N_hearts | picture **loops 2.7–3.5×** under one line → hard resets = the "post-1:30 drift" | **CRIT** | de-loop: trim VO to shot, or multi-clip b-roll |
| 2:16 | youdidme | uses **wrong source clip** (`talk_B_colorgame`) — mouth says different words | HIGH | re-render from the correct line |
| 3:40 | whereGoing | uses **wrong source clip** (`talk_B_ants`) — mouth ≠ line | MED | re-render from correct line |
| 0:33 | chase | **B_rude line dropped** (only B_chase laid) | MED | add B_rude |
| all talk | realize/stopped/why/snackpouch/button | 0.5–2.0s dead-picture tails | MED | trim each seg to embedded-audio length |

## 3. Story Logic Report
Spine holds; **Act 2 (chase→danger→turn) is the weak hinge** — the threat + panic that motivate the whole turn are never shown.
| Time | Beat | Problem | Sev | Fix |
|---|---|---|---|---|
| 1:08 | eelstir | the "moray eel" is a **smiling friendly fish** — no threat lands; load-bearing setup for Acts 3–4 fails | **CRIT** | re-do as soft dark silhouette + eye/teeth glint, darker grade |
| 1:03 | corner→bolt | no panic, no crevice; calm Indi → swimming away; reads random | **CRIT** | add 1s ink-puff/flinch; match environment |
| 1:14 | catchphrase | "Stop.Look.Listen." fires **before** Bentley sits/goes still (motivation inverted) | HIGH | re-order settle→stoplook |
| 2:23 | youdidme→wedged | Indi jumps from joy to wedged-panic with **no trigger** (eel-shadow cut) | HIGH | add 1–2s returning eel shadow |
| 0:40 | camo (15.8s) | Indi revealed full/cute/posing during the camouflage *fact*; kills mystery; too long | HIGH | trim ~6s; show only the rock morph, hide her face |

## 4. Character Animation Report
**BENTLEY:** 0:16 **sleepy/disengaged + most off-model (jowly/houndy)** at the discovery beat — should be surprised+curious (HIGH); human teeth/grin at 0:14, 0:36, realize(1:12), youdidme(2:16) (HIGH — hard-rule); recurring too-jowly/adult proportions vs the puppy master (MED); paw-tag engraving often missing (LOW). Paws correctly solid red-fawn throughout.
**INDI:** **teal/cyan eyes everywhere = the "creepy eye" complaint** (HIGH — baked into `Indi_LOCKED.png`); cold-open rock-eye (0:09–0:16) the scariest (saturated teal in red rock); teeth visible at 1:00 (HIGH — octopus is toothless); ORANGE not purple at 2:12 (this is the intended colour-match beat, flag only); colour drifts hot-magenta 0:42–0:51 (MED).
**Octopus-eye redesign (teal→brown/grey):** owner is right; it's the biggest kid-approachability issue. Requires **re-locking Indi's master** (FLUX eyes-only edit, preserve everything else) → then **re-render every Indi shot**. Soften iris to warm brown/muted grey-brown; warm the ocelli to grey-teal so they read decorative.

## 5. Scene Continuity Report
- **Environment jump 1:03** (surface↔underwater) — biggest continuity break.
- **Catchphrase ordering** (settle/stoplook swapped).
- **Wrong-source talk clips** (youdidme, whereGoing) — lip + content mismatch.
- **Indi colour/ocelli drift** (magenta vs purple; ring vs dot ocelli).
- **Letterbox breathing** + **match-jump CUs** — visual continuity.
- **End card** shows "Stop. Look. Listen." as TEXT — violates canon (must be Bentley's spoken VO).
- Shell-message macro (a6_33) + emphasis on the planted shell missing — weakens the "I left you shells" payoff.

---

## 6. PRIORITIZED FIX LIST (batched by type — NOT scene-by-scene)

### P0 — Edit / assembler (free, no re-render; fixes the majority of complaints)
1. **DE-LOOP narration shots** — ban single-clip loop >1.5×; trim each narration to its shot OR feed multiple b-roll clips. *(Fixes reintro/camo/squeeze/science + the post-1:30 "drift" — the #1 issue.)*
2. **Trim talk-clip dead tails** to embedded-audio length (kills dead air + the 1.4s catchphrase tail).
3. **Re-order** settle→stoplook; **add** the 1s panic beat (1:03) + the eel-shadow trigger (2:23) from existing clips.
4. **Title card → 0:00** + redesign with channel branding (drop the bland teal card); **end card catchphrase = Bentley VO**, not text.
5. **Kill all burned-in captions** (re-crop/re-render the stoplook clip); normalize letterbox to one frame size; add cold-open dissolves; intercut back-half CUs to break match-jumps.
6. **Restore the dropped B_rude line.**

### P1 — Targeted re-renders (character/story-critical)
7. **Cold-open rock-eye + Bentley (0:09–0:16)** — soften eye, Bentley surprised+curious (top single shot).
8. **Eel** → soft DARK menacing **silhouette** (threat via shadow, not a scary face — resolves the "not scary" vs "needs threat" tension).
9. **Re-render the 2 wrong-source talk clips** (youdidme, whereGoing) from the correct lines.
10. **No-smile / no-teeth re-renders**: Bentley realize, youdidme, gotcha; Indi teeth at 1:00.
11. **Re-stage gotcha** (water from the rock at Bentley, grounded launch) + **fix lunge float** + **opening live water**.

### P2 — Design change (largest scope)
12. **Indi eye redesign teal→brown/grey** → re-lock `Indi_LOCKED` (eyes only) → re-render ALL Indi shots. *(Touches every Indi shot; do as one batch after the master is re-locked.)*

**Decision flags for the owner:** (a) the **eel** — your earlier pick was the cute/not-scary one, but it kills the story's threat; recommend the soft *silhouette* middle ground. (b) **Indi eyes** brown vs grey — confirm the target. (c) the **2:12 orange Indi** is the intended colour-match payoff — keep (not a bug).
