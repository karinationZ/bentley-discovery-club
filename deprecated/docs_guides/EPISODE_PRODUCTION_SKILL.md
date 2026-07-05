> ⛔ **DEPRECATED 2026-07-03 — do not follow.** Superseded by the single normative chain:
> **10 Mandatory Rules** (`youtube_vault/Rules/Production Standards (10 Mandatory Rules).md`) →
> **`.claude/skills/episode-production/SKILL.md`** (enforcing rulebook, auto-loads) →
> **`.claude/skills/episode-production/references/PRODUCTION_PLAYBOOK.md`** (operating manual).
> Kept byte-for-byte below for history. Unique lessons were absorbed into the playbook before this move
> (avatar freezes-background / darkens / text-hallucination; worst-frame-fails QA). See `deprecated/DEPRECATED_LOG.md`.

# EPISODE PRODUCTION SKILL — MANDATORY
### The single source of truth for producing every "Bentley's Big Adventures" episode

> **This is a hard rule, not a guideline.** Every episode-production agent — and every human running a
> production workflow — MUST load and obey this before generating, rendering, editing, or assembling
> any episode footage, shot, card, or asset, starting with Episode 3 and onward.

**The machine-loadable, always-in-sync version is the skill at
`.claude/skills/episode-production/SKILL.md`** (it auto-loads whenever episode production work starts).
This document is the human-readable canonical copy of the same rulebook. The two must stay identical;
edit both together. The script/story phase lives in the companion skill
`.claude/skills/cinematic-episode-writer/` — write the script there, **produce it under these rules.**

**Prime directive:** *Maximize quality where viewers notice it most; minimize credit usage everywhere
else.* Premium animation for character moments, cheap tools for supporting footage, reuse approved
assets whenever possible — without sliding back into a "stitched-together montage."

---

## ⭐ THE KLING 3.0 COST GATE  (the urgent hard rule — Kling is expensive)

Before generating **any** shot, ask one question:

> **Is a character emoting or interacting, or is this a signature / hero / action moment a viewer will
> actually remember?**  YES → Kling 3.0.  NO → do not spend Kling.

**Use Kling 3.0 ONLY when at least one is true:**
- Bentley and another character are interacting
- Dialogue / emotional close-up where the face carries the moment
- An emotional beat · a key story moment · a signature episode image
- A hero shot · a complex action shot

**NEVER use Kling 3.0 for:**
- Static scenes · ocean/reef backgrounds · establishing shots · transition shots
- Title cards · fact cards · simple camera moves · hold shots · filler · narration-only scenes

**Model tiers (owner policy, 2026-06-24; updated with test results):**
- **Free — ALWAYS TRY FIRST:** reuse an approved clip · still + Ken-Burns (ffmpeg) · card/graphic (PIL)
  · editor transition. We have a large approved EP2 footage library — reuse covers most non-hero beats
  at **zero credits**.
- **Kling 3.0 (Premium)** — ALL hero character shots: Bentley+Indi close-ups, dialogue reactions, the
  camo/transformation reveal, emotional beats, any face-visible moment (~70 cr/5s on KIE). Use only
  when reuse can't serve.
- **Kling 3.0 Turbo (cheaper — TEST)** — only if a non-hero shot *must* be generated and no reuse fits
  (small-face wides, simple environment motion). ~7.5 cr/5s on Higgsfield; confirm the KIE slug. Same
  Kling family → holds our style far better than Seedance.
- **Kling 2.6 — BANNED** — not cheap enough; already fails on mouths/teeth.
- **Seedance 2.0 / 2.0 Mini — TESTED → AVOID for characters.** 2026-06-24 test (eel, 10 cr): it drifted
  the menacing moray into a cute big-eyed smiling fish — off-model, menace lost. Do not use for any
  shot with a recognizable character/creature. (No "Seedance 1.5 Pro" exists on our backends.)

*Caveat:* never substitute a cheap/procedural OR cheaper-model shot for the **character moment
itself** — cheap tiers are for supporting footage only (a procedural hero shot is a regression).

**Budget:** target ~12–18 Kling hero shots per episode; cover the rest by reuse/stills/cards; log
credits spent. Get owner sign-off on the Kling shot list **before** spending.

---

## The full rulebook (see the skill for detail)
1. **Kling cost gate** (above) — when premium animation is and isn't allowed.
2. **Asset reuse** — reuse before generating; one clip per beat (callbacks = different sub-range, no
   loops); masters frozen; fresh delivery filename; verify a frame from the FINAL file.
3. **Bentley canon** — red-fawn, black mask, floppy ears, **no white socks**, docked tail, collar +
   Listening Tag; **never human teeth/smile**; generate from the master, hand-pick, never auto-batch.
4. **Master props** — the Listening Tag (glows when still) and the shells; kept consistent across
   shots and episodes.
5. **Character animation** — motion in every shot (no static-zoom, no freeze, no >1.3× slow-mo);
   dialogue is VO-over-alive (no default lip-sync); never cut away from a speaker mid-line.
6. **Transitions** — **no dip-to-black**; hard cuts default, match-cut on motion, crossfade only for
   time/place jumps or settles; transitions are edits, never renders.
7. **Voice** — locked voices (Bentley=LauraZ, guest=its locked voice, Narrator=Bill); the catchphrase
   is **always Bentley**; every line over the correct, alive speaker; no dark lines.
8. **Storytelling** — obey the script's spine + causal chain; keep the cold-open, the bonding beat,
   and the cliffhanger; facts as wonder, not data-dumps.
9. **QA checklist** — run against the FINAL file before delivery (black scan, no loops/freezes/pale
   grade, canon on every Bentley shot, right speaker, catchphrase, causality, cost-gate audit) PLUS the
   **Animatic Lock** pre-render sub-checklist (full VO reel present + in order, line over the right
   speaker [weak on cards], every cut answers the last, hinge shown not narrated, reads as a story when
   muted) — certifies STORY + CUT only; §5a stays authoritative on the FINAL.
10. **Workflow** — script → tag every shot against the cost gate (owner sign-off) → **assemble the full
    VO reel (new + reused mp3s, in script order)** → **Story Scratch / Animatic Lock** (a timed animatic
    on the EDL from reuse/stills/cards + the recorded VO; **ZERO Kling/KIE/ElevenLabs credits**; built
    via the productionized `bentley/episode_builder/` animatic — never `pipeline.py` / `produce()` or
    the generation modules; **no Kling until the owner signs**; its EDL is the STARTING assembly EDL,
    re-timed at QA) → generate only approved Kling shots (hand-pick) → assemble → sync-verify → mix →
    grade → QA → deliver. *(Tool built 2026-06-27: `bentley/episode_builder/animatic.py` —
    `PYTHONPATH=. python -m bentley.episode_builder.animatic <shotlist>`; proven zero-credit on EP2.)*

---
*Pairs with `cinematic-episode-writer` (script phase). Full operational rules + the QA checklist:
`.claude/skills/episode-production/SKILL.md`.*
