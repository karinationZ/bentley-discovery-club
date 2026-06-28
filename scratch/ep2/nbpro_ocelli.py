#!/usr/bin/env python3
"""Try NANO BANANA PRO (Gemini 3 Pro Image) for the ocelli on the locked s14 master.
Pro params: image_input[], aspect_ratio, resolution. Uses catbox input (jobs API fetches catbox fine).
Add defined iridescent rings, keep everything else identical. No chains, no glow. Then I zoom-QA.
Run: KIE_KEY=... python3 scratch/ep2/nbpro_ocelli.py
"""
import sys, os, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

CATBOX = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()
OUT = f"{ROOT}/scratch/ep2/master/INDI_nbpro_ocelli.png"

PROMPT = ("Keep this octopus EXACTLY the same — same face, same teal eyes, same purple colour, same pose, same body and "
          "background; do not redraw or restyle her. ONLY add her two false-eye OCELLI: on each side of her head, just below "
          "and slightly behind each real eye, add ONE clear, defined, iridescent peacock-blue RING marking on the skin — a "
          "smooth blue circle with a slightly darker center and a soft pearlescent shimmer, like the two-spot ocellus of a "
          "real California two-spot octopus. Make them tasteful and clearly visible. They are skin markings, NOT light "
          "sources: NO glow, NO neon, NO emissive light, NO metal, NO chains, NO jewelry. Change nothing else in the image.")

INP = {"prompt": PROMPT, "image_input": [CATBOX], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"}

print("bal before:", kie_client.credits())
done = False
for slug in ["google/nano-banana-pro", "nano-banana-pro"]:
    for i in range(3):
        try:
            r = kie_client.run(slug, INP)
            kie_client.download(r["urls"][0], OUT)
            print(f"OK [{slug}] {r.get('credits')}cr {r.get('secs')}s -> {OUT}"); done = True; break
        except Exception as e:
            print(f"  [{slug}] attempt {i+1}: {str(e)[:100]}"); time.sleep(6)
    if done:
        break
if not done:
    print("nano-banana-pro unavailable")
print("bal after:", kie_client.credits())
