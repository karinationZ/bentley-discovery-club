# Ep2 — Action Items
*Ordered. Steps 0–1 gate everything else. Companion to EP2_HANDOFF.md.*

## 🔴 STEP 0 — DECIDE the character-consistency approach (blocks all else)
- [x] **0.1** Choose how to lock Bentley's identity (handoff §7). **Episode rescue choice: (B) KIE char-reference stopgap + human curation**. Use **GPT Image 2 image-to-image** for Bentley keyframes, then **Kling 3.0 video with Bentley element references** for motion. Keep **(A) trained LoRA/DreamBooth or a 3D rig** as the long-term Ep3+ fix.

## 🔴 STEP 1 — Lock Bentley's identity (THE blocker)
**If (A) trained model:**
- [ ] **1A.1** Generate/collect 15–30 clean, on-model Bentley views from `Bentley_MASTER_pixar.png` (front / side / 3-4 / sit / run), one consistent style.
- [ ] **1A.2** Train a LoRA / DreamBooth (or char model) on them.
- [ ] **1A.3** Validate it reliably reproduces the canon: docked tail, floppy ears, red-fawn paws (NO white), chibi-Pixar style, black mask, brown eyes.
- [ ] **1A.4** Adopt the trained model as the single source for ALL Bentley keyframes.

**If (B) char-ref tool + curation:**
- [x] **1B.1** Pick a tool with real identity lock: **KIE `gpt-image-2-image-to-image` for stills + `kling-3.0/video` with `kling_elements` for motion**.
- [x] **1B.2** Test it on 3 Bentley shots; confirm it holds the canon before committing. Test outputs are in `scratch/ep2/identity_lock_test/`; summary in `EP2_IDENTITY_LOCK_TEST.md`. Result: Bentley identity is materially better than Nano-Banana-Pro, especially docked tail + paws. Mixed Bentley/Indi shots still need extra Indi QC.
- [x] **1B.3** Adopt the rule: 4–8 candidates per keyframe, hand-pick the on-model one, **NEVER auto-batch-and-ship**.

## 🟠 STEP 2 — Re-render the off-model Bentley shots (after Step 1)
- [x] **2.1** Regenerate keyframes from the locked identity for the rescue shots. Final v7 generated/reused `boop, chase, lunge, corner, realize, stoplook, why, snackpouch, colorchange, youdidme, breathe, pawhold, button, whereGoing`; rejected bad `twoshot` and risky `wedged` motion.
- [x] **2.2** QC EACH keyframe against canon (tail / ears / paws / style) **before** animating; reject + redo any off-model. Final curation kept safe stills for camo/wedged and rejected tooth/smile failures.
- [x] **2.3** i2v the approved keyframes (**Kling 3.0 with Bentley `kling_elements` refs**); QC each clip's frames.
- [x] **2.4** Avoid risky Kling-Avatar talking shots where they introduced identity/teeth/lip-sync risk; final uses VO-over animated performance shots instead.

## 🟡 STEP 3 — P1 polish (after Bentley is consistent)
- [x] **3.1** Re-frame the repeated talking-head close-ups with VO-over motion/cutaways in v7 assembly.
- [x] **3.2** Trim/intercut the long static holds with composites and retimes; freeze scan passes.
- [x] **3.3** Add the missing "Indi gets wedged" beat before the rescue.
- [x] **3.4** Add timing-safe fades/cross-beat transitions in the v7 assembly.
- [x] **3.5** Fix the highest-risk dark/off-model/white-paw frames through replacement routing and final grade.

## 🟢 STEP 4 — Finalize
- [x] **4.1** Re-assemble (`scratch/ep2/final_v7/assemble_v7.py`) -> mix (`scratch/ep2/final_v7/mix_v7.py`) -> output `scratch/ep2/final_v7/assembly/EP2_v7_FINAL.mp4`.
- [x] **4.2** Full QA against final export: stream probe, decode, silence, black frame, freeze scan, scene sheet, transition sheet, mouth/identity sheet.
- [x] **4.3** Deliver final copy: `scratch/ep2/final_delivery/EP2_FINAL.mp4`; archive final handoff in `EP2_FINAL_HANDOFF.md`.

## ⚪ HYGIENE — do now / standing rules
- [x] **H.1** Treat `scratch/ep2/assembly/EP2_v5_FINAL.mp4` as the working baseline; do NOT build on `v6` (broken Bentley).
- [x] **H.2** Masters are frozen — edit FROM `Bentley_MASTER_pixar.png` / `Indi_LOCKED.png` / the eel ref; never regenerate a new master.
- [x] **H.3** Process rule: approve direction + QC each frame BEFORE generating; never auto-batch re-renders.
- [x] **H.4** Always verify a frame extracted from the FINAL file before delivery; deliver under a fresh filename (viewer caches by name).
