# Bentley — Character Design Direction & Model-Sheet Spec
### The locked design philosophy. Read before generating ANY Bentley.

## The principle (why we simplify)
**Consistency comes from SIMPLICITY, not detail.** The more photoreal/detailed a character, the more there is to drift — every fur strand, wrinkle, and subtle proportion must match across hundreds of shots, which is impossible by hand and *especially* with AI (it reinterprets detail every time). Iconic characters (Bluey, Mickey, Dug) are built from **simple repeatable shapes + a few locked signature features.** Simpler = more consistent + more recognizable + more lovable + better for merch + reproducible by AI.

## Visual style (locked)
**3D dimensional animated cartoon WITH soft real fur** — a fluffy, dimensional, premium animated-feature puppy (a rendered 3D film look). Soft visible fur texture, real dimensional shading and depth, soulful eyes. NOT flat, NOT 2D, NOT clay-smooth, NOT over-simplified — but also NOT photoreal (which drifts and goes uncanny). The sweet spot: a **dimensional furry animated Boxer** that's appealing, warm, and consistent. **Master design locked from `assets/character_design/Bentley_3Dfur_1.jpg` → Element `Bentley-MASTER`.**

## The 5 locked SIGNATURE features (must appear in EVERY shot)
1. **Black mask** shape on the muzzle.
2. **BOTH floppy folded ears** at the sides — never erect.
3. Rich **red-fawn coat**.
4. Small **white chest blaze** — white is **ONLY** here. Legs and **all four paws are solid red-fawn: NO white socks, NO white feet** (must be negated in every prompt).
5. **Soulful furrowed brow** + soft deep eyes.
- **Costume:** teal collar + glowing spiral seashell charm ("the Listening Shell").
- **Female** — smooth neutral underside, no genitalia.

## Simplify / Exaggerate / Lock
- **Simplify:** fur → flat + soft shading; muzzle wrinkles → 1–2 signature brow lines; realistic shading → clean forms.
- **Exaggerate (her charm):** the soulful furrowed brow, the floppy ears, slightly larger soulful eyes.
- **Lock proportions** (the model sheet enforces these): head-to-body ratio, eye size + placement, muzzle length, leg length. Youthful athletic-boxer build, simplified and friendly.

## Likeness anchor
The faithful realistic renders (`assets/character_design/Bentley_realistic_*.png`) are the **truth reference** for her actual features (athletic boxer build, black mask, floppy ears, soulful brow). The **production design is a simplified stylization of that truth** — caricature, not photocopy. She must still read as the real dog, distilled to her 5 signature traits.

## Consistency methodology (the AI workflow rules)
1. **ONE master model sheet is law.** Every shot references the locked master Element — **NEVER** regenerate Bentley off a previous *shot* (copy-of-a-copy = drift; this is what broke us before).
2. **Restate the 5 signature features + "same dog, match the model sheet"** in every prompt.
3. Use the **turnaround as a multi-image reference** where possible.
4. **Generate 2–3 takes per shot; keep the on-model one.**
5. Anchor to the **real photos only** when re-deriving the master — never for individual shots.

## The model sheet (deliverable that locks her)
1. **Turnaround** — front / 3-quarter / side / back, consistent scale.
2. **Expression sheet** — happy, sad, surprised, curious, scared (the real consistency test).
3. **Construction + proportion notes**, exact color hex, do's & don'ts.
4. **Master front view → the locked reference Element** everything traces to.
