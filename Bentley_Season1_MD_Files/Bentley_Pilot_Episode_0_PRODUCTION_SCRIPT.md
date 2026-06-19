# BENTLEY'S DISCOVERY CLUB — PILOT (Ep 0)
# "The Voice in the Shell" — FULL AI-PRODUCTION SHOOTING SCRIPT
### 122 shots · ~7:50 runtime · built for Claude → Higgsfield → AI voice → CapCut/Premiere

> Companion to `Bentley_Pilot_Episode_0_GREENLIGHT.md` (the story) and `Bentley_Channel_Engine_Bible.md` (the strategy). This file is the **production** layer: locked refs, shot list, VO, Shorts cut, QA.

---

## 0. HOW TO USE THIS DOC (the pipeline, 6 steps)

1. **Generate the locked reference images FIRST** (Section 2). Make 1 hero image per character + per environment. Approve them. *Nothing else gets generated until refs are locked* — this is how you beat character drift.
2. **Batch-generate the voice** from the clean VO script (Section 5) in your AI voice tool. One pass, four voices. Save each line by its `[Sxxx]` ID.
3. **Generate each shot** (Section 4): paste the 🎬 GEN prompt, attach the named reference image(s) as image-to-video input, append the global **[STYLE]** token, render at the listed duration.
4. **Assemble** in CapCut/Premiere in shot order; drop VO lines onto matching `[Sxxx]`; add music/SFX from the cue sheet (Section 6).
5. **Cut the 5 Shorts** (Section 7) from the same renders, reframed 9:16.
6. **Run the QA checklist** (Section 8) before publish.

---

## 1. GLOBAL SETTINGS

- **Main aspect:** 16:9, 4K (3840×2160). **Shorts:** 9:16, 1080×1920.
- **Frame feel:** cinematic, ~24fps motion, shallow depth of field.
- **Average shot length:** ~3.8s (range 1–5s) — short shots = better AI consistency + better retention.
- **[STYLE] token — APPEND TO EVERY GEN PROMPT:**
  > `Pixar/DreamWorks-style 3D animated film, cinematic lighting, soft global illumination, shallow depth of field, expressive wholesome cartoon character acting, warm golden-hour California-coast palette (warm gold + teal + coral), subtle film grain, high detail, 16:9, no text, no watermark, no captions.`
- **Negative (where supported):** `photorealistic, live-action, horror, scary, dark, gore, text, logo, distorted anatomy, extra limbs, watermark.`

---

## 2. ASSET & CHARACTER REFERENCE BIBLE (lock these first)

> Workflow: generate each as a clean neutral hero shot, approve, then **reuse as the image reference for every shot that character appears in.** Restate the **bolded anchor features** in shot prompts to reinforce.

### 🐶 BENTLEY (lead) — `[BENTLEY]`
> **LOCKED — see `assets/character_design/LOCKED_ELEMENTS.md` (authoritative).** Young female Boxer based on the **real dog Bentley**: rich **red-fawn coat**, strong **black mask** with a subtle **dark brindle** hint on the forehead, **grey-white frosting** on the chin, gentle **brow wrinkles**, **soulful** dark-brown eyes, natural **floppy ears (both folded)**, small **white chest blaze**, wet black nose. Friendly athletic Boxer build, slightly rounded/cute. Wears a **teal collar with a glowing spiral seashell charm** (her only accessory). Style = **premium dimensional cartoon** (Pixar/Bluey-grade), soft fur warmth — NOT photoreal, NOT flat. **Production: embed `<<<b6adcf93-5849-44fc-b686-74455b2ea54b>>>` (Bentley-hero Element) in every prompt; model `nano_banana_2`.**

### ⭐ STELLA (mentor) — `[STELLA]`
> A wise, gentle **violet-purple sea star, five arms — one arm noticeably shorter and regrowing with a pale-pink bud tip.** Soft painted friendly eyes, faint bioluminescent freckles, warm grandmotherly presence. *Hero ref: draped on a wet rock, soft smile.*

### 🦀 PIP (guest) — `[PIP]`
> A tiny expressive **hermit crab with big worried eyes**, START state: cramped in a **dull, cracked, too-small brown snail shell.** Grumpy-but-soft, small-and-tough energy. END state: snug in a **glowing cream-and-blue spiral shell.** *Hero ref: close macro, big eyes, on wet sand.*

### 🌸 THE ANEMONE (comic) — `[ANEMONE]`
> A large **green sea anemone that looks deceptively like a soft flower**, frilly swaying tentacles, a wide "mouth" center. Comedic, a little smug. *Hero ref: open on a rock, flower-like.*

### 🦀 CRAB CROWD — `[CRABS]`
> A lineup of assorted hermit crabs of graduated sizes (large → tiny), varied shell colors, friendly cartoon faces. Used for the vacancy-chain climax.

