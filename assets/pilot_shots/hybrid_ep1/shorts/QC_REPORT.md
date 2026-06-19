# Shorts QC Report — Episode 1 Launch Set

**Verdict: all 6 Shorts PASS.** Built entirely from Episode 1 footage (`Bentley_Ep1_v2_FINAL_1080p.mp4`) — **$0 / 0 credits of new generation.** Originals untouched.

## Per-Short QC matrix

| Check | #1 Char | #2 Mystery | #3 Science | #4 Comedy | #5 Emotion | #6 Cliff |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **Strong first 2s** (face/surprise) | ✅ fond face | ✅ wonder face | ✅ crab line-up | ✅ guess face | ✅ Pip face | ✅ astonished face |
| **Standalone story** (cold viewer) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Accurate science** | n/a | n/a | ✅ "one by one" | n/a | n/a | n/a |
| **No important cropping** | ✅ punch-in | ✅ blur-fill | ✅ blur-fill | ✅ punch-in | ✅ punch-in | ✅ mix |
| **No caption overlap** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Clean audio** (from final mix) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Correct aspect (1080×1920)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Made-for-Kids safe** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ warm, not scary |
| **Duration** | 14.0s | 13.7s | 16.8s | 12.3s | 17.3s | 13.0s |
| **Ends on Ep1 pull** | ✅ >> | ✅ >> | ✅ >> | ✅ >> | ✅ >> | ✅ >> + Bentley face |

## QC issues found and FIXED (round 1 → round 2)
1. **Emoji rendered as missing-glyph boxes** (Pillow caption font has no color emoji) → **stripped all emoji from burned captions** + hardened `make_caption` to auto-strip emoji/dingbats. Emoji kept only in YouTube titles/descriptions (rendered natively). ✅
2. **#1 Character and #2 Mystery opened on the identical Bentley shot** → moved Character to open on the fond "tiny knight" CU; Mystery keeps the wonder CU. Now visually distinct. ✅
3. **#4 Comedy and #5 Emotional opened on slow wides** (violates "first frame = face") → Comedy now opens on Bentley's excited guessing face; Emotional punches into Pip's worried face. ✅
4. **Science caption accuracy** → verified by the Nature-Science editor: the vacancy chain is **sequential ("one by one"), not "at once"/"synchronized."** Caption corrected; "borrows"/"snail shell" wording enforced. ✅

## Distinctness (no two near-identical Shorts)
First frames: fond Bentley CU · wonder Bentley CU · crab line-up · excited Bentley CU · Pip's face · astonished Bentley CU — six different images. Hooks: intro · mystery · science · comedy · emotion · cliffhanger — six different responses. ✅

## Caption safe-area
All captions sit in the upper-third (~y0.10–0.13) or lower-third (~y0.82–0.83), centered, clear of the bottom-right Shorts UI and Bentley's lower-center charm. High-contrast white-on-navy pill, mute-readable. ✅

## Deliverables present
- 6× `Short_*.mp4` (1080×1920) + 6× `Short_*.srt` in `exports/`
- `SHORTS_CAMPAIGN_PLAN.md`, `LAUNCH_SCHEDULE_14DAY.md`, `ANALYTICS_SCORECARD.md`, `BRIEF.md`
- `CONTACT_SHEET.png` + `preview_reel.mp4`
- Builder + spec: `shorts_lib.py`, `shorts_specs.json` (re-buildable)
