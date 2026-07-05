# EP2 Companion Short — "The Octopus That Disappears" (camouflage / color-change)

**Status:** spec for owner review (not yet built). **Cost:** ~$0 (free footage + reused art + ~pennies of VO; no Kling/KIE). **Effort:** ~1.5–2 hr.

## Concept
The **real science behind Episode 2.** EP2's signature beat is Indi turning Bentley-colored ("you did *ME*!"). This Short shows a **real octopus doing the exact same thing** — instant color *and* texture change — so a child watching goes *"wait… that's REAL?!"* Same concept as the episode, opposite register: the cartoon is the *story*, the Short is *"…and that really happens."*

- **Format:** vertical YouTube Short, ~30s, **Made for Kids**.
- **Register wall (brand cohesion):** realistic footage is *only ever the thing Bentley discovers*; cartoon Bentley bookends in her locked Pixar style and never goes photoreal. Gold Listening-Tag glow + "Stop. Look. Listen." (LauraZ) is the hinge into the real footage. Bill's narration + brand type + music ride continuously as glue.
- **Repeatable template** for every future episode's companion Short.

## The fact (science-checked)
An octopus can change **both color and skin texture in under a second** to match its surroundings — using **millions of tiny pigment sacs (chromatophores)** in its skin, plus muscle-raised skin bumps (papillae). The wonder twist: **octopuses are effectively colorblind** — they match colors they can't even see. (Teach one smart word: *chromatophores* → "color sacs.")

## VO script (the audio spine)
| # | Speaker (voice) | Line | Seg |
|---|---|---|---|
| 1 | **Bill** (`tts_bill`) | "Watch this octopus… *disappear*." | 0–3s |
| 2 | **Bentley** (`tts_catchphrase`, LauraZ) | "Stop. Look. Listen." | 3–6s |
| 3 | **Bill** | "In less than a second, an octopus can change her color — and even her bumpy skin — to match almost anything." | 6–14s |
| 4 | **Bill** | "She has millions of tiny color sacs in her skin — *chromatophores* — that open and shut in a flash." | 14–22s |
| 5 | **Bill** | "And the wildest part? She's colorblind — she can't even see the colors she's copying." | 22–27s |
| 6 | **Bentley** (LauraZ) | "That's Indi's secret too — and there's a whole adventure about her." | 27–30s |

*VO timing is approximate; trim each segment's duration to its recorded line at the mix.*

## On-screen captions (`shorts.py` Pillow list)
`WATCH HER DISAPPEAR 🐙` → `STOP. LOOK. LISTEN.` *(gold)* → `color + texture, in < 1 second` → `chromatophores = "color sacs"` → `…and she's COLORBLIND` → `Indi did this in EP 2 →`

## Shotlist (`shorts_specs.json` schema — `src` overrides)
```json
[{
  "id": "ep2_short_camo",
  "test": "EP2 companion — real octopus camouflage",
  "out": "EP2_Short_The_Octopus_That_Disappears.mp4",
  "segments": [
    {"src": "clips/oct_camo_reveal.mp4",  "start": 0, "end": 3.0, "mode": "blurfill"},
    {"start": 224.0, "end": 227.0, "mode": "crop", "xoff": 656, "_note": "REUSED EP1 Bentley reaction (muted); LauraZ catchphrase laid in mix; rotate to a fresh frame, NOT 182.4-186.0 used in Shorts 3&6"},
    {"src": "clips/oct_match_coral.mp4", "start": 0, "end": 8.0, "mode": "blurfill"},
    {"src": "clips/oct_skin_macro.mp4",  "start": 0, "end": 8.0, "mode": "blurfill"},
    {"src": "clips/oct_full_reveal.mp4", "start": 0, "end": 5.0, "mode": "blurfill"},
    {"start": 226.0, "end": 229.0, "mode": "crop", "xoff": 656, "_note": "REUSED EP1 Bentley happy/tongue-out (muted); LauraZ sign-off in mix; match-cut/loop back to seg0"}
  ]
}
```
*(Captions are added with `t/dur/y/size` per the existing EP1 specs; finalized at build.)*

## Sourcing checklist (all free)
- **4 octopus clips → Pexels** (free, no attribution, kid-safe). Curate **bright reef / tide-pool, NOT dark/abyssal** (age-4–8 wonder tone): (1) a fast color-change *reveal*, (2) an octopus matched to coral/rock with bumpy texture, (3) a macro of skin color rippling, (4) a dramatic full reveal / "it was there the whole time." Drop into `assets/pilot_shots/ep2/shorts/clips/`. Log source + license per clip.
- **2 Bentley clips → reuse** existing EP1 master frames ($0, on-model, zero drift); pick reaction beats the other Shorts don't already use.
- **Music → YouTube Audio Library**, no-attribution soft-wonder bed.

## Build (honest, 2 steps)
1. **Picture + captions:** `shorts.py` (octopus segments via `src` + reused Bentley + Pillow captions). Zero new code for video clips.
2. **Audio:** record 6 VO lines (`tts_bill` / `tts_catchphrase` — pennies, **no Kling/KIE, cost-gate not triggered**); lay VO + music under the picture with `mix.py` / `overlay_vo.py`, ducked; fade-in at open, **no end fade** (seamless loop).

## Upload / funnel (no ad-feel)
- **Title:** *This octopus can vanish in 1 second 🐙 #shorts*
- **Pinned comment:** "🐙 This is exactly what Indi does in Bentley's Episode 2 — watch her surprise Bentley → [EP2 link]"
- **Hashtags:** #shorts #octopus #camouflage #oceananimals #scienceforkids #BentleysBigAdventures
- **Related video:** attach EP2 · **Cadence:** post 1–3 days after EP2 is live.

## QA before delivery
- Register wall holds: Bentley stays 100% cartoony-Pixar (mask, floppy ears, red-fawn paws/no white socks, docked tail, tag; **no human teeth**); octopus is the only realistic element.
- Catchphrase is **Bentley's voice (LauraZ)**, never Bill's. No dark/scary clips (wonder, not peril). Hook lands in <3s. Seamless loop. Clip licenses logged. Fresh delivery filename.

## Open item
Source the 4 Pexels camouflage clips (owner downloads, or fetch via browser) → then build.
