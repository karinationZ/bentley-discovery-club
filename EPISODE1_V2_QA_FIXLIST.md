# EPISODE 1 "THE VOICE IN THE SHELL" — v2 QA FIX LIST (EXECUTABLE)

**Supervising-producer merge of 4 QA passes** (Animation / Character / Audio / Story).
Backbone: `/home/user/src/youtube/assets/pilot_shots/hybrid_ep1/v2/work/EP1_v2_base_av.mp4` — 197.88s (3:17.9), dialogue-only, narration NOT yet laid in.
Timeline: `…/v2/work/timeline.json` (27 shots, 6 movements).

**fal cost model:** Image keyframes are free. The ONLY spend is video re-renders. House rate (LOCKED): **Minimax Hailuo 2.3 ≈ 6 cr / 6s** for character/emotion; **Veo 3.1 Lite ≈ 6 cr** for wide/cinematic. We tag each re-render `~6 cr` (one 6s take) and budget **2 takes** on the two hero-defect shots (N6, a3_03) because multi-character/pose drift is high. Convention below: **1 credit ≈ $1** for the `~$` tag (adjust to your plan's actual cr→USD).

**Headline reconciliations (where the 4 reports disagreed — resolved here):**
- **N6 long tail** — all 4 reports CONFIRM. Mandatory re-render. ✅ on the list.
- **a3_02 "frozen wave"** — Animation QA proved the **wave NOW MOVES in v2** (6-frame spray-wall check, waveSSIM 0.48–0.82): **NO motion re-render for the wave.** Story QA found the *real* a3_02 problem: **off-model Pip (human teeth/gritted mouth) + a 21.7s over-long hold.** So a3_02 is on the re-render list for the **Pip character defect + hard trim**, and the residual back-third stall is masked with **layered wave SFX** (not a render). ✅ both N6-tail and a3_02-wave dispositions are captured.
- **a5_03_disco white socks** — Animation QA = BROKEN (white socks); Character QA = PASS (solid red-fawn). **Unresolved conflict on a 2.4s shot** → treat as a **frame-verify-then-maybe-render** (cheapest path; see RR-4).
- **a3_03_recoil eyes** — Character QA = FAIL (googly/bulging at startle peak); Animation QA = strongest motion. **Re-key the startle pose for eyes; keep the great motion.** ✅ RR-3.
- **8 static-BG talking close-ups** — Animation + Character agree: **do NOT re-render.** Fix with a post composite (subtle parallax water + drifting cloud). See POST-FIX block; zero fal cost.

---

## 1. RE-RENDER LIST — the ONLY fal cost

Re-render only what truly fails the LOCKED design or is technically unusable. Everything else is post/audio/edit (free).
**Video model:** Hailuo 2.3 unless noted. **Always trim avatar/talk clips to ~VO length +0.2s** (LOCKED) and **pin VO to the shot's frame start** (kills A/V drift).

| ID | shot @ time | WHY (fault class) | motion-vs-talk | corrective KEYFRAME prompt (free re-key first) | corrective MOTION prompt | takes | ~$ |
|----|-------------|-------------------|----------------|-----------------------------------------------|--------------------------|-------|-----|
| **RR-1** | **N6_payoff_armor** @2:54 (174.26s, slot 10.5s) | **character-defect (worst):** LONG upward-curving tail behind haunch (frames @8.0s/9.5s) — violates LOCKED short-docked-stub. Tail is **hallucinated by the video model** (source key hides it front-on) + dead background. | **talk** (VO `N6_payoff_armor_vo.mp3` = 10.32s) | `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>` Bentley 3/4, **SHORT docked stubby Boxer tail clearly visible and correct**, both floppy ears folded DOWN, solid red-fawn legs (NO white socks), natural dog mouth + small dog teeth (NO human teeth), soulful well-proportioned eyes, teal collar + glowing spiral shell. Behind her: live tidepool + ocean. NEG: "long tail, curled tail, sweeping tail, plume tail, human teeth, white socks, pricked ears." | Gentle settle/talk; **living water + drifting clouds behind**; subtle surf shimmer; trim to ~10.5s. | **2** | ~$12 |
| **RR-2** | **a3_02_pip_flip** @1:07 (67.80s, slot 21.68s) | **character-defect + structural:** Pip renders **human teeth / gritted "angry" mouth** (off-model, frame @5s). Shot also held **21.7s** for one gesture → reads as wallpaper. *(Wave motion is FINE — do not touch it.)* | **talk** (VO `a3_02_pip_flip_vo.mp3` = 21.50s) → **but HARD-TRIM picture to ~8s**; let the rest of the VO play over the trimmed clip + b-roll/recoil. | `<<<752fec82-e78e-4289-8257-07176fcb82e0>>>` Pip the hermit crab, **eyes set IN the face (NO eye-stalks), clean face NO antennae/whiskers**, dull cracked brown spiral shell, reddish-orange body, worried-but-soft expression, **natural small crab mouth — NO human teeth, NO human grin**. NEG: "human teeth, eye-stalks, antennae, whiskers." | Agitated little gestures, claw raise; keep existing live wave; render ~8s. | 1 | ~$6 |
| **RR-3** | **a3_03_recoil** @1:29 (89.49s, slot 5.04s) | **character-defect:** at startle peak (~t2.5s) Bentley's eyes are **oversized / bulging / googly** + ear splay — violates "soulful, NOT googly." (Motion itself is the best in the ep — preserve the recoil/foam-explosion.) | **motion** (no VO; SFX-carried) | `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>` Bentley mid-recoil/startle, **soulful well-proportioned eyes — NOT oversized, NOT googly, NOT cross-eyed**, ears floppy folded down (splay OK but folded), short docked tail, solid red-fawn (NO socks). NEG: "big eyes, googly, bulging eyes, pricked ears." | Recoil/bound back as a wave explodes into foam (match current energy); ~5s. | **2** | ~$12 |
| **RR-4** | **a5_03_disco** @2:52 (171.86s, slot 2.4s) — `…/acts456/a5_03_disco.mp4` | **CONFLICT — verify first.** Animation QA: **white socks/paws on front feet** (LOCKED violation) + static water. Character QA: PASS. **Action:** pull frames; **if socks confirmed → re-render; if clean → ship as-is** (no spend). Static water is post-fixable regardless. | **talk** (uses backbone audio) | (only if socks confirmed) `<<<1c82ee5b-8713-4596-80ec-6ce854502a4d>>>` Bentley playful, **all four paws solid red-fawn — NO white socks, NO white toes**, collar + glowing spiral charm, floppy ears, short docked tail. NEG: "white socks, white paws, white feet, white toes." | Quick happy beat; light water motion; trim to ~2.4s. | 0–1 | **$0–$6** |
| **RR-5** | **N4_pip_lonely** @1:48 (108.07s, slot 13.33s) | **technical:** source is **972×554** — the lowest-res clip in the episode, will look soft beside 1080p neighbors after the grade. Also near-frozen BG. Pip is on-model. | **talk** (VO `N4_pip_lonely_vo.mp3` = 13.35s) | `<<<752fec82-e78e-4289-8257-07176fcb82e0>>>` Pip alone, sad, single tear, **eyes in face, NO eye-stalks/antennae**, dull cracked brown spiral shell — **render at full 1080p**. | Gentle cloud + water drift behind; intimate; ~13.3s. | 1 | ~$6 |

### RE-RENDER TOTAL
- **Committed (RR-1,2,3,5):** ~**$36** (6 takes: 2+1+2+1).
- **Conditional (RR-4):** **$0–$6** pending frame check.
- **TOTAL: ~$36, max ~$42.**

**Confirmation requested in the brief:** ✅ **N6 tail is on the list (RR-1, top priority).** ✅ **a3_02 frozen-wave is addressed (RR-2):** the wave needs NO re-render (it moves in v2); a3_02 is re-rendered only for the off-model-Pip defect and hard-trimmed, with wave SFX layered to sell motion.

### POST-FIX (NOT re-renders — zero fal cost, do in the finishing/comp pass)
These 8 are talking close-ups where only the face moves and the ocean behind is frozen (BG-band SSIM ~0.96–0.99). Both Animation + Character QA recommend **composite a subtle live-water/parallax + drifting-cloud layer behind each**, re-render ONLY if the comp looks fake:
`a3_04_bentley_stunned`, `a4_04_whoaa`, `a5_04_tag`, `a1_06_twoshot`, `a1_02_bentley_hear`, `N1_bentley_guess`, `N5_bentley_empathy`, `a3_01_bentley_fix`.
Plus a optional faint foreground-pool ripple on `a3_02` and a subtle BG drift on `a5_03` (if it's NOT re-rendered).

---

## 2. SOUND-DESIGN BUILD SPEC

### 2.1 Global mix bus (ffmpeg targets)
- **Ambient bed** `sfx/amb_ocean.mp3` (22s): continuous, **looped ×9** to cover 198s+, **−16 dB**, ducked ~3 dB under VO. Never stops.
- **Music:** **−8 dB under any VO** (sidechain); static −18 to −20 dBFS under dialogue, up to −12 to −14 in music-only motion windows. **Crossfade 1.0–1.5s** between cues — never hard-cut music.
- **VO:** anchor; ride to ~−14 to −16 dBFS peaks.
- **SFX:** spot −12 to −20 dB; transients (`wave_crash`, `shake`) may peak −8.
- **Duck recipe:** `sidechaincompress` keyed off a **summed VO stem** → threshold ~0.05, ratio 6–8, attack 5 ms, release 300 ms, applied to the music+ambient sub-bus.
- **Final:** single-pass `loudnorm=I=-14:TP=-1.5:LRA=11` (YouTube −14 LUFS), 48 kHz stereo, after the full premix; mux to the 1080p picture.

### 2.2 CRITICAL — silent windows to fill (backbone is DEAD −91 dB on every motion shot)
These 11 windows are 100% silent on playback and are the **highest-priority fills**:
`a1_01` (0–5, cold open) · `a1_03` (8.7–11.9) · `a1_04` (11.9–17) · `N2` (59.8–64.9) · `a3_03` (89.5–94.5) · `N3` (94.5–99.6) · `a4_01`/`a4_02`/`a4_03` (131.9–147, the 3 cascade shots) · `a5_01` (152.7–157.8) · `a6_01` (192.8–197.9, the stinger).

### 2.3 Scene-by-scene audio map (assemble-ready)
Format: **[t] shot — MUSIC | AMBIENT | SFX | VO/O.S.** · all paths under `…/v2/`. Times shift +~26s once the intro (§3) is prepended; map is relative to the current backbone.

**MOVEMENT 1 — COLD OPEN (0–30.1) · cue `calm_mystery` → `theme_wonder`**
- **[0.0] a1_01_shell** (SILENT) — `calm_mystery` fade-in soft | `amb_ocean` full + `gull` @~1.5s,~3.8s | `wave_rise` @~2.0s, `sparkle` @~3.5s on the glow | **HOOK: `audio/PIPOS_help1.mp3` (5.19s) @~1.0s** ("Help! Is anyone out there?") ducking music/amb ~4 dB — the audience hears the voice before it sees who. *(With intro prepended, this becomes the inciting button at ~0:24 — see §3.)*
- **[5.0] a1_02_bentley_hear** (talk) — `calm_mystery` lift | bed+`gull` | `audio/PIPOS_help2.mp3` (3.82s) bleeding ~5.0–8.0s so she reacts TO it; soft sniff/breath | backbone Bentley line.
- **[8.7] a1_03_tracking** (SILENT) — `calm_mystery` curiosity | bed | **`sfx/paws.mp3` synced to gait −12 dB**; water trickle | **O.S. `audio/BENTOS_track.mp3` (5.76s) @~8.9–14s** ("Hello? Where are you?"). *Primary fill.*
- **[11.9] a1_04_reveal** (SILENT) — **crossfade to `theme_wonder`** (~1.2s, the discovery cue) | bed warms | `sfx/chime.mp3`+`sfx/sparkle.mp3` on the reveal ~13.5s; soft `sfx/clicks.mp3` | **NEW NARRATION FACT-1** (see §4) seats here.
- **[17.0] a1_05_pip_meet** (talk) — `theme_wonder` soft | bed+`gull` | light `clicks` | **`a1_05_pip_meet_vo.mp3` (6.87s) @17.0**.
- **[24.0] a1_06_twoshot** (talk) — `theme_wonder` | bed laps | subtle `clicks` | backbone two-shot.

**MOVEMENT 2 — THE PROBLEM (30.1–59.8) · `theme_wonder` → `calm_mystery`/light `suspense`**
- **[30.1] N1_bentley_guess** (talk) — `theme_wonder` settling | soft `clicks` | **`N1_bentley_guess_vo.mp3` (7.92s) @30.1**.
- **[38.1] a2_01_pip_correct** (talk) — ease to `calm_mystery` | `clicks` on Pip | **`a2_01_pip_correct_vo.mp3` (9.91s) @38.1** + **FACT-2 narration** rides into N2.
- **[48.2] a2_02_softbody** (talk) — `calm_mystery` gentle concern | shell `clicks`, soft squish; **O.S. `audio/BENTOS_awe_n2.mp3` (5.04s) ~54–59s** if it doesn't fight Pip | **`a2_02_softbody_vo.mp3` (11.43s) @48.2**.
- **[59.8] N2_shell_science** (SILENT) — push to curious/`suspense` bed | `sparkle`/`chime` on diagram-pop, `wave_rise` for life | **NARRATION `audio/THEO_N06.mp3` (11.12s)** — **slot is 5.04s → extend shot to seat the science fact (ties §4) OR use `THEO_N02b.mp3` (4.48s).** *Primary fill + narration anchor.*

**MOVEMENT 3 — THE TWIST (64.9–108.1) · `suspense` (peak @recoil) → `emotional_piano`**
- **[64.9] a3_01_bentley_fix** (talk) — hopeful lift | small `paws` | backbone.
- **[67.8] a3_02_pip_flip** (talk, trimmed to ~8s picture) — `suspense` building | **MASK THE BACK-THIRD: layer `sfx/wave_rise.mp3` + `sfx/wave_crash.mp3` staggered ×2–3 across 67.8→89.5 @−10 dB** + stronger `gull` + bed swell so the ear hears a live ocean | `clicks`/`skitter` on Pip | **`a3_02_pip_flip_vo.mp3` (21.50s) @67.8** (plays over the trimmed clip + recoil) + **FACT-3 narration** (the "crabs can't swim" beat).
- **[89.5] a3_03_recoil** (SILENT) — `suspense` **stinger/hit @89.5** | **`sfx/wave_crash.mp3` hard @−8**, `sfx/shake.mp3`, quick `skitter` | SFX+music carry. *Primary fill.*
- **[94.5] N3_bridge_safe** (SILENT) — `suspense` resolving | `wave_rise`, soft `chime` | **NARRATION `audio/THEO_N10a.mp3` (9.04s)** — **slot 5.04s → extend or trim line.** *Fill + narration.* (Enter continuous wet→dry from recoil, no hard slam.)
- **[99.6] a3_04_bentley_stunned** (talk) — **crossfade to `emotional_piano`** | soft bed | backbone.

**MOVEMENT 4 — THE HEART (108.1–131.9) · `emotional_piano`**
- **[108.1] N4_pip_lonely** (talk) — `emotional_piano` featured, swell | bed down/intimate, lose gulls | **`N4_pip_lonely_vo.mp3` (13.35s) @108.1**; seat the Theodore emotional beat (`THEO_N11` 6.88s or `THEO_N16` 11.36s — whichever scripts as Theodore here).
- **[121.4] N5_bentley_empathy** (talk) — `emotional_piano` brightening toward hope | minimal, soft `paws` if she steps in | **`N5_bentley_empathy_vo.mp3` (10.32s) @121.4**. *(Hold ~1s silent shared look after this before cutting to crowd — §4 warmth.)*

**MOVEMENT 5 — VACANCY-CHAIN PAYOFF (131.9–152.7) · build `triumph`**
- **[131.9] a4_01_crowd** (SILENT) — **`triumph` build (crossfade in)** | bed lifts, `gull` | `sfx/skitter.mp3` ×2 + light `clicks` | **O.S. `audio/BENTOS_chain.mp3` (5.68s) ~132–138s** ("they're all lining up!"). *Primary fill.*
- **[137.0] a4_02_lineup** (SILENT) — `triumph` rising | `skitter`+`clicks` rhythmic, a `chime` per crab as they slot in | **FACT-4 narration** (recycled homes). *Fill.*
- **[142.0] a4_03_cascade** (SILENT) — `triumph` near-peak | **cascade of `clicks`+`sparkle` per swap, ascending; `shake` as shells trade** (the money shot — make it a domino run). *Fill.*
- **[147.0] a4_04_whoaa** (talk) — `triumph` **peaks/hits** | big `sparkle`+`chime` swell | backbone "whoaa".

**MOVEMENT 6 — RESOLUTION + TAG (152.7–197.9) · `triumph` resolve → `theme_wonder` → outro**
- **[152.7] a5_01_piphome** (SILENT) — `triumph` resolving warm | `clicks` + settled `chime` as Pip seats; `shake` (snug fit) | content bed. *Primary fill.*
- **[157.8] a5_02_pipthanks** (talk) — warm `theme_wonder` reprise | soft `clicks` | **`a5_02_pipthanks_vo.mp3` (13.91s) @157.8** — **trim the silent head/tail of picture, KEEP the full line** (emotional payoff).
- **[171.9] a5_03_disco** (talk, 2.4s) — continue | light `sparkle` | backbone.
- **[174.3] N6_payoff_armor** (talk) — `theme_wonder` swelling to the lesson | `sparkle`/`chime` on "armor" | **`N6_payoff_armor_vo.mp3` (10.32s) @174.3**; Theodore payoff candidate `THEO_N16` (11.36s) or `THEO_N19` (8.32s).
- **[184.8] a5_04_tag** (talk) — `theme_wonder` resolve | warm `chime` button | backbone tag + **`audio/THEO_outro.mp3` (10.72s) sign-off** seated here/bridging into the stinger.
- **[192.8] a6_01_octopus** (SILENT) — final mysterious `calm_mystery` re-tease | **`sfx/octo_curl.mp3` (3s) ~193–196s** on the curl; `wave_rise` + last `sparkle`; soft `wave_crash` as it submerges | **O.S. `audio/BENTOS_octo.mp3` (7.92s) 192.8→end** — but **re-record/relight the read as DELIGHTED not ominous** ("Did that octopus just WAVE at me?! New friend!" — §4). *Final fill.*

### 2.4 AUDIO ASSETS STILL TO GENERATE (flag to user)
1. **Theodore narration too SHORT for 2 slots (the #1 audio blocker):** `N2` & `N3` are 5.04s motion shots but `THEO_N06` (11.12s) / `THEO_N10a` (9.04s) need 9–11s. **Resolve by extending those shots (ties to the ≥4-min new content, §4) OR record/trim ~5s Theodore lines.**
2. **Bentley-INTRO narration — MISSING.** No "meet Bentley" line exists. **Generate 4 new Theodore cold-open lines (§3).**
3. **5 new Nat-Geo FACT lines (§4)** — Theodore VO, warm-grandpa voice, ≤1 sentence each (FACT-1…FACT-5). The current 7 Theodore lines won't cover them.
4. **2 re-read O.S. lines:** Pip callback "we do NOT do the big water" (over N3 shake); **delighted** octopus button (replaces ominous `BENTOS_octo` read).
5. **Transition whooshes/risers — MISSING** (no whoosh in `sfx/`). **Generate 2–3 soft risers** for movement seams (reveal 11.9, recoil hit 89.5, triumph build 131.9, stinger 192.8). `wave_rise`/`chime` can stand in.
6. **Nice-to-have:** light **crab-chitter ambient loop** for 131.9–147 (better than re-triggering 3s `skitter` one-shots).
7. **Music:** the 5 existing cues + crossfades cover all 198s — **no new music needed.**

---

## 3. INTRO SEQUENCE SPEC — "MEET BENTLEY" (0:00–0:26, prepended before current open)

**Goal (26s):** establish her name, that she's a happy curious puppy, her superpower (she *listens*), her world (Crystal Cove at dawn), and the mantra "Stop. Look. Listen." — so Pip's "Help?" becomes the **inciting incident** at ~0:24 instead of the cold first frame. The current backbone then resumes **unchanged**.

| t | shot | source | what we see | Theodore VO (NEW — record) | sound |
|---|------|--------|-------------|----------------------------|-------|
| 0:00–0:06 | **INTRO-1 establish** | ♻️ **REUSE `…/opening_redo/clips/S1_establish.mp4`** (6.0s — clean pearlescent spiral shell on black sand + surf; **retire fuzzy `a1_01` as the opener**) | Slow Ken-Burns in on the dawn cove; mist, far gull, a row of little shells. Title card **"BENTLEY'S BIG ADVENTURES"** fades in/out. | *"Every morning, before the world wakes up… the ocean leaves Crystal Cove full of secrets."* | 2-note wonder motif (sparse `theme_wonder` head), `amb_ocean`, lone `gull`. Fills the current 0–5s dead silence. |
| 0:06–0:14 | **INTRO-2 hero reveal** | 🆕 **1 NEW wide motion shot (Hailuo ~6 cr)** — **cannot reuse `H1_wonder` (ear UP + long tail) or `H4_collar` (flat style)** | Bentley trots onto a tide-pool rock, ears flopping, stub-tail wagging, sniffs, a happy play-bow. Wide, full-body, her world behind. | *"And THIS… is Bentley. She's not the biggest pup on the beach… but nobody — nobody — is more curious."* | Music blooms to light curious-adventure bed; `paws` on wet rock, ear-flaps, a happy snuffle. |
| 0:14–0:20 | **INTRO-3 the superpower** | ♻️ **REUSE `a1_02_bentley_hear`** CU (on-model, floppy ears, head-tilt) — re-purposed: listening to the *world*, not yet to Pip | Tight on her face: ears swivel, head-tilt, the collar-shell gives its first soft glow. | *"While everyone else just runs past… Bentley stops. She looks. And she listens."* | Collar-glow `chime` (leitmotif seed). Music holds on "listens." |
| 0:20–0:26 | **INTRO-4 mantra → hand-off** | ♻️ **REUSE tail of `a1_02` / head of `a1_03_tracking`** | Her ear pricks-toward-sound (now motivated), she turns screen-left toward the cove. | *"Because when you really listen… the whole world starts talking back."* → **then Pip O.S. `PIPOS_help1`:** *"…H-help? Is anybody out there?"* | Motif drops to a lonely sting under Pip's cry — inciting hook lands ~0:24. |

**New renders for the intro: exactly ONE** = INTRO-2 (already counted as the project-wide intro spend, **~$6**, listed in §5). Everything else = reuse + 4 new Theodore lines + a title card.
**INTRO-2 keyframe MUST bake the guards hard** (the wide `H1_wonder` failed all three): **short docked stub tail, BOTH ears floppy-down, NO white socks, NO human teeth, soulful well-proportioned eyes.**

---

## 4. NEW CONTENT to clear ≥4:00 (fact beats / reactions / transitions)

Almost all new content is **Theodore/character VO over existing or trimmed footage** — **zero new render** beyond the §3 intro shot.

### 4.1 Five Nat-Geo FACT beats (new Theodore VO, ≤1 sentence each)
- **FACT-1 — "carries his house"** over `a1_04_reveal` (~0:30, currently silent): *"That's Pip — a hermit crab. He's so soft he has to wear a borrowed seashell like a backpack… and carry his whole house on his back, everywhere he goes."*
- **FACT-2 — "he can feel it getting tight"** over `a2_01`→`N2` (~0:50): *"A hermit crab can FEEL when his shell gets too snug — just like outgrowing your favorite shoes. So he has to go shopping for a bigger one."*
- **FACT-3 — "crabs walk, they don't swim"** on `a3_02` (~1:25) — **this fact justifies the §1 RR-2 trim to ~8s:** *"Here's what the big dog didn't know: little shore crabs like Pip can't swim at all. They WALK on the sea floor — so a big wave isn't fun, it's the scariest thing in the world."*
- **FACT-4 — "shells are recycled homes"** over `a4_02_lineup` (~2:17, currently silent): *"Hermit crabs never waste a good home. When one crab leaves a shell behind… it becomes someone else's brand-new house. The ocean's very own hand-me-downs."*
- **FACT-5 — "this really happens" credibility tag** appended to `THEO_N16` (~3:30): *"Scientists really do call it a 'vacancy chain' — and they've filmed dozens of real crabs doing it on beaches all over the world. It's true!"*

### 4.2 Warmth / reaction beats (mostly reaction-trims of existing shots + short VO — no render)
1. **After the soft-body reveal (`a2_02`, ~0:50):** cut to a 1.5s Bentley CU trimmed from `a1_06`/`N5` — BENTLEY (tender): *"Aww. I'd never let you be a snack, Pip."*
2. **After the shake (`N3`, ~96s):** PIP (breathless, relieved, VO over the shake): *"Thank you. Thank you. We do NOT do the big water. We've discussed this."* (biggest laugh-with-warmth).
3. **Heart-scene breath:** after `N5_bentley_empathy`, hold ~1s of silent shared look (collar glowing) before cutting to the crowd — let "you're not alone" land (cap the held beat ~6s, don't wallow).
4. **Octopus button — DELIGHT not scare** (over `a6_01_octopus`): BENTLEY O.S. (delighted): *"…Wait. Did that octopus just WAVE at me?! Ooh — new friend!"* (re-read replaces ominous `BENTOS_octo`).
5. **Protect the existing payoff:** `a5_02_pipthanks` ("you were the first one who really listened… come back any time") — trim only the **silent head/tail**, keep the full line.

### 4.3 Transitions pass (4 real treatments + cheap sound-bridges; all free)
**Do these:**
1. **`a3_04`(99s) → `N4`(108s):** **cross-dissolve ~0.5s + piano carries across; music does NOT change N4→N5** so the two faces read as one shared moment.
2. **`a1_01`(0s) → `a1_02`(5s):** **match-cut on the GLOW** — shell glow-pulse motivates the cut to her collar-shell catching the same light; Pip O.S. continues across. *(Seam moves under the intro but the glow-match still applies.)*
3. **`a3_03` recoil → `N3`(94.5s):** verify **continuous wet→dry** (soaked at recoil end, soaked at N3 start) — no hard slam.
4. **`a5_03`→`N6`→`a5_04`** (three Bentley CUs): **sound-bridge** her grin/laugh under the cuts; **if Act 6 sags, drop N6 first** (also dodges the long-tail bug until RR-1 lands).

**Sound-bridge only:** `N1`→`a2_01` (tail "best morning ever" under Pip's deadpan); `N5`(~131s)→`a4_01` cut wide on her **eyes OPENING** as first shell-clicks rise (the single best motivated cut — protect it). **Match-cut:** final cascade click → `a4_04` jaw-drop (smash on the last click).
**Hard rule:** no hard cut between two static frames — every cut motivated by motion, eyeline, or sound bridge.

### 4.4 Runtime math (≥4:00 target)
Current backbone 197.88s = 3:17.9.

| addition | method | Δ |
|----------|--------|---|
| Cold-open intro (§3, 4 beats) | 1 new render + reuse | **+26s** |
| 5 fact beats (FACT-1,2,4 ride silent/over-long ≈0; FACT-3 adds breath; FACT-5 extends N16) | VO over existing | **+8s** |
| Theodore narration laid in (N02b/N06/N10a/N11/N16/N19/outro ≈ 62s of VO, currently absent; outro+bridges extend tail) | lay existing VO | **+18s** |
| Warmth lines + 1s held look (§4.2) | VO + hold | **+9s** |
| Trims (savings): a3_02 21.7→~8s (−13.7), a5_02 −4, a1_03 −2, silent-head trims | trim holds | **−22s** |

**Net:** 197.9 + 26 + 8 + 18 + 9 − 22 ≈ **237s = 3:57** (conservative — excludes music tails, title-card hold, dissolve overlaps). **Honest landing 4:05–4:15**, comfortably past the ≥4:00 floor and short of 4:45 (3–5yo drop-off risk).

---

## 5. EXECUTION ORDER (checklist)

**PHASE A — RE-RENDERS (the only fal spend; do first so the cut is final before audio pins to frames)**
- [ ] **A0. Frame-verify RR-4 (`a5_03_disco`)** — pull frames; confirm white socks yes/no. Resolves $0 vs $6.
- [ ] **A1. RR-1 N6_payoff_armor** — re-key (short docked tail in frame, NO long tail) → Hailuo **2 takes** → pick best → trim to ~10.5s. *(top priority)*
- [ ] **A2. RR-2 a3_02_pip_flip** — re-key Pip (eyes-in-face, NO human teeth) → 1 take ~8s → **hard-trim picture to ~8s**.
- [ ] **A3. RR-3 a3_03_recoil** — re-key startle eyes (soulful, NOT googly) → Hailuo **2 takes** → keep best motion.
- [ ] **A4. RR-5 N4_pip_lonely** — re-render full **1080p** → 1 take ~13.3s.
- [ ] **A5. RR-4** only if A0 confirmed socks → 1 take ~2.4s.

**PHASE B — INTRO (§3)**
- [ ] B1. Render **INTRO-2** Bentley hero-reveal wide (~$6, guards baked).
- [ ] B2. Cut the title card; assemble INTRO-1 (`S1_establish`) + INTRO-2 + reuse `a1_02`/`a1_03` per §3.
- [ ] B3. Record the 4 new Theodore intro lines.

**PHASE C — NEW VO (free)**
- [ ] C1. Record 5 Nat-Geo fact lines (FACT-1…5) + FACT-5 N16 tail.
- [ ] C2. Record/re-read warmth lines: Pip "we've discussed this," Bentley "never a snack," **delighted** octopus button.
- [ ] C3. Resolve the 2 over-length Theodore slots (extend N2/N3 shots OR trim THEO_N06/N10a to ~5s).
- [ ] C4. Generate 2–3 transition risers (+ optional crab-chitter loop).

**PHASE D — SOUND DESIGN (§2)**
- [ ] D1. Lay `amb_ocean` continuous bed (−16 dB, ×9).
- [ ] D2. Drop 5 music cues on a bus with 1.2s crossfades at movement seams.
- [ ] D3. **Re-pin every `*_vo` + `THEO_*`/`PIPOS_*`/`BENTOS_*` to exact frame starts** (kills drift; LOCKED).
- [ ] D4. Spot all SFX — prioritize the 11 silent windows; **layer wave SFX under a3_02** to mask the back-third stall.
- [ ] D5. Sidechain-duck music+ambient under the summed VO stem (−8 dB).

**PHASE E — ASSEMBLE / EDIT (free)**
- [ ] E1. Insert intro at head; apply the 4 transition treatments + sound-bridges (§4.3).
- [ ] E2. Apply trims (a3_02→~8s, a5_02 keep-line trim, a1_03 −2s, silent-heads) + warmth inserts + 1s held look.

**PHASE F — GRADE / FINISH**
- [ ] F1. **Normalize resolution + fps to one spec** (mixed: acts 1904×1088@24, v2 talk 1264×720@30, re-renders 1080p) → upscale to 1080p, conform fps; removes visible quality steps.
- [ ] F2. Color grade to the golden-dawn look; comp the **POST-FIX parallax water + cloud drift** behind the 8 static-BG close-ups.
- [ ] F3. Premix → `loudnorm I=-14:TP=-1.5:LRA=11` → mux to picture.

**PHASE G — FINAL QA VERIFY**
- [ ] G1. Re-extract frames on the 5 re-renders: N6 tail SHORT ✓, a3_02 Pip eyes-in-face/no-human-teeth ✓, a3_03 eyes not googly ✓, a5_03 no socks ✓, N4 1080p ✓.
- [ ] G2. Per-segment volume scan: **no −91 dB silent windows remain**; cold-open `PIPOS_help1` audible ~1.0s.
- [ ] G3. Confirm runtime ≥4:00; A/V sync (no drift); music never hard-cuts.

### TOTALS
- **Final runtime estimate:** **~4:05–4:15** (≥4:00 floor cleared).
- **Total NEW fal cost:** **~$36 committed** (RR-1/2/3/5 = 6 takes) **+ ~$6 intro (INTRO-2)** **= ~$42; max ~$48** if RR-4 (a5_03) needs a re-render. Everything else (all VO, edit, sound design, transitions, grade) is **free**.
