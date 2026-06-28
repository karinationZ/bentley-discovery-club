# Bentley's Big Adventures — Branding Review & Direction

> Premium children's (ages 3–12 + parents) educational **adventure** channel about nature, science, and ocean / tide-pool exploration, led by **Bentley**, a cartoon red-fawn Boxer puppy who is an explorer and scientist at heart.
> **Target brand feel:** Pixar × National Geographic Kids × a premium YouTube Kids franchise.
> Reviewed 2026-06-17. Single source of truth for Bentley: `assets/character_design/Bentley_MASTER_clean_16x9.png` + `assets/character_design/LOCKED_ELEMENTS.md`.

---

## 0. TL;DR — what to change first

1. **Fix the avatar.** The current `Channel_Avatar*.png` files are the biggest problem: googly/bug eyes on the "happy" variant, an overly droopy/sad face on the "soulful" variant, a photoreal-leaning render that fights the Pixar look, and a busy decorative ring that turns to mush at 48px. Replace with the new face-forward icon (`Bentley_PROFILE_icon_v1.png`) and drop the ring.
2. **Change Bentley's expression everywhere** from passive/neutral/sad to **curious · alert · adventurous** — "this dog is about to take me on an adventure." New on-model reference: `Bentley_HERO_expression_v1.png`.
3. **Lock a real brand system** (palette + type + thumbnail grid + one ownable graphic container), because the #1 cross-cutting lesson from every winning channel in this niche is *own one asset and repeat it religiously*.

New on-model example assets produced in this review (all verified against the master — correct red-fawn coat, black mask, floppy ears DOWN, short docked tail, NO white socks, teal collar + glowing spiral shell, Pixar soft-fur style):

| Asset | Path | Use |
|---|---|---|
| **Hero expression (primary)** | `assets/branding/Bentley_HERO_expression_v1.png` | The new face of the channel — adventurous, paw lifted mid-step, brand-teal ocean backdrop, left negative space for text |
| Hero candidate A (alt) | `assets/branding/Bentley_HERO_cand_A.png` | Golden-hour sitting "curious gaze" — great for emotional beats / warm key art |
| Hero candidate B | `assets/branding/Bentley_HERO_cand_B.png` | Source of the promoted hero |
| **Profile icon** | `assets/branding/Bentley_PROFILE_icon_v1.png` | Face-forward avatar, big readable shapes, solid teal background — reads at 48px |

---

## 1. Branding critique (current assets)

Inventory reviewed in `assets/branding/`:
- `Channel_Avatar.png` (1024×1024) and `Channel_Avatar_3D_soulful.png` — **identical files**, soulful/slightly sad face inside a decorative ring.
- `Channel_Avatar_3D_happy.png` — same ring, but a googly bug-eyed open-mouth face.
- `Channel_Banner.png` / `Channel_Banner_4K.png` / `Channel_Banner_upload.jpg` (2560×1440) — Bentley sitting on a tide-pool rock at sunset, sea behind, tiny critters bottom-left.

**What's working**
- The **core identity is right**: red-fawn Boxer + teal collar + glowing spiral seashell charm is a distinctive, ownable mascot. The shell-charm "Listening Shell" is a genuinely good brand hook.
- The **palette instinct is right**: teal + warm coral/peach + cream + golden-hour sky is a strong ocean/nature/premium direction.
- The **banner has real atmosphere** — the cinematic sunset over the sea reads premium and on-theme.

