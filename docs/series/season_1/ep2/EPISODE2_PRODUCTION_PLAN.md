# Episode 2 — "The Octopus Escape Artist" · Implementation & Budget Plan
### Season 1 · Episode 2 · **Bentley's Big Adventures**

> **STATUS: PLAN ONLY — NOT APPROVED FOR PRODUCTION.** No renders, no voice generation, no animation, no credits spent. Production begins only after sign-off on the Approval Checklist (§14).
>
> Prepared by the EP/showrunner desk with 7 specialist passes: Story Editor · Science/Nat-Geo Editor · Production Designer · AI Production Supervisor · Voice/Audio Director · YouTube/SEO/Shorts Strategist · QC Producer.
>
> **Channel rename note:** ✅ Done at T0 — *"Bentley's Discovery Club"* → **"Bentley's Big Adventures"** swept across **27 active docs** (source draft, `LOCKED_ELEMENTS.md`, all series scripts, launch kit, README). `deprecated/` left untouched. This plan keeps a few quoted "Discovery Club" mentions only to document the rename.
>
> **✅ DECISIONS LOCKED:** Backend = **KIE.ai (primary; fal.ai retired)** · Tier = **Recommended ("Hero-Balanced", ~$20–35 all-in)** · Eel = **Silhouette-soft** · Indi voice = **Guarded-but-warm** (blind 5-voice audition) · Title **B** + Thumbnail **A** · **Pip = OUT** (no cameo).
>
> **▶ STATUS (2026-06-20): Indi master FINAL (s14 + defined ocelli, via Nano Banana Pro) · voice LOCKED.** `Indi_LOCKED.png` (anchor URL in `.indi_locked_url.txt`) = the single source every shot edits from. **Edit Indi with `nano-banana-pro`** (best consistency). Voice = `FcZStbCG9g9QxDlJioSD` → `tts_indi()`. **~242 KIE cr** of 10,439 (~$1.20). **To do:** regenerate the model sheet + hero shots from this final master (earlier ones used superseded looks) → then Gate D (motion). **Locked rules:** lock-to-reference (never re-describe Indi's face); ocelli = defined iridescent ring, **NO "chain-link", NO glow**; QA every frame before showing. Still NO motion/avatar/episode spend.

---

## 1. Executive Summary

Episode 2 turns Episode 1's mystery tentacle into a character: **Indi**, a shy **California two-spot octopus** who vanishes the instant she's seen. Bentley's flaw — *helping by doing* — is active and costly: she chases and grabs to "catch" Indi, and her chasing literally drives Indi toward a moray eel. The turn is **stillness**: Bentley stops, the Listening Shell glows, and Indi *chooses* to come out. The episode's feeling is social-emotional gold for the 4–8 audience: *you don't have to disappear to be safe.*

**Why this episode is cheap to make well:** almost every expensive element already exists and is approved.
- The **octopus teaser** (`octopus_NEW.mp4`, 10s, 1904×1088) seeds Indi *and* gives us a season-callback shot.
- The **Tidepool-cove plate** is the locked environment.
- The **glowing Listening Shell** (`CLEAN_shell.mp4`) IS the turn beat.
- **Bentley, Pip, and Narrator voices are locked**; only **Indi** is a net-new voice.
- The hard part of octopus animation (8 articulated arms + lip-sync) is **designed around**, not brute-forced: partial reveals, one expressive arm, the **eye** and **eyespots** as hero focus, and **ink puffs as cheap transitions**.

**Current production stack (this matters for budget):** the team has migrated off Higgsfield credits, and **KIE.ai is now the primary backend** (cheaper than fal.ai, which is **no longer used**) — keyframes via **Nano-Banana** (≈free), motion via **Kling 2.6 i2v**, talking via **Kling-Avatar**, voice via **ElevenLabs `eleven_v3`**, assembly in ffmpeg. Observed KIE rates run roughly **½ the image / ¾ the video / ½ the talking** cost of the old fal path. Episode 1's re-render pass cost **~$36–42** on the older path; on KIE, Episode 2's recommended tier lands around **~$20–35 all-in**. The real cost here is *iteration for on-model consistency*, not raw render fees. ⚠️ **Two KIE gotchas to design around:** image inputs must be **URL-hosted (catbox)**, and **Kling-Avatar tends to darken** output — which compounds the "too-dark underwater" risk (§10).

**Recommendation:** approve the **Recommended ("Hero-Balanced") tier (~$20–35 on KIE)**. The eel (silhouette-soft), Indi voice (guarded-but-warm), and Title B / Thumbnail A are already locked. Everything is staged so we can start the moment you pick a tier and sign §14.

---

## 2. Revised Episode 2 Story Spine

**Logline (kept, sharpened):** The mysterious tentacle finally has a face — **Indi**, a shy octopus who vanishes the instant anyone looks at her. Bentley chases her to "help," not realizing Indi isn't running *away* — she's terrified of being *seen* — and she's been leaving shell-messages because the open water is in trouble.

**Format:** ~4:00–4:45 runtime · cold-open hook → 6 beats → cliffhanger. Built for new viewers and Ep-1-only viewers (re-introduce Bentley + the Listening Shell in the first 25s without slowing the hook).

| Beat | What happens | Function |
|---|---|---|
| **Cold hook** | Bentley reaches to boop a "cute speckled rock." The rock **opens one giant eye**, flushes deep red, vanishes in ink. *"The ROCK had an EYEBALL!"* | Curiosity gap; the thumbnail moment. |
| **Re-intro (fast)** | Narrator: who Bentley is, what the glowing shell does ("Stop. Look. Listen."). 1 line, over motion. | New-viewer onboarding without a speed bump. |
| **Flaw on display** | Bentley tries to *catch* Indi to "help" — lunges, herds, **boops six wrong rocks; one squirts her.** | Comedy + character flaw active. |
| **It gets worse** | Bentley corners Indi in a crevice. Indi panics, inks, and **bolts toward a moray eel's lair.** *Her chasing drove Indi into danger.* | Stakes; Bentley's method backfires. |
| **THE TURN** | Stop. Look. Listen. **Shell glows.** Bentley sits, backs off, goes still. Indi *chooses* to creep out: *"I wasn't running from you. I run from everybody… But I kept leaving you shells because somebody finally needs to listen — the open water's gone wrong."* | The lesson, dramatized as an action (stop doing). |
| **Climax (clock + setback)** | The eel looms; Indi gets **wedged** hiding. Bentley's instinct to **yank her free fails** (could hurt her). Bentley talks her calm — *"You don't need me to pull. You can pour yourself out — just breathe."* Indi **squeezes through an impossibly tiny gap** to safety. | Science = the solution. Bentley wins by *not* grabbing. |
| **Emotional button** | A shy tentacle reaches and **holds Bentley's paw.** *"You don't have to disappear to be safe with me. I see you. And you're not scary OR small. You're amazing."* | Payoff of the feeling. |
| **Cliffhanger → Ep 3** | Indi presses an urgent message into Bentley's paw — a warning about **"the gathering"** — and points inland to a perfect line of **ants** marching off with a **car-sized crumb.** *"Wait — where are you all going?"* → *The Ant City Beneath Our Feet.* | Season engine; next-episode pull. |

**Story-editor notes (changes from draft):**
1. **Add a 1-line re-intro** after the hook (currently the draft jumps straight in). Keeps new viewers oriented; costs one narrator line over reused footage.
2. **Plant the shells early.** In the chase, show one of Bentley's "wrong rocks" actually has a **tiny arranged shell beside it** — so Indi's shell-messages are visually seeded *before* the confession pays them off.
3. **Make the squirt gag land the theme.** The rock that squirts Bentley should be the one she's *most sure* about — "doing" confidence punished. Small touch, big character.
4. **Pip is OUT of Episode 2** (locked decision). No cameo — keeps the cast tight (Bentley + Indi + Narrator), avoids an extra voice track and clips, and keeps full focus on Indi as the guest character. Pip returns in a later episode.

---

## 3. Emotional Arc

**Bentley's arc (active flaw → growth):** *Doing → Backfire → Stillness → Trust.*

| Stage | Bentley's internal state | Visible behavior | Turn |
|---|---|---|---|
| 1. Confident helper | "I can fix this / catch this!" | Chasing, grabbing, herding, booping rocks | — |
| 2. Backfire | "Wait… I made it worse." | Freezes as Indi bolts toward the eel | The cost of doing |
| 3. Surrender of control | "Maybe I help by *not* grabbing." | Sits, backs off, goes still; shell glows | The lesson, as an action |
| 4. Earned trust | "I see her. She chose me." | Stays put; lets Indi pour herself free; paw-hold | Payoff |

**Indi's arc (guarded → seen):** terrified-of-being-seen → tests Bentley by staying hidden → risks one arm → confesses → trusts. Indi's **eyespots** are an emotional instrument: flared/bright when startled (defense), dim/soft when she feels safe. We *animate trust as light in her false eyes.*

**Audience feeling (SEL):** *Being so shy/anxious you "disappear" to feel safe — and learning you don't have to vanish to be loved.* Target emotion curve: delight (hook) → laughter (chase) → worry (eel) → tenderness (turn) → relief + warmth (escape + paw-hold) → curiosity (ants).

---

## 4. Science Facts & How Each Is Dramatized

**All facts verified against current sources (June 2026). California two-spot octopus = _Octopus bimaculoides_, "bimac."** The species genuinely lives in SoCal/Baja **rocky-reef tide pools at low tide**, so the cove premise is accurate, not a liberty.

| # | Verified fact (accurate framing) | How it's dramatized | Accuracy guardrail |
|---|---|---|---|
| **F1** | **Master camouflage:** changes **color (chromatophores) AND texture (papillae)** to vanish into rock/coral/sand — **in under a second** (smooth→spiky as fast as it recolors). | The cold-hook "rock with an eye"; the six wrong rocks; one rock's skin visibly goes **smooth→bumpy** as Bentley stares. | ❌ Don't say "milliseconds" — say **"in the blink of an eye / faster than you can blink."** |
| **F2** | **Two blue eyespots (ocelli):** the namesake — one iridescent-blue, black-ringed false eye on **each side of the head**, a **startle defense.** | Indi's signature look; eyespots **flare bright** when she's scared (at the eel), **dim** when safe (paw-hold). | ❌ NOT the deadly **blue-ringed octopus** — two *large false-eye* rings, not many small electric rings. Bimac is harmless. |
| **F3** | **Three hearts + blue blood:** two gill (branchial) hearts + one body (systemic) heart; blood is blue because it carries oxygen with **copper-based hemocyanin** (not iron). The body heart **stops when she swims**, so she'd rather **crawl/ooze.** | Narrator payoff montage; *and* it motivates character — Indi **creeps and pours** rather than zooming, because swimming tires her big heart. | ✔ "Copper makes her blood blue" is correct and kid-clear. |
| **F4** | **Boneless escape artist:** the **only hard part is the beak** (chitin, like a crab claw); she can squeeze through **any gap bigger than her beak** — about the size of a coin. | **The climax.** Wedged hiding from the eel, Indi **pours her whole body through a coin-size gap** to safety. Bentley's *yank* fails; *breathing and pouring* works. | ✔ Real-world anchor for narrator: "Inky the octopus" escaped through a drainpipe. |
| **F5** | **Arms that taste & think:** ~**two-thirds of her neurons are in her arms**; suckers **"taste by touch"** (chemotactile sensors); arms act semi-autonomously. | One expressive arm explores the shell-message and "reads" Bentley's paw by touch; narrator: *"Her arms can taste whatever they touch."* | ❌ Don't claim "9 full brains / a brain in every arm" — say **"her arms can taste and think a little for themselves."** |

**Optional "mind-blown" aside (Short #6 candidate):** octopuses are **colorblind** yet camouflage to color perfectly. Great wow-fact, but can confuse the core camouflage beat for the youngest viewers — recommend it as a **Short**, not a main-episode line.

**Science editor verdict:** **APPROVED with the two wording fixes above** (F1 "blink of an eye," F5 "taste and think a little"). No fact rejected. The eel is a *real* bimac predator in this exact habitat, so the jeopardy is honest nature, not invented peril.

---

## 5. Shot-by-Shot Production Plan

**Master spec:** 1904×1088 @ 24fps (matches Ep1 + all reusable plates). Shorts derived at 1080×1920. **Legend:** Status **R** = reuse approved asset · **R+** = reuse with edit · **N** = net-new · **N(seed)** = new but seeded from a reused keyframe. Diff/Risk = Low/Med/High. $ = per-shot estimate at **Recommended** tier (includes expected re-takes; this is a conservative *fal-era ceiling* — on the current KIE backend expect ~25–35% lower). Tools: **NB** = Nano-Banana keyframe (≈free) · **K2.6** = Kling 2.6 i2v motion (KIE) · **KAv** = Kling-Avatar talking (KIE) · **FFX** = ffmpeg/VFX (ink, Ken-Burns, glow) — no AI cost.

### ACT 0 — Cold Hook (0:00–0:20)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4s | Wide dawn tide-pool cove; gentle water; settle in | — | **Tidepool_plate** (R) + wave plate `a3_02a_wave_NEW` (R+) | FFX Ken-Burns | R+ | Low | Low | ~$0 |
| 2 | 4s | Bentley creeps to a "cute speckled rock," paw reaching to boop | Bentley | Bentley locks; new rock prop | NB→K2.6 | N(seed) | Med | Off-model | ~$1.2 |
| 3 | 4s | **MONEY SHOT:** rock **opens one huge eye**, flushes deep red | (Indi-as-rock) | rock→eye morph; eyespot hint | NB→K2.6 | N | **High** | camouflage clarity | ~$2.5 |
| 4 | 5s | **Ink puff**, Indi gone; Bentley through cloud: *"The ROCK had an EYEBALL!"* | Bentley | ink FFX kit; Bentley talk | KAv + FFX | N | Med | human teeth | ~$1.8 |
| — | — | **Title card / channel ident: "Bentley's Big Adventures"** | — | brand template (R) | FFX | R | Low | Low | ~$0 |

### ACT 1 — The Chase / Flaw (0:20–1:35)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 7s | Narrator re-intro over Bentley + glowing shell ("Stop. Look. Listen.") | Bentley | Bentley still (R) + **CLEAN_shell** (R) + Narrator VO | FFX | R | Low | Low | ~$0 |
| 6 | 8s | Comedy montage: Bentley **boops 6 wrong rocks**; one **squirts** her | Bentley | 2–3 quick clips; reuse reaction seeds H2/H5 | NB→K2.6 | N(seed) | Med | continuity | ~$2.4 |
| 7 | 5s | Close: a rock's skin goes **smooth→bumpy** (texture science F1) | (Indi skin) | papillae morph VFX | NB→K2.6 | N | Med | camouflage clarity | ~$1.5 |
| 8 | 5s | Bentley spots a real **arm**, lunges to herd; Indi **camouflages, gone** (+ a tiny arranged **shell** beside the rock) | Bentley + 1 arm | one-arm partial reveal; shell prop (R) | NB→K2.6 | N | Med | arm chaos | ~$1.6 |

### ACT 2 — It Gets Worse (1:35–2:25)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 9 | 5s | Bentley **corners Indi** in a crevice; Indi panics, **eyespots flare** | Bentley + Indi | Indi (eye + arm), crevice plate | NB→K2.6 | N | Med-High | arm chaos | ~$2.0 |
| 10 | 5s | Indi **inks and bolts** toward the **moray eel's lair** (shadow/teeth glint) | Indi, eel(silhouette) | eel as **silhouette**; ink FFX | NB→K2.6 | N | **High** | too scary / too dark | ~$2.5 |
| 11 | 4s | Eel stirs in the dark; **Bentley realizes** her chase drove Indi into danger | Bentley, eel(partial) | Bentley dawning-horror (seed H3 recoil) | NB→K2.6 | N | High | too scary | ~$2.0 |

### ACT 3 — The Turn (2:25–3:15)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 12 | 4s | **Stop. Look. Listen.** The **shell glows.** | Bentley | **CLEAN_shell.mp4** (R as-is) | FFX | R | Low | Low | ~$0 |
| 13 | 5s | Bentley **sits, backs off, goes still** | Bentley | calm-still keyframe (seed H1 wonder) | NB→K2.6 | N(seed) | Low-Med | off-model | ~$1.2 |
| 14 | 6s | **HERO:** long beat — Indi **chooses** to creep out; eyespots soften | Indi | full Indi reveal (locked design) | NB→K2.6 | N | **High** | arm chaos | ~$3.0 |
| 15 | 7s | Indi confession (VO over subtle arm gestures, minimal lip-sync): *"I wasn't running from you… the open water's gone wrong."* | Indi | Indi VO; arm motion | K2.6 + VO | N | Med-High | lip-sync | ~$2.2 |
| 16 | 8s | **HERO exchange** (intercut CUs): *"Why do you keep hiding?" / "If nobody sees me, nobody can be disappointed by me." / "…right in the snack pouch. But I'm not leaving."* | Bentley + Indi | Bentley talk (KAv) + Indi VO | KAv + K2.6 | N | High | human teeth / lip-sync | ~$3.2 |
| **16A** | 7s | **BONDING — no plot, "the color game"** (per showrunner note; see [[bentley-bonding-two-shot]]): trust won, the chase becomes PLAY — Indi shyly shows off, color-shifting for fun, then turns the exact **red-fawn of Bentley's coat** to "match" her new friend; Bentley melts (*"You did ME!"*); a gentle peek-a-boo. The cute two-shot that makes us care before the climax. *(Recontextualizes the chase as joy; strong Short + thumbnail. Flavor swappable — alt: Indi fetches Bentley's slipped shell charm with a boneless arm.)* | **Bentley + Indi together** | reuse tidepool plate; Indi color states (model sheet) | NB→K2.6 | N | Med | arm chaos | ~$2.0 |

### ACT 4 — Climax (3:15–4:05)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 17 | 5s | Eel looms again; Indi panics, gets **wedged** | Indi, eel | eel silhouette; crevice | NB→K2.6 | N | High | too scary | ~$2.2 |
| 18 | 4s | Bentley's instinct: **tries to yank Indi free — fails** (could hurt her) | Bentley + arm | tension beat | NB→K2.6 | N | Med-High | arm chaos | ~$1.8 |
| 19 | 6s | Bentley talks her calm: *"You don't need me to pull. You can pour yourself out — just breathe."* | Bentley + Indi | Bentley talk (KAv) | KAv | N | Med | human teeth | ~$2.2 |
| 20 | 6s | **BIGGEST MONEY SHOT:** Indi **pours her boneless body through a coin-size gap** (F4) | Indi | squeeze VFX; ink-assisted | NB→K2.6 | N | **High** | arm chaos / believability | ~$3.5 |
| 21 | 4s | Indi **reforms** safe; eyespots soft; relief | Indi | Indi reform | NB→K2.6 | N | Med | continuity | ~$1.5 |

### ACT 5 — Emotional Button + Science Payoff (4:05–4:40)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 22 | 6s | **HEART SHOT:** a shy **tentacle holds Bentley's paw** (macro, slow) | Bentley paw + 1 arm | macro paw + one arm | NB→K2.6 | N | Med-High | arm chaos | ~$3.0 |
| 23 | 6s | Button line: *"You don't have to disappear to be safe with me. I see you… You're amazing."* | Bentley | Bentley talk CU (KAv) | KAv | N | Med | human teeth | ~$2.2 |
| 24 | 8s | **Science payoff montage** (Narrator F3+F4+F5): 3 hearts/blue blood, boneless, arms taste | Indi clips | reuse Indi shots + motion-graphic overlays | FFX + VO | R+ | Low-Med | accuracy | ~$0.6 |

### ACT 6 — Cliffhanger → Ep 3 (4:40–5:00)
| # | Dur | Visual | Chars | Assets | Tool | Status | Diff | Risk | $ |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 4s | Indi **presses an urgent message** into Bentley's paw — *"the gathering"* | Indi arm + paw | macro callback | NB→K2.6 | N | Med | arm chaos | ~$1.5 |
| 26 | 5s | Indi **points inland** → a perfect line of **ants** with a **car-sized crumb** | Indi, ants | new ants plate | NB→K2.6 | N | Med | new env | ~$1.8 |
| 27 | 4s | Bentley: *"Wait — where are you all going?"* → tease card **"The Ant City Beneath Our Feet"** | Bentley | end-tag template (R+) | FFX + VO | R+ | Low | Low | ~$0.3 |
| 28 | 5s | Outro / subscribe / channel ident | — | brand template (R) | FFX | R | Low | Low | ~$0 |

**Totals (Recommended tier):** ~28 shots · ~**4:35** runtime · **~13 net-new keyframes**, **~24 net-new motion/talking clips** (incl. expected re-takes). The per-shot $ column is a conservative fal-era ceiling (~$55 raw); on **KIE** the real Recommended-tier all-in is **~$20–35** (§9), via reuse + cheaper KIE rates + Ken-Burns/FFX free shots. *(Hero shots 3, 14, 16, 20, 22 carry the budget; reused/FFX shots 1, 5, 12, 24, 28 carry ~$0.)*

---

## 6. Asset Reuse Table

> Verified on disk (paths relative to repo root unless noted). This is the single biggest cost + consistency win of the episode.

| Asset | Path | Spec | Ep2 use | Verdict |
|---|---|---|---|---|
| **Octopus teaser** | `assets/approved/scenes/octopus_NEW.mp4` (= `assets/pilot_shots/ep1/v2/fixed/octopus_NEW.mp4`) | 10.04s · 1904×1088 · 24fps | **Seed Indi's design** + **callback reveal shot**. Ep1 octopus *is* Indi. | **R+ / seed** |
| **Tidepool-cove plate** | `assets/character_design/TidePool_plate.jpg` (+ `_alt`) | 1376×768 | Primary environment for all wides/establishers | **R as-is** |
| **Listening Shell (glow)** | `assets/approved/shells/CLEAN_shell.mp4` + `CLEAN_shell_key.png` | 5.04s · 1904×1088 | **The Turn beat** (shot 12) + re-intro (shot 5) | **R as-is** |
| **Water/wave motion** | `assets/approved/scenes/a3_02a_wave_NEW.mp4` | 10.04s · 1904×1088 | Establishers, transitions, ambience | **R+** |
| **Bentley hero/locked stills** | `assets/character_design/Bentley_HERO_LOCKED.jpg`, `assets/approved/bentley/N6_kie_key_bright2.png`, `BR3_explore_key.png`, `Bentley_MASTER_clean_16x9.png` | 896×1200 / 1344×768 | Keyframe bases for new Bentley shots + thumbnail | **R / reference** |
| **Bentley model sheets** | `assets/character_design/Bentley_MODEL_SHEET_turnaround.png`, `…_expressions.png` | 1376×768 | Embed in every new Bentley keyframe prompt | **R as-is** |
| **Bentley expression seeds** | `assets/pilot_shots/ep1/hero_keyframes/HK1_wonder`, `HK2_whoaa`, `HK3_recoil`, `HK5_vacwhoaa`.png | 1280×720 | Seed reaction keyframes (shots 6, 11, 13) | **R+ / seed** |
| ~~Pip~~ (cut) | `assets/character_design/Pip_LOCKED.jpg` etc. | — | **NOT used in Ep2** (Pip out — locked decision) | — |
| **Stella** | `assets/character_design/Stella_LOCKED.jpg` | 1024×1024 | Reference only (not in Ep2 unless added) | **reference** |
| **Locked voices** | `bentley/shared/eleven.py` | — | Bentley=LauraZ, Pip=Callum+10%, Narrator=Bill | **R as-is** |
| **Voice tone refs** | `assets/approved/voices/BENTOS_awe_n2.mp3`, `THEO_INTRO1.mp3`, `THEO_FACT1.mp3` | — | Prosody reference for new lines | **reference** |
| **Music/ambience + SFX** | `assets/pilot_shots/ep1/audio/new/` (B_disco, B_hear, B_tag, B_vacwhoaa), `build/a01–a30.wav` | — | Reaction SFX + bed continuity | **R+** |
| **End-tag / brand templates** | Ep1 outro + `assets/pilot_shots/ep1/Bentley_Ep1_thumbnail.jpg` | — | Outro structure + thumbnail style ref | **R+** |

**⛔ Do NOT reuse (superseded):** Higgsfield `Bentley-hero` (`b6adcf93…`) → use **Bentley-MASTER**; old whiskered **Pip** (`d74e14ad…`) → use **Pip-clean**; **George** narrator → use **Bill**.

---

## 7. New Asset Creation List

**Characters / design (the only true "new IP" of the episode):**
1. **Indi — locked character design** ✅ **DONE** (`Indi_LOCKED.png`). Designed **octopus-first** (real octopus stylized, never a human face): iridescent **grape-purple** jewel body matching the Ep1 teaser, **teal** non-human eyes (lateral, no sclera, no line), **no nose / no eyebrows**, tiny lipless mouth, two **low** blue ocelli (below each eye), 8 suckered arms dominant. Personality via color/glow + arm acting ("Mood-Light"). **Model sheet + expression + color/camo states DONE** (`Indi_MODEL_SHEET.png`): front/side turnaround + shy / curious / trusting / scared (pale) / startled (deep-red flush) / camouflage (red-brown) — all edited from `Indi_LOCKED.png`.
2. **Indi expression set** — Recommended **6**: *guarded/hidden, startled (eyespots flared), curious one-arm reach, confession (soft), trusting (eyespots dim), wedged/panic.*
3. **Indi camouflage states** — at least: *as-rock, mid-morph (smooth→bumpy), full-color flush (red), inking.*

**Props / environment:**
4. **Speckled "rock" prop** that morphs to eye (cold hook).
5. **Crevice / reef-edge micro-plates** (2): the cornering crevice + the squeeze gap.
6. **Moray eel** — as **silhouette/shadow asset** (NOT a full hero creature): a dark sinuous shape, eye glint, teeth hint. Deliberately under-built for tone + cost.
7. **Ants + car-sized crumb plate** (cliffhanger, 1 plate).
8. **Ink-puff VFX kit** (reusable transition element — pays off all episode).
9. **Science motion-graphic overlays** (3 hearts / blue-blood / coin-gap diagram) — simple, Pillow/ffmpeg, no AI.

**Audio (new):**
10. **Indi voice** (new ElevenLabs casting — see §8).
11. **New dialogue lines** for Bentley (locked voice) + Indi + 1 narrator pass.
12. **Indi "theme" sting** (optional, Premium only) — a short signature motif.

---

## 8. Voice Plan & Indi Audition Recommendations

**Keep locked (no change):** **Bentley = LauraZ** (`jkNABRZGatAuwawcS9xX`, stability 0.30 / sim 0.75 / style 0.60 / speed 1.12), **Narrator = Bill** (`pqHfZKP75CvOlQylNhV4`), **Pip = Callum +10%** (`N2lVS1w4EtoT3dr4eOWO`) if used. Engine: **ElevenLabs `eleven_v3`**.

**Indi voice direction:** *shy, intelligent, soft, emotionally guarded — not babyish, not villainous, not theatrical.* She should sound like a careful, watchful kid who's used to going unnoticed, capable of **anxiety → trust → wonder**. She must be **clearly distinct** from Bentley (bright/peppy), Pip (gruff/small), and Bill (warm grandpa). Slight **breathy / underwater** character (light low-pass + a hair of reverb in post) sells "submerged and small" — but **keep it intelligible** and **do not pitch up into chipmunk** (that reads babyish). Suggested starting settings to audition at: **stability ~0.40, similarity ~0.75, style ~0.45, speed ~0.95** (slightly slow = careful/shy).

**Audition protocol:** generate the **same 3 lines** through **5 candidate voices** at the settings above, then pick **blind** (filenames hidden). Cheap (a handful of short TTS gens, effectively covered by the ElevenLabs subscription).

**Candidate voices (ElevenLabs library archetypes — exact pick confirmed at audition):**
| Option | Archetype | Why it fits | Watch-out |
|---|---|---|---|
| **A. Matilda** | warm, young, gentle | soft + kind without baby pitch | could be *too* sunny — dial style down |
| **B. Alice** | clear, thoughtful (Brit) | reads "intelligent + careful" | keep warmth up so she's not cold |
| **C. Charlotte** | soft, slightly husky | best for *guarded/anxious* texture | can skew older — raise speed slightly |
| **D. Lily** | gentle, youthful-grounded | "shy kid" sweet spot | may need more emotional range |
| **E. River / Dakota** | soft androgynous/neutral | otherworldly, fits a sea creature | guard intelligibility |

**Exact audition lines (from the script, 3 contrasting registers):**
1. *(guarded, flat-protective)* — "If nobody sees me, nobody can be disappointed by me."
2. *(anxious → purposeful)* — "I wasn't running from you. I run from everybody. It's safer to disappear. …But I kept leaving you shells because somebody finally needs to listen — the open water's gone wrong."
3. *(tender, trusting — the turn)* — "You don't have to disappear… to be seen by you."

**Director's pick (pre-audition lean):** **C (Charlotte)** or **D (Lily)** for the guarded-but-warm core; **E** if you want Indi to feel more alien/oceanic. Final call after blind listen.

**Lip-sync policy:** use **Kling Avatar (KAv)** lip-sync **only** where the mouth is clearly on-screen and matters — Bentley's hero talking CUs (shots 4, 16, 19, 23). For **Indi**, prefer **VO over subtle arm/eye motion** (octopus mouth is hidden under the arms anyway) — this dodges the hardest, riskiest animation and is *more* accurate. Trim every avatar clip to **speech length + ~0.2s** (locked rule) to avoid silent mouth-flap.

---

## 9. Budget / Credit Estimate by Category (3 Tiers)

**Unit costs (current KIE.ai stack — primary backend; fal.ai retired):** keyframe **Nano-Banana** ≈ **$0.01–0.02** (≈free) · motion **Kling 2.6 i2v** ≈ **$0.18–0.25/clip** (~$0.22 avg) · talking **Kling-Avatar** ≈ **$0.15–0.22** (~$0.18 avg) · **ElevenLabs `eleven_v3`** ≈ $0.30/1k chars (effectively covered by subscription) · **ffmpeg/Shorts/Ken-Burns/ink = $0.** KIE runs ~½ image / ¾ video / ½ talking vs the old fal path, so every figure below is *lower* than a fal build would have been. Re-takes are the swing factor (cheap shots 1–2 takes, hero shots 3–4). ⚠️ **KIE workflow notes:** image inputs need **catbox URL hosting**; **Kling-Avatar darkens** output (pre-brighten keyframes / grade up). *(Ep1 re-render cost ~$36–42 on the older path — our upper anchor.)*

| Category | LOW ("Lean") | RECOMMENDED ("Hero-Balanced") ✅ | PREMIUM ("Showcase") |
|---|---|---|---|
| New keyframes | ~10 | **~13–16** | ~24 |
| New motion clips (incl. re-takes) | ~22 renders | **~55–70 renders** | ~110 renders |
| New talking/avatar clips | 2–3 | **4–5** | 6–8 |
| Indi design | 1 base + 3 expr | **model sheet + 6 expr + camo states** | full library + theme sting |
| Eel scene | static shadow | **animated silhouette** | richer set-piece |
| Finishing | none | ink kit + grade | + upscale/60fps hero pass, A/B thumbs |
| **Hard generation cost (KIE)** | **~$5–10** | **~$13–20** | **~$28–45** |
| **All-in (incl. audition + ~20% buffer)** | **~$8–15** | **~$20–35** | **~$40–70** |
| VO/audio | Indi cast + lines (sub) | Indi cast + full lines (sub) | + custom music sting (~$0–15) |
| Runtime | ~3:30 | ~4:35 | ~5:00 |

**Credit-system note:** KIE bills in its own credits, priced *well below* the old Higgsfield credit — the USD-equivalents above are authoritative. For comparison to the legacy 90-Day plan only: at the old Higgsfield framing (~3.5 cr/finished-sec + 40% revisions) a ~4:35 episode ≈ **~1,150–1,300 Higgsfield-credits**, but that path is retired and overstates real KIE spend by roughly an order of magnitude.

**What we save by reusing Ep1 assets (quantified):**
- Octopus teaser as Indi seed + callback → avoids a full hero design-from-scratch + a reveal clip ≈ **$4–7** and **days** of design iteration.
- Tidepool-cove plate → avoids 2–3 new env keyframes + establishers ≈ **$2–4**.
- CLEAN_shell glow (the Turn) → avoids a hero VFX clip ≈ **$1.5–3**.
- Water/wave plates → establishers/transitions ≈ **$1–3**.
- Locked Bentley/Pip/Narrator voices → **only Indi** is new; saves an entire 3-voice casting effort.
- Bentley expression seeds + model sheets → faster, on-model keyframes ≈ **$2–4** + fewer rejects.
- Music/ambience/SFX continuity → sourcing time saved.
- **Net hard-dollar savings ≈ $8–18 on KIE; the bigger win is schedule (≈40–50% faster) and guaranteed visual/voice consistency with Ep1.**

**Where to SPEND more (hero shots — fund 3–4 takes):**
- **Shot 3** rock→eye reveal (the thumbnail).
- **Shot 14** Indi's chosen emergence (trust, on-model Indi).
- **Shot 16** the "snack pouch" exchange (emotional core).
- **Shot 20** the boneless coin-gap squeeze (science climax, believability).
- **Shot 22** the paw-hold (the feeling the whole episode sells).

**Where to STAY cheap (1 take / reuse / FFX):**
- Establishers/wides (1, 5) → reuse plate + Ken-Burns.
- The Turn glow (12) → reuse `CLEAN_shell.mp4` as-is.
- Science payoff montage (24) → reuse Indi shots + motion-graphic overlays + VO.
- Outro/tease (27, 28) → templates.
- Ink-puff transitions → one reusable kit covers many cuts.

---

## 10. Risk Table & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Off-model Bentley** (proportions/eyes drift) | Med | High | Embed Bentley-MASTER + model sheets in every keyframe; pull 2–3 takes; reject off-model before motion. |
| **Human teeth / human grin** on talking CUs (#1 recurring bug) | **High** | High | Bake "natural dog mouth, soft pink tongue, small dog teeth, NO human teeth" into every KAv keyframe; favor partial opens; **reject + regen** any frame with human teeth. |
| **Long tail / ears-up** (off-model) | Med | High | Keyframe must show **short docked tail + floppy folded ears**; never prompt "ears up"; models inherit the keyframe. |
| **White socks/paws** hallucination | Med | Med | Negate "white socks/feet/toes" in every motion prompt; paws solid red-fawn. |
| **Octopus arm chaos** (tangled/extra arms) | **High** | High | Partial reveals, **one expressive arm**, eye/eyespots as focus, ink puffs to hide transitions; lock Indi model sheet first; never feature all 8 arms articulating at once. |
| **Confusing camouflage** (viewer can't read the reveal) | Med | Med | Stage clear before→after; let texture morph happen *while Bentley stares*; hold the eye-open a beat longer. |
| **Eel scene too scary / too dark** | Med | High | Silhouette + glint only, no gore, soft lighting, short cuts; lift exposure; QC against a "could a 4-yo watch this?" gate. |
| **Indi looks like the deadly blue-ringed octopus** | Med | Med-High | Two *large* false-eye rings (one per side), not many small electric rings; art-direct away from venom-warning look. |
| **Bad/mistimed lip-sync** | Med | Med | KAv only where mouth matters; Indi = VO over motion; trim clips to speech +0.2s; pin audio to shot frame. |
| **Too dark underwater** (compounded by **KIE Kling-Avatar darkening**) | **Med-High** | Med | Keep "reef edge" shallow + dawn light from the cove plate; avoid deep-water blackness; **pre-brighten avatar keyframes**; grade exposure up; spot-check every KIE-Avatar clip and lift any that came back dark. |
| **KIE workflow gotchas** (catbox hosting, avatar darkening) | Med | Low-Med | Host all image inputs on catbox before calls; budget a brightness-lift grade pass on talking clips; keep `bentley/shared/kie_client.py` keys/paths warm; smoketest one clip before any batch. |
| **Inaccurate science** | Low | High | §4 wording locked ("blink of an eye," "taste and think a little"); science QC pass before VO record. |
| **Indi voice wrong** (babyish/villainous) | Med | Med | Blind 5-voice audition at locked settings; director pick C/D/E; reject baby pitch. |
| **Cost overrun from re-takes** | Med | Low-Med | KIE is cheap; cap hero shots at 4 takes; resumable pipeline skips done shots; keyframes are ≈free to re-roll before committing to motion. |
| **Channel-name inconsistency** (old "Discovery Club" in templates) | Med | Low | T0 rename sweep before assembly (§13). |

---

## 11. Shorts Plan (6 — each a different hook, all ~$0)

All Shorts are **cut from the finished episode** (ffmpeg crop/blur-fill to 1080×1920 + Pillow captions via `bentley/episode_builder/shorts.py`) → **no new generation cost.** Each tests a distinct hook for the algorithm.

| # | Hook type | Source shots | Title (searchable) | Description |
|---|---|---|---|---|
| **S1** | Camouflage reveal | 2–4 | **"The ROCK had an EYEBALL 👁️🐙"** | A dog boops a rock… and it BLINKS. How octopuses vanish in the blink of an eye. #octopus #camouflage #kids |
| **S2** | Funny Bentley mistake | 6 | **"She booped SIX wrong rocks 🐶💦 (one fought back)"** | When you're *so* sure you found it… Bentley vs. the world's best hide-and-seek champion. #funnydogs #octopus |
| **S3** | 3 hearts / blue blood | 24 | **"This animal has 3 HEARTS and BLUE blood 💙"** | Why octopus blood is blue (it's copper!) and why her biggest heart takes a break when she swims. #didyouknow #ocean |
| **S4** | Boneless escape | 17–20 | **"It squeezed through a hole the size of a COIN 🪙"** | No bones! The only hard part of an octopus is its beak — so it can pour through almost any gap. #escapeartist #octopus |
| **S5** | Emotional trust | 14, 22 | **"You don't have to disappear to be safe with me 🥹"** | A shy octopus learns she doesn't have to vanish to be loved. The paw-hold that got us. #wholesome #kindness |
| **S6** | Cliffhanger → ants (+bonus fact) | 26, 27 | **"Why are the ANTS carrying a crumb the size of a CAR? 🐜"** | Indi's warning points inland… Next time on Bentley's Big Adventures. (Bonus: octopuses are *colorblind* — yet match any color.) #cliffhanger |

**Posting order (zero-sub friendly, per house playbook):** S1 (visual shock) → S4 (satisfying) → S3 (fact) → S2 (funny) → S5 (heart) → S6 (cliffhanger pull to subscribe). Stagger ~1/day around episode launch.

---

## 12. SEO Title / Thumbnail Plan

**Episode titles (pick one — keyword-front for search + curiosity for click):**
- **A.** "Bentley Booped a ROCK… and It Had an EYE 👁️🐙 | Bentley's Big Adventures Ep 2"
- **B. ✅ (recommended)** "The Octopus Who Didn't Want to Be Seen 🐙 | Bentley's Big Adventures Ep 2" — leads with emotional hook + "octopus" keyword; pairs with the boop thumbnail for curiosity.
- **C.** "Bentley Meets a SHY Octopus 🐙 (Real Octopus Facts for Kids!) | Ep 2" — most searchable ("octopus facts for kids").
- **D.** "Can You Find the Hidden Octopus? 🔍🐙 | Bentley's Big Adventures Ep 2" — interactive/searchable.

**Description skeleton (front-loaded keywords):** "Bentley meets **Indi**, a shy **California two-spot octopus** who can **change color, squeeze through a coin-size gap, and has three hearts and blue blood!** A gentle story about **kindness, shyness, and trust** for kids 4–8. Real **octopus facts** + a big adventure. 🐙 *Subscribe for new Bentley's Big Adventures every week.*" + timestamps + fact list + #tags (octopus, octopus for kids, camouflage, ocean animals, kids cartoon, SEL).

**Thumbnail options:**
- **A. ✅ (recommended)** Bentley's paw about to boop a speckled rock that's **opening one huge octopus eye**; ink swirl; **shocked Boxer face**; big 👁️. (Matches the hook + highest curiosity gap.)
- **B.** Bentley nose-to-eyespot with Indi (both blue eyespots glowing), warm tender framing — leans emotional. Good A/B partner.
- **C.** Split "spot the octopus" — a rock on one side, the **same rock revealed as Indi** on the other, "FIND THE OCTOPUS!" — leans interactive/educational.

**Test plan:** ship **A** at launch; A/B against **B** after 48h if CTR < target. Use `Bentley_closeup_expression.jpg` (bigger-eyed) for the Boxer face per the locked thumbnail note.

---

## 13. Production Schedule (post-approval)

Sequenced so the **risky, identity-defining work is front-loaded and gated**, and cheap/reused work is batched last. Assumes solo/AI-assisted operator; "days" are working sessions, compressible.

| Phase | Work | Gate |
|---|---|---|
| **T0 — Prep ✅ DONE (2026-06-20)** | Rename swept across 27 docs; script science wording locked; Pip removed; KIE auth verified (bal 10,439 cr). *Token-smart:* the motion/avatar darkening smoketest is **deferred to the first real post-Gate-A render** (no throwaway clip). | ✅ Script + science locked; KIE live |
| **T1 — Indi design lock (1–1.5 days)** | Seed Indi from `octopus_NEW`; produce **model sheet + 6 expressions + camo states**; lock the eyespot signature. | **GATE A: Indi approved** (on-model, not blue-ring, not scary) |
| **T2 — Voice casting (0.5 day)** | Blind 5-voice Indi audition on the 3 lines; pick; set processing chain. | **GATE B: Indi voice approved** |
| **T3 — Hero keyframes (1 day)** | Keyframes for shots 3, 14, 16, 20, 22 (+ Bentley talking CUs); 2–3 takes each; reject off-model. | **GATE C: hero keyframes approved** |
| **T4 — Hero motion + talking (1–1.5 days)** | Render hero motion/avatar clips; trim avatar to speech len; QC teeth/tail/ears/arms. | Hero shots locked |
| **T5 — B-roll + cheap shots (1 day)** | Establishers (reuse plates + Ken-Burns), montage, science overlays, ink kit, eel silhouette, ants plate. | — |
| **T6 — VO record (0.5 day)** | All Bentley/Indi/Narrator lines via locked voices; pin to shots. | — |
| **T7 — Assembly + grade + mix (1 day)** | ffmpeg edit, color (brightness for underwater), sound design, music bed. | — |
| **T8 — QC pass (0.5 day)** | Full §14 checklist; frame-check every talking CU. | **GATE D: episode QC pass** |
| **T9 — Shorts + SEO (0.5 day)** | Cut 6 Shorts, captions, SRT; titles/desc/thumbnail A. | **GATE E: publish-ready** |

**Critical path:** T1 (Indi) → T3/T4 (hero shots). If Indi or a hero shot fails its gate, stop and fix before spending on b-roll. Estimated **~7–8 working sessions** end-to-end.

---

## 14. Approval Checklist (sign before any production)

**Pre-production gates (must all be ✅ to start spending):**
- [x] Script + §4 **science wording** locked ✅ (draft updated: "blink of an eye"; arms "taste by touch", ~two-thirds of neurons in arms).
- [x] **Budget tier** → **Recommended ("Hero-Balanced", ~$20–35 on KIE)** ✅
- [x] **Eel intensity** → **Silhouette-soft** ✅
- [x] **Indi voice LOCKED** ✅ → ElevenLabs `FcZStbCG9g9QxDlJioSD` (user's pick from a 6-way audition; guarded-but-warm) → `tts_indi()` in `bentley/voices/dialogue.py`
- [x] **Title + Thumbnail** → **Title B + Thumbnail A** ✅
- [x] **Backend** → **KIE.ai primary** (fal.ai retired) ✅
- [x] **Indi design LOCKED** at Gate A ✅ — `Indi_LOCKED.png` (octopus-first; iridescent purple; **teal** eyes; NO nose / NO eyebrows; low ocelli; small lipless mouth). Generate all Indi shots by editing from this frame.
- [x] **Pip cameo** → **OUT** ✅ (no cameo).

**Per-shot QC gates (during production — reject + regen on any fail):**
- [ ] Bentley **on-model**: red-fawn coat, black mask, **floppy folded ears**, **short docked tail**, **solid red-fawn paws (no white socks)**, teal collar + glowing shell, well-proportioned soulful eyes.
- [ ] **NO human teeth / no human grin** on any talking close-up (frame-checked).
- [ ] **Octopus arms** controlled — no tangle/extra arms; partial reveal honored; eyespots correct.
- [ ] **Camouflage** reads clearly (before→after legible).
- [ ] **Eel** not too scary / not too dark for ages 4–8.
- [ ] **Lip-sync** clean; avatar clips trimmed to speech +0.2s; audio pinned to frame.
- [ ] **Underwater not too dark**; graded for brightness.
- [ ] **Science** accurate per §4; no rejected facts slipped in.
- [ ] **Indi consistent** across shots (matches model sheet; eyespot signature intact).
- [ ] Channel name = **"Bentley's Big Adventures"** everywhere; no "Discovery Club" leftovers.

**Final publish gate:**
- [ ] Full episode watched start-to-finish for tone (delight→worry→tenderness→relief→curiosity).
- [ ] 6 Shorts cut + captioned; titles/desc/tags set.
- [ ] Thumbnail A exported; A/B partner ready.

---

*End of plan. Production is HOLD until the §14 pre-production gates are signed. — Bentley's Big Adventures EP desk.*
