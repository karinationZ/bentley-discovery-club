# Bentley's Big Adventures — production repo

Kids' YouTube animation series (age 4–8) starring Bentley the Boxer puppy. Built with generative
tools (KIE: Kling/nano-banana, ElevenLabs, ffmpeg). Credits are FINITE and real money.

## MANDATORY — before any episode work

- ANY task touching episode content — shots, keyframes, renders, VO, EDL/shotlists, cards, assembly,
  mixing, grading, QA, thumbnails, or spending ANY KIE/ElevenLabs credit — requires the
  **`episode-production` skill loaded FIRST**. This includes tasks that look like trivial file edits:
  a JSON tweak under `episodes/` IS production work.
- Scripts/story → `cinematic-episode-writer` skill. Any talking/lip-sync shot → `lipsync-pro` skill.
  Companion shorts → `companion-short` skill.
- Owner gates are recorded in `episodes/<ep>/GATES.md` — **an unrecorded gate is an UNPASSED gate.**
  Check the ledger before assuming or claiming any approval; never mark a gate from recollection.

## Hard guardrails (the full rules live in the skill chain — do not restate or fork them here)

- **No video render before the episode's Animatic Lock is recorded PASSED in GATES.md.**
  `bentley.shared.kie_client` enforces this mechanically: video models require `BENTLEY_EPISODE=ep<N>`
  (ledger-checked). `BENTLEY_GATE_OVERRIDE="<reason>"` exists for owner-approved non-episode video
  only — never set it to route around a failed gate.
- On KIE **402 (credits out): STOP and tell the owner.** Never hunt for workarounds.
- Never auto-batch-and-ship renders. Never regenerate a locked master. Never re-explore closed
  method tables (lip-sync, voices, thumbnails).
- When delivering any generated asset, always include its absolute file path.

## Layout & running things

- `bentley/` — the package: `shared/` (KIE/ElevenLabs clients, gates), `qa/` (mouthmotion, qa_vo,
  shot_ratios, verify_sync), `episode_builder/` (animatic, shorts), `voices/`, `character_framework/`
- `episodes/ep<N>/` — per-episode EDLs, GATES.md ledger, VO, builds · `assets/` — locked masters +
  approved footage · `scratch/` — experiments (per-episode one-off scripts) · `docs/guides/` +
  `youtube_vault/` — reference docs
- Run tools: `PYTHONPATH=. python -m bentley.<pkg>.<tool>` · tests: `pytest tests/`
