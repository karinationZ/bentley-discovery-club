---
title: Production Standards — 11 Mandatory Rules
tags:
  - rules
  - production
  - mandatory
status: active
established: 2026-07-03
updated: 2026-07-05
---

# Production Standards — 11 Mandatory Rules

> [!danger] These are REQUIREMENTS, not suggestions.
> Established by the owner 2026-07-03 after the Episode 3 production review; **Rule 11 added 2026-07-05**
> after the EP4 batch loss. **Every episode must be reviewed against all eleven before it is approved for
> release.** Codified as the governing charter in the `episode-production` skill (§0.0) and as a
> ship-blocking gate in the pre-delivery QA checklist (§9). *(Filename keeps "10" for link stability.)*

## The rules

1. **Prioritize action over dialogue.** Visuals support the story, not the dialogue. Put multiple
   characters on screen doing meaningful things while the VO plays — interacting, exploring,
   demonstrating — plus environmental movement (plants, insects, wind, water, birds). The audience is
   watching an adventure, not a conversation. No talking heads carrying a beat.
2. **Use only the approved master character props.** When Bentley speaks, always use the approved master
   **Talking Bentley** prop. No alternative versions, no experimenting with facial styles, no new
   interpretations. Same for Marco and every recurring character. Gives consistent appearance, reliable
   lip-sync, visual continuity.
3. **Never drift from the approved character style.** A recurring EP3 failure: Bentley gradually drifted —
   too realistic / too cartoonish / off proportions / off expression / off render. Every generated scene
   is compared against the approved master prop. Consistency is non-negotiable — same Bentley every time.
4. **Avoid extreme close-ups.** EP3 had far too many oversized single-face shots — repetitive and
   visually boring. Prefer medium and wide; keep both characters in frame; show the environment. Reserve
   close-ups only for genuinely important emotional moments.
5. **Build one scene per story beat.** Do not split one logical thought into multiple stitched clips.
   Break the script into logical beats, make one cohesive animated sequence per beat, let the whole
   narration play over it. No unnecessary cuts, no angle change every sentence. Continuous cinematography.
6. **Smooth transitions are mandatory.** Every transition has a reason. No abrupt switches of camera
   angle, background, character style, or animation style. If the audience notices the edit, it failed.
7. **Maintain absolute character consistency.** Bentley stays identical — face, eyes, muzzle, fur, body
   proportions, lighting style, rendering style, background style. Never "different Bentleys."
8. **Story comes before animation.** Finalize the story, verify the dialogue, confirm the logical flow,
   define the beats — THEN animate. Generating animation before validating the story wastes time and
   AI credits. (Enforced by the zero-credit Animatic Lock gate.)
9. **Multi-character lip-sync is a mandatory QA check.** The biggest technical issue in EP3. When
   multiple characters are on screen: only the speaker has lip-sync; the other reacts naturally; never
   animate the wrong mouth; never both unless both are speaking. Checked before every release.
10. **Think like an animator, not an editor.** Not "which clip should I show next?" but "what is the best
    animated scene that tells this part of the story?" Scenes should feel alive and cinematic — not
    disconnected clips stitched to match dialogue.
11. **Do not work in large batches — produce incrementally.** *(Added 2026-07-05.)* Applies to both
    initial shot generation and animation generation. Generating dozens of shots or animations at once is
    inefficient: if a problem is discovered later, a significant number of AI tokens is already wasted.
    Instead, follow the incremental workflow: generate a small logical group of shots → review them
    carefully → QA against the production standards (owner review & approval required) → fix any issues →
    obtain quality approval → only then generate the next group. The same applies to animation: never
    animate an entire episode in one batch — animate a small section, verify lip-sync, character
    consistency, transitions and story flow, then continue. **Every stage has a quality gate before
    additional tokens are spent.** Objective: catch issues early, prevent regressions, reduce token waste,
    and ensure each production step meets the quality standards before moving on.

## Final production standard

Every episode should feel like **one continuous adventure.** The audience remembers the character
interaction, the beauty of the environment, the scientific discovery, and the emotional journey. They
should **never** notice: the editing · character inconsistencies · abrupt cuts · animation reuse ·
lip-sync mistakes.

## Related

[[Animation Rules]] · [[Storytelling Rules]] · [[Voice Rules]] · [[Episode QA Checklist]] · [[Production Workflow]]
