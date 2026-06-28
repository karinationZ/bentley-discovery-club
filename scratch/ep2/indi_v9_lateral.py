#!/usr/bin/env python3
"""Ep2 — Indi v9: push the REAL eyes MORE LATERAL (client change-of-mind), editing FROM the locked Indi frame
so identity stays consistent. Also render the two low ocelli as cleaner organic chain-link rings (not plain dots).
Keep everything else locked: teal eyes, purple body, no nose/brows, tiny lipless mouth, colorful, clean.
ONE keyframe (= 4 cr). Run: KIE_KEY=... python3 scratch/ep2/indi_v9_lateral.py
"""
import sys, os, json
sys.path.insert(0, "/project")
from bentley.shared import kie_client

OUT = "/project/scratch/ep2/indi_v9"
os.makedirs(OUT, exist_ok=True)
INDI_LOCKED_URL = "https://files.catbox.moe/viszfx.png"  # the locked Indi master

PROMPT = (
 "Edit this locked cartoon octopus character (keep it the SAME character). ONE main change: reposition her two REAL eyes to "
 "be MORE LATERAL — set them noticeably WIDER APART and a bit higher, more on the SIDES of her rounded domed head, angled "
 "outward like a real octopus, clearly NOT a close-set forward-facing human pair (but still readable in a three-quarter view). "
 "Keep the clean luminous TEAL / aqua-cyan iris, a soft simple pupil, one small catchlight, NO white sclera, NO line or seam "
 "across the eye, and a soft eyelid hood (a skin fold, NOT an eyebrow). "
 "Render her two low ocelli ('false eyes') a little more clearly: one just BELOW/in front of each real eye, as a soft ORGANIC "
 "iridescent-blue CHAIN-LINK ring (not a plain flat dot), small and natural, NOT high on the temples, NOT the deadly "
 "blue-ringed-octopus many-rings look. "
 "Keep EVERYTHING else exactly the same: iridescent grape-purple body with lighter pinkish-lavender highlights, NO nose, NO "
 "nostrils, NO eyebrows, NO brow ridge, NO human face; one tiny soft LIPLESS mouth (no teeth); eight tapering suckered arms; "
 "the bright colorful sunny daytime tide-pool (blue-green water, warm rocks); clean, sharp, vibrant, NO grain. Three-quarter "
 "view, character-design hero. "
 "NEGATIVE — avoid: forward-facing eyes, close-set frontal eye pair, centered eyes, human eyes, white sclera, brown eyes, "
 "amber eyes, gold eyes, line in the eye, nose, nostrils, muzzle, eyebrows, brow ridge, human face, cheeks, teeth, lips, grin, "
 "film grain, noise, ocelli high on the temples, headphones, blue-ringed octopus, many small rings, monochrome purple, dark, watermark.")

print("bal before:", kie_client.credits())
r = kie_client.run("google/nano-banana-edit",
                   {"prompt": PROMPT, "image_urls": [INDI_LOCKED_URL], "image_size": "16:9", "output_format": "png"})
lp = f"{OUT}/indi_v9_lateral.png"; kie_client.download(r["urls"][0], lp)
json.dump({"out": lp, "credits": r["credits"], "secs": r["secs"]}, open(f"{OUT}/_v9.json", "w"), indent=1)
print(f"v9 lateral: {r['credits']}cr {r['secs']}s -> {lp}")
print("bal after:", kie_client.credits())
