#!/usr/bin/env python3
"""Ep2 GATE A — Indi v8b HERO (ONE image). Fixes from client feedback on v8:
 - EYES back to TEAL (the locked unnatural color), NOT brown/amber. Lateral, clean, no line, no sclera.
 - LESS PURPLE overall: keep Indi's Ep1 purple body, but put her in a BRIGHT, COLORFUL daytime tide pool
   (blue-green water, warm rocks) so the frame isn't a monochrome purple wash; add lighter highlights on her.
 - Closer/clearer framing. Keeps octopus-first: lateral eyes, no nose, no brows, minimal mouth, arms dominant.
ONE keyframe (= 4 cr). Run: KIE_KEY=... python3 scratch/ep2/indi_v8_hero.py
"""
import sys, os, json
sys.path.insert(0, "/project")
from bentley.shared import kie_client

OUT = "/project/scratch/ep2/indi_v8"
os.makedirs(OUT, exist_ok=True)
REF_URL = "https://files.catbox.moe/vk2snn.png"  # Ep1 octopus anchor (iridescent purple material)

PROMPT = (
 "Using the reference image's iridescent grape-purple skin material as Indi's body color, create the character below as a "
 "full octopus, but in a NEW brighter colorful setting (do NOT copy the dark purple sunset of the reference). "
 "Indi, a young California two-spot octopus, OCTOPUS-FIRST: a real octopus gently simplified for animation, never a humanlike "
 "face on a ball. Soft rounded domed mantle with two tiny soft nubs on top; EIGHT long tapering arms with visible sucker "
 "rows, curling in soft spirals, one arm reaching forward — arms are the dominant mass. Her skin is iridescent GRAPE-PURPLE "
 "with lighter pinkish-lavender highlights and a paler underside, glossy and wet with subtle papillae bumps (vivid, not a "
 "flat purple mass). "
 "EYES (lateral + TEAL): two eyes set WIDE APART and HIGH on the SIDES of the domed head (lateral, like a real octopus, "
 "angled outward, not a close-set frontal human pair). Each eye has a clean luminous TEAL / aqua-cyan iris (her signature "
 "unnatural, magical, NON-HUMAN eye color), a soft simple pupil, ONE small catchlight, NO white sclera, NO line or seam "
 "across the eye, and a soft eyelid hood (a skin fold, NOT an eyebrow). DEFINITELY NOT brown, NOT amber, NOT gold eyes. "
 "OCTOPUS-FIRST RULES: NO nose, NO nostrils, NO muzzle, NO eyebrows, NO brow ridge, NO human face plane, NO cheeks, NO chin. "
 "Smooth purple skin between/below the eyes. Only features: two lateral teal eyes + one tiny mouth. "
 "MOUTH: one tiny, soft, low, LIPLESS mouth (a gentle small seam, can open to a soft 'o'); NO teeth, NO lips, NO cheek-smile. "
 "Two iridescent-blue ocelli sit LOW, one just below/in front of each eye, soft and organic. "
 "MOOD: gentle, curious, approachable, a soft warm happiness glow in her skin. "
 "SETTING: a BRIGHT, COLORFUL, SUNNY DAYTIME tide pool — clear blue-green water, warm wet tan-and-black rocks, a little green "
 "seaweed and a pink anemone, soft blue sky; bright clean natural daylight. The scene is colorful and NOT monochrome, so her "
 "purple body POPS against the blue-green water. "
 "Character-design HERO, medium close shot (she fills much of the frame), three-quarter view, CLEAN, SHARP, crisp, vibrant, "
 "high-clarity modern Pixar/Bluey-style 3D animated kids-series render. NO grain, NO noise. No text, no watermark. "
 "NEGATIVE — avoid: brown eyes, amber eyes, gold eyes, monochrome purple scene, all-purple image, purple wash, purple sunset, "
 "purple lighting everywhere, dark, murky, nose, nostrils, muzzle, eyebrows, brow ridge, human eyes, white sclera, round "
 "forward-facing eye pair, close-set eyes, human face, cheeks, chin, human mouth, lips, teeth, grin, eyelashes, film grain, "
 "noise, speckle noise, headphones, symmetric temple spots, blue-ringed octopus, many small rings, baby, chibi, blob, plastic "
 "toy, creepy, flat 2D, watermark.")

print("bal before:", kie_client.credits())
r = kie_client.run("google/nano-banana-edit",
                   {"prompt": PROMPT, "image_urls": [REF_URL], "image_size": "16:9", "output_format": "png"})
lp = f"{OUT}/indi_v8b_hero.png"; kie_client.download(r["urls"][0], lp)
json.dump({"out": lp, "credits": r["credits"], "secs": r["secs"]}, open(f"{OUT}/_hero_v8b.json", "w"), indent=1)
print(f"hero v8b: {r['credits']}cr {r['secs']}s -> {lp}")
print("bal after:", kie_client.credits())
