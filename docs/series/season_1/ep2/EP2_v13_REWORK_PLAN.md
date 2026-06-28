# EP2 v13 — Production-Release Rework Plan
*Driven by the owner's defect list. Maps every issue → fix → FREE (edit-layer) vs PAID (re-render). KIE balance: 806 cr.*

## The headline: Bentley must talk (mouth animation, teeth OK)
- **Why she didn't:** her dialogue shots were built "VO-over-alive" — voice over a moving shot, **mouth closed.** That was the rulebook default (mouth-accurate lip-sync was avoided to dodge human-teeth/identity drift). **Owner override:** real mouth animation whenever Bentley speaks; teeth acceptable. This wins.
- **The reality:** Bentley speaks in **~30 of 42 beats.** Real audio-driven lip-sync (Kling-Avatar) on *every* one ≈ **~1,800–2,100 cr** — we have 806. The free mouth-atlas trick only works on a *static* base frame (breaks "never static"), so it is **not** a shortcut for Bentley.
- **Therefore tiered:** real lip-sync now on the beats where Bentley is the clear on-screen speaker and it matters most; decide separately whether to top up for full coverage.

## PAID — lip-sync + targeted re-renders (the only new spend; ~60 cr/talking shot, confirm on first)
| Beat | @ | Fix | ~cr |
|---|---|---|---:|
| 04_names | 0:17 | **Bentley talking-CU "I'm Bentley"** (Kling-Avatar), looking AT Indi — fixes the octopus-mouth-moving / wrong-gaze defect | 60 |
| 22_stop | 2:05 | Re-roll **eyes OPEN, head tilting, cute & curious** + lip-synced "Stop. Look. Listen." (replaces the eyes-closed H4) | 60 |
| 40_catchphrase | 3:51 | Lip-synced "Stop. Look. Listen." talking-CU | 60 |
| 04_names | 0:20 | Indi has a **star-shaped hand** → swap to a clean Indi shot (free) or re-render | 0–60 |
| 12_geology | 0:59 | Rewrite the awkward "I was looking at you…" line (cinematic-episode-writer) + re-record VO (ElevenLabs, ~free) + Bentley reaction shot | ~10 |
| 15_flashlight | 1:20 | **Bentley chases the octopus** (sets up the eel chase) — reuse chase footage if it serves, else fresh | 0–70 |
| + key Bentley CUs | — | intro/emotional close-ups get real lip-sync as budget allows | ~60 ea |

**Tiered-now target: ~6–8 talking/re-roll shots ≈ 350–500 cr** (fits the 806 balance, leaves a buffer).

## FREE — edit-layer re-cut (fixes the "biggest issue: pacing" + most timestamps, ZERO credits)
Principle: **longer holds, fewer cuts, smooth transitions, no loops, no statics.** Collapse multi-piece beats that cause rapid cutting; reuse only *distinct* sub-ranges; crossfade settles.
| @ | Beat | Issue | Edit fix |
|---|---|---|---|
| 0:09 | 02_eye | transition too quick (1.45s) | Lengthen the eye-reveal to ~3s; smooth in |
| 0:47 | 09_camo_fact | camo loops (reuses H1 right after 08) | Swap to Bentley-searching footage; don't repeat the camo |
| 0:51 | 10_hidden | static/lifeless | Swap to a livelier sub-range or different clip |
| 1:07 | 13_shell_trail | completely static | Swap to a moving shot |
| 1:13 | 14_fun_mouths | abrupt transition | Crossfade/match-cut in; re-time the beat |
| 1:16 | 14_fun_mouths | static octopus, already used | Replace with distinct, alive sub-ranges |
| 1:38 | 17_moray_fact | repeated static octopus | Distinct/livelier reused shots |
| 1:52 | 20_tag_taste | loops | One longer take; keep the scene on screen longer |
| 2:26 | 25→26 | abrupt cut | Crossfade/match the brave-outfit→shadow cut |
| 3:04 | 32_safe_twoshot | doesn't fit | Replace with footage like 3:10 (the recap/button) |
| 3:24 | 35_blueblood | loops | Distinct ranges; hold longer |
| 3:39 | 37_shell_handoff | static | Swap to a moving shot |
| global | — | choppy pacing | Fewer cuts overall; longer connected scenes; crossfade settles |

*Note:* where the approved library has no lively shot for a de-static/de-loop beat, that beat becomes a PAID re-render candidate (flagged at build).

## Order of work
1. Owner picks lip-sync scope/budget (below).
2. Rewrite the 0:59 line (cinematic-episode-writer) + re-record.
3. Render the approved talking/re-roll shots — hand-pick, QC for canon (mouth may show teeth; no human *smile*).
4. FREE edit-layer re-cut (v13) addressing all pacing/static/loop/transition items.
5. Mix + QA §9 against the FINAL file; deliver `EP2_v13_FINAL.mp4` with its path.
