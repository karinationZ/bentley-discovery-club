---
title: Episode QA Checklist
tags:
  - production
  - qa
  - checklist
---

# Episode QA Checklist

> [!important] The gate before publish
> Copy this checklist for each episode. **Nothing ships until every box is checked** and `verify_sync.py` reports zero overlaps. When a box fails, fix it at the **right** stage (re-render vs grade vs mix) — see [[Lessons Learned]].

## 🔊 Audio QA
- [ ] No silent gaps where there should be sound (open, action beats, transitions)
- [ ] SFX present on every key action (splash, crash, skitter, etc.)
- [ ] Music supports the beat; cues don't restart ("stitch") mid-continuous-scene
- [ ] Ambient bed continuous across cuts
- [ ] Final loudness normalized (~ -14 LUFS); no clipping

## 🎙️ Voice QA
- [ ] Correct **locked** voice for every character ([[Voice Rules]])
- [ ] Pip pitched +10%; all VO cleaned (not raw)
- [ ] **Zero overlapping voices** — `verify_sync.py` passes
- [ ] Lip-sync reads on every talking shot (mouth matches words)
- [ ] Delivery / emotion fits the moment

## 📖 Story QA
- [ ] One clear concept, taught once ([[Storytelling Rules]])
- [ ] Five beats present: intro · setup · problem · climax · resolution
- [ ] Memorable takeaway lands at the end
- [ ] Opened loops are paid off
- [ ] Ends on Bentley's face, then the stinger button
- [ ] Entertaining first, educational second

## 🎬 Animation QA
- [ ] **Everything alive** — water / waves / sky / grass moving in every outdoor shot ([[Animation Rules]])
- [ ] **No frozen backgrounds** (no live water in a talking shot)
- [ ] Native speed; no slow-mo as fake animation
- [ ] No glitchy / looping motion; no match-jump cuts between near-identical shots
- [ ] Transitions flow (continuous bed across seams)
- [ ] One consistent grade; no shot brighter / darker than its scene

## 🐶 Character QA
- [ ] Bentley on-model in **every** shot — short docked tail, ears down, no human teeth, soulful eyes, teal collar + spiral charm ([[Bentley Master Prop]])
- [ ] Guest creature on-model throughout ([[Pip the Hermit Crab]])
- [ ] Consistent face / muzzle / markings / age across all shots
- [ ] Props (shells, etc.) smooth and correct — no fur, no nautilus
- [ ] Faces bright, not dark / backlit

## 🔬 Fact QA
- [ ] The science fact is **real** and **verified** against a source ([[National Geographic Standards]])
- [ ] It delivers a genuine "wow"
- [ ] Creature anatomy / behavior is plausible
- [ ] The takeaway is accurate

---
> [!success] Ready to publish when…
> All sections checked · `verify_sync.py` clean · FINAL is 1080p graded · publish kit ready (title, description, tags, custom thumbnail).
