# QA_CHECKLIST — per-episode acceptance

Copy this list for each episode and tick every box before publishing. Anything
unchecked is a blocker. Character + Fact rules are defined in `MASTER_PROP_RULES.md`.

**Episode:** ____   **Reviewer:** ____   **Date:** ____

---

## 🔊 Audio
- [ ] Final loudness normalized (delivery target, ~-14 LUFS) — no clipping.
- [ ] **No two voices overlap** anywhere (`verify_sync.py` passes with zero overlaps).
- [ ] Dialogue rides the picture's embedded lip-synced track; narration sits only over motion shots.
- [ ] Music re-pinned to shot anchors; ducks under dialogue; no abrupt cuts.
- [ ] SFX present and in sync (waves, paws, skitter, chimes, etc.); ambient bed continuous.
- [ ] No stray `_raw` (un-cleaned) takes used anywhere in the mix.

## 🎙️ Voice
- [ ] Bentley = **"Laura Z"**, Pip = **"Callum" pitched +10%**, Narrator = **"Bill"** — correct voice per character, no swaps.
- [ ] Every line cleaned (ElevenLabs clean chain), not the raw export.
- [ ] Pip is audibly pitched up (+10%) — small, fussy crab.
- [ ] Delivery/pace matches the beat; no garbled or truncated lines.
- [ ] Lip-sync: mouth movement matches the spoken line on every talk shot.

## 📖 Story
- [ ] Beats land in order (intro → setup → conflict → empathy → payoff → tag).
- [ ] The episode's lesson/payoff is clear and age-appropriate (kids' content).
- [ ] No continuity gaps between shots (props, positions, time of day consistent).
- [ ] Pacing holds — no dead air, no rushed beat.
- [ ] Title card + end tag present and correct.

## 🎬 Animation
- [ ] Water/waves actually MOVE on environment shots (no frozen background).
- [ ] **No frozen-background talking shot** is standing in for a motion shot (see avatar-freeze lesson).
- [ ] Consistent premium 3D Pixar soft-fur style + warm dawn lighting across every shot (not painterly/flat).
- [ ] No slow-mo on action (motion = native speed; only the 2 title cards get a gentle ramp).
- [ ] Camera stable — no unwanted jitter/shake; cuts are clean.
- [ ] Grade is bright + vibrant + consistent (no dark/backlit faces shipped; those need Tier-1 re-renders).

## 🐾 Character (see `MASTER_PROP_RULES.md`)
**Bentley:**
- [ ] Short **docked** tail (NOT long/upright).
- [ ] Floppy ears folded **DOWN** (NOT pricked/upright).
- [ ] Natural dog mouth, **small lower teeth only** (NO human teeth / wide grin).
- [ ] Black mask, grey chin, white chest blaze, natural Boxer proportions.
- [ ] Teal collar with the glowing **spiral seashell** charm present.
- [ ] Consistent face/muzzle/markings shot-to-shot; correct age.
- [ ] **PAWS:** solid red-fawn, **NO white socks** (owner-confirmed canon). `fix_paws.py` removes any white socks — flag any render that adds them.

**Pip:**
- [ ] Eyes set **IN the face** (NO eye-stalks).
- [ ] Dull cracked **brown SPIRAL** shell (NOT a white nautilus).
- [ ] **SMOOTH** shell — NO fur/hair/fuzz.
- [ ] Clean face (NO antennae/whiskers); small natural crab mouth (NO human teeth); reddish-orange.

**Props:**
- [ ] No fur/hair on the seashell or any hard prop.

## ✅ Fact
- [ ] Any real-world fact stated by the Narrator is accurate (e.g. hermit-crab biology).
- [ ] Educational claims are true and age-appropriate.
- [ ] Names/spelling on title card, thumbnail text, and end card are correct.
- [ ] Thumbnail represents the episode honestly (no misleading frame).

---

### Sign-off
- [ ] All sections above complete.
- [ ] Reuse-first honored (approved assets used where possible; new spend got owner approval).
- [ ] Owner approved the final cut.