**What's hurting the brand**
1. **The avatar ring is over-decorated and low-contrast.** The teal-on-cream ring with tiny waves + leaves looks like a sticker/medallion, not a channel logo. At 48–98px the leaf/wave filigree collapses into noise, and the cream ring barely separates from YouTube's white UI. Winning kids' avatars (Bluey, Nat Geo Kids, Octonauts) are **bold, simple, high-contrast** and survive shrinking.
2. **Two avatars, two different dogs.** The "happy" and "soulful" files read as different characters (different eye size, different mouth, different mood). That breaks the one-rule that matters most for a mascot brand: *the face is the logo, and it must be identical every time.*
3. **Expression is off-brand on every existing asset** (see §3). The avatars are sad or goofy; the banner Bentley is passive/wary. None say "adventure."
4. **No system, only one-offs.** There is no defined palette with hex codes, no type pairing, no thumbnail template, no wordmark/logo lockup. Right now the "brand" is three pictures, not a system a team can reproduce.
5. **Banner safe-area risk.** Bentley currently sits **far left**, and at the wide desktop crop part of him plus the empty right side will be cut or stranded; on mobile/TV only the centered `1546×423` survives, where the current composition has no title and no clearly-centered subject (see §6).
6. **Render style drifts toward photoreal** on the avatars (especially the wet-looking muzzle and skin-real wrinkles), fighting the locked "premium dimensional Pixar/Bluey, NOT photoreal" art direction.

---

## 2. Character-consistency issues vs. the master (per asset)

Master reference (`Bentley_MASTER_clean_16x9.png`): rich red-fawn coat, black mask, grey chin frosting, soulful **well-proportioned** eyes, **both ears floppy folded DOWN**, **short docked stubby tail**, white blaze **only on chest**, **solid red-fawn paws (no socks)**, teal collar + glowing spiral seashell, Pixar soft-fur (not photoreal).

**`Channel_Avatar_3D_happy.png`** — *off-model.*
- **Eyes are googly / bug-eyed** — the exact "big eyes" failure called out in `LOCKED_ELEMENTS.md`. Reads cartoonish-cheap, not premium.
- Open-mouth toothy grin = "goofy/overly-happy," one of the explicitly forbidden first impressions.
- Muzzle/wrinkles render **photoreal**, not the soft Pixar fur of the master.
- Ears are correctly floppy ✓, collar + shell ✓ — but mood and eyes break it.

**`Channel_Avatar.png` / `Channel_Avatar_3D_soulful.png`** — *off-model (mood).*
- Eyes/brow pushed into a **sad, worried, almost pleading** look. The brief's "must NOT look sad" is violated head-on.
- Slightly **photoreal** muzzle vs. the master's stylized fur.
- Markings, ears (down) ✓, collar + shell ✓, no white socks ✓ — anatomy is fine; it's the **emotion** that's wrong.

**`Channel_Banner*.png`** — *mostly on-model, wrong attitude.*
- Coat, black mask, floppy ears down, short docked tail, chest-only blaze, **no white socks**, collar + shell — all ✓. Good Pixar-style render. This is the closest existing asset to the master.
- **Expression is passive / slightly wary**, looking away rather than eagerly toward a discovery. Needs the curious/alert/forward-leaning energy.
- Composition strands Bentley far left with dead space right (a layout problem more than a character problem — see §6).

**Reference note:** the `assets/character_design/Bentley_MODEL_SHEET_expressions.png` sheet itself contains several **bug-eyed** takes — do **not** use those frames as a basis for thumbnails or avatars; they reproduce the googly-eye bug. Use the master and the new `Bentley_HERO_expression_v1.png` as the expression north-star instead.

---

## 3. Bentley's expression — the key fix (concrete direction)

**Target read (first impression in <0.5s):** *"This dog just found something amazing and is about to take me to go investigate it."*
Emotional register = **curious · excited · alert · adventurous · intelligent · friendly.**
Forbidden: sad, droopy, overly-happy/grinning, goofy, angry, aggressive, too-young/puppy-helpless, too-old/tired, generic-cartoon-dog.