### 🌅 SETTING — `[POOL]`
> **Crystal Cove–style Southern California tide pools at sunrise:** wet black volcanic rock, glassy mirror-still pools, strands of kelp, scattered seashells, soft sea mist, low warm sun, sparkling reflections. Establish a **high dry sun-baked rock** (Pip's trap) and a **cool blue pool** below.

### ✨ HERO VFX — `[GLOW]`
> Soft pulsing blue bioluminescent glow from the spiral shell — warm, magical, gentle. **Reusable across the whole series.** (Also the "listening activates" cue.)

### 🐙 SEASON HOOK — `[TENTACLE]`
> A single curious **purple octopus tentacle** rising from deep water, suckers visible, waving in a friendly way. (Pays off in Ep 2.)

---

## 3. VOICE CASTING & DIRECTION (for AI voice)

| Role | Voice profile | Direction |
|------|---------------|-----------|
| **NARRATOR** | Warm adult female, "favorite aunt" | Cozy, twinkly, unhurried. Think bedtime-story meets nature doc. |
| **BENTLEY** | Bright young, gender-neutral-leaning female, puppy energy | Eager, fast, big-hearted, comedic; drops to soft & sincere in the turn. |
| **PIP** | Small, raspy, grumpy-cute | Tough-guy bravado hiding fear; cracks into vulnerable. |
| **STELLA** | Gentle, wise, older female | Calm, warm, a little playful-dry. The anchor of calm. |

---

## 4. THE SHOT LIST (122 shots)

> Format: **`[Sxxx]` · duration · SHOT TYPE, camera** — 🎬 GEN (append **[STYLE]**) · 🎭 action · 🔊 VO · 🎵 audio. **⚡SHORT-n** = belongs to Short n.

### SCENE A — COLD OPEN (0:00–0:17)

**[S001]** · 2.0s · BLACK, audio only
🎬 *(no render — hold on pure black)*
🔊 PIP (O.S.): "...Help. Somebody? *Anybody?*"
🎵 silence → a single distant shell-chime

**[S002]** · 3.0s · ECU macro, slow push-in — ⚡SHORT-1
🎬 GEN: Extreme macro of a **pale spiral seashell** half-buried in wet sand, pulsing soft blue **[GLOW]** from within, dawn light, a thin wave sheet washing past. [POOL]
🎭 the shell pulses in time with the voice
🔊 PIP (O.S.): "I'm stuck. And it's getting *hot.*"
🎵 low warm drone, water hiss

**[S003]** · 2.0s · whip-pan into ECU — ⚡SHORT-1
🎬 GEN: A big wet **[BENTLEY]** dog nose shoves into frame and sniffs the glowing shell, sand grains sticking to it, macro.
🎭 sniff, the glow lights her nose
🎵 sniff SFX, comedic boing-in

**[S004]** · 3.0s · MCU, pull-out — ⚡SHORT-1
🎬 GEN: [BENTLEY] going cross-eyed trying to look at her own nose, sitting at the waterline at sunrise. [POOL]
🔊 BENTLEY: "Did... did the *beach* just talk to me?"
🎵 light curious mallet motif

**[S005]** · 1.8s · CU, static
🎬 GEN: [BENTLEY] head-tilt, one ear flops over, big amber eyes blinking at the glowing shell.
🎵 ear-flop SFX, single pizzicato

**[S006]** · 1.5s · INSERT, static
🎬 GEN: the spiral shell pulses **[GLOW]** brighter, casting blue light on wet black rock. [POOL]
🎵 glow swells

**[S007]** · 1.4s · CU, slow push
🎬 GEN: blue glow reflecting in [BENTLEY]'s wide eyes, dawn rim-light on fawn fur.
🎵 magical shimmer rising

**[S008]** · 1.0s · transition
🎬 GEN: bright sunburst lens flare wipe off the glowing shell.
🎵 ★ 2-NOTE MOTIF "ba-DING!" (title hit incoming)

### SCENE B — TITLE STING (0:17–0:29)

**[S009]** · 2.2s · GFX title card
🎬 GEN: Title logo "BENTLEY'S DISCOVERY CLUB" slamming in over the glowing shell + sunburst; bright, playful, kid-friendly. *(add text in edit, not in render)*
🎵 ★ theme sting, big and bright

**[S010]** · 2.6s · WS→MS, quick push
🎬 GEN: [BENTLEY] pops up into frame on the rocks, does a full-body Boxer **wiggle-butt** dance and throws one paw forward, joyful, sunrise behind. [POOL]
🔊 BENTLEY: "Discovery Club — *let's GO!*"
🎵 theme button + cymbal

**[S011]** · 1.4s · whip transition
🎬 GEN: fast motion-blur whip across the tide pools.
🎵 whoosh

### SCENE C — ACT 1: THE FLAW ON DISPLAY (0:29–1:54)

**[S012]** · 3.2s · EWS establishing (hold)
🎬 GEN: sweeping wide of the [POOL] at golden sunrise, glassy pools, mist, tide visibly low, beautiful and calm.
🔊 NARRATOR: "This is Bentley. Bentley loves the beach."
🎵 warm strings bed begins

**[S013]** · 3.0s · MS, tracking
🎬 GEN: [BENTLEY] trotting along the rocks; she pulls a **dog biscuit** from her collar pouch, eyes it longingly, tucks it back.
🔊 NARRATOR: "Bentley loves snacks—" / BENTLEY: "Emergency snack. For *later.*"
🎵 playful woodwinds

**[S014]** · 3.4s · MCU, push-in
🎬 GEN: [BENTLEY] ears perking, head lifting toward an unheard sound, curious and earnest.
🔊 NARRATOR: "—but most of all, Bentley loves to *help.* The only problem... is *how.*"
🎵 strings lift, a question-mark motif

**[S015]** · 2.4s · MS, tracking
🎬 GEN: [BENTLEY] scrambling up the wet rocks toward the glowing shell, eager.
🎵 scurry rhythm

**[S016]** · 3.0s · CU macro, tilt-reveal
🎬 GEN: reveal [PIP] wedged in his cracked too-small brown shell, stranded high on a **dry sun-baked rock** above the waterline, sun glinting hot. [POOL]
🔊 PIP: "Down here! On the *dry rock!*"
🎵 heat-shimmer sting

**[S017]** · 3.0s · MCU, on Bentley
🎬 GEN: [BENTLEY] gasps with delight, eyes huge, tail wagging.
🔊 BENTLEY: "A talking *crab!* Don't worry, tiny guy — I am an *expert* helper."
🎵 comedic confidence brass

**[S018]** · 2.8s · OTS (over Pip to Bentley)
🎬 GEN: over [PIP]'s shoulder, [BENTLEY] looming in close, beaming.
🔊 BENTLEY: "Obviously you fell out of the ocean!" / PIP: "What? *No—*"
🎵 record-scratch tease

**[S019]** · 2.0s · CU, Bentley
🎬 GEN: [BENTLEY] with a determined, oblivious grin, ready to "rescue."
🔊 BENTLEY: "So I'll just put you *BACK!*"
🎵 mischief upswing

**[S020]** · 2.6s · MS, tracking — ⚡SHORT-2
🎬 GEN: [BENTLEY] gently scoops [PIP] into her mouth and gallops toward the crashing open surf, big waves ahead.
🔊 PIP (muffled): "NO no no — not the BIG water—"
🎵 frantic gallop strings

**[S021]** · 3.0s · WS, dynamic — ⚡SHORT-2
🎬 GEN: a big wave looms; [BENTLEY] skids to a stop at the foam line, spray flying, comedic panic.
🔊 PIP: "I'm too *little* for the big water! Put me DOWN—"
🎵 wave crash, brakes screech

**[S022]** · 2.6s · MS, low angle — ⚡SHORT-2
🎬 GEN: [BENTLEY] backpedals, sets [PIP] down on wet sand; the wave retreats behind them.
🎭 both panting
🎵 tension release

**[S023]** · 3.0s · CU, Pip
🎬 GEN: [PIP] furious, pointing a tiny claw, shaken.
🔊 PIP: "You almost fed me to the *ocean!*"
🎵 grumpy stinger

**[S024]** · 2.8s · CU, Bentley
🎬 GEN: [BENTLEY] crushed, ears flat, eyes welling, tail tucked.
🔊 BENTLEY: "I was... *helping.*"
🎵 sad solo cello note

**[S025]** · 2.6s · INSERT
🎬 GEN: the sun edging higher over the horizon; the high rocks beginning to steam faintly. [POOL]
🔊 NARRATOR (soft): "But helping isn't the same as *listening.* Not yet."
🎵 ticking-clock unease begins (subtle)

**[S026]** · 2.4s · CU, Pip
🎬 GEN: [PIP] glancing nervously at the rising sun, claw fidgeting.
🎵 clock motif

**[S027]** · 2.2s · MS, Bentley
🎬 GEN: [BENTLEY] perking up again, already cooking up her next "fix," distracted.
🔊 BENTLEY: "Okay okay — new plan! I am *great* at plans."
🎵 bouncy comedic

**[S028]** · 2.0s · WS
🎬 GEN: [BENTLEY] spotting something off-frame, ears up.
🎵 curiosity ping

**[S029]** · 2.6s · MS
🎬 GEN: [BENTLEY] bounding toward a sunlit lower pool, leaving Pip on his rock (he watches, worried).
🎵 transition run

**[S030]** · 1.8s · INSERT
🎬 GEN: Pip alone on the hot rock, small in frame, the sea out of reach below. [POOL]
🔊 PIP (quiet): "...hurry."
🎵 lonely note

### SCENE D — ACT 2A: DISCOVERY + IT GETS WORSE (1:54–3:34)

**[S031]** · 3.0s · MS, reveal
🎬 GEN: a calm sunlit pool; [STELLA] the violet sea star draped on a rock, one short regrowing arm, smiling warmly.
🔊 STELLA (O.S. then on): "He's not from the ocean, sweetheart. He's from *here.*"
🎵 warm mentor theme (new motif)

**[S032]** · 3.0s · CU, Stella
🎬 GEN: macro of [STELLA]'s face, gentle painted eyes, bioluminescent freckles, the regrowing arm visible.
🔊 BENTLEY (O.S.): "Whoa — what happened to your *arm?*"
🎵 soft wonder

**[S033]** · 3.4s · CU, Stella stretches arm — ⚡SHORT-3-alt
🎬 GEN: [STELLA] flexes her short **regrowing arm**, the pale-pink bud tip catching light. 🟢FACT
🔊 STELLA: "Lost it. Growing it back. Sea stars do that. Takes time. Most good things do."
🎵 twinkle on "growing it back"

**[S034]** · 2.6s · MS, Bentley
🎬 GEN: [BENTLEY] amazed, leaning in over the pool, reflection shimmering.
🔊 NARRATOR: "A sea star can regrow a whole *arm.* Slowly. Patiently."
🎵 wonder swell

**[S035]** · 3.2s · WS, Stella gestures to sun
🎬 GEN: [STELLA] glancing up at the climbing sun; the high rocks where Pip sits steaming faintly. [POOL]
🔊 STELLA: "These pools? They're the ocean's *leftovers* — left behind when the tide goes out."
🎵 clock motif returns, gentle

**[S036]** · 3.4s · CU, Stella (serious-warm)
🎬 GEN: [STELLA] glancing toward Pip's hot rock, concern.
🔊 STELLA: "Pip woke up too high, too dry. And now—" *(beat)* "—now it's a *race.*"
🎵 stakes sting

**[S037]** · 2.6s · POV/INSERT
🎬 GEN: Bentley's POV: the sun's reflection creeping across the drying rock toward tiny Pip.
🎵 ticking intensifies slightly

**[S038]** · 2.4s · MS, Bentley (panic-fix mode)
🎬 GEN: [BENTLEY] snapping into frantic "I'll fix it fast" energy, looking around wildly.
🔊 BENTLEY: "A race! Okay! I'll make him a comfy bed — there!"
🎵 comedic scramble

**[S039]** · 3.0s · MS, the "flower" — ⚡SHORT-3
🎬 GEN: [BENTLEY] spots [ANEMONE] (looks like a big soft green flower) on a rock and trots over delighted.
🔊 BENTLEY: "A *flower!* Perfect. Soft flower bed coming up!"
🎵 sweet naive theme

**[S040]** · 3.2s · CU macro — ⚡SHORT-3
🎬 GEN: [BENTLEY] nudges her **biscuit** toward the [ANEMONE] as a gift; the anemone's frilly tentacles close around the biscuit and *swallow* it. 🟢FACT
🔊 BENTLEY: "...did the flower just eat my *snack?*"
🎵 comedic gulp SFX

**[S041]** · 2.8s · MS, Stella (dry)
🎬 GEN: [STELLA] giving a flat, knowing look.
🔊 STELLA: "That's not a flower. That's an *animal.* Anemones look like plants. They are *not.* And they *will* eat your snack."
🎵 deadpan woodblock

**[S042]** · 2.4s · CU, Bentley
🎬 GEN: [BENTLEY] mind-blown, staring at the anemone, then at her empty pouch.
🔊 NARRATOR: "A sea anemone — an *animal* dressed up like a flower."
🎵 wonder ping

**[S043]** · 2.6s · MS — comedy
🎬 GEN: [BENTLEY] does an embarrassed, overexcited spin (zoomies starting), flustered.
🔊 BENTLEY: "Okay that's amazing and also rude—"
🎵 zoomies whirl

**[S044]** · 3.0s · WS, the mistake
🎬 GEN: [BENTLEY]'s zoomies knock loose a small slide of pebbles tumbling toward Pip's rock. [POOL]
🎵 uh-oh descending run

**[S045]** · 2.8s · CU, Pip
🎬 GEN: [PIP] flinching as pebbles bump him into a worse wedged spot, shell scraping.
🔊 PIP: "Hey — *hey!*"
🎵 alarm hit

**[S046]** · 3.0s · MS, Bentley realizes
🎬 GEN: [BENTLEY] freezing, horrified at what she caused, the sun now harsh.
🔊 BENTLEY: "Pip! I'm sorry — I'm *trying*—"
🎵 guilt swell

**[S047]** · 2.6s · CU, Pip (smaller, scared)
🎬 GEN: macro of [PIP] now truly stuck, the bravado cracking, sun blazing on him.
🔊 PIP (small): "...I'm really stuck now."
🎵 vulnerable cello

**[S048]** · 2.4s · INSERT
🎬 GEN: heat shimmer rising off the dry rock; the cool pool tantalizingly below. [POOL]
🎵 clock louder

**[S049]** · 2.2s · CU, Bentley spiraling
🎬 GEN: [BENTLEY] panicking, pacing, reaching to grab Pip again.
🎵 anxious strings rising

**[S050]** · 2.0s · CU, Stella (firm-kind)
🎬 GEN: [STELLA] turning sharply, warm but firm.
🔊 STELLA: "Bentley. *Stop.*"
🎵 ★ music CUTS OUT

**[S051]** · 2.4s · MS, freeze
🎬 GEN: [BENTLEY] frozen mid-reach, blinking, everything suddenly still and quiet. [POOL]
🎵 silence + waves + breath only

**[S052]** · 2.0s · CU, Bentley
🎬 GEN: [BENTLEY]'s frantic face slowly settling, listening for the first time.
🎵 single soft heartbeat

**[S053]** · 2.4s · CU, Stella
🎬 GEN: [STELLA] gentle, teaching.
🔊 STELLA: "You keep *doing.* You haven't *listened.*"
🎵 warm low pad enters

**[S054]** · 2.6s · MS, two-shot
🎬 GEN: [STELLA] and [BENTLEY] across the still pool, dawn glow.
🔊 STELLA: "The world's been telling you what it needs this whole time. Try it. **Stop. Look. Listen.**"
🎵 the method motif (will recur all series)

### SCENE E — ACT 2B: THE TURN (3:34–4:46)

**[S055]** · 3.0s · MS, Bentley sits
🎬 GEN: [BENTLEY] sits, closes her eyes, takes a slow breath, going completely still on the rocks. [POOL]
🎵 held breath, soft

**[S056]** · 3.2s · CU, the shell ignites — ⚡SHORT-4
🎬 GEN: the spiral charm on [BENTLEY]'s collar **[GLOW]** blooms bright warm blue, alive, light spilling over her fur.
🎵 ★ magical shimmer rises — the "listening" cue

**[S057]** · 3.0s · WS, soundscape blooms
🎬 GEN: the whole tide pool subtly lights with tiny glints as if sound became visible — gentle magical realism. [POOL][GLOW]
🔊 NARRATOR (hushed): "And for the very first time... Bentley got *quiet* enough to *hear.*"
🎵 the pool's voices swell softly

**[S058]** · 3.4s · CU macro, Pip
🎬 GEN: [PIP] in soft focus, the glow reaching him, his face open and real now.
🔊 PIP (quiet, real): "...I'm not scared of being *stuck.*"
🎵 intimate piano enters

**[S059]** · 3.6s · CU, Pip (vulnerable)
🎬 GEN: macro of [PIP], eyes shining, tiny and honest.
🔊 PIP: "I'm scared 'cause I'm *growing.* My shell got too tight and nothing fits and everybody's too busy to help."
🎵 piano + soft strings

**[S060]** · 3.0s · CU, Pip
🎬 GEN: [PIP] looking down, ashamed.
🔊 PIP: "I thought... I'd just have to stay too *small* forever."
🎵 aching hold

**[S061]** · 3.4s · CU, Bentley (tears) — ⚡SHORT-4
🎬 GEN: [BENTLEY]'s eyes welling, deep empathy dawning — she *gets* it.
🔊 BENTLEY (gentle): "You're not too small. You're just *between shells.*"
🎵 warm resolve

**[S062]** · 3.0s · CU, Bentley — ⚡SHORT-4
🎬 GEN: [BENTLEY] soft and sincere, close.
🔊 BENTLEY: "...I know that feeling."
🎵 single tender note

**[S063]** · 2.6s · two-shot, soft
🎬 GEN: [BENTLEY] and [PIP] sharing a quiet look, the glow between them. [POOL]
🎵 connection theme

**[S064]** · 3.0s · MS, Stella (proud)
🎬 GEN: [STELLA] watching, a knowing warm smile.
🔊 STELLA: "*There* it is. Now you're listening. So — what does he *actually* need?"
🎵 hope lifts

**[S065]** · 2.8s · CU, Bentley realizes
🎬 GEN: [BENTLEY]'s face shifting from sad to determined-in-a-new-way (calm, not frantic).
🔊 BENTLEY: "A bigger house. The *right* size. Not the ocean — a *home.*"
🎵 idea sparkle

**[S066]** · 2.4s · INSERT
🎬 GEN: macro of Pip's cracked too-small shell, clearly outgrown. [PIP]
🔊 NARRATOR: "A hermit crab's shell isn't its *body.* It's a borrowed *house* — and Pip had outgrown his."
🎵 gentle reveal

**[S067]** · 2.0s · CU, Pip
🎬 GEN: [PIP] nodding, hopeful for the first time.
🎵 hopeful ping

**[S068]** · 2.6s · MS, Bentley stands (resolve)
🎬 GEN: [BENTLEY] rising with calm purpose, the glow steady on her collar. [POOL]
🔊 BENTLEY: "And I bet somebody here is moving up, too."
🎵 the build begins

**[S069]** · 2.2s · WS
🎬 GEN: [BENTLEY] turning to the wider tide pool, addressing its hidden residents.
🔊 BENTLEY: "Discovery Club — *let's GO!*"
🎵 rally motif

**[S070]** · 2.0s · reaction
🎬 GEN: ripples and little eyes appearing around the pool, residents waking. [POOL]
🎵 curious patter

**[S071]** · 2.0s · CU, Stella
🎬 GEN: [STELLA] delighted, ready to help explain.
🔊 STELLA: "Oh, you're going to *love* how we do this."
🎵 playful lift

**[S072]** · 1.8s · transition
🎬 GEN: light wipe across the brightening pool.
🎵 whoosh into climax

### SCENE F — ACT 3: THE VACANCY CHAIN + THE CLOCK (4:46–6:20)

**[S073]** · 3.2s · WS, reveal the crowd — ⚡SHORT-5
🎬 GEN: [CRABS] — a crowd of hermit crabs of graduated sizes emerging across the rocks, curious. [POOL]
🔊 STELLA: "When one crab finds a bigger shell, the next-biggest moves into *its* old one. And the next. We line up by size."
🎵 jaunty "teamwork" theme starts

**[S074]** · 2.8s · CU, Stella (the term)
🎬 GEN: [STELLA] explaining brightly.
🔊 STELLA: "We call it the *vacancy chain.*" 🟢FACT
🎵 fun marimba

**[S075]** · 2.6s · CU, Pip (parent joke)
🎬 GEN: [PIP] muttering, arms crossed, comedic.
🔊 PIP: "Location, location, tide-*pool*-cation."
🎵 rimshot

**[S076]** · 3.0s · WS, the line forms — ⚡SHORT-5
🎬 GEN: [CRABS] hustling into a neat line biggest-to-smallest along a rock ledge, comedic bustle. [POOL]
🔊 NARRATOR: "Biggest to smallest. Everybody waiting for the *perfect* fit."
🎵 build rhythm

**[S077]** · 2.6s · CU, big crab finds shell — ⚡SHORT-5
🎬 GEN: a large hermit crab discovers a roomy empty whelk shell, eyes lighting up. [CRABS]
🎵 "ooh!" rise

**[S078]** · 2.4s · INSERT, the swap — ⚡SHORT-5
🎬 GEN: macro: the big crab slips into the new shell — *click* — leaving its old one. [CRABS]
🎵 satisfying click

**[S079]** · 3.0s · WS, the domino — ⚡SHORT-5
🎬 GEN: a chain reaction down the line — each [CRABS] member hops into the next-larger vacated shell, *click click click*, a perfect domino of homes. [POOL]
🔊 BENTLEY (delighted): "It's like *musical chairs* — but for HOUSES!"
🎵 cascading xylophone run

**[S080]** · 2.6s · MS, Bentley cheering
🎬 GEN: [BENTLEY] bouncing, tail going, watching the chain reach toward Pip.
🎵 excitement peak

**[S081]** · 2.4s · CU, Pip hopeful
🎬 GEN: [PIP] inching forward, the line nearly to him, hope rising.
🎵 anticipation

**[S082]** · 3.0s · INSERT, the SETBACK
🎬 GEN: the last vacated shell reaches Pip — but it's visibly **one size too small**; he can't fit. Macro, deflating. [PIP]
🔊 PIP: "...it's too small. *Again.*"
🎵 ★ music stumbles / drops — the failure

**[S083]** · 2.8s · WS, everyone freezes
🎬 GEN: the whole [CRABS] line stops, the chain broken, the sun now brutal and high. [POOL]
🎵 silence + heat shimmer

**[S084]** · 2.6s · CU, Pip fading
🎬 GEN: [PIP] drooping in the heat, energy low, the rock steaming.
🔊 NARRATOR (soft, tense): "And the sun was *winning.*"
🎵 thin high tension

**[S085]** · 2.4s · CU, Bentley — almost rushes
🎬 GEN: [BENTLEY]'s instinct kicks in, she lurches to grab/fix — then catches herself.
🎵 anxious spike → held

**[S086]** · 2.8s · CU, Bentley chooses to listen
🎬 GEN: [BENTLEY] closes her eyes, breathes, the collar **[GLOW]** pulses once. Calm over panic.
🔊 BENTLEY (to herself): "...Okay. Stop. Look. *Listen.*"
🎵 the method motif, quiet

**[S087]** · 3.0s · POV, she really looks
🎬 GEN: Bentley's POV sweeping the pool slowly... landing on her own collar — the glowing spiral shell. [GLOW]
🎵 realization shimmer building

**[S088]** · 3.0s · CU, the realization
🎬 GEN: [BENTLEY] eyes going wide with a soft gasp, looking down at her own collar shell.
🔊 BENTLEY: "...It was on me the *whole time.*"
🎵 ★ warm reveal swell

**[S089]** · 2.8s · MCU, she unclips it
🎬 GEN: [BENTLEY] gently unclips the **glowing spiral shell** from her collar with a paw, holding it out. [GLOW]
🎵 tender resolve

**[S090]** · 2.6s · INSERT, offering
🎬 GEN: macro: the perfect cream-and-blue spiral shell set down before tiny [PIP]; it's exactly his size.
🔊 BENTLEY: "Try this one, Pip."
🎵 hope returns

**[S091]** · 3.2s · CU macro, the perfect fit
🎬 GEN: [PIP] slips into the glowing spiral shell — a *perfect fit* — the shell glows warm once: *home.* [PIP][GLOW]
🔊 PIP (awed): "...it *fits.*"
🎵 ★ triumphant warm chord

**[S092]** · 2.6s · WS, crowd cheers
🎬 GEN: the [CRABS] crowd throws claws up, cheering; Stella beams. [POOL]
🎵 cheer + celebratory theme

**[S093]** · 3.0s · WS, the wave returns (clock beaten)
🎬 GEN: a fresh cool wave finally rolls back into the low pool, sweeping toward Pip's rock. [POOL]
🔊 NARRATOR: "And right on time... the sea came *back.*"
🎵 swelling relief

**[S094]** · 3.0s · MS, Pip carried to safety
🎬 GEN: the gentle wave lifts [PIP] in his glowing new shell and carries him safe into the cool blue pool. [GLOW]
🎵 joyful release

**[S095]** · 2.4s · CU, Pip floating happy
🎬 GEN: [PIP] bobbing safe and cool in the pool, glowing shell, relieved grin.
🎵 warm settle

**[S096]** · 2.2s · MS, Bentley exhales
🎬 GEN: [BENTLEY] sitting back, relieved, a happy tired smile.
🎵 breath out

**[S097]** · 2.0s · CU, Stella proud
🎬 GEN: [STELLA] watching Bentley with warm pride.
🎵 mentor theme soft

**[S098]** · 2.0s · WS, the calmed pool
🎬 GEN: the tide pool now cool, full, alive, sparkling, sun softened. [POOL]
🎵 peace

**[S099]** · 2.0s · CU, Bentley & Pip eyeline
🎬 GEN: [BENTLEY] and [PIP] catching each other's eye across the water, a bond.
🎵 connection motif

**[S100]** · 1.8s · transition
🎬 GEN: gentle light bloom into the emotional button.
🎵 settle into tender theme

### SCENE G — EMOTIONAL BUTTON + LESSON (6:20–7:08)

**[S101]** · 3.4s · CU macro, Pip
🎬 GEN: [PIP] in his glowing shell looking up at Bentley, grateful.
🔊 PIP: "You gave me your *shell.*"
🎵 intimate piano

**[S102]** · 3.4s · CU, Bentley
🎬 GEN: [BENTLEY] warm, humble, close.
🔊 BENTLEY: "You needed it more. Besides — turns out I don't help by *grabbing.* I help by *listening.*"
🎵 theme blooms

**[S103]** · 3.6s · CU, Pip (the heart line)
🎬 GEN: [PIP] quiet, moved, eyes shining.
🔊 PIP: "...You're the first one who actually *did.*"
🎵 ★ emotional peak, strings

**[S104]** · 3.0s · MS, Stella approaches
🎬 GEN: [STELLA] glides over holding a small new spiral shell charm that glows softly. [GLOW]
🎵 magical warmth

**[S105]** · 3.4s · CU, Stella gifts the shell
🎬 GEN: [STELLA] clips the new glowing shell charm onto [BENTLEY]'s teal collar. [GLOW]
🔊 STELLA: "Every good listener gets one. It glows when somebody nearby needs help—"
🎵 induction theme rising

**[S106]** · 3.2s · CU, Stella
🎬 GEN: [STELLA] warm and twinkling.
🔊 STELLA: "—and it only works when you get *quiet* enough to hear them. Welcome to the Discovery Club, Bentley."
🎵 ★ theme swells

**[S107]** · 2.6s · CU, Bentley glowing
🎬 GEN: [BENTLEY] looking down at her new glowing charm, awed and proud. [GLOW]
🎵 wonder

**[S108]** · 3.6s · WS, golden hero shot
🎬 GEN: [BENTLEY] on the rocks, the whole sparkling [POOL] and its creatures around her, warm sun, the Club assembled.
🔊 NARRATOR: "Bentley came to the beach to *help.* She left knowing the secret..."
🎵 full warm theme

**[S109]** · 3.4s · slow push, Bentley
🎬 GEN: [BENTLEY] gazing out, content and changed.
🔊 NARRATOR: "...the whole world is talking, all the time. You just have to get *quiet* enough to hear it."
🎵 theme peak settle

**[S110]** · 3.0s · CU, Bentley to camera
🎬 GEN: [BENTLEY] turns to the camera, warm direct address, gentle smile.
🔊 BENTLEY: "Stop. Look. Listen. ...*Discover.*"
🎵 ★ method motif button

**[S111]** · 2.0s · CU, Pip waves
🎬 GEN: [PIP] in his glowing shell waving a happy claw goodbye. [PIP]
🎵 sweet

**[S112]** · 2.0s · CU, Stella smiles
🎬 GEN: [STELLA] warm farewell smile.
🎵 mentor soft

**[S113]** · 2.0s · WS settle
🎬 GEN: wide of the peaceful glowing tide pool at full golden morning. [POOL]
🎵 breath before the hook

### SCENE H — CLIFFHANGER + CTA + END CARD (7:08–7:50)

**[S114]** · 2.6s · MS, Bentley trots up beach
🎬 GEN: [BENTLEY] trotting happily up the sand away from the pool, content.
🎵 light walking theme

**[S115]** · 2.6s · CU, the shell tugs
🎬 GEN: [BENTLEY]'s collar shell suddenly **[GLOW]** flares and pulls her gaze out to sea.
🎵 ★ mystery sting

**[S116]** · 3.2s · WS, the tentacle — season hook
🎬 GEN: far offshore, a single curious **purple octopus tentacle** rises from the water and curls into a friendly *wave.* [TENTACLE][POOL]
🎵 wonder + question motif

**[S117]** · 3.0s · CU, Bentley head-tilt
🎬 GEN: [BENTLEY] doing a big quizzical Boxer head-tilt at the waving tentacle.
🔊 BENTLEY: "...Do octopuses usually say *hello?*"
🎵 comedic curious button

**[S118]** · 2.4s · INSERT
🎬 GEN: the collar shell pulses *toward* the deep water — the next mystery calling. [GLOW]
🎵 pull-to-adventure

**[S119]** · 2.0s · CU, Bentley grin
🎬 GEN: [BENTLEY] grinning with excitement at the sea.
🔊 BENTLEY: "Discovery Club — where to *next?!*"
🎵 ★ theme hit

**[S120]** · 1.5s · CUT TO BLACK
🎬 *(black)*
🎵 ★ 2-NOTE MOTIF "ba-DING!"

**[S121]** · 3.0s · END CARD (GFX)
🎬 GEN: bright end card: glowing shell + "Episode 1 — The Octopus Escape Artist" + a thumbnail of the tentacle. *(text/buttons in edit)*
🔊 NARRATOR: "Tap to dive in! Episode 1 — *The Octopus Escape Artist.*"
🎵 theme bed

**[S122]** · 3.0s · SUBSCRIBE CTA (GFX)
🎬 GEN: [BENTLEY] wiggle-butt loop + subscribe button animation space. *(animate in edit)*
🔊 BENTLEY: "Subscribe so I can find you for the next adventure!"
🎵 theme button out

---

## 5. CLEAN VO SCRIPT (batch voice generation)

> Generate in 4 voices; save each clip by `[Sxxx]`. Punctuation = performance.

**NARRATOR**
- [S025] "But helping isn't the same as listening. Not yet."
- [S034] "A sea star can regrow a whole arm. Slowly. Patiently."
- [S042] "A sea anemone — an animal dressed up like a flower."
- [S057] "And for the very first time... Bentley got quiet enough to hear."
- [S066] "A hermit crab's shell isn't its body. It's a borrowed house — and Pip had outgrown his."
- [S076] "Biggest to smallest. Everybody waiting for the perfect fit."
- [S084] "And the sun was winning."
- [S093] "And right on time... the sea came back."
- [S108] "Bentley came to the beach to help. She left knowing the secret..."
- [S109] "...the whole world is talking, all the time. You just have to get quiet enough to hear it."
- [S121] "Tap to dive in! Episode 1 — The Octopus Escape Artist."

**BENTLEY**
- [S004] "Did... did the beach just talk to me?"
- [S010] "Discovery Club — let's GO!"
- [S013] "Emergency snack. For later."
- [S017] "A talking crab! Don't worry, tiny guy — I am an expert helper."
- [S018] "Obviously you fell out of the ocean!"
- [S019] "So I'll just put you BACK!"
- [S024] "I was... helping."
- [S027] "Okay okay — new plan! I am great at plans."
- [S038] "A race! Okay! I'll make him a comfy bed — there!"
- [S039] "A flower! Perfect. Soft flower bed coming up!"
- [S040] "...did the flower just eat my snack?"
- [S043] "Okay that's amazing and also rude—"
- [S046] "Pip! I'm sorry — I'm trying—"
- [S061] "You're not too small. You're just between shells."
- [S062] "...I know that feeling."
- [S065] "A bigger house. The right size. Not the ocean — a home."
- [S068] "And I bet somebody here is moving up, too."
- [S069] "Discovery Club — let's GO!"
- [S079] "It's like musical chairs — but for HOUSES!"
- [S086] "...Okay. Stop. Look. Listen."
- [S088] "...It was on me the whole time."
- [S090] "Try this one, Pip."
- [S102] "You needed it more. Besides — turns out I don't help by grabbing. I help by listening."
- [S110] "Stop. Look. Listen. ...Discover."
- [S117] "...Do octopuses usually say hello?"
- [S119] "Discovery Club — where to next?!"
- [S122] "Subscribe so I can find you for the next adventure!"

**PIP**
- [S001] "...Help. Somebody? Anybody?"
- [S002] "I'm stuck. And it's getting hot."
- [S016] "Down here! On the dry rock!"
- [S018] "What? No—"
- [S021] "I'm too little for the big water! Put me DOWN—"
- [S023] "You almost fed me to the ocean!"
- [S030] "...hurry."
- [S045] "Hey — hey!"
- [S047] "...I'm really stuck now."
- [S058] "...I'm not scared of being stuck."
- [S059] "I'm scared 'cause I'm growing. My shell got too tight and nothing fits and everybody's too busy to help."
- [S060] "I thought... I'd just have to stay too small forever."
- [S075] "Location, location, tide-pool-cation."
- [S082] "...it's too small. Again."
- [S091] "...it fits."
- [S101] "You gave me your shell."
- [S103] "...You're the first one who actually did."

**STELLA**
- [S031] "He's not from the ocean, sweetheart. He's from here."
- [S033] "Lost it. Growing it back. Sea stars do that. Takes time. Most good things do."
- [S035] "These pools? They're the ocean's leftovers — left behind when the tide goes out."
- [S036] "Pip woke up too high, too dry. And now— now it's a race."
- [S041] "That's not a flower. That's an animal. Anemones look like plants. They are not. And they will eat your snack."
- [S050] "Bentley. Stop."
- [S053] "You keep doing. You haven't listened."
- [S054] "The world's been telling you what it needs this whole time. Try it. Stop. Look. Listen."
- [S064] "There it is. Now you're listening. So — what does he actually need?"
- [S071] "Oh, you're going to love how we do this."
- [S073] "When one crab finds a bigger shell, the next-biggest moves into its old one. And the next. We line up by size."
- [S074] "We call it the vacancy chain."
- [S105] "Every good listener gets one. It glows when somebody nearby needs help—"
- [S106] "—and it only works when you get quiet enough to hear them. Welcome to the Discovery Club, Bentley."

---

## 6. MUSIC & SFX CUE SHEET

| Cue | Where | Feel |
|-----|-------|------|
| **Main theme** | S009–S010, S106, S119 | bright, adventurous, hummable, 2-note "ba-DING" motif |
| **Curiosity motif** | S004–S007, S014 | light mallets / pizzicato question marks |
| **Comedy beds** | S017–S023, S039–S043, S073–S079 | bouncy woodwinds, rimshots, xylophone |
| **Clock/tension** | S025–S037, S048, S082–S085 | subtle ticking, thin high strings — never scary |
| **★ Silence drop** | S050–S052 | music fully cuts → waves + breath (the turn) |
| **Method motif** | S054, S086, S110 | 3 soft warm notes for "Stop. Look. Listen." |
| **Emotional piano** | S058–S063, S101–S103 | intimate piano + strings |
| **Triumph** | S091–S094 | warm major swell |
| **Mystery hook** | S115–S118 | wonder + unresolved question chord |
| **Key SFX** | — | shell-glow shimmer (reused), wave wash/crash, anemone gulp, shell *click* (vacancy chain), Boxer ear-flop, wiggle-butt jingle |

---

## 7. THE 5 SHORTS (vertical 9:16 assembly)

> Reframe the same renders to 9:16 (center on Bentley's face). Each Short: cold-open on the spike, big captions, end on a hook + "Full adventure on the channel 🐾".

1. **"Did the beach just TALK to me?!"** — S002→S003→S004→S007 (+ S116 tease). *Mystery hook.* Caption: "Something was glowing in the sand…"
2. **"The WORST rescue ever 😅"** — S020→S021→S022→S023→S024. *Comedy.* Caption: "She thought she was helping…"
3. **"I fed my snack to a FLOWER (it was NOT a flower) 🌸"** — S039→S040→S041→S042. *Comedy + fact.* Caption: "Sea anemones are ANIMALS."
4. **"You're not too small — you're just between shells 🐚"** — S058→S059→S060→S061→S062. *The heart clip (highest share potential).* Caption: "When you feel like you're growing too fast…"
5. **"REAL hermit crabs trade houses in a CHAIN 🦀"** — S073→S076→S077→S078→S079 (+ S091 payoff). *Fact/spectacle.* Caption: "It's called a vacancy chain!"

---

## 8. ASSEMBLY + CONSISTENCY QA CHECKLIST

**Before generating shots**
- [ ] Hero reference image approved for: Bentley, Stella, Pip (both shell states), Anemone, Crab crowd, the Pool (wide + Pip's dry rock + cool pool).
- [ ] [STYLE] token saved as a paste snippet; negative prompt saved.
- [ ] Bentley's anchor features written into a checklist (white blaze, one floppy ear, teal collar + shell) to eyeball every render against.

**During generation**
- [ ] Every shot uses the named reference image as image-to-video input.
- [ ] Reject + regenerate any shot where Bentley's blaze/ears/collar drift.
- [ ] Keep continuity of light direction (sun rising → higher/harsher → softened).
- [ ] Shell-glow color identical across S002, S056, S088–S091, S105, S115, S118 (reuse one VFX).

**Edit**
- [ ] VO synced to `[Sxxx]`; talking-animal mouths kept subtle (no full lip-sync).
- [ ] Music silence-drop lands exactly on S050.
- [ ] Total runtime 7:30–7:55; if over, trim Act 2A cutaways (S027–S029, S043) per the 5-min-cut logic in the greenlight doc.
- [ ] Captions/subtitles burned for sound-off viewing.
- [ ] End screen (S121–S122) links Episode 1 + Subscribe.

**Publish**
- [ ] "Made for Kids" set; no scary frames; facts spot-checked.
- [ ] 5 Shorts exported 9:16 with the long-form pinned/linked.
- [ ] Thumbnail + A/B titles from the bible loaded.