**Concrete, repeatable expression recipe (the "Discovery Look"):**
- **Head lifted and tilted slightly forward**, as if leaning in toward something just spotted. Not head-down (sad), not chin-up-and-back (wary).
- **Eyes:** bright, alert, intelligent, **wide with focused wonder** — pupils catching a small specular highlight for "spark." Keep them **well-proportioned and soulful, never googly/oversized** (per the locked rule). The eyes look *at a target* (slightly off-camera for hero shots, straight-on for the avatar).
- **Brow:** gently raised inner brow = curiosity/interest. Avoid the down-pulled "worried/sad" brow of the current soulful avatar.
- **Mouth:** softly open, **alert and ready** (a breath-held "ooh, what's that?"), NOT a wide toothy grin and NOT a closed sad line. A hint of tongue is okay; full goofy pant is not.
- **Body:** weight shifted forward, **one front paw lifted mid-step** or a slight forward lean — the universal "about to spring into exploration" pose. This single posture does most of the "adventurous" work.
- **Ears stay floppy, folded DOWN** even while alert (never prompt "ears up/pricked" — it produces an off-model pointed-ear dog).
- **Tail:** short docked stub, can read as a happy little wag.

The promoted asset `Bentley_HERO_expression_v1.png` is the canonical example of this look; `Bentley_HERO_cand_A.png` is the calmer "curious gaze" variant for emotional beats. Use these as the reference image for every future generation so the expression stays locked alongside the anatomy.

---

## 4. Color palette (with hex codes)

A focused ocean / nature / premium system. **Two hero colors do 80% of the work** (teal + coral), warmed by sand/cream and deepened by a navy for contrast and "premium." Use the 60-30-10 rule: ~60% deep teal/ocean, ~30% sand/cream + sky, ~10% coral accent.

### Primary (own these two)
| Role | Name | Hex | Use |
|---|---|---|---|
| **Primary** | Tide-Pool Teal | `#1AA7A0` | Collar, logo, dominant brand color, thumbnail color-blocks, "ocean world" |
| **Primary deep** | Deep Sea Navy | `#0B3B57` | Backgrounds, text-on-light, banner base, premium anchor, contrast |

### Secondary (the warmth — the "Pixar/nature" half)
| Role | Name | Hex | Use |
|---|---|---|---|
| Secondary | Coral Reef | `#FF6F61` | The pop accent — titles, CTA, the "exciting" highlight (from the existing coral) |
| Secondary | Sunlit Sand | `#F4E4C1` | Warm light areas, soft panels, friendly ground tone |
| Secondary | Sea-Glass Aqua | `#7FD4C8` | Lighter teal for gradients, glows, Bentley's "ocean" backdrop (used in the new hero/icon) |

### Accents (small doses, energy + the shell)
| Role | Name | Hex | Use |
|---|---|---|---|
| Accent | Discovery Gold | `#FBBF3D` | The Listening-Shell glow, sparkles, "aha!" moments, star ratings/badges |
| Accent | Kelp Green | `#3FA35B` | Nature/plants/leaves, secondary educational tags, variety vs. all-teal |
| Accent | Sky Wash | `#BFE6F0` | Airy sky gradients, light negative space, "breathing room" |

### Neutrals
| Role | Name | Hex | Use |
|---|---|---|---|
| Neutral dark | Driftwood Ink | `#13262E` | Body/heavy text, outlines, max-legibility dark |
| Neutral mid | Stone Grey | `#6B7B82` | Captions, secondary UI, dividers |
| Neutral light | Shell White | `#FBF7EF` | Off-white surfaces (warmer than pure #FFF so the avatar separates from YouTube's UI) |

**Rules:** Bentley's own coat is warm red-fawn `#B5642E`-ish, so the *brand* leans **teal** to make her pop (complementary). Reserve **Coral `#FF6F61`** strictly for the single most important call-to-attention element per asset. Reserve **Discovery Gold** for the shell glow and "aha" sparkle so it stays special. Keep saturated colors for accents, not whole backgrounds — premium kids' brands (Bluey, Octonauts, Nat Geo Kids) win with *restraint*.

---

## 5. Typography — font pairing

Goal: **rounded, friendly, confident, premium** — legible to early readers and trusted by parents; bold enough to survive thumbnail compression.

### Recommended pairing (display + body)
- **Display / titles & thumbnails: `Baloo 2`** (Google Fonts, free, ExtraBold/Bold).
  - *Why:* rounded terminals = friendly + safe for kids; heavy weights have thick stems that stay punchy and readable at thumbnail size; has a warm, characterful personality without being childish-cheap. This is the workhorse for the channel name, thumbnail words, and the wordmark.
- **Body / descriptions, captions, lower-thirds: `Nunito Sans`** (Google Fonts, free) — or `Nunito` for slightly rounder.
  - *Why:* a humanist rounded sans that pairs naturally with Baloo's roundness, but is calmer and highly legible in long form (video descriptions, on-screen facts, "creature cards"). Excellent weight range for hierarchy.

**Pairing logic:** both are rounded and humanist, so they feel like one family (cohesion), but Baloo 2 is characterful/loud for impact and Nunito Sans is quiet/clean for reading (contrast of role). This is the same "one characterful display + one clean rounded sans" structure premium kids' brands use.

### Strong alternatives (if you want a more bespoke/premium tier)
- **Display:** `Fredoka` (rounded, slightly more geometric/modern than Baloo) — great for a logo; or **`Quicksand` Bold** for an airier, more upmarket feel.
- **Body:** `Poppins` (geometric, premium, very clean) if you want the body to feel a touch more "design-forward" than Nunito.
- **Numbers/badges/UI accents:** `Baloo 2` SemiBold works, but `Poppins` Medium reads cleaner for stats on "creature cards."

**Type rules:** Titles in **Baloo 2 ExtraBold**, ALL-CAPS or Title Case, with a subtle dark outline/shadow on thumbnails for contrast over photography. Never more than **two type sizes** on a thumbnail. Keep a consistent thumbnail word style (color + outline) so it becomes part of the logo system.

---

## 6. Channel banner composition (2560×1440, safe area 1546×423 centered)

YouTube shows the banner at wildly different crops. **Everything essential must live inside the centered `1546×423` safe area** (TV/phone show roughly only this); the outer 2560×1440 is "bleed" that desktop shows and TV crops.

```
2560 ──────────────────────────────────────────────────────
│  [ ocean / tide-pool bleed — extends the scene, no text ] │
│      ┌──────────── SAFE AREA 1546 × 423 ────────────┐      │  1440 px
│      │  [Bentley peeking,   BENTLEY'S DISCOVERY CLUB │      │  tall
│      │   left third]        Explore. Discover. Wonder.│     │
│      │   (lifted paw)       ·new adventures weekly·   │      │
│      └────────────────────────────────────────────────┘     │
│  [ ocean / tide-pool bleed — extends the scene, no text ] │
└───────────────────────────────────────────────────────────┘
```

**Layout (left-anchored subject + right-anchored title — the YouTube-banner standard):**
- **Left ~third (inside safe area):** the new **`Bentley_HERO_expression_v1.png`** Bentley — head up, paw lifted, looking *toward the title*, glowing shell catching the eye. She frames into the safe area from the left.
- **Center→right (inside safe area):** the **wordmark** "BENTLEY'S DISCOVERY CLUB" in **Baloo 2 ExtraBold** (Shell White or Coral on the deep-teal/navy side), a one-line tagline beneath in **Nunito Sans** ("Explore. Discover. Wonder." / "Ocean & nature adventures for curious kids"), and a small cadence line ("New adventures every week").
- **Background:** the existing **golden-hour-sea / tide-pool** scene, but graded toward the brand palette — deepen to **Deep Sea Navy `#0B3B57` → Tide-Pool Teal `#1AA7A0`** with warm sky highlights and a few **Discovery Gold** sparkles. Let the scene bleed past the safe area so desktop gets a cinematic wide and TV still gets a complete composition.
- **Contrast:** put the title over the darker teal/navy area so Shell-White text pops; keep a soft vignette/gradient behind text for legibility.

**Spec checklist:** canvas `2560×1440`; keep text/logo/Bentley's face inside the centered `1546×423`; export the upload JPG/PNG ≤ 6 MB; test the YouTube preview for TV/desktop/mobile crops before publishing. (A `Channel_Banner_v2` should be produced from this composition; the current banner strands Bentley far left with no title in the safe area.)

---

## 7. Profile icon (800×800 source, shown ~48–98px)

**Problem with current avatars:** decorative ring + filigree + low cream/white contrast + wrong expression (and two inconsistent faces). At 48px the ring detail is mud and the cream ring melts into YouTube's white UI.

**Recommendation — adopt `Bentley_PROFILE_icon_v1.png`:**
- **Crop:** tight **head-and-shoulders, face mostly forward**, face filling ~70–80% of the frame. No body, no scene.
- **Expression:** the curious/alert "Discovery Look," eyes straight at the viewer (friendly, eager).
- **Background:** a **solid Tide-Pool Teal `#1AA7A0`** field with a soft radial glow behind the head — high contrast so the fawn face pops, and it separates cleanly from YouTube's white/dark UI. **No ring, no filigree.**
- **Readable shapes:** the black mask + big soulful eyes + the glowing spiral shell are the three shapes that survive shrinking; keep them large and centered. (Optionally a thin 6–10px Shell-White keyline around the circle for extra separation on white UI — but keep the *inside* clean.)
- **Export:** 800×800 PNG; sanity-check it pasted at 48px and 24px (comment-size).

**One brand-consistency rule:** the avatar face and every thumbnail face must be the **same Bentley** — same eye size, same mask, same Discovery Look. Pick one and lock it.

---

## 8. Thumbnail style — a repeatable system (1280×720)

The single biggest "premium vs. amateur" lever in this niche is a **rigid, repeatable thumbnail template** (Coyote Peterson, Kurzgesagt, TierZoo all win on this). Here is the system.

### The grid (1280×720, split into a 3-col feel)
```
1280 × 720
┌───────────────────────────────┬───────────────────┐
│                               │  TITLE WORD 1     │  ← Bentley's face
│      [ subject / discovery    │  TITLE WORD 2     │     occupies left
│        — crab, wave, shell,   │   (Baloo 2 XBold) │     45–55% with
│        tide pool, big & clear]│                   │     a reacting
│                               │  [tide-pool       │     expression
│   ◐ Bentley face, lower-left, │   "field card"    │
│     reacting, 35–45% of frame │    badge, opt.]   │
└───────────────────────────────┴───────────────────┘
```

**Repeatable rules:**
1. **Bentley's reacting face is the hero** — sized **35–45% of the thumbnail**, anchored **bottom-left** (consistent corner = recognition). Build a small library of **4–5 stock reactions** ("WONDER / WOW / WHOA / DELIGHT / CURIOUS") and reuse them. The face must be the locked Bentley (same as the avatar).
2. **The discovery subject is large and obvious** (the crab/wave/starfish/shell), upper area, in focus — the viewer instantly knows the episode topic.
3. **Text = max 3 words**, **Baloo 2 ExtraBold**, right third, with a **dark outline + soft drop shadow** for legibility. Title-color is **Coral `#FF6F61`** or **Shell White** — pick one and keep it consistent. Never cover Bentley's face or eyes with text.
4. **Color-blocking / brand frame:** add a consistent brand device — e.g., a **rounded "tide-pool porthole" oval** or a bottom **Tide-Pool-Teal `#1AA7A0` color bar** behind the title — so every thumbnail shares a frame. (This is the "own one container" lesson from Nat Geo's yellow rectangle.)
5. **The shell glow** (Discovery Gold) is the recurring micro-signature — keep it visible.
6. **One light direction, one grade:** warm key + teal ambient on every thumbnail so they look like a set.
7. **Consistency test:** crop the title off and remove the logo — you should *still* know it's Bentley's Big Adventures from face + color + frame alone. If not, the template isn't strong enough.

**Anti-patterns to avoid:** more than 3 words, two competing focal points, busy backgrounds behind the text, a different Bentley face per video, neon/over-saturated full-bleed backgrounds (reads as overstimulating "low-quality kids' content," the opposite of the premium/parent-trust lane).

---

## 9. Reference channels — what works in this niche (researched)

Eight currently-successful channels across mascot-led preschool, animal-adventure, and premium-explainer lanes. Focus is on **visual identity / brand systems**, plus one move to steal for Bentley.

**1. Nat Geo Kids — the "premium-but-for-kids" gold standard.** `https://www.youtube.com/@natgeokids` (~600K; parent `@natgeo` ~20M+).
*Does well:* the entire brand is **one ownable asset — the yellow rectangular frame**, redeployed from the adult logo as a "container for curiosity." It's a thumbnail border, a logo lockup, and a compositional device, giving instant brand presence on every asset with zero per-video redesign; high-contrast yellow pops against nature blues/greens, and it reads premium/trustworthy to parents.
*Steal this:* invent **one ownable graphic container** (a "tide-pool porthole" rounded frame in Tide-Pool Teal that Bentley peeks through) and put it on every thumbnail.

**2. Brave Wilderness / Coyote Peterson — expressive-face adventure thumbnails.** `https://www.youtube.com/@CoyotePeterson` (~21M).
*Does well:* the masterclass in **face-forward adventure framing** — tight host close-up in a high-stakes expression (awe/shock/grin), the animal large and clear, clean color-pop, 2–4 punchy words. The emotional read is instant; **the host's face IS the logo.**
*Steal this:* make **Bentley's expression the hero of every thumbnail**, large and reacting to the discovery; keep a reusable library of reactions.

**3. Wild Kratts — the closest content cousin (animal-adventure + animation).** `https://www.youtube.com/@WildKratts` (~1M+).
*Does well:* **character-color coding as a system** — the two leads own green vs. blue, recurring across thumbnails, the "Creature Power" motif, and key art, so the brand is legible even in a tiny avatar; heroes are always paired with the featured animal in a dynamic pose.
*Steal this:* **lock one hero color for Bentley** (Tide-Pool Teal) anchoring logo, lower-thirds, and thumbnail accents — the cheapest recognition lever that survives shrinking to avatar size.

**4. Octonauts — premium ocean-exploration animated IP.** `https://www.youtube.com/@octonauts-officialchannel5128` (~1.7M).
*Does well:* your **direct tonal target** — ocean exploration + cute animal characters + premium polish. Strong simple **wordmark** always present; consistent **deep-ocean-blue palette** that instantly says "underwater world"; rounded friendly characters with a clear lead anchoring recognition; thumbnails keep characters big, expressions warm, setting unmistakable.
*Steal this:* build a **deep-blue "ocean world" as your default brand environment** + a clean wordmark on every thumbnail; the *background color* alone should signal your channel.

**5. Bluey (Official) — the single-dog-led premium preschool gold standard.** `https://www.youtube.com/@blueyofficialchannel` (~13M).
*Does well:* your **most direct mascot analog.** Ruthlessly consistent flat, soft-pastel art (no harsh gradients); a calm palette dominated by the character's own blue; a simple rounded wordmark; clean **uncluttered, emotion-led** thumbnails. It's deliberately **gentle and parent-trusted** (the un-CoComelon), and the character's **silhouette alone** is identifiable.
*Steal this:* design **Bentley for silhouette recognition** (ears, jowls, stance) and keep thumbnails calm and uncluttered — restraint signals premium quality to the parents who actually subscribe.

**6. Kurzgesagt — the premium-explainer visual-system to emulate.** `https://www.youtube.com/@kurzgesagt` (~25M).
*Does well:* arguably **the most disciplined brand system on YouTube** — fixed geometric style, a famously vivid recognizable palette, recurring cute "duck" Easter-egg mascots, and **custom-illustrated thumbnails** (never stock, never clickbait-face). You can ID a thumbnail with the text removed and logo cropped — rigorous art-direction = premium perception.
*Steal this:* write a **one-page art-direction bible and never deviate** (fixed palette, defined style, fixed type, every thumbnail custom-rendered in-style). Pass the "recognizable with the logo cropped" test. Borrow the **recurring-cameo trick** — hide a tiny recurring critter (a crab/barnacle) in every episode for kids to hunt.

**7. TierZoo — one ownable, repeated graphic gimmick.** `https://www.youtube.com/@TierZoo` (~3.8M).
*Does well:* a multimillion-sub animal brand built on **one repeatable visual conceit** (wildlife as a video game — tier-lists, RPG/stat overlays) applied identically everywhere, so the **format itself becomes the logo**; proves you don't need a big budget with one distinctive, rigorously-repeated graphic system.
*Steal this:* give discoveries a **recurring on-screen "field-guide / creature card"** overlay (name + fun fact + cute icon) in one fixed style every episode — cheap, high-recognition, and reinforces the *educational* promise.

**8. Maddie Moate — premium kids' nature/curiosity, solo-creator scale.** `https://www.youtube.com/@maddiemoate` (~325K; BAFTA-winning, Kidscreen "Best Kids Channel" 2022).
*Does well:* the most directly comparable **positioning** ("curiosity-fueled science & nature for kids and families"): warm bright friendly palette, host-as-mascot anchor (her warm smile recurs as the brand), clean thumbnails led by **genuine wonder/curiosity, not manufactured shock** — the premium-yet-warm, parent-trusted, curiosity-first tone.
*Steal this:* anchor the brand on **"curiosity and wonder" as the emotional register** (not hype) — Bentley's thumbnail emotion should say *"come explore with me,"* not "you won't BELIEVE this." For parent-trust brands, **warmth beats clickbait.**

*Bonus study (lower priority):* **SciShow Kids** `@SciShowKids` (~1.5M) — sidekick-mascot model (Squeaks) if Bentley gets a tide-pool buddy. **Blippi** `@Blippi` (~27M) — mascot-IP dominance, but its loud orange/blue high-stimulation look is the *opposite* of the premium lane. **Gecko's Garage** (~3.4M) — single-animal 3D-CGI mascot, useful for character-consistency cues.

### Cross-cutting patterns that win in this niche
- **Own ONE asset and repeat it religiously.** Every winner has a single ownable element that survives at thumbnail/avatar size (Nat Geo's frame, Bluey's silhouette+blue, Kurzgesagt's palette, TierZoo's UI, Coyote's face). For Bentley: **face + Tide-Pool Teal + a porthole frame.** Consistency reads as premium; novelty-per-video reads as amateur.
- **The mascot's readable emotion is the logo.** A recurring character with a large, clearly-readable expression is the core recognition driver in both live-action and animated channels. Big, emotive Bentley face + a small reaction library.
- **For a parent-trusted premium brand, calm + warm beats loud + shocking.** Your exact-lane winners (Bluey, Maddie Moate, Octonauts, Nat Geo Kids) use restrained palettes, uncluttered thumbnails, and a "come explore with me" tone — the deliberate opposite of CoComelon/Blippi overstimulation. Less noise = higher perceived quality.
- **A consistent setting-color + one repeatable overlay do as much branding work as the character.** Lock a default tide-pool/ocean color so the *background* signals your channel, and add one recurring "creature card" overlay that brands every episode while reinforcing the learning promise (plus a hidden recurring critter for an engagement Easter egg).

---

## 10. Updated branding direction (the consolidated vision)

**Positioning statement:** *Bentley's Big Adventures is the place where a curious little Boxer takes kids on real ocean and nature adventures — Pixar-warm, Nat-Geo-smart, premium and parent-trusted.*

**The three pillars (Pixar × Nat Geo Kids × premium YouTube Kids):**
- **Pixar** → the *craft*: dimensional soft-fur character, cinematic warm lighting, genuine emotion, restraint over clutter. Bentley always renders in the locked Pixar/Bluey soft-fur style — never photoreal, never flat.
- **Nat Geo Kids** → the *substance + system*: real, credible nature/science, and **one ownable container** (the tide-pool porthole frame + Tide-Pool Teal) on everything, so the brand looks premium and trustworthy to parents.
- **Premium YouTube Kids** → the *discipline*: a rigid, repeatable thumbnail/avatar/banner system, a locked palette and type, and a recurring "creature card" overlay — the operational consistency that makes a channel feel like a franchise, not a hobby.

**The locked brand system (single source of truth going forward):**
- **Mascot:** Bentley exactly per `Bentley_MASTER_clean_16x9.png` + `LOCKED_ELEMENTS.md`, with the **"Discovery Look"** expression (curious · alert · adventurous) as the canonical mood — reference `Bentley_HERO_expression_v1.png`. The glowing spiral **Listening Shell** is the signature micro-icon.
- **Palette:** Tide-Pool Teal `#1AA7A0` + Deep Sea Navy `#0B3B57` (primary), Coral Reef `#FF6F61` + Sunlit Sand `#F4E4C1` + Sea-Glass Aqua `#7FD4C8` (secondary), Discovery Gold `#FBBF3D` / Kelp Green `#3FA35B` / Sky Wash `#BFE6F0` (accents), Driftwood Ink `#13262E` / Stone Grey `#6B7B82` / Shell White `#FBF7EF` (neutrals). 60-30-10, teal-dominant so Bentley pops.
- **Type:** **Baloo 2 ExtraBold** (display/titles/wordmark) + **Nunito Sans** (body/captions/creature-cards).
- **Avatar:** `Bentley_PROFILE_icon_v1.png` — face-forward, solid teal, no ring; reads at 48px.
- **Banner:** left-anchored Bentley (hero) + right-anchored wordmark + tagline, ocean scene graded to palette, everything inside the centered `1546×423` safe area.
- **Thumbnails:** Bentley reacting bottom-left (35–45%), big clear discovery subject, ≤3 words in Baloo 2 right third with outline, consistent porthole/teal frame, shell glow, one light grade. "Recognizable with the logo cropped."
- **Signatures (brand glue):** the porthole frame, the Listening-Shell gold glow, a recurring "creature card" overlay, and a hidden cameo critter every episode.

**First production steps:** (1) ship the new avatar; (2) rebuild the banner per §6 as `Channel_Banner_v2`; (3) build the porthole-frame + creature-card overlay templates; (4) generate the 4–5 stock Bentley reaction faces from `Bentley_HERO_expression_v1.png`; (5) apply the §8 thumbnail template to the first batch of episodes.

---

### Appendix — example assets in this folder
- `Bentley_HERO_expression_v1.png` — **primary hero**, the "Discovery Look" (adventurous, paw lifted, brand-teal ocean, left negative space). Verified on-model.
- `Bentley_HERO_cand_A.png` — alt "curious gaze," golden-hour sitting. Verified on-model.
- `Bentley_HERO_cand_B.png` — source of the promoted hero.
- `Bentley_PROFILE_icon_v1.png` — **profile avatar**, face-forward, solid teal, reads small. Verified on-model.
- All assets verified against the master: red-fawn coat ✓, black mask ✓, floppy ears DOWN ✓, short docked tail ✓, soulful (not googly) eyes ✓, white blaze on chest only / **no white socks** ✓, teal collar + glowing spiral seashell ✓, Pixar soft-fur (not photoreal) ✓.
